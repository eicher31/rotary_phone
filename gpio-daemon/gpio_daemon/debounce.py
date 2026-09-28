"""Software debouncing of raw GPIO level changes.

Takes a stream of (value, timestamp) samples for a single pin and only
reports a level change once it has stayed stable for `stable_seconds`.

Purely edge-driven debouncing has a gap: if the very last raw edge before
the contact settles already carries the final value, nothing else will
ever call back into the debouncer to confirm it. To cover that, the
caller must also call `tick(now)` periodically (the daemon's main loop
does this every few milliseconds) so a settled state gets reported even
without a further edge.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Debouncer:
    stable_seconds: float
    on_change: Callable[[int, float], None]
    _pending_value: Optional[int] = None
    _pending_since: Optional[float] = None
    _stable_value: Optional[int] = None

    def feed(self, value: int, timestamp: float) -> None:
        """Record a raw level change (call this from the GPIO edge callback)."""
        if value == self._stable_value:
            # Back to the already-confirmed level: not a real transition.
            self._pending_value = None
            self._pending_since = None
            return

        if value != self._pending_value:
            self._pending_value = value
            self._pending_since = timestamp

        self._maybe_fire(timestamp)

    def tick(self, timestamp: float) -> None:
        """Call periodically so a settled state is confirmed even with no further edge."""
        self._maybe_fire(timestamp)

    def _maybe_fire(self, timestamp: float) -> None:
        if self._pending_value is None or self._pending_since is None:
            return
        if timestamp - self._pending_since >= self.stable_seconds:
            self._stable_value = self._pending_value
            self._pending_value = None
            self._pending_since = None
            self.on_change(self._stable_value, timestamp)
