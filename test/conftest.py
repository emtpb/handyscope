from tiepie.device import Device
from tiepie.deviceList import DeviceList
from tiepie.oscilloscope import Oscilloscope
from tiepie.generator import Generator
from tiepie.i2cHost import I2CHost
import tiepie.deviceList
import pytest

_product_id = "HS5"


@pytest.fixture(scope="module")
def dev_list():
    return tiepie.deviceList.device_list

@pytest.fixture(scope="module", params=[key for key in DeviceList.DEVICE_TYPES])
def device(request):
    dev_instance = Device(_product_id, "product id", request.param)
    yield dev_instance
    dev_instance.dev_close()


@pytest.fixture(scope="module")
def osc():
    osc_instance = Oscilloscope(_product_id)
    yield osc_instance
    osc_instance.dev_close()


@pytest.fixture(scope="function")
def default_osc(osc):
    if osc.is_running:
        osc.stop()
    osc.measure_mode = "block"
    osc.clock_source = "internal"
    osc.auto_resolution = "disabled"
    osc.resolution = 14
    osc.record_length = 5000
    osc.segment_cnt = 1
    osc.trig_delay = 0.0
    osc.trig_holdoff = 0

    osc.channels[0].is_enabled = True
    for channel in osc.channels[1:]:
        channel.is_enabled = False

    return osc


@pytest.fixture(scope="module")
def gen():
    gen_instance = Generator(_product_id)
    yield gen_instance
    gen_instance.dev_close()


@pytest.fixture(scope="function")
def default_gen_sine(gen):
    gen.is_amplitude_autorange = True
    gen.signal_type = "sine"
    gen.mode = "continuous"
    gen.offset = 0.0
    gen.amplitude = 1.0
    gen.stop()

    return gen


@pytest.fixture(scope="function")
def default_gen_pulse(gen):
    gen.is_amplitude_autorange = True
    gen.signal_type = "pulse"
    gen.mode = "continuous"
    gen.offset = 0.0
    gen.amplitude = 1.0
    gen.freq = 1000.0

    return gen


@pytest.fixture(scope="function")
def default_gen_arb(gen):
    gen.is_amplitude_autorange = True
    gen.signal_type = "arbitrary"
    gen.mode = "continuous"
    gen.offset = 0.0
    gen.amplitude = 1.0

    return gen


@pytest.fixture(scope="function")
def default_gen_burst(gen):
    gen.is_amplitude_autorange = True
    gen.signal_type = "sine"
    gen.mode = "burst count"
    gen.offset = 0.0
    gen.amplitude = 1.0

    return gen


@pytest.fixture(scope="function")
def default_gen_burst_sample(gen):
    gen.is_amplitude_autorange = True
    gen.signal_type = "arbitrary"
    gen.arb_data([0.0, 1.0, 2.0, 3.0, 4.0])
    gen.mode = "burst sample count"
    gen.offset = 0.0
    gen.amplitude = 1.0

    return gen


@pytest.fixture(scope="function")
def default_gen_burst_segment(gen):
    gen.is_amplitude_autorange = True
    gen.signal_type = "arbitrary"
    gen.arb_data([0.0, 1.0, 2.0, 3.0, 4.0])
    gen.mode = "burst segment count"
    gen.offset = 0.0
    gen.amplitude = 1.0

    return gen


@pytest.fixture(scope="module")
def i2c():
    i2c_instance = I2CHost(_product_id)
    yield i2c_instance
    i2c_instance.dev_close()
