from tiepie.oscilloscopeChannel import OscilloscopeChannel
import pytest
import time


def test_channel_cnt(osc):
    assert type(osc.channel_cnt) is int
    assert osc.channel_cnt > 0


def test_channels(osc):
    assert type(osc.channels) is tuple
    assert len(osc.channels) is osc.channel_cnt
    for channel in osc.channels:
        assert type(channel) is OscilloscopeChannel


def test__get_sample_cnts(osc):
    assert len(osc._get_sample_cnts()) == 2
    for element in osc._get_sample_cnts():
        assert type(element) is int
        assert element >= 0


def test_retrieve(osc):
    # Deactivate every channel
    for channel in osc.channels:
        channel.is_enabled = False
    with pytest.raises(ValueError):
        osc.retrieve()

    # Incrementally activate channels and call retrieve
    for idx, channel in enumerate(osc.channels):
        channel.is_enabled = True

        osc.start()
        while not osc.is_data_ready:
            time.sleep(0.05)
        data = osc.retrieve()

        assert type(data) is list
        assert len(data) == idx + 1
        for channel_data in data:
            assert type(channel_data) is list
            for sample in channel_data:
                assert type(sample) is float

    # Deactivate all except the last channel
    for channel in osc.channels[0:-1]:
        channel.is_enabled = False
    osc.channels[-1].is_enabled = True

    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve()

    assert type(data) is list
    assert len(data) == osc.channel_cnt
    # Only the last channel should contain actual samples
    for channel_data in data[0:-1]:
        assert channel_data is None
    assert type(data[-1]) is list
    for sample in data[-1]:
        assert type(sample) is float

    # Test parameter channel_nos: Get deactivated channel -> should raise a ValueError
    osc.channels[0].is_enabled = False
    osc.channels[1].is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    with pytest.raises(ValueError):
        osc.retrieve(channel_nos=[1])

    # Test parameter channel_nos: Get activated channel -> should work
    osc.channels[0].is_enabled = False
    osc.channels[1].is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve(channel_nos=[2])
    assert type(data) is list
    assert len(data) is 2
    assert data[0] is None
    assert type(data[1]) is list
    for sample in data[1]:
        assert type(sample) is float


def test_retrieve_ch1(osc):
    # Enable available channels
    for channel in osc.channels:
        channel.is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve_ch1()
    assert type(data) is list
    assert len(data) == 1
    for idx, channel_data in enumerate(data):
        # Check, if channel is valid
        if idx < osc.channel_cnt:
            # Valid channel -> there must be valid data
            assert type(channel_data) is list
            for sample in channel_data:
                assert type(sample) is float
        else:
            # Invalid channel -> None
            assert channel_data is None

    # Check for multiple channels
    if osc.channel_cnt >= 2:
        # There is more than one channel -> we can disable the first without getting an error
        osc.channels[0].is_enabled = False
        osc.start()
        while not osc.is_data_ready:
            time.sleep(0.05)
        data = osc.retrieve_ch1()
        assert data == [None]


def test_retrieve_ch1_to_ch2(osc):
    # --- Try to retrieve all channels
    # Enable all available channels
    for channel in osc.channels:
        channel.is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve_ch1_to_ch2()
    assert type(data) is list
    assert len(data) == 2
    for idx, channel_data in enumerate(data):
        # Check, if channel is valid
        if idx < osc.channel_cnt:
            # Valid channel -> there must be valid data
            assert type(channel_data) is list
            for sample in channel_data:
                assert type(sample) is float
        else:
            # Invalid channel -> None
            assert channel_data is None

    # --- Try to retrieve all except the first channel
    # Check for multiple channels
    if osc.channel_cnt >= 2:
        # There is more than one channel -> we can disable the first without getting an error
        osc.channels[0].is_enabled = False
        osc.start()
        while not osc.is_data_ready:
            time.sleep(0.05)
        data = osc.retrieve_ch1_to_ch2()
        assert type(data) is list
        assert len(data) == 2
        # First channel was disabled
        assert data[0] is None
        # Second channel should contain data
        assert type(data[1]) is list
        for sample in data[1]:
            assert type(sample) is float


