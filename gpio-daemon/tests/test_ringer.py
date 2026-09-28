from gpio_daemon.ringer import Ringer, RingCadence


def test_ringer_toggles_output_according_to_cadence():
    writes = []
    cadence = RingCadence(steps=[(0.1, True), (0.1, False)])
    ringer = Ringer(write_pin=writes.append, cadence=cadence)

    ringer.start(timestamp=0.0)
    ringer.tick(0.05)
    ringer.tick(0.15)

    assert writes == [1, 0]


def test_cadence_repeats():
    writes = []
    cadence = RingCadence(steps=[(0.1, True), (0.1, False)])
    ringer = Ringer(write_pin=writes.append, cadence=cadence)

    ringer.start(timestamp=0.0)
    ringer.tick(0.25)  # 0.25 % 0.2 = 0.05 -> back in the "active" step of the 2nd cycle

    assert writes == [1]


def test_stop_forces_output_low_and_silences_further_ticks():
    writes = []
    ringer = Ringer(write_pin=writes.append)

    ringer.start(timestamp=0.0)
    ringer.tick(0.05)
    ringer.stop()
    assert writes[-1] == 0

    writes.clear()
    ringer.tick(0.1)
    assert writes == []


def test_no_output_before_start():
    writes = []
    ringer = Ringer(write_pin=writes.append)

    ringer.tick(1.0)

    assert writes == []
