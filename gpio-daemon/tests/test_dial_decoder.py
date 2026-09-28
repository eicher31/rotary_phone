from gpio_daemon.dial_decoder import DialDecoder, TimeoutDialDecoder


def _dial_digit(decoder: DialDecoder, pulse_count: int) -> None:
    decoder.off_normal_changed(active=True)
    for _ in range(pulse_count):
        decoder.pulse_changed(active=True)
        decoder.pulse_changed(active=False)
    decoder.off_normal_changed(active=False)


def test_counts_pulses_into_digit():
    digits = []
    decoder = DialDecoder(on_digit=digits.append)

    _dial_digit(decoder, 5)

    assert digits == [5]


def test_ten_pulses_is_zero():
    digits = []
    decoder = DialDecoder(on_digit=digits.append)

    _dial_digit(decoder, 10)

    assert digits == [0]


def test_multiple_digits_in_sequence():
    digits = []
    decoder = DialDecoder(on_digit=digits.append)

    for count in (1, 9, 5, 8):
        _dial_digit(decoder, count)

    assert digits == [1, 9, 5, 8]


def test_ignores_spurious_off_normal_with_no_pulses():
    digits = []
    decoder = DialDecoder(on_digit=digits.append)

    decoder.off_normal_changed(active=True)
    decoder.off_normal_changed(active=False)

    assert digits == []


def test_pulses_outside_dialing_window_are_ignored():
    digits = []
    decoder = DialDecoder(on_digit=digits.append)

    # a pulse contact glitch while the dial is at rest must not count
    decoder.pulse_changed(active=True)
    decoder.pulse_changed(active=False)
    _dial_digit(decoder, 3)

    assert digits == [3]


def test_timeout_decoder_groups_pulses_by_silence():
    digits = []
    decoder = TimeoutDialDecoder(on_digit=digits.append, inter_digit_timeout=0.3)

    t = 0.0
    for _ in range(7):
        decoder.pulse_changed(active=True, timestamp=t)
        t += 0.1
    decoder.tick(t + 0.3)

    assert digits == [7]


def test_timeout_decoder_ten_pulses_is_zero():
    digits = []
    decoder = TimeoutDialDecoder(on_digit=digits.append, inter_digit_timeout=0.3)

    t = 0.0
    for _ in range(10):
        decoder.pulse_changed(active=True, timestamp=t)
        t += 0.1
    decoder.tick(t + 0.3)

    assert digits == [0]


def test_timeout_decoder_does_not_fire_before_timeout_elapses():
    digits = []
    decoder = TimeoutDialDecoder(on_digit=digits.append, inter_digit_timeout=0.3)

    decoder.pulse_changed(active=True, timestamp=0.0)
    decoder.tick(0.1)

    assert digits == []
