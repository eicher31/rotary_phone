"""Drives the GPIO output wired to the bell-striking motor/solenoid,
producing a ring cadence on the phone's own mechanical bells.

Like the debouncers, this is driven by a periodic `tick(now)` call rather
than blocking sleeps, so it can run on the same simple main loop and be
unit-tested with synthetic timestamps.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Tuple


@dataclass
class RingCadence:
    """A repeating sequence of (duration_seconds, pin_active) steps."""

    steps: List[Tuple[float, bool]]

    @property
    def total_duration(self) -> float:
        return sum(duration for duration, _ in self.steps)


# ~1s of rapid strikes against the bells ("buzz"), then ~4s of silence,
# repeating — a reasonable approximation of a classic European ring
# cadence. Tune to taste once you've heard it on the real bells.
DEFAULT_CADENCE = RingCadence(
    steps=[
        (0.08, True), (0.08, False),
        (0.08, True), (0.08, False),
        (0.08, True), (0.08, False),
        (0.08, True), (0.08, False),
        (0.08, True), (0.08, False),
        (0.08, True), (0.08, False),
        (4.0, False),
    ]
)


@dataclass
class Ringer:
    write_pin: Callable[[int], None]
    cadence: RingCadence = field(default_factory=lambda: DEFAULT_CADENCE)
    _ringing: bool = False
    _cycle_start: float = 0.0

    def start(self, timestamp: float) -> None:
        self._ringing = True
        self._cycle_start = timestamp

    def stop(self) -> None:
        self._ringing = False
        self.write_pin(0)

    def tick(self, timestamp: float) -> None:
        if not self._ringing:
            return
        elapsed = (timestamp - self._cycle_start) % self.cadence.total_duration
        acc = 0.0
        for duration, active in self.cadence.steps:
            if elapsed < acc + duration:
                self.write_pin(1 if active else 0)
                return
            acc += duration
