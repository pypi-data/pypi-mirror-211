from __future__ import annotations
from dataclasses import dataclass
from typeguard import typechecked
from typing import List, Optional, Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['ValidateBondsRequest', 'NodeValidateBondsParams']


@dataclass(slots=True)
@typechecked
class NodeValidateBondsParams:
    bondAddr: int
    mid: int

    def __post_init__(self):
        if not (dpa_constants.BYTE_MIN <= self.bondAddr <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Bond address value should be between 1 and 239.')
        if not (dpa_constants.MID_MIN <= self.mid <= dpa_constants.MID_MAX):
            raise RequestParameterInvalidValueError('MID value should be an unsigned 32bit integer.')


@typechecked
class ValidateBondsRequest(IRequest):

    __slots__ = '_nodes'

    def __init__(self, nadr: int, nodes: List[NodeValidateBondsParams], hwpid: int = dpa_constants.HWPID_MAX,
                 timeout: Optional[float] = None, msgid: Optional[str] = None):
        self._validate(nodes)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.VALIDATE_BONDS,
            m_type=NodeMessages.VALIDATE_BONDS,
            hwpid=hwpid,
            timeout=timeout,
            msgid=msgid
        ),
        self._nodes: List[NodeValidateBondsParams] = nodes

    @staticmethod
    def _validate(nodes: List[NodeValidateBondsParams]) -> None:
        if len(nodes) > 11:
            raise RequestParameterInvalidValueError('Request can carry at most 11 pairs of address and MID.')

    def set_nodes(self, nodes: List[NodeValidateBondsParams]) -> None:
        self._validate(nodes)
        self._nodes = nodes

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        pdata = []
        for node in self._nodes:
            pdata.append(node.bondAddr)
            pdata.append(node.mid & 0xFF)
            pdata.append((node.mid >> 8) & 0xFF)
            pdata.append((node.mid >> 16) & 0xFF)
            pdata.append((node.mid >> 24) & 0xFF)
        self._pdata = pdata
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'nodes': [{'bondAddr': node.bondAddr, 'mid': node.mid} for node in self._nodes]}
        return super().to_json()
