"""Decodes rotary-dial pulses into digits.

Two decoders are provided:

- `DialDecoder` — the classic, robust scheme, used when the dial exposes
  *two* contacts: an "off-normal" contact closed for the whole time the
  dial is off its rest position, and a "pulse" contact that opens/closes
  once per pulse as the dial *returns*. The number of pulses is the digit
  (0 is sent as 10 pulses). The off-normal contact bounds the counting
  window exactly, so there's no ambiguity about when a digit ends.

- `TimeoutDialDecoder` — a fallback for dials wired with *only* a pulse
  contact (2 wires). Groups pulses into a digit after a period of silence
  (`inter_digit_timeout`). Less robust — a slow last pulse can delay
  recognition — but works without the off-normal wire.

Both are pure/hardware-independent: feed them already-debounced level
changes (see `debounce.Debouncer`) and they call back with each decoded
digit.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


def _pulses_to_digit(pulse_count: int) -> int:
    return 0 if pulse_count == 10 else pulse_count


@dataclass
class DialDecoder:
    on_digit: Callable[[int], None]
    _pulse_count: int = 0
    _dialing: bool = False

    def off_normal_changed(self, active: bool) -> None:
        if active and not self._dialing:
            self._dialing = True
            self._pulse_count = 0
        elif not active and self._dialing:
            self._dialing = False
            if self._pulse_count > 0:
                self.on_digit(_pulses_to_digit(self._pulse_count))
            self._pulse_count = 0

    def pulse_changed(self, active: bool) -> None:
        if self._dialing and active:
            self._pulse_count += 1


@dataclass
class TimeoutDialDecoder:
    on_digit: Callable[[int], None]
    inter_digit_timeout: float = 0.3
    _pulse_count: int = 0
    _last_pulse_time: Optional[float] = None

    def pulse_changed(self, active: bool, timestamp: float) -> None:
        if active:
            self._pulse_count += 1
            self._last_pulse_time = timestamp

    def tick(self, timestamp: float) -> None:
        if (
            self._pulse_count > 0
            and self._last_pulse_time is not None
            and timestamp - self._last_pulse_time >= self.inter_digit_timeout
        ):
            self.on_digit(_pulses_to_digit(self._pulse_count))
            self._pulse_count = 0
            self._last_pulse_time = None