def test_retrieve_ch1_to_ch3(osc):
    # --- Try to retrieve all channels
    # Enable available channels
    for channel in osc.channels:
        channel.is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve_ch1_to_ch3()
    assert type(data) is list
    assert len(data) == 3
    for idx, channel_data in enumerate(data):
        # Check, if channel is valid
        if idx < osc.channel_cnt:
            # Valid channel -> there must be valid data
            assert type(channel_data) is list
            for sample in channel_data:
                assert type(sample) is float
        else:
            # Invalid channel -> None
            assert channel_data is None

    # --- Try to retrieve all except the first channel
    # Check for multiple channels
    if osc.channel_cnt >= 2:
        # There is more than one channel -> we can disable the first without getting an error
        osc.channels[0].is_enabled = False
        osc.start()
        while not osc.is_data_ready:
            time.sleep(0.05)
        data = osc.retrieve_ch1_to_ch3()

        assert type(data) is list
        assert len(data) == 3
        # First channel was disabled
        assert data[0] is None
        # Other channels should contain data, if they are valid ones
        for idx, channel_data in enumerate(data[1:]):
            # Check, if channel is valid
            if idx+1 < osc.channel_cnt:
                # Valid channel -> there must be valid data
                assert type(channel_data) is list
                for sample in channel_data:
                    assert type(sample) is float
            else:
                # Invalid channel -> None
                assert channel_data is None


def test_retrieve_ch1_to_ch4(osc):
    # --- Try to retrieve all channels
    # Enable available channels
    for channel in osc.channels:
        channel.is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve_ch1_to_ch4()
    assert type(data) is list
    assert len(data) == 4
    for idx, channel_data in enumerate(data):
        # Check, if channel is valid
        if idx < osc.channel_cnt:
            # Valid channel -> there must be valid data
            assert type(channel_data) is list
            for sample in channel_data:
                assert type(sample) is float
        else:
            # Invalid channel -> None
            assert channel_data is None

    # --- Try to retrieve all except the first channel
    # Check for multiple channels
    if osc.channel_cnt >= 2:
        # There is more than one channel -> we can disable the first without getting an error
        osc.channels[0].is_enabled = False
        osc.start()
        while not osc.is_data_ready:
            time.sleep(0.05)
        data = osc.retrieve_ch1_to_ch4()

        assert type(data) is list
        assert len(data) == 4
        # First channel was disabled
        assert data[0] is None
        # Other channels should contain data, if they are valid ones
        for idx, channel_data in enumerate(data[1:]):
            # Check, if channel is valid
            if idx+1 < osc.channel_cnt:
                # Valid channel -> there must be valid data
                assert type(channel_data) is list
                for sample in channel_data:
                    assert type(sample) is float
            else:
                # Invalid channel -> None
                assert channel_data is None


def test_valid_pre_sample_cnt(osc):
    assert type(osc.valid_pre_sample_cnt) is int
    assert osc.valid_pre_sample_cnt >= 0


def test_start(default_osc):
    # Starting a measurement should work without problems and return True
    assert default_osc.start() is True


def test_stop(default_osc):
    # Stopping a measurement right after start should return True
    default_osc.start()
    assert default_osc.stop() is True


def test_force_trig(default_osc):
    # Disable triggers
    for channel in default_osc.channels:
        channel.trig_is_enabled = False
    default_osc.trig_timeout = -1

    assert default_osc.is_force_trig is False

    # Start measurement and force trigger
    default_osc.start()
    default_osc.force_trig()

    while not default_osc.is_data_ready:
        time.sleep(0.01)
    assert default_osc.is_force_trig is True


def test_measure_modes_available(default_osc):
    assert type(default_osc.measure_modes_available) is tuple
    for mode in default_osc.measure_modes_available:
        assert mode in default_osc.MEASURE_MODES


def test_measure_mode(default_osc):
    # Test getter
    assert default_osc.measure_mode in default_osc.MEASURE_MODES

    # Test setter
    for mode in default_osc.measure_modes_available:
        default_osc.measure_mode = mode
        assert default_osc.measure_mode == mode


def test_is_running(default_osc):
    assert default_osc.is_running is False
    default_osc.start()
    assert default_osc.is_running is True


def test_is_triggered(default_osc):
    assert default_osc.is_triggered is False

    # Start measurement and force trigger
    default_osc.start()
    default_osc.force_trig()

    while not default_osc.is_data_ready:
        time.sleep(0.01)
    assert default_osc.is_triggered is True


