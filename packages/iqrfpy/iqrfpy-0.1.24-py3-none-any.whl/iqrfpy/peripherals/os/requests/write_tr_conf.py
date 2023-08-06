from __future__ import annotations
from typeguard import typechecked
from typing import List, Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['WriteTrConfRequest', 'OsWriteTrConfData']


@typechecked
class OsWriteTrConfData:
    __slots__ = 'embedded_peripherals', 'custom_dpa_handler', 'dpa_peer_to_peer', 'routing_off', 'io_setup', \
        'user_peer_to_peer', 'stay_awake_when_not_bonded', 'std_and_lp_network', 'rf_output_power', \
        'rf_signal_filter', 'lp_rf_timeout', 'uart_baud_rate', 'alternative_dsm_channel', 'local_frc', 'rf_channel_a', \
        'rf_channel_b', 'undocumented'

    def __init__(self, embedded_peripherals: Optional[List[int]] = None, custom_dpa_handler: bool = False,
                 dpa_peer_to_peer: bool = False, routing_off: bool = False, io_setup: bool = False,
                 user_peer_to_peer: bool = False, stay_awake_when_not_bonded: bool = False,
                 std_and_lp_network: bool = False, rf_output_power: int = 7, rf_signal_filter: int = 5,
                 lp_rf_timeout: int = 6,
                 uart_baud_rate: Union[dpa_constants.BaudRates, int] = dpa_constants.BaudRates.B9600,
                 alternative_dsm_channel: int = 0, local_frc: bool = False, rf_channel_a: int = 52,
                 rf_channel_b: int = 2, undocumented: Optional[List[int]] = None):
        if embedded_peripherals is None:
            embedded_peripherals = []
        self.embedded_peripherals = embedded_peripherals
        self.custom_dpa_handler = custom_dpa_handler
        self.dpa_peer_to_peer = dpa_peer_to_peer
        self.routing_off = routing_off
        self.io_setup = io_setup
        self.user_peer_to_peer = user_peer_to_peer
        self.stay_awake_when_not_bonded = stay_awake_when_not_bonded
        self.std_and_lp_network = std_and_lp_network
        self.rf_output_power = rf_output_power
        self.rf_signal_filter = rf_signal_filter
        self.lp_rf_timeout = lp_rf_timeout
        self.uart_baud_rate = uart_baud_rate
        self.alternative_dsm_channel = alternative_dsm_channel
        self.local_frc = local_frc
        self.rf_channel_a = rf_channel_a
        self.rf_channel_b = rf_channel_b
        if undocumented is None:
            undocumented = [0] * 13
        self.undocumented = undocumented
        self._validate()

    def _validate(self):
        self.validate_embedded_peripherals(self.embedded_peripherals)
        self.validate_rf_output_power(self.rf_output_power)
        self.validate_rf_signal_filter(self.rf_signal_filter)
        self.validate_lp_rf_timeout(self.lp_rf_timeout)
        self.validate_uart_baud_rate(self.uart_baud_rate)
        self.validate_alternative_dsm_channel(self.alternative_dsm_channel)
        self.validate_rf_channel_a(self.rf_channel_a)
        self.validate_rf_channel_b(self.rf_channel_b)
        self.validate_undocumented(self.undocumented)

    @staticmethod
    def validate_embedded_peripherals(embedded_peripherals: List[Union[EmbedPeripherals, int]]) -> None:
        if len(embedded_peripherals) > 32:
            raise RequestParameterInvalidValueError('Embedded peripherals should be at most 32 values.')
        if min(embedded_peripherals, default=0) < 0 or max(embedded_peripherals, default=0) > 31:
            raise RequestParameterInvalidValueError('Embedded peripherals values should be between 0 and 31.')

    @staticmethod
    def validate_rf_output_power(rf_output_power: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_output_power <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF output power value should be between 0 and 255.')

    @staticmethod
    def validate_rf_signal_filter(rf_signal_filter: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_signal_filter <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF signal filter value should be between 0 and 255.')

    @staticmethod
    def validate_lp_rf_timeout(lp_rf_timeout: int) -> None:
        if not (dpa_constants.BYTE_MIN <= lp_rf_timeout <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('LP RF timeout value should be between 0 and 255.')

    @staticmethod
    def validate_uart_baud_rate(uart_baud_rate: Union[dpa_constants.BaudRates, int]) -> None:
        if not (dpa_constants.BYTE_MIN <= uart_baud_rate <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('UART baud rate value should be between 0 and 255.')

    @staticmethod
    def validate_alternative_dsm_channel(alternative_dsm_channels: int) -> None:
        if not (dpa_constants.BYTE_MIN <= alternative_dsm_channels <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Alternative DMS channel value should be between 0 and 255.')

    @staticmethod
    def validate_rf_channel_a(rf_channel_a: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_channel_a <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF channel A value should be between 0 and 255.')

    @staticmethod
    def validate_rf_channel_b(rf_channel_b: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_channel_b <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF channel B value should be between 0 and 255.')

    @staticmethod
    def validate_undocumented(undocumented: List[int]) -> None:
        if len(undocumented) != 13:
            raise RequestParameterInvalidValueError('Undocumented block should be 13B long.')
        if not Common.values_in_byte_range(undocumented):
            raise RequestParameterInvalidValueError('Undocumented block values should be between 0 and 255.')

    def to_pdata(self) -> List[int]:
        embed_pers = Common.peripheral_list_to_bitmap(self.embedded_peripherals)
        conf_bits_0 = int(self.custom_dpa_handler) | int(self.dpa_peer_to_peer) << 1 | int(self.routing_off) << 3 | \
            int(self.io_setup) << 4 | int(self.user_peer_to_peer) << 5 | \
            int(self.stay_awake_when_not_bonded) << 6 | int(self.std_and_lp_network) << 7
        return embed_pers + [conf_bits_0] + [0] * 2 + \
            [self.rf_output_power, self.rf_signal_filter, self.lp_rf_timeout, self.uart_baud_rate,
             self.alternative_dsm_channel, int(self.local_frc)] + [0] * 3 + [self.rf_channel_a, self.rf_channel_b] + \
            self.undocumented


@typechecked
class WriteTrConfRequest(IRequest):
    __slots__ = '_configuration', '_rfpgm'

    def __init__(self, nadr: int, configuration: Union[OsWriteTrConfData, List[int]], rfpgm: int,
                 hwpid: int = dpa_constants.HWPID_MAX, timeout: Optional[float] = None, msgid: Optional[str] = None):
        self._validate(configuration=configuration, rfpgm=rfpgm)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.WRITE_CFG,
            m_type=OSMessages.WRITE_CFG,
            hwpid=hwpid,
            timeout=timeout,
            msgid=msgid
        )
        self._configuration = configuration
        self._rfpgm = rfpgm

    def _validate(self, configuration: Union[OsWriteTrConfData, List[int]], rfpgm: int) -> None:
        self._validate_configuration(configuration)
        self._validate_rfpgm(rfpgm)

    @staticmethod
    def _validate_configuration(configuration: Union[OsWriteTrConfData, List[int]]) -> None:
        if type(configuration) == OsWriteTrConfData:
            OsWriteTrConfData.validate_embedded_peripherals(configuration.embedded_peripherals)
            OsWriteTrConfData.validate_rf_output_power(configuration.rf_output_power)
            OsWriteTrConfData.validate_rf_signal_filter(configuration.rf_signal_filter)
            OsWriteTrConfData.validate_lp_rf_timeout(configuration.lp_rf_timeout)
            OsWriteTrConfData.validate_uart_baud_rate(configuration.uart_baud_rate)
            OsWriteTrConfData.validate_alternative_dsm_channel(configuration.alternative_dsm_channel)
            OsWriteTrConfData.validate_rf_channel_b(configuration.rf_channel_a)
            OsWriteTrConfData.validate_rf_channel_b(configuration.rf_channel_b)
            OsWriteTrConfData.validate_undocumented(configuration.undocumented)
        else:
            if len(configuration) != 31:
                raise RequestParameterInvalidValueError('Configuration byte list should be 31B long.')
            if not Common.values_in_byte_range(configuration):
                raise RequestParameterInvalidValueError('Configuration byte list values should be between 0 and 255.')

    @staticmethod
    def _validate_rfpgm(rfpgm: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rfpgm <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RFPGM should be a value between 0 and 255.')

    def set_configuration(self, configuration: Union[OsWriteTrConfData, List[int]]) -> None:
        self._validate_configuration(configuration)
        self._configuration = configuration

    def set_rfpgm(self, rfpgm: int) -> None:
        self._validate_rfpgm(rfpgm)
        self._rfpgm = rfpgm

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        if type(self._configuration) == OsWriteTrConfData:
            self._pdata = [0] + self._configuration.to_pdata() + [self._rfpgm]
        else:
            self._pdata = [0] + self._configuration + [self._rfpgm]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {
            'checksum': 0,
            'configuration': self._configuration.to_pdata() if type(
                self._configuration) == OsWriteTrConfData else self._configuration,
            'rfpgm': self._rfpgm,
        }
        return super().to_json()
