"""Loads the per-phone YAML configuration (see config.example.yaml)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import yaml


@dataclass
class PinConfig:
    hook: int
    dial_pulse: int
    ringer_output: int
    dial_off_normal: Optional[int] = None
    hook_active_low: bool = True
    dial_pulse_active_low: bool = True
    dial_off_normal_active_low: bool = True


@dataclass
class DaemonConfig:
    phone_id: str
    sip_extension: str
    mqtt_host: str
    pins: PinConfig
    mqtt_port: int = 1883
    baresip_ctrl_host: str = "127.0.0.1"
    baresip_ctrl_port: int = 4444
    dial_digit_count: int = 3
    hook_debounce_seconds: float = 0.05
    pulse_debounce_seconds: float = 0.008
    inter_digit_timeout_seconds: float = 0.3

    @classmethod
    def from_file(cls, path: str) -> "DaemonConfig":
        with open(path, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        pins = PinConfig(**raw.pop("pins"))
        return cls(pins=pins, **raw)
