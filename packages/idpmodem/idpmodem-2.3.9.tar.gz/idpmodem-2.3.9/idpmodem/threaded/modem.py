"""A threaded IDP modem client with abstracted properties."""
import logging
import os
import queue
from base64 import b64decode, b64encode
from datetime import datetime, timezone
from math import ceil
from time import time
from typing import Callable

from idpmodem.aterror import AtCrcError, AtException, AtGnssTimeout, AtTimeout
from idpmodem.constants import (EVENT_TRACES, AtErrorCode, BeamSearchState,
                                DataFormat, EventNotification, GeoBeam,
                                GnssMode, MessagePriority, MessageState,
                                PowerMode, SatelliteControlState,
                                SignalLevelRegional, SignalQuality,
                                TransmitterStatus, WakeupPeriod)
from idpmodem.helpers import printable_crlf
from idpmodem.location import Location, location_from_nmea
from idpmodem.s_registers import SRegisters
from idpmodem.threaded.atcommand import AtProtocol, ByteReaderThread, Serial
from idpmodem.propertycache import PropertyCache

GNSS_STALE_SECS = int(os.getenv('GNSS_STALE_SECS', 1))
GNSS_WAIT_SECS = int(os.getenv('GNSS_WAIT_SECS', 35))
SAT_STATUS_HOLDOFF = 5
MODEM_REBOOT_HOLDOFF = os.getenv('MODEM_REBOOT_HOLDOFF')
VERBOSE_DEBUG = (str(os.getenv('VERBOSE_DEBUG', False)).lower() == 'true' or
                 'idpmodem' in str(os.getenv('LOG_VERBOSE', False)))
LOG_VERBOSE = os.getenv('LOG_VERBOSE')

_log = logging.getLogger(__name__)


class ModemBusy(Exception):
    """Indicates the modem is busy processing a prior command."""


class AtConfiguration:
    """Configuration settings of the modem.
    
    Attributes:
        crc (bool): Using cyclic redundancy check for all transactions.
        echo (bool): Echoing back commands
        quiet (bool): Limiting responses
        verbose (bool): Using text-based responses
        
    """
    def __init__(self) -> None:
        self.crc: bool = False
        self.echo: bool = True
        self.quiet: bool = False
        self.verbose: bool = True


