from __future__ import annotations
from dataclasses import dataclass
from typeguard import typechecked
from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.common import Common
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['ReadTrConfResponse', 'OsReadTrConfData']


@dataclass
class OsReadTrConfData:

    __slots__ = 'embedded_peripherals', 'custom_dpa_handler', 'dpa_peer_to_peer', 'routing_off', 'io_setup', \
        'user_peer_to_peer', 'stay_awake_when_not_bonded', 'std_and_lp_network', 'rf_output_power', \
        'rf_signal_filter', 'lp_rf_timeout', 'uart_baud_rate', 'alternative_dsm_channel', 'local_frc', 'rf_channel_a', \
        'rf_channel_b', 'undocumented', 'raw_data'

    def __init__(self, data: List[int]):
        embed_pers_data = data[0:4]
        embedded_pers = []
        for i in range(0, len(embed_pers_data * 8)):
            if embed_pers_data[int(i / 8)] & (1 << (i % 8)) and EmbedPeripherals.has_value(i):
                embedded_pers.append(EmbedPeripherals(i))
        self.embedded_peripherals = embedded_pers
        self.custom_dpa_handler = bool(data[4] & 1)
        self.dpa_peer_to_peer = bool(data[4] & 2)
        self.routing_off = bool(data[4] & 8)
        self.io_setup = bool(data[4] & 16)
        self.user_peer_to_peer = bool(data[4] & 32)
        self.stay_awake_when_not_bonded = bool(data[4] & 64)
        self.std_and_lp_network = bool(data[4] & 128)
        self.rf_output_power = data[7]
        self.rf_signal_filter = data[8]
        self.lp_rf_timeout = data[9]
        self.uart_baud_rate = data[10]
        self.alternative_dsm_channel = data[11]
        self.local_frc = bool(data[12] & 1)
        self.rf_channel_a = data[16]
        self.rf_channel_b = data[17]
        self.undocumented = data[18:]
        self.raw_data = data


@typechecked
class ReadTrConfResponse(IResponseGetterMixin):

    __slots__ = '_checksum', '_configuration', '_rfpgm', '_init_phy'

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSResponseCommands.READ_CFG,
            m_type=OSMessages.READ_CFG,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._checksum = result['checksum']
            self._configuration = OsReadTrConfData(result['configuration'])
            self._rfpgm = result['rfpgm']
            self._init_phy = result['initphy']

    def get_checksum(self) -> int:
        return self._checksum

    def get_configuration(self) -> OsReadTrConfData:
        return self._configuration

    def get_rfpgm(self) -> int:
        return self._rfpgm

    def get_init_phy(self) -> int:
        return self._init_phy

    @staticmethod
    def from_dpa(dpa: bytes) -> ReadTrConfResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = None
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=42)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'checksum': pdata[0],
                'configuration': list(pdata[1:32]),
                'rfpgm': pdata[32],
                'initphy': pdata[33],
            }
        return ReadTrConfResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @staticmethod
    def from_json(json: dict) -> ReadTrConfResponse:
        JsonValidator.response_received(json=json)
        nadr = Common.nadr_from_json(json=json)
        msgid = Common.msgid_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        return ReadTrConfResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata,
                                  result=result)
