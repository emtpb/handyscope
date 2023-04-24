from handyscope.oscilloscopeChannel import OscilloscopeChannel
import pytest


def test_bandwidths_available(osc):
    for channel in osc.channels:
        assert type(channel.bandwidths_available) is tuple


def test_bandwidth(osc):
    for channel in osc.channels:
        assert type(channel.bandwidth) is float
        assert channel.bandwidth >= 0


def test_is_safe_ground_available(osc):
    for channel in osc.channels:
        assert type(channel.is_safe_ground_available) is bool


def test_connector_type(osc):
    for channel in osc.channels:
        assert channel.connector_type in OscilloscopeChannel.CONNECTOR_TYPES


def test_is_differential(osc):
    for channel in osc.channels:
        assert type(channel.is_differential) is bool


def test_impedance(osc):
    for channel in osc.channels:
        assert type(channel.impedance) is float
        assert channel.impedance > 0


def test_couplings_available(osc):
    for channel in osc.channels:
        # must at least contain "unknown"
        assert len(channel.couplings_available) > 0

        for coupling in channel.couplings_available:
            assert coupling in OscilloscopeChannel.COUPLINGS


def test_coupling(osc):
    for channel in osc.channels:
        # test getter
        assert channel.coupling in OscilloscopeChannel.COUPLINGS

        # test setter
        for coupling in channel.couplings_available:
            channel.coupling = coupling
            assert channel.coupling is coupling


def test_is_enabled(osc):
    for channel in osc.channels:
        # test getter
        assert type(channel.is_enabled) is bool

        # test setter
        channel.is_enabled = True
        assert channel.is_enabled is True
        channel.is_enabled = False
        assert channel.is_enabled is False


def test_probe_gain(osc):
    for channel in osc.channels:
        # test getter
        assert type(channel.probe_gain) is float
        assert -1e6 <= channel.probe_gain <= 1e6
        assert channel.probe_gain != 0

        # test setter
        # valid gains
        for valid_gain in [-1e6, 1, 1e6]:
            channel.probe_gain = valid_gain
            assert channel.probe_gain == valid_gain

        # invalid gain (0)
        with pytest.raises(OSError) as err:
            channel.probe_gain = 0
        assert err.value.args[0] == "[-4]: INVALID_VALUE"

        # gains out of range
        for oor_gain in [-2e6, 2e6]:
            with pytest.warns(UserWarning) as record:
                channel.probe_gain = oor_gain
            # check that only one warning was raised
            assert len(record) == 1
            # check that the message matches
            assert record[0].message.args[0] == "[1]: VALUE_CLIPPED"


def test_probe_offset(osc):
    for channel in osc.channels:
        # test getter
        assert type(channel.probe_offset) is float
        assert -1e6 <= channel.probe_offset <= 1e6

        # test setter
        # valid offsets
        for valid_offset in [-1e6, 0, 1, 1e6]:
            channel.probe_offset = valid_offset
            assert channel.probe_offset == valid_offset

        # offsets out of range
        for oor_offset in [-2e6, 2e6]:
            with pytest.warns(UserWarning) as record:
                channel.probe_offset = oor_offset
            # check that only one warning was raised
            assert len(record) == 1
            # check that the message matches
            assert record[0].message.args[0] == "[1]: VALUE_CLIPPED"


def test_is_auto_range(osc):
    for channel in osc.channels:
        # test getter
        assert type(channel.is_auto_range) is bool

        # test setter
        channel.is_auto_range = True
        assert channel.is_auto_range is True
        channel.is_auto_range = False
        assert channel.is_auto_range is False


def test_ranges_available(osc):
    for channel in osc.channels:
        assert type(channel.ranges_available) is tuple
        for element in channel.ranges_available:
            assert type(element) is float
            assert element > 0


def test_range(osc):
    for channel in osc.channels:
        # Test getter
        assert type(channel.range) is float
        assert channel.range > 0

        # Test setter
        for range_available in channel.ranges_available:
            channel.range = range_available
            assert channel.range == range_available


def test_is_trig_enabled(osc):
    for channel in osc.channels:
        # test getter
        assert type(channel.is_trig_enabled) is bool

        # test setter
        channel.is_trig_enabled = True
        assert channel.is_trig_enabled is True
        channel.is_trig_enabled = False
        assert channel.is_trig_enabled is False


def test_trig_kinds_available(osc):
    for channel in osc.channels:
        for trig_kind in channel.trig_kinds_available:
            assert trig_kind in channel.TRIGGER_KINDS