class IdpModem:
    """Abstracts AT commands to relevant functions for an IDP modem.
    
    Attributes:
        connected (bool): Indicates if connected to a modem on serial.
        baudrate (int): The baudrate of the modem.
        crc (bool): Indicates if CRC error checking is enabled.
        mobile_id (str): The unique modem ID.
        versions (dict): The versions reported by the modem.
        manufacturer (str): The modem manufacturer.
        model (str): The modem model.
        power_mode (IntEnum):
        wakeup_period (IntEnum):
        temperature (float):
        gnss_refresh_interval (int):
        location (object):
        control_state (IntEnum):
        beam_search_state (IntEnum):
        network_status (IntEnum):
        registered (bool):
        
    """
    
    SERIAL_KWARGS = ['baudrate', 'timeout', 'write_timeout']
    BAUD_RATES = [1200, 2400, 4800, 9600, 19200]
    PROTOCOL_KWARGS = ['event_callback', 'at_timeout']
    OTHER_KWARGS = ['error_detail', 'stale_secs', 'wait_secs']
    
    def __init__(self, serial_port: str, **kwargs):
        self.serial_kwargs = {
            'port': serial_port,
            'baudrate': int(kwargs.pop('baudrate', 9600)),
        }
        self.protocol_kwargs = {}
        self.error_detail = bool(kwargs.pop('error_detail', True))
        for kwarg in kwargs:
            if kwarg in self.SERIAL_KWARGS:
                self.serial_kwargs[kwarg] = kwargs[kwarg]
            elif kwarg in self.PROTOCOL_KWARGS:
                self.protocol_kwargs[kwarg] = kwargs[kwarg]
        self.serial_port = None
        self._main_thread = None
        self._transport = None
        self._protocol: AtProtocol = None
        try:
            self._reboot_holdoff = int(MODEM_REBOOT_HOLDOFF)
        except:
            self._reboot_holdoff = None
        self._commands = queue.Queue(1)
        self._at_config = AtConfiguration()
        self._loc_query: dict = {
            'stale_secs': int(kwargs.pop('stale_secs', GNSS_STALE_SECS)),
            'wait_secs': int(kwargs.pop('wait_secs', GNSS_WAIT_SECS)),
        }
        self._holdoffs: dict = {}   # used to ignore frequent repeat commands
        self._statistics: dict = {}
        self.s_registers: SRegisters = SRegisters()
        self._property_cache = PropertyCache()
        self._trace_log_mode: bool = False
    
    def connect(self):
        """Connects to a modem using a serial and protocol instance."""
        self.serial_port = Serial(**self.serial_kwargs)
        self._main_thread = ByteReaderThread(self.serial_port,
                                            AtProtocol,
                                            **self.protocol_kwargs)
        self._main_thread.start()
        self._transport, self._protocol = self._main_thread.connect()
        assert isinstance(self._protocol, AtProtocol)
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        if self._reboot_holdoff is not None:
            self._protocol.event_callback = self._unsolicited

    def disconnect(self):
        """Disconnects from the modem."""
        with self._commands.mutex:
            self._commands.queue.clear()
        if self._main_thread:
            self._main_thread.close()
        if self.serial_port:
            self.serial_port.close()
        self._transport = None
        self._protocol = None
        self._property_cache.clear()
    
    def property_cache_clear(self):
        """Clears the property cache."""
        self._property_cache.clear()
    
    def is_connected(self) -> bool:
        try:
            res = self.atcommand('AT')
            if res is not None:
                return True
        except AtCrcError:
            return True
        except AtTimeout:
            return False
        
    @property
    def connected(self) -> bool:
        """Indicates if the modem is connected.
        
        Attempts to send a basic `AT` command and check for any response.

        Cached for 1 second.
        """
        if self._transport is None or self._protocol is None:
            return False
        CACHE_TAG = 'connected'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        connected = self.is_connected()
        self._property_cache.cache(connected, CACHE_TAG)
        return connected

    @property
    def baudrate(self) -> 'int|None':
        """The baud rate of the serial connecton."""
        return self.serial_port.baudrate if self.serial_port else None
    
    @baudrate.setter
    def baudrate(self, value: int):
        if not self.connected:
            raise ConnectionError('Modem is not connected')
        if value not in self.BAUD_RATES:
            raise ValueError(f'Baud rate must be one of {self.BAUD_RATES}')
        response = self.atcommand(f'AT+IPR={value}')
        if response and response[0] != 'ERROR':
            self.serial_port.baudrate = value

    @property
    def crc(self) -> 'bool|None':
        """Indicates if CRC error checking is enabled on the modem."""
        return self._protocol.crc if self._protocol is not None else None

    def register_unsolicited_callback(self, callback: Callable):
        if not callable(callback):
            raise ValueError(f'Callback must be callable')
        self._protocol.event_callback = callback
    
    def _unsolicited(self, data: str) -> None:
        if self._commands.full():
            raise ModemBusy('Unsolicited data received during AT command'
                            f'processing: {printable_crlf(data)}')
        if self._reboot_holdoff:
            BOOT_INDICATORS = ['boot loader', 'Copyright (c)', '*** Reset',
                'starting appl firmware', '.....']
            if any(indicator in data for indicator in BOOT_INDICATORS):
                _log.warning('Reboot indicator found - holding off commands'
                            f' {self._reboot_holdoff}s')
                self._holdoffs['reboot'] = int(time())

    def atcommand(self,
                  command: str,
                  filter: 'list[str]' = [],
                  timeout: int = 5,
                  await_previous: bool = True,
                  ) -> 'list[str]':
        """Sends an AT command to the modem and returns the response.
        
        Args:
            command: The AT command
            filter: (optional) list of sub/strings to remove from response.
            timeout: Number of seconds to wait for a reply
                (not including messages queued by other threads)
            await_previous: If True, this will block if a prior command was
                submitted by another thread
        
        Returns:
            list of filtered and stripped response(s) to the command(s)
        
        Raises:
            ModemBusy if await_previous is False and a prior command is queued.
            AtException if an error occurred that is unrecognized.

        """
        if not self._transport or not self._protocol:
            raise ConnectionError('No serial or protocol instance.')
        while self._commands.full():
            if not await_previous:
                raise ModemBusy('Queue full')
            pass
        if 'reboot' in self._holdoffs and isinstance(self._reboot_holdoff, int):
            while int(time()) - self._holdoffs['reboot'] < self._reboot_holdoff:
                pass
        if self.trace_log_mode and command != '\x18':
            raise ModemBusy('Trace log mode enabled')
        self._commands.put(command)
        try:
            res: list = self._protocol.command(command,
                                              filter=filter,
                                              timeout=timeout)
            if VERBOSE_DEBUG:
                _log.debug(f'Response: {res}')
            if self.error_detail and res and res[0] == 'ERROR':
                _log.debug(f'Querying error code response to {command}')
                err_res = self._protocol.command('ATS80?')
                if not err_res or err_res[0] == 'ERROR':
                    raise AtException('Unhandled error getting last error code'
                                      f' ({err_res})')
                last_err_code = err_res[0]
                detail = 'UNDEFINED'
                if AtErrorCode.is_valid(int(last_err_code)):
                    detail = AtErrorCode(int(last_err_code)).name
                res.append(f'{detail} ({last_err_code})')
                _log.warning(f'AT error: {detail} for command {command}')
            return res
        except AtException as err:
            _log.error(f'{err} on command {command}')
            raise err
        finally:
            self._commands.get()
            self._commands.task_done()
    
    def _handle_at_error(self, response: 'list[str]') -> None:
        err = response[1] if self.error_detail else response[0]
        _log.error(f'AT Error: {err}')
        raise AtException(err)

    def config_init(self, crc: bool = False) -> bool:
        """Initializes modem communications with Echo, Verbose. CRC optional."""
        _log.debug(f'Initializing modem Echo|Verbose{"|CRC" if crc else ""}'
                   f' (CRC={self._protocol.crc})')
        command = f'ATZ;E1;V1;Q0;%CRC={1 if crc else 0}'
        res_attempt_1 = self.atcommand(command)
        if res_attempt_1[0] != 'OK':
            # case 1: crc True but previously set; should now be T in factory
            # case 2: crc False but previously set; should now be F in factory
            if len(res_attempt_1) > 1:
                at_error = res_attempt_1[1]
                if ('INVALID_CRC' not in at_error and
                    'UNKNOWN_COMMAND' not in at_error):
                    _log.warning(f'Unexpected AT error {at_error}')
            _log.debug(f'CRC mismatch, re-attempting (CRC={self._protocol.crc})')
            res_attempt_2 = self.atcommand(command)
            if res_attempt_2[0] != 'OK':
                _log.error('Unable to initialize modem after second attempt')
                if len(res_attempt_2) > 1:
                    _log.error(f'AT error: {res_attempt_2[1]}')
                return False
        # self._protocol.crc = crc   #: redundant should be set by attempt
        self._at_config.crc = crc
        _log.debug('Initialization success')
        return True

    def config_restore_nvm(self) -> bool:
        """Sends ATZ to restore config from non-volatile memory."""
        _log.debug('Restoring modem stored configuration')
        response = self.atcommand('ATZ')
        if response[0] == 'ERROR':
            return False
        return True

    def config_restore_factory(self) -> bool:
        """Sends AT&F to restore factory default and returns True on success."""
        _log.debug('Restoring modem factory defaults')
        response = self.atcommand('AT&F')
        if response[0] == 'ERROR':
            return False
        return True
    
    def config_report(self) -> 'tuple[dict, dict]':
        """Sends the AT&V command to retrieve S-register settings.
        
        Returns:
            A tuple with two dictionaries (empty if failed) with:
            at_config with booleans crc, echo, quiet and verbose
            reg_config with S-register tags and integer values
        
        Raises:
            AtException if an error was returned.

        """
        _log.debug('Retrieving modem verbose configuration')
        response = self.atcommand('AT&V')
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        at_config = response[1]
        s_regs = response[2]
        echo, quiet, verbose, crc = at_config.split(' ')
        self._at_config.crc = bool(int(crc[4]))
        self._at_config.echo = bool(int(echo[1]))
        self._at_config.quiet = bool(int(quiet[1]))
        self._at_config.verbose = bool(int(verbose[1]))
        reg_config = {}
        for reg in s_regs.split(' '):
            name, value = reg.split(':')
            reg_config[name] = int(value)
        return (at_config, reg_config)

    def config_volatile_report(self) -> 'dict|None':
        """Gets key S-register settings.
        
        GNSS Mode (S39), GNSS fix timeout (S41), GNSS Continuous (S55),
        GNSS Jamming Status (S56), GNSS Jamming Indicator (S57), 
        Low power Wakeup Period (S51)

        Returns:
            Dictionary of S-register values, or None if failed
            
        """
        register_list = [
            'S39',   #: GNSS Mode
            'S41',   #: GNSS Fix Timeout
            'S51',   #: Wakeup Interval
            'S55',   #: GNSS Continuous
            'S56',   #: GNSS Jamming Status
            'S57',   #: GNSS Jamming Indicator
        ]
        _log.debug(f'Querying volatile S-register set: {register_list}')
        command = 'AT'
        for reg in register_list:
            command += f'{reg if command == "AT" else " " + reg}?'
        response = self.atcommand(command)
        if response[0] == 'ERROR':
            return None
        if 'OK' in response: response.remove('OK')
        volatile_regs = {}
        for r in range(len(response)):
            volatile_regs[register_list[r]] = int(response[r])
        return volatile_regs

    def config_nvm_save(self) -> bool:
        """Sends the AT&W command and returns True if successful."""
        _log.debug('Saving modem configuration to non-volatile memory')
        response = self.atcommand('AT&W')
        return response[0] == 'OK'

    def crc_enable(self, enable: bool = True) -> bool:
        """Sends the AT%CRC command and returns success flag.
        
        Args:
            enable: turn on CRC if True else turn off

        Returns:
            True if the operation succeeded else False

        """
        _log.debug(f'{"en" if enable else "dis"}abling modem CRC')
        command = f'AT%CRC={1 if enable else 0}'
        response = self.atcommand(command)
        if response[0] == 'ERROR':
            return False
        self._protocol.crc = enable
        self._at_config.crc = enable
        return True

    def mobile_id_get(self) -> 'str|None':
        """Retrieves the mobile ID of the modem."""
        response = self.atcommand('AT+GSN', filter=['+GSN:'])
        if response[0] != 'ERROR':
            return response[0]
        self._handle_at_error(response)
        
    @property
    def mobile_id(self) -> 'str|None':
        """The unique Mobile ID (Inmarsat serial number).
        
        Cached indefinitely.
        """
        CACHE_TAG = 'mobile_id'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        mobile_id = self.mobile_id_get()
        self._property_cache.cache(mobile_id, CACHE_TAG, None)
        return mobile_id

    def versions_get(self) -> 'dict|None':
        response = self.atcommand('AT+GMR', filter=['+GMR:'])
        if response[0] != 'ERROR':
            version_meta = {}
            versions = response[0].split(',')
            if len(versions) == 3:
                version_meta['firmware'] = versions[0]
                version_meta['hardware'] = versions[1]
                version_meta['at'] = versions[2]
            else:
                for i, v in enumerate(versions):
                    version_meta[i] = v
            return version_meta
        self._handle_at_error(response)
        
    @property
    def versions(self) -> 'dict|None':
        """The hardware, firmware and AT versions.
        
        Cached indefinitely.
        """
        CACHE_TAG = 'versions'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        versions = self.versions_get()
        self._property_cache.cache(versions, CACHE_TAG, None)
        return versions

    def manufacturer_get(self) -> 'str|None':
        response = self.atcommand('ATI0')
        if response[0] != 'ERROR':
            return response[0]
        self._handle_at_error(response)
        
    @property
    def manufacturer(self) -> str:
        """The modem manufacturer reported by `ATI0`.
        
        Cached indefinitely.
        """
        CACHE_TAG = 'manufacturer'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        manufacturer = self.manufacturer_get()
        self._property_cache.cache(manufacturer, CACHE_TAG, None)
        return manufacturer

    def model_get(self) -> 'str|None':
        response = self.atcommand('ATI4')
        if response[0] != 'ERROR':
            return response[0]
        self._handle_at_error(response)
        
    @property
    def model(self) -> str:
        """The modem model reported by `ATI4`.
        
        Cached indefinitely.
        """
        CACHE_TAG = 'model'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        model = self.model_get()
        self._property_cache.cache(model, CACHE_TAG, None)
        return model

    def power_mode_get(self) -> 'PowerMode|None':
        response = self.atcommand('ATS50?')
        if response[0] != 'ERROR':
            return PowerMode(int(response[0]))
        self._handle_at_error(response)
        
    def power_mode_set(self, value: 'str|int|PowerMode') -> bool:
        if isinstance(value, str):
            if value not in PowerMode.__members__:
                raise ValueError(f'Invalid PowerMode {value}')
            value = PowerMode[value].value
        if not PowerMode.is_valid(value):
            raise ValueError(f'Invalid PowerMode {value}')
        if VERBOSE_DEBUG:
            _log.debug(f'Setting modem power mode {PowerMode(value)}')
        response = self.atcommand(f'ATS50={value}')
        if response[0] != 'ERROR':
            return True
        return False
    
    @property
    def power_mode(self) -> 'PowerMode|None':
        """The modem power mode setting (enumerated) in `S50`.
        
        Cached until set.
        """
        CACHE_TAG = 'power_mode'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        power_mode = self.power_mode_get()
        self._property_cache.cache(power_mode, CACHE_TAG, None)
        return power_mode
    
    @power_mode.setter
    def power_mode(self, value: 'str|int|PowerMode'):
        CACHE_TAG = 'power_mode'
        try:
            self.power_mode_set(value)
            self._property_cache.remove(CACHE_TAG)
        except Exception as err:
            _log.error(f'Failed to set power_mode {value}: {err}')
    
    def wakeup_period_get(self) -> 'WakeupPeriod|None':
        """The modem wakeup period setting (enumerated) in `S51`."""
        response = self.atcommand('ATS51?')
        if response[0] != 'ERROR':
            return WakeupPeriod(int(response[0]))
        self._handle_at_error(response)
    
    def wakeup_period_set(self, value: 'str|int|WakeupPeriod') -> bool:
        if isinstance(value, str):
            if value not in WakeupPeriod.__members__:
                raise ValueError(f'Invalid WakeupPeriod {value}')
            value = WakeupPeriod[value].value
        if not WakeupPeriod.is_valid(value):
            raise ValueError(f'Invalid WakeupPeriod {value}')
        if VERBOSE_DEBUG:
            _log.debug(f'Setting modem power mode {WakeupPeriod(value)}')
        response = self.atcommand(f'ATS51={value}')
        if response[0] != 'ERROR':
            return True
        return False
    
    @property
    def wakeup_period(self) -> 'WakeupPeriod|None':
        """The modem wakeup period setting (enumerated) in `S51`.
        
        May be remotely changed by MT message.
        
        Cached for shorter of 1 second or until set.
        """
        CACHE_TAG = 'wakeup_period'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        wakeup_period = self.wakeup_period_get()
        self._property_cache.cache(wakeup_period, CACHE_TAG)
        return wakeup_period

    @wakeup_period.setter
    def wakeup_period(self, value: 'str|int|WakeupPeriod'):
        CACHE_TAG = 'wakeup_period'
        try:
            self.wakeup_period_set(value)
            self._property_cache.remove(CACHE_TAG)
        except Exception as err:
            _log.error(f'Failed to set wakeup_period {value}: {err}')
    
    def temperature_get(self) -> int:
        response = self.atcommand('ATS85?')
        if response[0] != 'ERROR':
            return int(float(response[0]) / 10)
        self._handle_at_error(response)
    
    @property
    def temperature(self) -> int:
        """Temperature in degrees Celsius (`S85`).
        
        Cached for 1 second.
        """
        CACHE_TAG = 'temperature'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        temperature = self.temperature_get()
        self._property_cache.cache(temperature, CACHE_TAG)
        return temperature

    def gnss_refresh_interval_get(self) -> int:
        """GNSS refresh interval in seconds (`S55`)."""
        response = self.atcommand(f'ATS55?')
        if response[0] != 'ERROR':
            return int(response[0])
        self._handle_at_error(response)
    
    def gnss_refresh_interval_set(self, value: int) -> bool:
        return self.gnss_continuous_set(value)
    
    @property
    def gnss_refresh_interval(self) -> int:
        """GNSS refresh interval in seconds (`S55`).
        
        Cached until set.
        """
        CACHE_TAG = 'gnss_refresh_interval'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        gnss_refresh = self.gnss_refresh_interval_get()
        self._property_cache.cache(gnss_refresh, CACHE_TAG, None)
        return gnss_refresh

    @gnss_refresh_interval.setter
    def gnss_refresh_interval(self, value: int):
        CACHE_TAG = 'gnss_refresh_interval'
        try:
            self.gnss_refresh_interval_set(value)
            self._property_cache.remove(CACHE_TAG)
        except Exception as err:
            _log.error(f'Failed to set gnss_refresh_interval {value}: {err}')

    def gnss_continuous_set(self,
                            interval: int = 0,
                            doppler: bool = True,
                            ) -> bool:
        """Sets the GNSS continous mode (0 = on-demand).
        
        Args:
            interval: Seconds between GNSS refresh.
            doppler: Often required for moving assets.
        
        Returns:
            True if successful setting.
        """
        if interval < 0 or interval > 30:
            raise ValueError('GNSS continuous interval must be in range 0..30')
        _log.debug(f'Configuring GNSS continuous mode {interval} seconds')
        response = self.atcommand(f'AT%TRK={interval}{",1" if doppler else ""}')
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        return True

    def gnss_nmea_get(self,
                      stale_secs: int = GNSS_STALE_SECS,
                      wait_secs: int = GNSS_WAIT_SECS,
                      nmea: 'list[str]' = ['RMC', 'GSA', 'GGA', 'GSV'],
                      ) -> list:
        """Gets a list of NMEA-formatted sentences from GNSS.

        Args:
            stale_secs: Maximum age of fix in seconds (1..600)
            wait_secs: Maximum time to wait for fix (1..600)

        Returns:
            List of NMEA sentences

        Raises:
            ValueError if parameter out of range
            AtGnssTimeout if the fix timed out
            AtException if any other error code was returned

        """
        NMEA_SUPPORTED = ['RMC', 'GGA', 'GSA', 'GSV']
        BUFFER_SECONDS = 5
        if (stale_secs not in range(1, 600+1) or
            wait_secs not in range(1, 600+1)):
            raise ValueError('stale_secs and wait_secs must be 1..600')
        sentences = ''
        for sentence in nmea:
            sentence = sentence.upper()
            if sentence not in NMEA_SUPPORTED:
                raise ValueError(f'Unsupported NMEA sentence: {sentence}')
            if len(sentences) > 0:
                sentences += ','
            sentences += f'"{sentence}"'
        timeout = wait_secs + BUFFER_SECONDS
        request_time = time()
        _log.debug(f'Querying GNSS NMEA sentences {sentences}')
        response = self.atcommand(f'AT%GPS={stale_secs},{wait_secs},{sentences}',
                                  timeout=timeout,
                                  filter=['%GPS:'])
        if response[0] == 'ERROR':
            if self.error_detail:
                if 'TIMEOUT' in response[1]:
                    raise AtGnssTimeout(response[1])
            self._handle_at_error(response)
        if 'OK' in response: response.remove('OK')
        time_to_fix = round(time() - request_time, 3)
        if 'gnss_ttf' not in self._statistics:
            self._statistics['gnss_ttf'] = time_to_fix
        else:
            old_ttf = self._statistics['gnss_ttf']
            avg_ttf = round((time_to_fix + old_ttf) / 2, 3)
            self._statistics['gnss_ttf'] = avg_ttf
        return response

    def location_get(self) -> 'Location|None':
        """The modem location derived from NMEA data."""
        try:
            nmea_sentences = self.gnss_nmea_get(self._loc_query['stale_secs'],
                                                self._loc_query['wait_secs'])
            location = location_from_nmea(nmea_sentences)
            return location
        except AtGnssTimeout:
            _log.warning('GNSS request timed out')
            return None
    
    @property
    def location(self) -> 'Location|None':
        """The modem location derived from NMEA data.
        
        Cached for 1 second.
        """
        CACHE_TAG = 'location'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        location = self.location_get()
        if location is not None:
            self._property_cache.cache(location, CACHE_TAG)
        return location

    def gnss_jamming_get(self) -> bool:
        """The GNSS jamming detection status (`S56`)."""
        response = self.atcommand('ATS56?')
        if response[0] != 'ERROR':
            gnss_jamming = ((int(response[0]) & 0b100) >> 2 == 1)
            return gnss_jamming            
        self._handle_at_error(response)

    @property
    def gnss_jamming(self) -> bool:
        """The GNSS jamming detection status (`S56`).
        
        Cached for 1 second.
        """
        CACHE_TAG = 'gnss_jamming'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        gnss_jamming = self.gnss_jamming_get()
        self._property_cache.cache(gnss_jamming, CACHE_TAG)
        return gnss_jamming

    def gnss_mode_get(self) -> 'GnssMode':
        """The GNSS operating mode setting (`S39`)."""
        response = self.atcommand('ATS39?')
        if response[0] != 'ERROR':
            return GnssMode(int(response[0]))
        self._handle_at_error(response)

    def gnss_mode_set(self, mode: 'GnssMode|int') -> bool:
        if not isinstance(mode, GnssMode):
            if not GnssMode.is_valid(mode):
                raise ValueError(f'Invalid GNSS Mode {mode}')
        else:
            mode = mode.value
        response = self.atcommand(f'ATS39={mode}')
        if response[0] != 'ERROR':
            return True
        return False

    @property
    def gnss_mode(self) -> GnssMode:
        """The GNSS operating mode setting (`S39`).
        
        Cached until set.
        """
        CACHE_TAG = 'gnss_mode'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        gnss_mode = self.gnss_mode_get()
        self._property_cache.cache(gnss_mode, CACHE_TAG, None)
        return gnss_mode

    @gnss_mode.setter
    def gnss_mode(self, mode: 'GnssMode|int'):
        CACHE_TAG = 'gnss_mode'
        try:
            self.gnss_mode_set(mode)
            self._property_cache.remove(CACHE_TAG)
        except Exception as err:
            _log.error(f'Failed to set gnss_mode {mode}: {err}')

    def transmitter_status_get(self) -> TransmitterStatus:
        """The transmitter status reported by `S54`"""
        response = self.atcommand('ATS54?')
        if response[0] != 'ERROR':
            return TransmitterStatus(int(response[0]))
        self._handle_at_error(response)

    @property
    def transmitter_status(self) -> TransmitterStatus:
        """The transmitter status reported by `S54`.
        
        Cached for 1 second.
        """
        CACHE_TAG = 'transmitter_status'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        tx_status = self.transmitter_status_get()
        self._property_cache.cache(tx_status, CACHE_TAG)
        return tx_status

    def satellite_status_get(self) -> dict:
        """Retrieves key satellite status information.
        
        Derived from Class 3 Subclass 1: VCID, C/N, Satellite Control State,
        Beam Search State.
        
        Returns:
            A dictionary with `channel_id` (int), `snr` (float), `control_state` 
                (SatelliteControlState), `beamsearch_state` (BeamSearchState)
        
        """
        command = ('ATS90=3 S91=1 S92=1 S116? S122? S123? S101? S108? S119?')
        response = self.atcommand(command)
        if response[0] != 'ERROR':
            return {
                'snr': round(int(response[0]) / 100.0, 2),
                'control_state': SatelliteControlState(int(response[1])),
                'beamsearch_state': BeamSearchState(int(response[2])),
                'channel_id': int(response[3]),
                'tx_suspend_flags': int(response[4]),
                'system_flags': int(response[5]), 
            }
        self._handle_at_error(response)
    
    @property
    def control_state(self) -> 'SatelliteControlState|None':
        """The control state enumerated value.
        
        Trace Class 3, Subclass 1, Data 22
        
        Cached for 1 second.
        """
        CACHE_TAG = 'satellite_status'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is None:
            cached = self.satellite_status_get()
            self._property_cache.cache(cached, CACHE_TAG)
        return cached.get('control_state', None)
    
    @property
    def network_status(self) -> 'str|None':
        """The network status derived from control state.
        
        Cached for 1 second.
        """
        if self.control_state is not None:
            return self.control_state.name

    @property
    def registered(self) -> bool:
        """Indicates the modem is registered on the network.
        
        Cached for 1 second.
        """
        return self.control_state == 10

    @property
    def beamsearch_state(self) -> 'BeamSearchState|None':
        """The beam search state (Trace Class 3, Subclass 1, Data 23).
        
        Cached for 1 second.
        """
        CACHE_TAG = 'satellite_status'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is None:
            cached = self.satellite_status_get()
            self._property_cache.cache(cached, CACHE_TAG)
        return cached.get('beamsearch_state', None)
    
    @property
    def beamsearch(self) -> 'str|None':
        """The beam search state description.
        
        Cached for 1 second.
        """
        if self.beamsearch_state is not None:
            return self.beamsearch_state.name

    @property
    def snr(self) -> 'float|None':
        """The average main beam Carrier-to-Noise (C/N0).
        
        Cached for 1 second.
        """
        CACHE_TAG = 'satellite_status'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is None:
            cached = self.satellite_status_get()
            self._property_cache.cache(cached, CACHE_TAG)
        return cached.get('snr', None)
            
    @property
    def signal_quality(self) -> SignalQuality:
        """Qualitative interpretation of the SNR."""
        if self.snr is None:
            return SignalQuality.NONE
        if self.snr > SignalLevelRegional.INVALID.value:
            return SignalQuality.WARNING
        if self.snr > SignalLevelRegional.BARS_5.value:
            return SignalQuality.STRONG
        if self.snr > SignalLevelRegional.BARS_4.value:
            return SignalQuality.GOOD
        if self.snr > SignalLevelRegional.BARS_3.value:
            return SignalQuality.MID
        if self.snr > SignalLevelRegional.BARS_2.value:
            return SignalQuality.LOW
        return SignalQuality.WEAK
    
    def satellite_geographic_info_get(self) -> 'dict|None':
        """Retrieves satellite geographic information.
        
        Derived from Class 3 Subclass 5.
        If the satellite has not been acquired, the AT error code 102 will
        return from the modem and produce a `None` response.
        
        Returns:
            A dictionary with `geo_beam_id` (int), `latitude` (int),
                `longitude` (int), `geo_sat_longitude` (float)
        
        """
        command = ('ATS90=3 S91=5 S92=1 S100? S102? S109?')
        response = self.atcommand(command)
        if response[0] != 'ERROR':
            return {
                'vcid': int(response[0]),
                'geo_beam_id': int(response[1]),
                'rl_coding_rate': int(response[1]),
            }
        if len(response) < 2 or '102' not in response[1]:
            self._handle_at_error(response)
        _log.warning('Satellite not yet acquired - returning None')
    
    @property
    def beam_id(self) -> 'int|None':
        """The current active regional beam ID of the active satellite.
        
        Cached for 1 second.
        """
        CACHE_TAG = 'satellite_geographic_info'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is None:
            cached = self.satellite_geographic_info_get()
            self._property_cache.cache(cached, CACHE_TAG)
        return cached.get('geo_beam_id', None)
        
    @property
    def satellite(self) -> 'str|None':
        """The current active satellite name.
        
        Cached for 1 second.
        """
        if GeoBeam.is_valid(self.beam_id):
            return GeoBeam(self.beam_id).satellite
    
    def utc_time_get(self) -> str:
        """Gets current UTC time of the modem in ISO8601 format."""
        response = self.atcommand('AT%UTC', filter=['%UTC:'])
        if response[0] != 'ERROR':
            return response[0].replace(' ', 'T') + 'Z'
        self._handle_at_error(response)

    @property
    def utc_time(self) -> 'str|None':
        """Gets current UTC time of the modem in ISO8601 format."""
        try:
            return self.utc_time_get()
        except:
            _log.error('Unable to retrieve UTC time from modem')

    def message_mo_send(self,
                        data: 'bytes|bytearray|str',
                        data_format: int = DataFormat.BASE64,
                        name: str = None,
                        priority: int = MessagePriority.LOW,
                        sin: int = None,
                        min: int = None,
                        timeout: int = None,
                        ) -> str:
        """Submits a mobile-originated message to send.

        When submitting raw bytes, the first byte will be used as SIN. The
        first byte must not be in the reserved range (0..15).
        When submitting a string, the `sin` field is expected to be set and
        the data field will be appended to the `sin` byte and optionally the
        `min` byte if specified.
        
        Args:
            data: The data raw bytes or UTF-8 Text, Hexadecimal or Base64 string
            data_format: 1=text, 2=hexadecimal, 3=base64 (default)
            name: Optional unique name up to 8 characters long. If none is
                specified, use the 8 least-significant digits of unix timestamp.
            priority: 1=high, 4=low (default)
            sin: Optional first byte of payload used for codec, required if data
                is string type.
            min: Optional second byte of payload used for codec
            timeout: Optional timeout. If not provided will be calculated from
                the baudrate for the maximum message size, *3

        Returns:
            Name of the message if successful, or the error string.
        
        Raises:
            AtException if an error was returned by the modem.

        """
        name = str(int(time()))[-8:] if not name else name[0:8]
        if isinstance(data, bytes) or isinstance(data, bytearray):
            sin = data[0]
            data = b64encode(data[1:]).decode('utf-8')
            data_format = DataFormat.BASE64
        elif not isinstance(data, str):
            raise ValueError('Invalid data must be bytes, bytearray or string')
        if not isinstance(sin, int) or sin not in range(16, 256):
            raise ValueError('Invalid SIN must be 16..255')
        if isinstance(min, int) and min not in range(0, 256):
            raise ValueError('Invalid MIN must be 0..255')
        min = f'.{min}' if min is not None else ''
        data = f'"{data}"' if data_format == DataFormat.TEXT else data
        _log.debug(f'Submitting MO message with name {name}')
        command = f'AT%MGRT="{name}",{priority},{sin}{min},{data_format},{data}'
        baudrate = self.baudrate or 9600
        max_timeout = timeout or ceil(6400 / (baudrate / 8)) * 3
        response = self.atcommand(command, timeout=max_timeout)
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        return name

    def message_mo_state(self, name: str = None) -> 'list[dict]':
        """Gets the message state(s) requested.
        
        If no name filter is passed in, all available messages states
        are returned.  Returns False is the request failed.

        Args:
            name: The unique message name in the modem queue. If name is
                None, all available message states in transmit queue will be
                returned.

        Returns:
            List of metadata for each message in transmit queue including:
            - `name` (str) The ID in the modem transmit queue
            - `state` (int) The state of the message
            - `state_name` (str) The `MessageState.name`
            - `size` (int) in bytes
            - `sent` (int) in bytes for large message progress

        """
        states = []
        name = f'="{name}"' if name is not None else ''
        _log.debug(f'Querying MO message states {name if name else ""}')
        response = self.atcommand(f'AT%MGRS{name}', filter=['%MGRS:'])
        # %MGRS: "<name>",<msg_no>,<priority>,<sin>,<state>,<size>,<sent_bytes>
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        if 'OK' in response: response.remove('OK')
        for msg in response:
            if ',' in msg:
                detail = msg.split(',')
                states.append({
                    'name': detail[0].replace('"', ''),
                    'state': int(detail[4]),
                    'state_name': MessageState(int(detail[4])).name,
                    'size': int(detail[5]),
                    'sent': int(detail[6]),
                })
        return states
    
    def message_mo_cancel(self, name: str) -> bool:
        """Cancels a mobile-originated message in the Tx ready state."""
        _log.debug(f'Attempting to cancel message {name}')
        response = self.atcommand(f'AT%MGRC="{name}"')
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        return True

    def message_mo_clear(self) -> int:
        """Clears the modem transmit queue and returns the count cancelled.
        
        Returns:
            Count of messages deleted, or -1 in case of error

        """
        list_response = self.atcommand('AT%MGRL', filter=['%MGRL:'])
        if list_response[0] == 'ERROR':
            return -1
        message_count = len(list_response)
        for msg in list_response:
            _log.debug(f'Attempting to delete MO message {msg}')
            del_response = self.atcommand(f'AT%MGRD={msg}C')
            if del_response[0] == 'ERROR':
                _log.error(f'Error clearing messages from transmit queue')
                return -1
        return message_count

    def message_mt_waiting(self) -> 'list[dict]':
        """Gets a list of received mobile-terminated message information.
        
        Returns:
            List of message metadata in the receive queue including:
            - `name` (str)
            - `sin` (int) first byte of payload
            - `priority` (int)
            - `state` (int) The state number
            - `state_name` (str) The `MessageState.name`
            - `size` (int) in bytes
            - `received` (int) in bytes for large message progress

        """
        waiting = []
        _log.debug('Querying for waiting MT messages')
        response = self.atcommand('AT%MGFN', filter=['%MGFN:'])
        #: %MGFN: "name",number,priority,sin,state,length,bytes_received
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        if 'OK' in response: response.remove('OK')
        for msg in response:
            if (',' in msg):
                detail = msg.split(',')
                waiting.append({
                    'name': detail[0].replace('"', ''),
                    'sin': int(detail[3]),
                    'priority': int(detail[2]),
                    'state': int(detail[4]),
                    'state_name': MessageState(int(detail[4])).name,
                    'size': int(detail[5]),
                    'received': int(detail[6])
                    })
        return waiting

    def message_mt_get(self,
                       name: str,
                       data_format: int = DataFormat.BASE64,
                       meta: bool = False,
                       timeout: int = None,
                       ) -> 'bytes|dict':
        """Gets the payload of a specified mobile-terminated message.
        
        Payload is presented as a string with encoding based on data_format. 

        Args:
            name: The unique name in the modem queue e.g. FM01.01
            data_format: text=1, hex=2, base64=3 (default)
            meta: If False returns raw bytes, else returns formatted data
                with metadata.
            timeout: Optional timeout. If not specified, will be calculated
                based on the baudrate for the maximum message size, *3

        Returns:
            The raw data bytes if meta is False, or a dictionary with:
            - `name` (str) The name assigned by the modem
            - `system_message_number` (int) System-assigned number
            - `system_message_sequence` (int) System-assigned number
            - `sin` (int) First byte of payload
            - `priority` (int)
            - `state` (int) The message state number
            - `state_name` (str) The `MessageState.name`
            - `size` (int) in bytes
            - `data_format` (int) 1=text, 2=hex, 3=base64
            - `data` (str) presented based on data_format

        """
        if not meta and data_format != DataFormat.BASE64:
            data_format = DataFormat.BASE64
        baudrate = self.baudrate or 9600
        max_timeout = timeout or ceil(10000 / (baudrate / 8)) * 3
        _log.debug(f'Retrieving waiting MT message {name}')
        response = self.atcommand(f'AT%MGFG="{name}",{data_format}',
                                  filter=['%MGFG:'],
                                  timeout=max_timeout)
        if response[0] == 'ERROR':
            _log.error(f'Error retrieving message {name}')
            self._handle_at_error(response)
        #: name, number, priority, sin, state, length, data_format, data
        try:
            detail = response[0].split(',')
            sys_msg_num, sys_msg_seq = detail[1].split('.')
            msg_sin = int(detail[3])
            data_str_no_sin = detail[7]
            if data_format == DataFormat.HEX:
                data = hex(msg_sin) + data_str_no_sin.lower()
            elif data_format == DataFormat.BASE64:
                # add SIN byte to base64 blob
                databytes = bytes([msg_sin]) + b64decode(data_str_no_sin)
                if not meta:
                    return databytes
                data = b64encode(databytes).decode('ascii')
            elif data_format == DataFormat.TEXT:
                data = f'\\{msg_sin:02x}' + data_str_no_sin
            return {
                'name': detail[0].replace('"', ''),
                'system_message_number': int(sys_msg_num),
                'system_message_sequence': int(sys_msg_seq),
                'priority': int(detail[2]),
                'sin': msg_sin,
                'state': int(detail[4]),
                'state_name': MessageState(int(detail[4])).name,
                'size': int(detail[5]),
                'data_format': data_format,
                'data': data
            }
        except Exception as err:
            _log.exception(err)

    def message_mt_delete(self, name: str) -> bool:
        """Marks a Return message for deletion by the modem.
        
        Args:
            name: The unique mobile-terminated name in the queue

        Returns:
            True if the operation succeeded

        """
        _log.debug(f'Attempting to delete MT message {name}')
        response = self.atcommand(f'AT%MGFM="{name}"')
        if response[0] == 'ERROR':
            err = f' ({response[1]})' if self.error_detail else ''
            _log.error(f'Error deleting message {name}{err}')
        return response[0] == 'OK'

    def trace_event_detail_get(self) -> dict:
        """Gets a dictionary of monitored and cached class/subclass pairs.
        
        Returns:
            `{ 'monitored': [(<class,subclass>)], 'cached': [<class,subclass)] }` 
        """
        _log.debug('Querying monitored/cached trace events')
        response = self.atcommand('AT%EVMON', filter=['%EVMON:'])
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        if 'OK' in response: response.remove('OK')
        detail = {
            'monitored': [],
            'cached': [],
        }
        if len(response) > 0:
            events: 'list[str]' = response[0].split(',')
            for event in events:
                trace_class = int(event.split('.')[0])
                trace_subclass = int(event.split('.')[1].replace('*', ''))
                detail['monitored'].append((trace_class, trace_subclass))
                if event.endswith('*'):
                    detail['cached'].append((trace_class, trace_subclass))
        return detail

    def trace_event_monitor_get(self) -> 'list[tuple[int, int]]':
        return self.trace_event_detail_get()['monitored']
    
    def trace_event_monitor_set(self, events: 'list[tuple[int, int]]') -> bool:
        """Set a list of trace class/subclass pairs to monitor and cache."""
        command = 'AT%EVMON='
        for event in events:
            trace_class, trace_subclass = event
            if command != 'AT%EVMON=':
                command += ','
            command += f'{trace_class}.{trace_subclass}'
        _log.debug(f'Setting trace event monitoring for {events}')
        response = self.atcommand(command)
        if response[0] != 'ERROR':
            return True
        return False

    def trace_event_cache_get(self) -> 'list[tuple[int, int]]':
        return self.trace_event_detail_get()['cached']
    
    @property
    def trace_event_monitor(self) -> 'list[tuple[int, int]]':
        """The list of class/subclass pairs being monitored as events.
        
        Cached until set.
        """
        CACHE_TAG = 'trace_event_monitor'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        tem = self.trace_event_detail_get()['monitored']
        self._property_cache.cache(tem, CACHE_TAG, None)
        return tem
        
    @trace_event_monitor.setter
    def trace_event_monitor(self, events: 'list[tuple[int, int]]'):
        CACHE_TAG = 'trace_event_monitor'
        try:
            self.trace_event_monitor_set(events)
            self._property_cache.remove(CACHE_TAG)
        except Exception as err:
            _log.error(f'Failed to set trace_event_monitor {events}: {err}')

    @property
    def trace_events_cached(self) -> 'list[tuple[int, int]]':
        """The list of trace events cached for retrieval.
        
        Cached for 1 second.
        """
        CACHE_TAG = 'trace_events_cached'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        tec = self.trace_event_detail_get()['cached']
        self._property_cache.cache(tec, CACHE_TAG)
        return tec

    def trace_event_get(self,
                        event: 'tuple[int, int]',
                        meta: bool = False,
                        ) -> 'str|dict':
        """Gets the cached event by class/subclass.

        Args:
            event: tuple of (class, subclass)
            meta: Returns the raw text string if False (default)
        
        Returns:
            String if meta is True, else metadata dictionary including:
            - `data_count` (int)
            - `signed_bitmask` (str)
            - `mobile_id` (str)
            - `timestamp` (str)
            - `class` (str)
            - `subclass` (str)
            - `priority` (str)
            - `data` (str)
        
        Raises:
            AtException

        """
        def signed32(n: int) -> int:
            """Converts an integer to signed 32-bit format."""
            n = n & 0xffffffff
            return (n ^ 0x80000000) - 0x80000000
        def event_timestamp(log_timestamp: int) -> int:
            offset = int(datetime(2001, 1, 1, tzinfo=timezone.utc).timestamp())
            return log_timestamp + offset
        if not (isinstance(event, tuple) and len(event) == 2):
            raise ValueError('event_get expects (class, subclass)')
        trace_class, trace_subclass = event
        _log.debug(f'Retrieving trace event class {trace_class}'
                   f' subclass {trace_subclass}')
        response = self.atcommand(f'AT%EVNT={trace_class},{trace_subclass}',
                                  filter=['%EVNT:'])
        #: res %EVNT: <dataCount>,<signedBitmask>,<MTID>,<timestamp>,
        # <class>,<subclass>,<priority>,<data0>,<data1>,..,<dataN>
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        if not meta:
            return response[0]
        eventdata = response[0].split(',')
        event = {
            'data_count': int(eventdata[0]),
            'signed_bitmask': bin(int(eventdata[1])),
            'timestamp': event_timestamp(int(eventdata[3])),
            'class': int(eventdata[4]),
            'subclass': int(eventdata[5]),
            'priority': int(eventdata[6]),
            'raw_data': eventdata[7:],
            'data': {},
        }
        iso_time = datetime.utcfromtimestamp(event['timestamp']).isoformat()
        event['isotime'] = iso_time[:19] + 'Z'
        bitmask = event['signed_bitmask'][2:]
        while len(bitmask) < event['data_count']:
            bitmask = '0' + bitmask
        for i, bit in enumerate(reversed(bitmask)):
            if bit == '1':
                event['raw_data'][i] = signed32(int(event['raw_data'][i]))
            else:
                event['raw_data'][i] = int(event['raw_data'][i])
        # TODO lookup class/subclass definitions
        for trace_def in EVENT_TRACES:
            if trace_def.trace_class != trace_class:
                continue
            if trace_def.trace_subclass != trace_subclass:
                continue
            try:
                for i, value in enumerate(event['raw_data']):
                    tag, data_type = trace_def.data[i]
                    new_value = value
                    if 'flags' in tag and isinstance(data_type, dict):
                        new_value = []
                        for flag in data_type:
                            if flag & value:
                                new_value.append(data_type[flag])
                    elif str(tag).endswith('_state'):
                        if isinstance(data_type, dict):
                            new_value = data_type[value]
                        else:
                            try:   #: IntEnum
                                new_value = data_type(value)
                            except:
                                pass   # new_value stays as value
                    event['data'][tag] = new_value
            except Exception as err:
                _log.exception(err)
        return event

    @staticmethod
    def _list_events(bitmask: int) -> 'list[EventNotification]':
        events = []
        for notification in EventNotification:
            if bitmask & notification == notification:
                events.append(notification)
        return events

    def event_notification_monitor_get(self) -> 'list[EventNotification]':
        """The list of events monitored to assert the notification pin (`S88`)."""
        response = self.atcommand('ATS88?')
        if response[0] != 'ERROR':
            return self._list_events(int(response[0]))
        self._handle_at_error(response)
    
    def event_notification_monitor_set(self,
                                       event_list: 'list[EventNotification]',
                                       ) -> bool:
        bitmask = 0
        for event in event_list:
            bitmask = bitmask | event
        _log.debug(f'Setting event notifications: {event_list}')
        response = self.atcommand(f'ATS88={bitmask}')
        if response[0] != 'ERROR':
            return True
        return False
    
    @property
    def event_notification_monitor(self) -> 'list[EventNotification]':
        """The list of events monitored to assert the notification pin (`S88`).
        
        Cached until set.
        """
        CACHE_TAG = 'event_notification_monitor'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        events_monitored = self.event_notification_monitor_get()
        self._property_cache.cache(events_monitored, CACHE_TAG, None)
        return events_monitored
    
    @event_notification_monitor.setter
    def event_notification_monitor(self, event_list: 'list[EventNotification]'):
        CACHE_TAG = 'event_notification_monitor'
        try:
            self.event_notification_monitor_set(event_list)
            self._property_cache.remove(CACHE_TAG)
        except Exception as err:
            _log.error(f'Failed to set event_notification_monitor {event_list}'
                       f': {err}')

    def event_notifications_get(self) -> 'list[EventNotification]':
        """The list of active events reported in `S89`."""
        response = self.atcommand('ATS89?')
        if response[0] != 'ERROR':
            return self._list_events(int(response[0]))
        self._handle_at_error(response)
    
    @property
    def event_notifications(self) -> 'list[EventNotification]':
        """The list of active events reported in `S89`.
        
        Cached for 1 second.
        """
        CACHE_TAG = 'event_notifications'
        cached = self._property_cache.get_cached(CACHE_TAG)
        if cached is not None:
            return cached
        events = self.event_notifications_get()
        self._property_cache.cache(events, CACHE_TAG)
        return events
    
    def shutdown(self) -> bool:
        """Tell the modem to prepare for power-down."""
        _log.warning('Attempting to shut down modem')
        response = self.atcommand('AT%OFF')
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        return True

    @property
    def trace_log_mode(self) -> bool:
        return self._trace_log_mode
    
    def trace_log_mode_enable(self, enable: bool = True):
        """"""
        if (self._trace_log_mode is True and enable is True or
            self._trace_log_mode is False and enable is False):
            _log.warning('Trace log mode already'
                         f' {"en" if enable else "dis"}abled')
            return
        if enable:
            response = self.atcommand('AT%EXIT=5')
            if 'ERROR' in response[0]:
                self._handle_at_error(response)
            self._trace_log_mode = True
            return
        response = self.atcommand('\x18')
        if 'OK' in response:
            self._trace_log_mode = False
    
    def s_register_get(self, register: 'str|int') -> int:
        """Gets the value of the S-register requested.

        Args:
            register: The register name/number (e.g. S80)

        Returns:
            integer value or None
        """
        if isinstance(register, str):
            try:
                register = int(register.replace('S', ''))
            except ValueError:
                raise ValueError(f'Invalid S-register {register}')
        _log.debug(f'Querying S-register {register}')
        response = self.atcommand(f'ATS{register}?')
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        return int(response[0])

    def _s_registers_read(self) -> None:
        """Reads all defined S-registers."""
        raise NotImplementedError
        command = 'AT'
        for reg in self.s_registers:
            if command != 'AT':
                command += ' '
            command += f'{reg}?'
        _log.debug('Querying all S-register values')
        response = self.atcommand(command)
        if response[0] == 'ERROR':
            _log.error('Could not read S-registers')
            raise
        index = 0
        for name, register in self.s_registers.items():
            register.value = response[index]
            index += 1

    def s_register_get_definitions(self) -> list:
        """(Future) Gets a list of S-register definitions.
        
        R=read-only, S=signed, V=volatile
        
        Returns:
            tuple(register, RSV, current, default, minimum, maximum) or None
        """
        raise NotImplementedError
        #: AT%SREG
        #: Sreg, RSV, CurrentVal, DefaultVal, MinimumVal, MaximumVal
        response = self.atcommand('AT%SREG')
        if response[0] == 'ERROR':
            self._handle_at_error(response)
        if 'OK' in response: response.remove('OK')
        # header_rows = response[0:1]
        # Sreg RSV CurrentVal NvmValue DefaultValue MinimumValue MaximumVal
        reg_defs = response[2:]
        registers = []
        for row in reg_defs:
            reg_def = row.split(' ')
            reg_def = tuple(filter(None, reg_def))
            registers.append(reg_def)
        return registers
