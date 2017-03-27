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
    data = osc.retrieve_ch1_ch2()
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

    # Check for multiple channels
    if osc.channel_cnt >= 2:
        # There is more than one channel -> we can disable the first without getting an error
        osc.channels[0].is_enabled = False
        osc.start()
        while not osc.is_data_ready:
            time.sleep(0.05)
        data = osc.retrieve_ch1()
        assert data == [None]


def test_retrieve_ch1_ch2(osc):
    # --- Try to retrieve all channels
    # Enable all available channels
    for channel in osc.channels:
        channel.is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve_ch1_ch2()
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
        data = osc.retrieve_ch1_ch2()
        assert type(data) is list
        assert len(data) == 2
        # First channel was disabled
        assert data[0] is None
        # Second channel should contain data
        assert type(data[1]) is list
        for sample in data[1]:
            assert type(sample) is float


def test_retrieve_ch1_ch2_ch3(osc):
    # --- Try to retrieve all channels
    # Enable available channels
    for channel in osc.channels:
        channel.is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve_ch1_ch2_ch3()
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
        data = osc.retrieve_ch1_ch2_ch3()

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


def test_retrieve_ch1_ch2_ch3_ch4(osc):
    # --- Try to retrieve all channels
    # Enable available channels
    for channel in osc.channels:
        channel.is_enabled = True
    osc.start()
    while not osc.is_data_ready:
        time.sleep(0.05)
    data = osc.retrieve_ch1_ch2_ch3_ch4()
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
        data = osc.retrieve_ch1_ch2_ch3_ch4()

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
