"""Main daemon: wires GPIO events (hook switch, rotary dial) to MQTT
publication and to baresip call control.

Run as a systemd service — see rotary-phone-daemon.service and
docs/setup.md.

Threading note: gpiozero delivers edge callbacks on its own background
threads, while the main loop below drives the periodic `tick()` calls
(needed by the debouncers and the ringer, see their docstrings) on the
daemon's own thread. `_lock` serializes access to the shared decoder/
debouncer state between the two; at the event rates a single phone
produces (a handful of edges per second) a single coarse lock is more
than enough, no need for anything fancier.
"""
from __future__ import annotations

import argparse
import threading
import time
from typing import List

from .baresip_client import BaresipClient
from .config import DaemonConfig
from .debounce import Debouncer
from .dial_decoder import DialDecoder, TimeoutDialDecoder
from .gpio_backend import GpiozeroBackend, active_from_level
from .mqtt_client import MqttClient
from .ringer import Ringer

TICK_INTERVAL = 0.005  # 5 ms: fine enough to resolve a ~33 ms rotary-dial pulse


class PhoneDaemon:
    def __init__(self, config: DaemonConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
        self._backend = GpiozeroBackend()
        self._mqtt = MqttClient(config.mqtt_host, config.mqtt_port, client_id=f"rotary-{config.phone_id}")
        self._baresip = BaresipClient(config.baresip_ctrl_host, config.baresip_ctrl_port)

        self._digits: List[int] = []
        self._off_hook = False

        self._hook_debouncer = Debouncer(config.hook_debounce_seconds, self._on_hook_change)
        self._pulse_debouncer = Debouncer(config.pulse_debounce_seconds, self._on_pulse_change)

        self._two_contact_dial = config.pins.dial_off_normal is not None
        if self._two_contact_dial:
            self._off_normal_debouncer: "Debouncer | None" = Debouncer(
                config.pulse_debounce_seconds, self._on_off_normal_change
            )
            self._dial_decoder = DialDecoder(on_digit=self._on_digit)
        else:
            # No off-normal wire available: fall back to grouping pulses
            # by inter-digit silence (see dial_decoder.TimeoutDialDecoder).
            self._off_normal_debouncer = None
            self._dial_decoder = TimeoutDialDecoder(
                on_digit=self._on_digit, inter_digit_timeout=config.inter_digit_timeout_seconds
            )

        self._ringer = Ringer(write_pin=lambda v: self._backend.write(config.pins.ringer_output, v))

    def start(self) -> None:
        pins = self._config.pins
        self._backend.setup_output(pins.ringer_output, initial=0)
        self._backend.watch_input(pins.hook, pull_up=pins.hook_active_low, callback=self._raw_hook_edge)
        self._backend.watch_input(
            pins.dial_pulse, pull_up=pins.dial_pulse_active_low, callback=self._raw_pulse_edge
        )
        if pins.dial_off_normal is not None:
            self._backend.watch_input(
                pins.dial_off_normal,
                pull_up=pins.dial_off_normal_active_low,
                callback=self._raw_off_normal_edge,
            )

        self._mqtt.connect()
        self._mqtt.subscribe(f"phone/{self._config.phone_id}/cmd/#", self._on_command)
        self._baresip.connect()
        self._baresip.on_event(self._on_baresip_event)

        self._publish_state()
        self._run_loop()

    def _run_loop(self) -> None:
        while True:
            now = time.monotonic()
            with self._lock:
                self._hook_debouncer.tick(now)
                self._pulse_debouncer.tick(now)
                if self._off_normal_debouncer is not None:
                    self._off_normal_debouncer.tick(now)
                elif isinstance(self._dial_decoder, TimeoutDialDecoder):
                    self._dial_decoder.tick(now)
                self._ringer.tick(now)
            time.sleep(TICK_INTERVAL)

    # --- raw GPIO callbacks (may run on a gpiozero background thread) ---

    def _raw_hook_edge(self, _pin: int, value: int, timestamp: float) -> None:
        active = active_from_level(value, self._config.pins.hook_active_low)
        with self._lock:
            self._hook_debouncer.feed(int(active), timestamp)

    def _raw_pulse_edge(self, _pin: int, value: int, timestamp: float) -> None:
        active = active_from_level(value, self._config.pins.dial_pulse_active_low)
        with self._lock:
            self._pulse_debouncer.feed(int(active), timestamp)

    def _raw_off_normal_edge(self, _pin: int, value: int, timestamp: float) -> None:
        active = active_from_level(value, self._config.pins.dial_off_normal_active_low)
        with self._lock:
            assert self._off_normal_debouncer is not None
            self._off_normal_debouncer.feed(int(active), timestamp)

    # --- debounced-level callbacks (already run under self._lock) ---

    def _on_hook_change(self, value: int, _timestamp: float) -> None:
        self._off_hook = bool(value)
        if self._off_hook:
            self._digits = []
            self._ringer.stop()
            self._baresip.answer()
        else:
            self._baresip.hangup()
        self._publish_state()

    def _on_pulse_change(self, value: int, timestamp: float) -> None:
        if self._two_contact_dial:
            self._dial_decoder.pulse_changed(active=bool(value))
        else:
            self._dial_decoder.pulse_changed(active=bool(value), timestamp=timestamp)

    def _on_off_normal_change(self, value: int, _timestamp: float) -> None:
        self._dial_decoder.off_normal_changed(active=bool(value))

    def _on_digit(self, digit: int) -> None:
        self._digits.append(digit)
        self._mqtt.publish(
            f"phone/{self._config.phone_id}/digit",
            {"digit": digit, "buffer": "".join(str(d) for d in self._digits)},
        )
        if len(self._digits) >= self._config.dial_digit_count:
            number = "".join(str(d) for d in self._digits)
            self._baresip.dial(number)
            self._digits = []

    # --- MQTT command handling (régie de jeu -> ce poste) ---

    def _on_command(self, topic: str, _payload: bytes) -> None:
        command = topic.rsplit("/", 1)[-1]
        if command == "ring":
            self._ringer.start(time.monotonic())
        elif command == "ring_stop":
            self._ringer.stop()

    # --- baresip events -> MQTT + ringer ---

    def _on_baresip_event(self, event: dict) -> None:
        self._mqtt.publish(f"phone/{self._config.phone_id}/call_state", event)
        if event.get("type") == "CALL_INCOMING":
            self._ringer.start(time.monotonic())
        elif event.get("type") in ("CALL_CLOSED", "CALL_ESTABLISHED"):
            self._ringer.stop()

    def _publish_state(self) -> None:
        self._mqtt.publish(
            f"phone/{self._config.phone_id}/state",
            {"hook": "offhook" if self._off_hook else "onhook"},
            retain=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Rotary phone GPIO/SIP/MQTT daemon")
    parser.add_argument("--config", required=True, help="Path to config YAML (see config.example.yaml)")
    args = parser.parse_args()

    config = DaemonConfig.from_file(args.config)
    PhoneDaemon(config).start()


if __name__ == "__main__":
    main()
