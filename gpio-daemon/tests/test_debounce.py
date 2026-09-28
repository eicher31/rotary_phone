from gpio_daemon.debounce import Debouncer


def test_filters_short_bounce_and_fires_on_tick():
    changes = []
    d = Debouncer(stable_seconds=0.01, on_change=lambda v, t: changes.append((v, t)))

    d.feed(1, 0.000)
    d.feed(0, 0.001)  # bounce
    d.feed(1, 0.002)  # bounce, settles here
    d.tick(0.003)  # not yet stable
    assert changes == []
    d.tick(0.020)  # long enough after the last edge

    assert changes == [(1, 0.020)]


def test_requires_stability_before_firing():
    changes = []
    d = Debouncer(stable_seconds=0.01, on_change=lambda v, t: changes.append((v, t)))

    d.feed(1, 0.0)
    d.tick(0.005)  # not yet stable
    assert changes == []
    d.tick(0.011)
    assert changes == [(1, 0.011)]


def test_returning_to_stable_value_before_confirmation_cancels_pending():
    changes = []
    d = Debouncer(stable_seconds=0.01, on_change=lambda v, t: changes.append((v, t)))

    d.feed(1, 0.0)
    d.tick(0.011)
    assert changes == [(1, 0.011)]

    # brief glitch back to 0, then back to the already-stable 1: no new event
    d.feed(0, 0.020)
    d.feed(1, 0.021)
    d.tick(0.040)
    assert changes == [(1, 0.011)]
