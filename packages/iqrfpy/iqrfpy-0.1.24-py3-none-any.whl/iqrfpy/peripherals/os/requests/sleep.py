from __future__ import annotations
from dataclasses import dataclass
from typeguard import typechecked
from typing import Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = [
    'SleepRequest',
    'OsSleepParams'
]


@typechecked
class OsSleepParams:
    time: int = 0
    wake_up_on_negative_edge: bool = False
    calibrate_before_sleep: bool = False
    flash_led_after_sleep: bool = False
    wake_up_on_positive_edge: bool = False
    use_milliseconds: bool = False
    use_deep_sleep: bool = False

    def __init__(self, time: int = 0, wake_up_on_negative_edge: bool = False, calibrate_before_sleep: bool = False,
                 flash_led_after_sleep: bool = False, wake_up_on_positive_edge: bool = False,
                 use_milliseconds: bool = False, use_deep_sleep: bool = False):
        self.time = time
        self.wake_up_on_negative_edge = wake_up_on_negative_edge
        self.calibrate_before_sleep = calibrate_before_sleep
        self.flash_led_after_sleep = flash_led_after_sleep
        self.wake_up_on_positive_edge = wake_up_on_positive_edge
        self.use_milliseconds = use_milliseconds
        self.use_deep_sleep = use_deep_sleep
        self.__post_init__()

    def __post_init__(self):
        if not (dpa_constants.WORD_MIN <= self.time <= dpa_constants.WORD_MAX):
            raise RequestParameterInvalidValueError('Time value should be between 0 and 65535.')

    def _calculate_control(self):
        return self.wake_up_on_negative_edge | (self.calibrate_before_sleep << 1) | \
                  (self.flash_led_after_sleep << 2) | (self.wake_up_on_positive_edge << 3) | \
                  (self.use_milliseconds << 4) | (self.use_deep_sleep << 5)

    def to_pdata(self):
        return [self.time & 0xFF, (self.time >> 8) & 0xFF, self._calculate_control()]

    def to_json(self):
        return {
            'time': self.time,
            'control': self._calculate_control()
        }


@typechecked
class SleepRequest(IRequest):

    __slots__ = '_sleep_params'

    def __init__(self, nadr: int, params: OsSleepParams, hwpid: int = dpa_constants.HWPID_MAX,
                 timeout: Optional[float] = None, msgid: Optional[str] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.SLEEP,
            m_type=OSMessages.SLEEP,
            hwpid=hwpid,
            timeout=timeout,
            msgid=msgid
        )
        self._sleep_params = params

    def set_sleep_params(self, params: OsSleepParams):
        self._sleep_params = params
        c = OsSleepParams()

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = self._sleep_params.to_pdata()
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = self._sleep_params.to_json()
        return super().to_json()
