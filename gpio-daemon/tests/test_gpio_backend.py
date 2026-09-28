from gpio_daemon.gpio_backend import FakeBackend, active_from_level


def test_active_from_level_active_low():
    assert active_from_level(0, active_low=True) is True
    assert active_from_level(1, active_low=True) is False


def test_active_from_level_active_high():
    assert active_from_level(1, active_low=False) is True
    assert active_from_level(0, active_low=False) is False


def test_fake_backend_roundtrips_edges_and_output_writes():
    backend = FakeBackend()
    received = []
    backend.watch_input(17, pull_up=True, callback=lambda pin, value, ts: received.append((pin, value, ts)))

    backend.emit(17, 0, 1.0)
    backend.emit(17, 1, 1.5)

    assert received == [(17, 0, 1.0), (17, 1, 1.5)]

    backend.setup_output(23, initial=0)
    backend.write(23, 1)
    backend.write(23, 0)

    assert backend.output_log == [(23, 1), (23, 0)]
    assert backend.read(23) == 0
