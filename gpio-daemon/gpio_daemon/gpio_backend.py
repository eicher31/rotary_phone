"""GPIO backend abstraction.

Only the two things the daemon actually needs are exposed: watching a pin
for raw level changes, and driving an output pin. Keeping this layer thin
and "dumb" (no debouncing here) means the interesting logic —
`debounce.Debouncer`, `dial_decoder`, `ringer` — stays hardware-free and
unit-testable; only this module needs real GPIO to exercise, which is why
`GpiozeroBackend` has not been tested outside of this repository (see
docs/README.md — "État du projet").
"""
from __future__ import annotations

import time
from typing import Callable, Dict, Protocol

# pin, raw level (0/1), monotonic timestamp
EdgeCallback = Callable[[int, int, float], None]


def active_from_level(value: int, active_low: bool) -> bool:
    """Translate a raw GPIO level into a semantic "contact closed" state."""
    return (value == 0) if active_low else (value == 1)


class GPIOBackend(Protocol):
    def watch_input(self, pin: int, pull_up: bool, callback: EdgeCallback) -> None: ...

    def read(self, pin: int) -> int: ...

    def setup_output(self, pin: int, initial: int = 0) -> None: ...

    def write(self, pin: int, value: int) -> None: ...


class GpiozeroBackend:
    """Real hardware backend, built on gpiozero (lgpio under the hood on
    a Raspberry Pi Zero 2 W / recent Raspberry Pi OS)."""

    def __init__(self) -> None:
        from gpiozero import DigitalInputDevice, DigitalOutputDevice  # local: only needed on a Pi

        self._DigitalInputDevice = DigitalInputDevice
        self._DigitalOutputDevice = DigitalOutputDevice
        self._inputs: Dict[int, "DigitalInputDevice"] = {}
        self._outputs: Dict[int, "DigitalOutputDevice"] = {}

    def watch_input(self, pin: int, pull_up: bool, callback: EdgeCallback) -> None:
        # bounce_time=None: no debouncing here, it's handled explicitly
        # in debounce.Debouncer so the same logic can be unit-tested.
        device = self._DigitalInputDevice(pin, pull_up=pull_up, bounce_time=None)
        device.when_activated = lambda: callback(pin, 1, time.monotonic())
        device.when_deactivated = lambda: callback(pin, 0, time.monotonic())
        self._inputs[pin] = device

    def read(self, pin: int) -> int:
        return int(self._inputs[pin].value)

    def setup_output(self, pin: int, initial: int = 0) -> None:
        self._outputs[pin] = self._DigitalOutputDevice(pin, initial_value=bool(initial))

    def write(self, pin: int, value: int) -> None:
        device = self._outputs[pin]
        if value:
            device.on()
        else:
            device.off()


class FakeBackend:
    """In-memory backend for tests: lets a test feed synthetic edges and
    inspect output writes without any real GPIO."""

    def __init__(self) -> None:
        self._callbacks: Dict[int, EdgeCallback] = {}
        self.output_log: list = []
        self._output_state: Dict[int, int] = {}

    def watch_input(self, pin: int, pull_up: bool, callback: EdgeCallback) -> None:
        self._callbacks[pin] = callback

    def read(self, pin: int) -> int:
        return self._output_state.get(pin, 0)

    def setup_output(self, pin: int, initial: int = 0) -> None:
        self._output_state[pin] = initial

    def write(self, pin: int, value: int) -> None:
        self._output_state[pin] = value
        self.output_log.append((pin, value))

    def emit(self, pin: int, value: int, timestamp: float) -> None:
        """Test helper: simulate a raw edge on `pin`."""
        callback = self._callbacks.get(pin)
        if callback is not None:
            callback(pin, value, timestamp)
