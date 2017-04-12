import pytest


def test_connector_type(default_gen_sine):
    assert default_gen_sine.connector_type in default_gen_sine.CONNECTOR_TYPES


def test_is_differential(default_gen_sine):
    assert type(default_gen_sine.is_differential) is bool


def test_impedance(default_gen_sine):
    assert type(default_gen_sine.impedance) is float
    assert default_gen_sine.impedance > 0


def test_resolution(default_gen_sine):
    assert type(default_gen_sine.resolution) is int
    assert default_gen_sine.resolution > 0


def test_out_min(default_gen_sine):
    assert type(default_gen_sine.out_min) is float
    assert default_gen_sine.out_min < 0


def test_out_max(default_gen_sine):
    assert type(default_gen_sine.out_max) is float
    assert default_gen_sine.out_max > 0


def test_is_controllable(default_gen_sine):
    assert default_gen_sine.is_controllable is True


def test_status(default_gen_sine):
    assert default_gen_sine.status in default_gen_sine.GENERATOR_STATUSES


def test_is_out_on(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.is_out_on) is bool

    # Test setter
    for value in [True, False]:
        default_gen_sine.is_out_on = value
        assert default_gen_sine.is_out_on is value


def test_is_out_inv(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.is_out_inv) is bool

    # Test setter
    for value in [True, False]:
        default_gen_sine.is_out_inv = value
        assert default_gen_sine.is_out_inv is value


def test_start(default_gen_sine):
    assert default_gen_sine.start() is True


def test_stop(default_gen_sine):
    default_gen_sine.start()
    assert default_gen_sine.stop() is True


def test_signal_types_available(default_gen_sine):
    assert type(default_gen_sine.signal_types_available) is tuple
    for sig_type in default_gen_sine.signal_types_available:
        assert sig_type in default_gen_sine.SIGNAL_TYPES


def test_signal_type(default_gen_sine):
    # Test getter
    assert default_gen_sine.signal_type in default_gen_sine.SIGNAL_TYPES

    # Test setter
    for sig_type in default_gen_sine.signal_types_available:
        default_gen_sine.signal_type = sig_type
        assert default_gen_sine.signal_type == sig_type


def test_amplitude_min(default_gen_sine):
    assert type(default_gen_sine.amplitude_min) is float
    assert default_gen_sine.amplitude_min < default_gen_sine.amplitude_max


def test_amplitude_max(default_gen_sine):
    assert type(default_gen_sine.amplitude_max) is float
    assert default_gen_sine.amplitude_max > default_gen_sine.amplitude_min


def test_amplitude(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.amplitude) is float

    # Test setter
    for ampl in [default_gen_sine.amplitude_min,
                 (default_gen_sine.amplitude_max-default_gen_sine.amplitude_min)/2,
                 default_gen_sine.amplitude_max]:
        default_gen_sine.amplitude = ampl
        assert default_gen_sine.amplitude == ampl


def test_amplitude_ranges_available(default_gen_sine):
    assert type(default_gen_sine.amplitude_ranges_available) is tuple
    for ampl_range in default_gen_sine.amplitude_ranges_available:
        assert type(ampl_range) is float
        assert ampl_range > 0


def test_amplitude_range(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.amplitude_range) is float
    assert default_gen_sine.amplitude_range > 0

    # Test setter
    for ampl_range in default_gen_sine.amplitude_ranges_available:
        default_gen_sine.amplitude_range = ampl_range
        assert default_gen_sine.amplitude_range == ampl_range


def test_is_amplitude_autorange(default_gen_sine):
    assert type(default_gen_sine.is_amplitude_autorange) is bool

    for value in [False, True]:
        default_gen_sine.is_amplitude_autorange = value
        assert default_gen_sine.is_amplitude_autorange == value


def test_offset_min(default_gen_sine):
    assert type(default_gen_sine.offset_min) is float
    assert default_gen_sine.offset_min < 0


def test_offset_max(default_gen_sine):
    assert type(default_gen_sine.offset_max) is float
    assert default_gen_sine.offset_max > 0


def test_offset(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.offset) is float

    # Test setter
    # Selectable offset depends on the signal amplitude
    low_limit = default_gen_sine.offset_min + default_gen_sine.amplitude
    high_limit = default_gen_sine.offset_max - default_gen_sine.amplitude
    for value in [low_limit, (high_limit-low_limit)/2, high_limit]:
        default_gen_sine.offset = value
        assert default_gen_sine.offset == pytest.approx(value)


def test_freq_min(default_gen_sine):
    assert type(default_gen_sine.freq_min) is float
    assert default_gen_sine.freq_min > 0
    assert default_gen_sine.freq_min < default_gen_sine.freq_max


def test_freq_max(default_gen_sine):
    assert type(default_gen_sine.freq_max) is float
    assert default_gen_sine.freq_max > 0
    assert default_gen_sine.freq_max > default_gen_sine.freq_min


