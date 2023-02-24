from tiepie.device import Device
from tiepie.deviceList import DeviceList
from tiepie.oscilloscope import Oscilloscope
from tiepie.generator import Generator
from tiepie.i2cHost import I2CHost
import tiepie.deviceList
import pytest


def pytest_addoption(parser):
    parser.addoption("--product_id", action="store", default="HS5")


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.product_id
    if 'product_id' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("product_id", [option_value], scope="module")


@pytest.fixture(scope="module")
def dev_list():
    return tiepie.deviceList.device_list


@pytest.fixture(scope="module", params=[key for key in DeviceList.DEVICE_TYPES])
def device(product_id, request):
    dev_instance = Device(product_id, "product id", request.param)
    yield dev_instance
    dev_instance.close()


@pytest.fixture(scope="module")
def osc(product_id):
    osc_instance = Oscilloscope(product_id)
    yield osc_instance
    osc_instance.close()


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
def gen(product_id):
    gen_instance = Generator(product_id)
    yield gen_instance
    gen_instance.close()


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
    gen.freq_mode = "sample"
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
def i2c(product_id):
    i2c_instance = I2CHost(product_id)
    yield i2c_instance
    i2c_instance.close()