def test_is_timeout_trig(default_osc):
    assert default_osc.is_timeout_trig is False
    default_osc.trig_timeout = 1e-6

    default_osc.start()

    while not default_osc.is_data_ready:
        time.sleep(0.01)
    assert default_osc.is_timeout_trig is True


def test_is_force_trig(default_osc):
    # Disable triggers
    for channel in default_osc.channels:
        channel.trig_is_enabled = False
    default_osc.trig_timeout = -1

    assert default_osc.is_force_trig is False

    # Start measurement and force trigger
    default_osc.start()
    default_osc.force_trig()

    while not default_osc.is_data_ready:
        time.sleep(0.01)
    assert default_osc.is_force_trig is True


def test_is_data_ready(default_osc):
    assert type(default_osc.is_data_ready) is bool

    default_osc.start()
    default_osc.force_trig()
    time.sleep(0.5)
    assert default_osc.is_data_ready is True


def test_is_data_overflow(default_osc):
    assert type(default_osc.is_data_overflow) is bool

    # Overflow can only occur in streaming mode
    default_osc.measure_mode = "stream"

    default_osc.start()

    # There should be no overflow in the beginning
    assert default_osc.is_data_overflow is False
    # No readout of data -> buffer should run full after some time
    time.sleep(1)
    assert default_osc.is_data_overflow is True


def test_resolutions_available(default_osc):
    assert type(default_osc.resolutions_available) is tuple
    for resolution in default_osc.resolutions_available:
        assert type(resolution) is int
        assert resolution > 0


def test_resolution(default_osc):
    # Test getter
    assert type(default_osc.resolution) is int
    assert default_osc.resolution > 0
    assert default_osc.resolution in default_osc.resolutions_available

    # Test setter
    for res in default_osc.resolutions_available:
        default_osc.resolution = res
        assert default_osc.resolution == res


def test_is_resolution_enhanced(default_osc):
    # Test for every available resolution
    for res in default_osc.resolutions_available:
        default_osc.resolution = res
        assert type(default_osc.is_resolution_enhanced) is bool


def test_auto_resolutions_available(default_osc):
    for res in default_osc.auto_resolutions_available:
        assert res in default_osc.AUTO_RESOLUTIONS


def test_auto_resolution(default_osc):
    # Test getter
    assert default_osc.auto_resolution in default_osc.AUTO_RESOLUTIONS

    # Test setter
    for res in default_osc.auto_resolutions_available:
        default_osc.auto_resolution = res
        assert default_osc.auto_resolution == res


def test_clock_sources_available(default_osc):
    for clk_src in default_osc.clock_sources_available:
        assert clk_src in default_osc.CLOCK_SOURCES


def test_clock_source(default_osc):
    # Test getter
    assert default_osc.clock_source in default_osc.CLOCK_SOURCES

    # Test setter
    for clk_src in default_osc.clock_sources_available:
        default_osc.clock_source = clk_src
        assert default_osc.clock_source == clk_src


def test_clock_outputs_available(default_osc):
    for clk_out in default_osc.clock_outputs_available:
        assert clk_out in default_osc.CLOCK_OUTPUTS


def test_clock_output(default_osc):
    # Test getter
    assert default_osc.clock_output in default_osc.CLOCK_OUTPUTS

    # Test setter
    for clk_out in default_osc.clock_outputs_available:
        default_osc.clock_output = clk_out
        assert default_osc.clock_output == clk_out


def test_sample_freq_max(default_osc):
    assert type(default_osc.sample_freq_max) is float
    assert default_osc.sample_freq_max > 0


def test_sample_freq(default_osc):
    # Test getter
    assert type(default_osc.sample_freq) is float
    assert default_osc.sample_freq > 0
    assert default_osc.sample_freq <= default_osc.sample_freq_max

    # Test setter
    freqs = [10e3, 100e3, default_osc.sample_freq_max]
    for freq in freqs:
        default_osc.sample_freq = freq
        assert default_osc.sample_freq == freq


def test_verify_sample_freq(default_osc):
    # Test type
    assert type(default_osc.verify_sample_freq(
        default_osc.sample_freq_max / 2)) is float
    # Test verify
    assert default_osc.verify_sample_freq(
        default_osc.sample_freq_max / 2) == default_osc.sample_freq_max / 2
    # Test if the frequency clips
    assert default_osc.verify_sample_freq(
        default_osc.sample_freq_max + 1.0) == default_osc.sample_freq_max


