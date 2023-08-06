from __future__ import annotations
from typeguard import typechecked
from typing import List, Optional, Union
from iqrfpy.enums.commands import Command, OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import Peripheral, EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['BatchRequest']


@typechecked
class BatchData:

    __slots__ = 'pnum', 'pcmd', 'hwpid', 'pdata'

    def __init__(self, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int, pdata: List[int]):
        self.pnum = pnum
        self.pcmd = pcmd
        self.hwpid = hwpid
        self.pdata = pdata

    def to_pdata(self):
        data = [self.pnum, self.pcmd, self.hwpid & 0xFF, (self.hwpid >> 8) & 0xFF] + self.pdata
        return [len(data)] + data

    def to_json(self):
        return {
            'pnum': f'{self.pnum:02x}',
            'pcmd': f'{self.pcmd:02x}',
            'hwpid': f'{self.hwpid:04x}',
            'rdata': '.'.join([f'{x:02x}' for x in self.pdata])
        }


@typechecked
class BatchRequest(IRequest):

    __slots__ = '_requests'

    def __init__(self, nadr: int, requests: List[BatchRequest], hwpid: int = dpa_constants.HWPID_MAX,
                 timeout: Optional[float] = None, msgid: Optional[str] = None):
        self._validate(requests)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.SET_SECURITY,
            m_type=OSMessages.SET_SECURITY,
            hwpid=hwpid,
            timeout=timeout,
            msgid=msgid
        )
        self._requests = requests

    @staticmethod
    def _validate(requests: List[BatchRequest]):
        data = []
        for request in requests:
            data += request.to_pdata()
        if len(data) + 1 > 58:
            raise RequestParameterInvalidValueError('Batch requests data should be no larger than 58B.')

    def set_requests(self, requests: List[BatchRequest]):
        self._validate(requests)
        self._requests = requests

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = []
        for request in self._requests:
            self._pdata += request.to_pdata()
        self._pdata.append(0)
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'requests': [request.to_json() for request in self._requests]}
        return super().to_json()
