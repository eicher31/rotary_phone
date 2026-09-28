"""Minimal client for baresip's `ctrl_tcp` module.

baresip's ctrl_tcp module accepts the same commands available in
baresip's interactive console as plain text lines (e.g. `/dial 100`,
`/hangup`, `/answer`), and emits status/events back on the same socket.

The exact event schema (field names, event types) depends on the baresip
version and build — this has NOT been verified against real hardware in
this repository (see docs/README.md — "État du projet"). Before relying
on `call_state` events for game logic, connect to the real `ctrl_tcp`
port (`nc 127.0.0.1 4444` or similar) on your actual deployment and check
what it actually sends; adjust `_handle_line` if needed.

To stay useful even if the schema differs from what's expected, unparsable
lines are passed through as a `{"type": "RAW", "line": ...}` event rather
than dropped or raising.
"""
from __future__ import annotations

import json
import socket
import threading
from typing import Callable, Optional


class BaresipClient:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._sock: Optional[socket.socket] = None
        self._on_event: Optional[Callable[[dict], None]] = None
        self._reader_thread: Optional[threading.Thread] = None

    def connect(self) -> None:
        self._sock = socket.create_connection((self._host, self._port))
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._reader_thread.start()

    def on_event(self, callback: Callable[[dict], None]) -> None:
        self._on_event = callback

    def dial(self, number: str) -> None:
        self._send(f"/dial {number}")

    def answer(self) -> None:
        self._send("/answer")

    def hangup(self) -> None:
        self._send("/hangup")

    def _send(self, command: str) -> None:
        if self._sock is None:
            raise RuntimeError("BaresipClient.connect() must be called first")
        self._sock.sendall((command + "\n").encode("utf-8"))

    def _read_loop(self) -> None:
        assert self._sock is not None
        buffer = b""
        while True:
            chunk = self._sock.recv(4096)
            if not chunk:
                return
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                self._handle_line(line)

    def _handle_line(self, line: bytes) -> None:
        if not line.strip() or self._on_event is None:
            return
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            event = {"type": "RAW", "line": line.decode("utf-8", errors="replace")}
        self._on_event(event)
