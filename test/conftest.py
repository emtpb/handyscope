from tiepie.device import Device
from tiepie.deviceList import DeviceList
from tiepie.oscilloscope import Oscilloscope
from tiepie.generator import Generator
from tiepie.i2cHost import I2CHost
import pytest

_product_id = "HS5"


@pytest.fixture(scope="module", params=[key for key in DeviceList.DEVICE_TYPES])
def device(request):
    return Device(_product_id, "product id", request.param)


@pytest.fixture(scope="module")
def osc():
    return Oscilloscope(_product_id)


@pytest.fixture(scope="function")
def default_osc(osc):
    if osc.is_running:
        osc.stop()
    osc.measure_mode = "block"
    osc.clock_source = "internal"

    return osc


@pytest.fixture(scope="module")
def gen():
    return Generator(_product_id)


@pytest.fixture(scope="module")
def i2c():
    return I2CHost(_product_id)