def test_record_length_max(default_osc):
    assert type(default_osc.record_length_max) is int
    assert default_osc.record_length_max > 0


def test_record_length(default_osc):
    # Test getter
    assert type(default_osc.record_length) is int
    assert default_osc.record_length > 0
    assert default_osc.record_length <= default_osc.record_length_max

    # Test setter
    lengths = [1000, 10000, default_osc.record_length_max]
    for length in lengths:
        default_osc.record_length = length
        assert default_osc.record_length == length


def test_verify_record_length(default_osc):
    # Test type
    assert type(default_osc.verify_record_length(
        default_osc.record_length_max // 2)) is int
    # Test verify
    assert default_osc.verify_record_length(
        default_osc.record_length_max // 2) == default_osc.record_length_max // 2


def test_pre_sample_ratio(default_osc):
    # Test getter
    assert type(default_osc.pre_sample_ratio) is float
    assert default_osc.pre_sample_ratio >= 0
    assert default_osc.pre_sample_ratio <= 1

    # Test setter
    ratios = [0.0, 0.25, 0.5, 0.75, 1.0]
    for ratio in ratios:
        default_osc.pre_sample_ratio = ratio
        assert default_osc.pre_sample_ratio == ratio


def test_segment_cnt_max(default_osc):
    assert type(default_osc.segment_cnt_max) is int
    assert default_osc.segment_cnt_max >= 0


def test_segment_cnt(default_osc):
    # Test getter
    assert type(default_osc.segment_cnt) is int
    assert default_osc.segment_cnt > 0

    # Test setter
    cnts = [1, 2, default_osc.segment_cnt_max]
    for cnt in cnts:
        default_osc.segment_cnt = cnt
        assert default_osc.segment_cnt == cnt


def test_verify_segment_cnt(default_osc):
    # Test type
    assert type(default_osc.verify_segment_cnt(
        default_osc.segment_cnt_max // 2)) is int
    # Test verify
    assert default_osc.verify_segment_cnt(
        default_osc.segment_cnt_max // 2) == default_osc.segment_cnt_max // 2
    # Test if the segment cnt clips
    assert default_osc.verify_segment_cnt(
        default_osc.segment_cnt_max + 1) == default_osc.segment_cnt_max


def test_trig_timeout(default_osc):
    # Test getter
    assert type(default_osc.trig_timeout) is float
    assert (default_osc.trig_timeout >= 0) | (default_osc.trig_timeout == -1)

    # Test setter
    timeouts = [-1, 0, 1e-3, 0.5, 1]
    for timeout in timeouts:
        default_osc.trig_timeout = timeout
        assert default_osc.trig_timeout == timeout


def test_verify_trig_timeout(default_osc):
    # Test type
    assert type(default_osc.verify_trig_timeout(1.0)) is float
    # Test verify
    assert default_osc.verify_trig_timeout(1.0) == 1.0


def test_is_trig_delay_available(default_osc):
    assert type(default_osc.is_trig_delay_available) is bool
    assert default_osc.is_trig_delay_available is True


def test_trig_delay_max(default_osc):
    assert type(default_osc.trig_delay_max) is float
    assert default_osc.trig_delay_max >= 0


def test_trig_delay(default_osc):
    # Test getter
    assert type(default_osc.trig_delay) is float
    assert default_osc.trig_delay >= 0

    # Test setter
    delays = [0, 1e-3, default_osc.trig_delay_max]
    for delay in delays:
        default_osc.trig_delay = delay
        assert default_osc.trig_delay == delay


def test_verify_trig_delay(default_osc):
    # Test type
    assert type(default_osc.verify_trig_delay(
        default_osc.trig_delay_max / 2)) is float
    # Test verify
    assert default_osc.verify_trig_delay(
        default_osc.trig_delay_max / 2) == default_osc.trig_delay_max / 2
    # Test if the segment cnt clips
    assert default_osc.verify_trig_delay(
        default_osc.trig_delay_max + 1.0) == default_osc.trig_delay_max


def test_is_trig_holdoff_available(default_osc):
    assert type(default_osc.is_trig_holdoff_available) is bool


def test_trig_holdoff_max(default_osc):
    assert type(default_osc.trig_holdoff_max) is int
    assert default_osc.trig_holdoff_max >= 0


def test_trig_holdoff(default_osc):
    # Test getter
    assert type(default_osc.trig_holdoff) is int
    assert default_osc.trig_holdoff >= 0

    # Test setter
    holdoffs = [0, 1, 100, default_osc.trig_holdoff_max, default_osc.TRIG_HOLDOFF_ALL_PRE_SAMPLES]
    for holdoff in holdoffs:
        default_osc.trig_holdoff = holdoff
        assert default_osc.trig_holdoff == holdoff


def test_is_trig_available(default_osc):
    assert type(default_osc.is_trig_available) is bool


def test_is_connection_test_available(default_osc):
    assert type(default_osc.is_connection_test_available) is bool


def test_start_connection_test(default_osc):
    if default_osc.is_connection_test_available:
        assert default_osc.start_connection_test() is True
        # Wait until connection test is completed before returning (there is no known way to stop the test)
        while not default_osc.is_connection_test_completed:
            time.sleep(0.01)
    else:
        with pytest.raises(OSError) as err:
            default_osc.start_connection_test()
            assert err.value.args[0] == "[-2]: NOT_SUPPORTED"


def test_is_connection_test_completed(default_osc):
    if default_osc.is_connection_test_available:
        assert type(default_osc.is_connection_test_completed) is bool
    else:
        with pytest.raises(OSError) as err:
            default_osc.is_connection_test_completed
            assert err.value.args[0] == "[-2]: NOT_SUPPORTED"


def test_connection_test_data(default_osc):
    if default_osc.is_connection_test_available:
        # Start the test
        default_osc.start_connection_test()
        # Wait, until it's finished
        while not default_osc.is_connection_test_completed:
            time.sleep(0.01)

        # Get the results
        results = default_osc.connection_test_data
        assert type(results) is tuple
        for idx, result in enumerate(results):
            if result == "undefined":
                assert default_osc.channels[idx].is_enabled is False
            else:
                assert default_osc.channels[idx].is_enabled is True
    else:
        with pytest.raises(OSError) as err:
            default_osc.connection_test_data
            assert err.value.args[0] == "[-2]: NOT_SUPPORTED"


def test_test_connection(default_osc):
    results = default_osc.test_connection()

    if default_osc.is_connection_test_available:
        assert type(results) is tuple
        for idx, result in enumerate(results):
            if result == "undefined":
                assert default_osc.channels[idx].is_enabled is False
            else:
                assert default_osc.channels[idx].is_enabled is True
    else:
        assert results is None


def test_measure(default_osc):
    data = default_osc.measure()
    assert type(data) is list
    # default_osc has only one enabled channel
    assert len(data) == 1
    assert type(data[0]) is list
    for sample in data[0]:
        assert type(sample) is float

    # Check for multiple channels
    if default_osc.channel_cnt >= 2:
        # There is more than one channel -> disable first, enable second
        default_osc.channels[0].is_enabled = False
        default_osc.channels[1].is_enabled = True

        data = default_osc.measure()

        assert type(data) is list
        assert len(data) == 2
        # First channel was disabled
        assert data[0] is None
        # Second channel should contain data
        assert type(data[1]) is list
        for sample in data[1]:
            assert type(sample) is float


def test_time_vector(default_osc):
    default_osc.pre_sample_ratio = 0
    assert len(default_osc.time_vector) == default_osc.record_length
    assert default_osc.time_vector[0] == 0
    assert default_osc.time_vector[1] == pytest.approx(1/default_osc.sample_freq)
    assert default_osc.time_vector[-1] == 1/default_osc.sample_freq*(default_osc.record_length-1)

    default_osc.pre_sample_ratio = 0.5
    # With correctly configured pre samples, it should work
    default_osc.trig_holdoff = default_osc.TRIG_HOLDOFF_ALL_PRE_SAMPLES
    assert len(default_osc.time_vector) == default_osc.record_length
    trig_idx = int(default_osc.record_length * default_osc.pre_sample_ratio)
    assert default_osc.time_vector[trig_idx] == 0
    assert default_osc.time_vector[trig_idx+1] == pytest.approx(1/default_osc.sample_freq)
    assert default_osc.time_vector[-1] == 1/default_osc.sample_freq*(default_osc.record_length-trig_idx-1)
    assert default_osc.time_vector[0] == -1/default_osc.sample_freq*(trig_idx)
