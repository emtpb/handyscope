from tiepie.oscilloscope import Oscilloscope
from tiepie.oscilloscopeChannel import OscilloscopeChannel
import pytest


@pytest.fixture(scope="module")
def osc():
    _osc = Oscilloscope('HS5')
    return _osc


@pytest.fixture(scope="module", params=[idx for idx in range(osc().channel_count)])
def channel(osc, request):
    return osc.channels[request.param]


def test_connector_type(channel):
    assert channel.connector_type in OscilloscopeChannel.CONNECTOR_TYPES


def test_is_differential(channel):
    assert type(channel.is_differential) is bool


def test_impedance(channel):
    assert type(channel.impedance) is float
    assert channel.impedance > 0


def test_couplings(channel):
    # must at least contain "unknown"
    assert len(channel.couplings) > 0

    for coupling in channel.couplings:
        assert coupling in OscilloscopeChannel.COUPLINGS


def test_coupling(channel):
    # test getter
    assert channel.coupling in OscilloscopeChannel.COUPLINGS

    # test setter
    for coupling in channel.couplings:
        channel.coupling = coupling
        assert channel.coupling is coupling


def test_is_enabled(channel):
    # test getter
    assert type(channel.is_enabled) is bool

    # test setter
    channel.is_enabled = True
    assert channel.is_enabled is True
    channel.is_enabled = False
    assert channel.is_enabled is False


def test_probe_gain(channel):
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


def test_probe_offset(channel):
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


def test_is_auto_range(channel):
    # test getter
    assert type(channel.is_auto_range) is bool

    # test setter
    channel.is_auto_range = True
    assert channel.is_auto_range is True
    channel.is_auto_range = False
    assert channel.is_auto_range is False


def test_trig_enabled(channel):
    # test getter
    assert type(channel.trig_enabled) is bool

    # test setter
    channel.trig_enabled = True
    assert channel.trig_enabled is True
    channel.trig_enabled = False
    assert channel.trig_enabled is False