def test_trig_kind(osc):
    for channel in osc.channels:
        # Test getter
        # If there are multiple kinds available, the chosen kind can be retrieved.
        if channel.trig_kinds_available != ("unknown", ):
            assert channel.trig_kind in channel.TRIGGER_KINDS
        # Else (no known kinds), accessing the chosen kind raises an OSError.
        else:
            with pytest.raises(OSError) as err:
                channel.trig_kind
            assert err.value.args[0] == "[-2]: NOT_SUPPORTED"

        # Test setter
        # If there are multiple kinds available, the chosen kind can be set.
        if channel.trig_kinds_available != ("unknown", ):
            # Test every available kind
            for kind in channel.trig_kinds_available:
                # Set the value
                channel.trig_kind = kind
                # Read it back & compare
                assert channel.trig_kind == kind
        # Else (no known kinds), setting the chosen kind raises an OSError.
        else:
            with pytest.raises(OSError) as err:
                channel.trig_kind = "unknown"
            assert err.value.args[0] == "[-2]: NOT_SUPPORTED"


def test_trig_lvl_cnt(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_lvl_cnt is influenced by them
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind
            assert type(channel.trig_lvl_cnt) is int
            assert channel.trig_lvl_cnt >= 0


def test_trig_lvl(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_lvl is influenced by them
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind

            # Test getter
            assert len(channel.trig_lvl) is channel.trig_lvl_cnt
            for element in channel.trig_lvl:
                assert type(element) is float

            # Test setter
            # Assuming the default trig_lvl_mode "relative", values range from 0 to 1
            channel.trig_lvl = tuple(0.0 for _ in range(channel.trig_lvl_cnt))
            assert channel.trig_lvl == tuple(0.0 for _ in range(channel.trig_lvl_cnt))
            channel.trig_lvl = tuple(0.5 for _ in range(channel.trig_lvl_cnt))
            assert channel.trig_lvl == tuple(0.5 for _ in range(channel.trig_lvl_cnt))
            channel.trig_lvl = tuple(1.0 for _ in range(channel.trig_lvl_cnt))
            assert channel.trig_lvl == tuple(1.0 for _ in range(channel.trig_lvl_cnt))


def test_trig_lvl_modes_available(osc):
    for channel in osc.channels:
        for mode in channel.trig_lvl_modes_available:
            assert mode in channel.TRIGGER_LVL_MODES


def test_trig_lvl_mode(osc):
    for channel in osc.channels:
        # Test getter
        # If there are multiple modes available, the mode can be retrieved.
        if channel.trig_lvl_modes_available != ("unknown", ):
            assert channel.trig_lvl_mode in channel.TRIGGER_LVL_MODES
        # Else (no known modes), accessing the chosen kind raises an OSError.
        else:
            with pytest.raises(OSError) as err:
                channel.trig_lvl_mode
            assert err.value.args[0] == "[-2]: NOT_SUPPORTED"

        # Test setter
        # If there are multiple modes available, the mode can be set.
        if channel.trig_lvl_modes_available != ("unknown", ):
            # Test every available mode
            for mode in channel.trig_lvl_modes_available:
                # Set the value
                channel.trig_lvl_mode = mode
                # Read it back & compare
                assert channel.trig_lvl_mode == mode
        # Else (no known modes), setting the mode raises an OSError.
        else:
            with pytest.raises(OSError) as err:
                channel.trig_lvl_mode = "unknown"
            assert err.value.args[0] == "[-2]: NOT_SUPPORTED"


def test_trig_hysteresis_cnt(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_hysteresis_cnt is influenced by them
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind
            assert type(channel.trig_hysteresis_cnt) is int
            assert channel.trig_hysteresis_cnt >= 0
            
            
def test_trig_hysteresis(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_hysteresis is influenced by them
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind

            # Test getter
            assert len(channel.trig_hysteresis) is channel.trig_hysteresis_cnt
            for element in channel.trig_hysteresis:
                assert type(element) is float

            # Test setter
            channel.trig_hysteresis = tuple(0.0 for _ in range(channel.trig_hysteresis_cnt))
            assert channel.trig_hysteresis == tuple(0.0 for _ in range(channel.trig_hysteresis_cnt))
            channel.trig_hysteresis = tuple(0.5 for _ in range(channel.trig_hysteresis_cnt))
            assert channel.trig_hysteresis == tuple(0.5 for _ in range(channel.trig_hysteresis_cnt))
            channel.trig_hysteresis = tuple(1.0 for _ in range(channel.trig_hysteresis_cnt))
            assert channel.trig_hysteresis == tuple(1.0 for _ in range(channel.trig_hysteresis_cnt))


def test_trig_conditions_available(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_conditions_available is influenced by them
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind

            for trig_condition in channel.trig_conditions_available:
                assert trig_condition in channel.TRIGGER_CONDITIONS


def test_trig_condition(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_condition is influenced by them
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind

            # Test getter
            # If there are multiple conditions available, the chosen condition can be retreived.
            if channel.trig_conditions_available != ("unknown", ):
                assert channel.trig_condition in channel.TRIGGER_CONDITIONS
            # Else (no known conditions), accessing the chosen condition raises an OSError.
            else:
                with pytest.raises(OSError) as err:
                    channel.trig_condition
                assert err.value.args[0] == "[-2]: NOT_SUPPORTED"

            # Test setter
            # If there are multiple conditions available, the condition can be set.
            if channel.trig_conditions_available != ("unknown", ):
                for condition in channel.trig_conditions_available:
                    channel.trig_condition = condition
                    assert channel.trig_condition is condition
            # Else (no known conditions), setting the chosen condition raises an OSError.
            else:
                with pytest.raises(OSError) as err:
                    channel.trig_condition = "unknown"
                assert err.value.args[0] == "[-2]: NOT_SUPPORTED"


def test_trig_time_cnt(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_time_cnt is influenced by it
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind
            # If possible, alter trig_condition, because trig_time_cnt is influenced by it
            if channel.trig_conditions_available != ("unknown", ):
                for trig_condition in channel.trig_conditions_available:
                    channel.trig_condition = trig_condition

                    assert type(channel.trig_time_cnt) is int
                    assert channel.trig_time_cnt >= 0
            # If not possible, just do the check
            else:
                assert type(channel.trig_time_cnt) is int
                assert channel.trig_time_cnt >= 0


def test_trig_time(osc):
    for channel in osc.channels:
        # Alter trig_kind, because trig_time_cnt is influenced by it
        for trig_kind in channel.trig_kinds_available:
            channel.trig_kind = trig_kind
            # If possible, alter trig_condition, because trig_time_cnt is influenced by it
            if channel.trig_conditions_available != ("unknown", ):
                for trig_condition in channel.trig_conditions_available:
                    channel.trig_condition = trig_condition

                    # Test getter
                    assert type(channel.trig_time) is tuple
                    assert len(channel.trig_time) is channel.trig_time_cnt
                    for element in channel.trig_time:
                        assert type(element) is float

                    # Test setter
                    channel.trig_time = tuple(0.1 for _ in range(channel.trig_time_cnt))
                    assert channel.trig_time == tuple(0.1 for _ in range(channel.trig_time_cnt))
                    channel.trig_time = tuple(0.001 for _ in range(channel.trig_time_cnt))
                    assert channel.trig_time == tuple(0.001 for _ in range(channel.trig_time_cnt))

            # If not possible, just do the check
            else:
                # Test getter
                assert type(channel.trig_time) is tuple
                assert len(channel.trig_time) is channel.trig_time_cnt
                for element in channel.trig_time:
                    assert type(element) is float

                # Test setter
                channel.trig_time = tuple(0.1 for _ in range(channel.trig_time_cnt))
                assert channel.trig_time == tuple(0.1 for _ in range(channel.trig_time_cnt))
                channel.trig_time = tuple(0.001 for _ in range(channel.trig_time_cnt))
                assert channel.trig_time == tuple(0.001 for _ in range(channel.trig_time_cnt))


def test_is_trig_available(osc):
    for channel in osc.channels:
        assert type(channel.is_trig_available) is bool


def test_is_available(osc):
    for channel in osc.channels:
        assert type(channel.is_available) is bool


def test_is_connection_test_available(osc):
    for channel in osc.channels:
        assert type(channel.is_connection_test_available) is bool


def test_data_range(osc):
    for channel in osc.channels:
        assert type(channel.data_range) is tuple
        assert len(channel.data_range) is 2
        for element in channel.data_range:
            assert type(element) is float


def test_data_value_min(osc):
    for channel in osc.channels:
        assert type(channel.data_value_min) is float


def test_data_value_max(osc):
    for channel in osc.channels:
        assert type(channel.data_value_max) is float


def test_raw_data_type(osc):
    for channel in osc.channels:
        assert type(channel.raw_data_type) is str
        assert channel.raw_data_type in channel.RAW_DATA_TYPES.keys()


def test_raw_value_min(osc):
    for channel in osc.channels:
        assert type(channel.raw_value_min) is int
        assert channel.raw_value_min >= 0


def test_raw_value_max(osc):
    for channel in osc.channels:
        assert type(channel.raw_value_max) is int
        assert channel.raw_value_max >= 0
        assert channel.raw_value_max >= channel.raw_value_min


def test_raw_value_zero(osc):
    for channel in osc.channels:
        assert type(channel.raw_value_zero) is int
        assert channel.raw_value_zero >= channel.raw_value_min
        assert channel.raw_value_zero <= channel.raw_value_max


def test_raw_data_range(osc):
    for channel in osc.channels:
        assert type(channel.raw_data_range) is tuple
        assert channel.raw_data_range[0] == channel.raw_value_min
        assert channel.raw_data_range[1] == channel.raw_value_zero
        assert channel.raw_data_range[2] == channel.raw_value_max