def test_freq(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.freq) is float
    assert default_gen_sine.freq >= default_gen_sine.freq_min
    assert default_gen_sine.freq <= default_gen_sine.freq_max

    # Test setter
    for freq in [default_gen_sine.freq_min,
                 (default_gen_sine.freq_max-default_gen_sine.freq_min)/2,
                 default_gen_sine.freq_max]:
        default_gen_sine.freq = freq
        assert default_gen_sine.freq == pytest.approx(freq)


def test_freq_modes_available(default_gen_sine):
    assert type(default_gen_sine.freq_modes_available) is tuple
    for freq_mode in default_gen_sine.freq_modes_available:
        assert freq_mode in default_gen_sine.FREQUENCY_MODES


def test_freq_mode(default_gen_sine):
    # Test getter
    assert default_gen_sine.freq_mode in default_gen_sine.FREQUENCY_MODES

    # Test setter
    print(default_gen_sine.freq_modes_available)
    for mode in default_gen_sine.freq_modes_available:
        default_gen_sine.freq_mode = mode
        assert default_gen_sine.freq_mode == mode


def test_phase_min(default_gen_sine):
    assert type(default_gen_sine.phase_min) is float
    assert default_gen_sine.phase_min >= 0
    assert default_gen_sine.phase_min <= 360


def test_phase_max(default_gen_sine):
    assert type(default_gen_sine.phase_max) is float
    assert default_gen_sine.phase_max >= 0
    assert default_gen_sine.phase_max <= 360


def test_phase(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.phase) is float
    assert default_gen_sine.phase >= default_gen_sine.phase_min
    assert default_gen_sine.phase <= default_gen_sine.phase_max

    # Test setter
    for phase in [default_gen_sine.phase_min,
                  (default_gen_sine.phase_max-default_gen_sine.phase_min)/2,
                  default_gen_sine.phase_max]:
        default_gen_sine.phase = phase
        assert default_gen_sine.phase == phase


def test_symmetry_min(default_gen_sine):
    assert type(default_gen_sine.symmetry_min) is float
    assert default_gen_sine.symmetry_min >= 0
    assert default_gen_sine.symmetry_min <= 1


def test_symmetry_max(default_gen_sine):
    assert type(default_gen_sine.symmetry_max) is float
    assert default_gen_sine.symmetry_max >= 0
    assert default_gen_sine.symmetry_min <= 1
    assert default_gen_sine.symmetry_max > default_gen_sine.symmetry_min


def test_symmetry(default_gen_sine):
    # Test getter
    assert type(default_gen_sine.symmetry) is float
    assert default_gen_sine.symmetry >= 0
    assert default_gen_sine.symmetry <= 1

    # Test setter
    values = [0.0, 0.25, 0.5, 0.75, 1.0]
    for value in values:
        default_gen_sine.symmetry = value
        assert default_gen_sine.symmetry == value


def test_pulse_width_min(default_gen_pulse):
    assert type(default_gen_pulse.pulse_width_min) is float
    assert default_gen_pulse.pulse_width_min >= 0


def test_pulse_width_max(default_gen_pulse):
    assert type(default_gen_pulse.pulse_width_max) is float
    assert default_gen_pulse.pulse_width_max >= 0
    assert default_gen_pulse.pulse_width_max >= default_gen_pulse.pulse_width_min


def test_pulse_width(default_gen_pulse):
    # Test getter
    assert type(default_gen_pulse.pulse_width) is float
    assert default_gen_pulse.pulse_width >= 0
    assert default_gen_pulse.pulse_width >= default_gen_pulse.pulse_width_min
    assert default_gen_pulse.pulse_width <= default_gen_pulse.pulse_width_max

    # Test setter
    values = [default_gen_pulse.pulse_width_min,
              (default_gen_pulse.pulse_width_max-default_gen_pulse.pulse_width_min)/2,
              default_gen_pulse.pulse_width_max]
    for value in values:
        default_gen_pulse.pulse_width = value
        assert default_gen_pulse.pulse_width == value


def test_arb_data_length_min(default_gen_arb):
    assert type(default_gen_arb.arb_data_length_min) is int
    assert default_gen_arb.arb_data_length_min > 0


def test_arb_data_length_max(default_gen_arb):
    assert type(default_gen_arb.arb_data_length_max) is int
    assert default_gen_arb.arb_data_length_max > default_gen_arb.arb_data_length_min


def test_arb_data_length(default_gen_arb):
    assert type(default_gen_arb.arb_data_length) is int
    assert default_gen_arb.arb_data_length >= default_gen_arb.arb_data_length_min
    assert default_gen_arb.arb_data_length <= default_gen_arb.arb_data_length_max


