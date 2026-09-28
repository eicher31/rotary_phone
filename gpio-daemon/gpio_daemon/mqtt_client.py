"""Thin wrapper around paho-mqtt for the daemon's needs: connect, publish
JSON, subscribe with a per-topic callback."""
from __future__ import annotations

import json
from typing import Any, Callable, Dict, Union

import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, host: str, port: int, client_id: str) -> None:
        self._client = mqtt.Client(client_id=client_id)
        self._host = host
        self._port = port

    def connect(self) -> None:
        self._client.connect(self._host, self._port)
        self._client.loop_start()

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def publish(self, topic: str, payload: Union[Dict[str, Any], str], retain: bool = False) -> None:
        body = payload if isinstance(payload, str) else json.dumps(payload)
        self._client.publish(topic, body, retain=retain)

    def subscribe(self, topic: str, on_message: Callable[[str, bytes], None]) -> None:
        def _handler(_client: Any, _userdata: Any, msg: Any) -> None:
            on_message(msg.topic, msg.payload)

        self._client.subscribe(topic)
        self._client.on_message = _handler