def test_arb_data(default_gen_arb):
    # Test with empty list
    default_gen_arb.arb_data([])
    assert default_gen_arb.arb_data_length == 1

    # Test with data
    default_gen_arb.arb_data([0.0, 1.0, 2.0, 3.0, 4.0])
    assert default_gen_arb.arb_data_length == 5


def test_modes_native_available(default_gen_sine):
    assert type(default_gen_sine.modes_native_available) is tuple
    for mode in default_gen_sine.modes_native_available:
        assert mode in default_gen_sine.GENERATOR_MODES


def test_modes_available(default_gen_sine):
    assert type(default_gen_sine.modes_available) is tuple
    for mode in default_gen_sine.modes_available:
        assert mode in default_gen_sine.GENERATOR_MODES


def test_mode(default_gen_sine):
    # Test getter
    assert default_gen_sine.mode in default_gen_sine.GENERATOR_MODES

    # Test setter
    for mode in default_gen_sine.modes_available:
        default_gen_sine.mode = mode
        assert default_gen_sine.mode == mode


def test_is_burst_active(default_gen_burst):
    assert type(default_gen_burst.is_burst_active) is bool
    # Maybe test after starting burst?


def test_burst_cnt_min(default_gen_burst):
    assert type(default_gen_burst.burst_cnt_min) is int
    assert default_gen_burst.burst_cnt_min >= 0


def test_burst_cnt_max(default_gen_burst):
    assert type(default_gen_burst.burst_cnt_max) is int
    assert default_gen_burst.burst_cnt_max > default_gen_burst.burst_cnt_min


def test_burst_cnt(default_gen_burst):
    # Test getter
    assert type(default_gen_burst.burst_cnt) is int
    assert default_gen_burst.burst_cnt >= default_gen_burst.burst_cnt_min
    assert default_gen_burst.burst_cnt <= default_gen_burst.burst_cnt_max

    # Test setter
    for value in [default_gen_burst.burst_cnt_min,
                  round((default_gen_burst.burst_cnt_max - default_gen_burst.burst_cnt_min)/2),
                  default_gen_burst.burst_cnt_max]:
        default_gen_burst.burst_cnt = value
        assert default_gen_burst.burst_cnt == value


def test_burst_sample_cnt_min(default_gen_burst_sample):
    assert type(default_gen_burst_sample.burst_sample_cnt_min) is int
    assert default_gen_burst_sample.burst_sample_cnt_min >= 0


def test_burst_sample_cnt_max(default_gen_burst_sample):
    assert type(default_gen_burst_sample.burst_sample_cnt_max) is int
    assert default_gen_burst_sample.burst_sample_cnt_max > default_gen_burst_sample.burst_sample_cnt_min


def test_burst_sample_cnt(default_gen_burst_sample):
    # Test getter
    assert type(default_gen_burst_sample.burst_sample_cnt) is int
    assert default_gen_burst_sample.burst_sample_cnt >= default_gen_burst_sample.burst_sample_cnt_min
    assert default_gen_burst_sample.burst_sample_cnt <= default_gen_burst_sample.burst_sample_cnt_max

    # Test setter
    for value in [default_gen_burst_sample.burst_sample_cnt_min,
                  round((default_gen_burst_sample.burst_sample_cnt_max -
                         default_gen_burst_sample.burst_sample_cnt_min) / 2),
                  default_gen_burst_sample.burst_sample_cnt_max]:
        default_gen_burst_sample.burst_sample_cnt = value
        assert default_gen_burst_sample.burst_sample_cnt == value


def test_burst_segment_cnt_min(default_gen_burst_segment):
    assert type(default_gen_burst_segment.burst_segment_cnt_min) is int
    assert default_gen_burst_segment.burst_segment_cnt_min >= 0


def test_burst_segment_cnt_max(default_gen_burst_segment):
    assert type(default_gen_burst_segment.burst_segment_cnt_max) is int
    assert default_gen_burst_segment.burst_segment_cnt_max > default_gen_burst_segment.burst_segment_cnt_min


def test_burst_segment_cnt(default_gen_burst_segment):
    # Test getter
    assert type(default_gen_burst_segment.burst_segment_cnt) is int
    # Note: burst_segment_cnt can be read as 0, even if burst_segment_cnt_min is 1
    assert default_gen_burst_segment.burst_segment_cnt >= 0
    assert default_gen_burst_segment.burst_segment_cnt <= default_gen_burst_segment.burst_segment_cnt_max

    # Test setter
    for value in [default_gen_burst_segment.burst_segment_cnt_min,
                  round((default_gen_burst_segment.burst_segment_cnt_max -
                         default_gen_burst_segment.burst_segment_cnt_min) / 2),
                  default_gen_burst_segment.burst_segment_cnt_max]:
        print(value)
        default_gen_burst_segment.burst_segment_cnt = value
        assert default_gen_burst_segment.burst_segment_cnt == value
