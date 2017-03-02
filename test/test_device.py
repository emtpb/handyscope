import pytest
from tiepie.triggerInput import TriggerInput
from tiepie.triggerOutput import TriggerOutput
from tiepie.deviceList import DeviceList
from tiepie.device import Device


@pytest.fixture(scope="module", params=[key for key in DeviceList.DEVICE_TYPES])
def device(request):
    return Device("HS5", "product id", request.param)


def test_driver_ver(device):
    ver_list = device.driver_ver.split('.')
    assert len(ver_list) == 4
    for element in ver_list:
        assert element.isdigit()


def test_firmware_ver(device):
    ver_list = device.firmware_ver.split('.')
    assert len(ver_list) == 4
    for element in ver_list:
        assert element.isdigit()


def test_calibration_date(device):
    import datetime

    assert type(device.calibration_date) is datetime.date


def test_serial_no(device):
    assert type(device.serial_no) is int
    assert device.serial_no >= 0


def test_product_id(device):
    from tiepie.deviceList import DeviceList

    product_id = device.product_id
    assert type(product_id) is str
    # Check if it is a valid key
    assert product_id in DeviceList.PRODUCT_IDS


def test_device_type(device):
    from tiepie.deviceList import DeviceList

    device_type = device.device_type
    assert type(device_type) is str
    # Check if it is a valid key
    assert device_type in DeviceList.DEVICE_TYPES


def test_short_name(device):
    from tiepie.deviceList import DeviceList

    name = device.short_name
    assert type(name) is str
    # For "Osc": Short name corresponds to product names -> look it up in the dict
    if device.device_type == "Osc":
        assert name in DeviceList.PRODUCT_IDS
    # For "I2C": Short name consist out of "I²C " + product name. Attention: This is just an assumption made while
    # working with the HS5.
    elif device.device_type == "I2C":
        assert name in ["I²C " + product for product in DeviceList.PRODUCT_IDS]
    # For "Gen": Short name consist out of "AWG " + product name. Attention: This is just an assumption made while
    # working with the HS5.
        if device.device_type == "Gen":
            assert name in ["AWG " + product for product in DeviceList.PRODUCT_IDS]


def test_name(device):
    name = device.name
    name_list = name.split('-')
    assert len(name_list) == 2
    # first part of name is the short name
    assert name_list[0] == device.short_name


def test_long_name(device):
    name = device.long_name
    name_list = name.split(' ')
    if device.device_type == "Osc":
        assert len(name_list) == 2
        # first part of long name is always the manufacturer name
        assert name_list[0] == "Handyscope"
        # second part of long name is the name
        assert name_list[1] == device.name
    elif device.device_type == "Gen":
        assert len(name_list) == 3
        # first part of long name is the device type
        assert name_list[0] == "AWG"
        # second part of long name is always the manufacturer name
        assert name_list[1] == "Handyscope"
        # third part of long name is the name (e.g. AWG HS5-540XMS) without the device type
        assert name_list[2] == device.name.split(' ')[1]
    elif device.device_type == "I2C":
        assert len(name_list) == 3
        # first part of long name is the device type
        assert name_list[0] == "I²C"
        # second part of long name is always the manufacturer name
        assert name_list[1] == "Handyscope"
        # third part of long name is the name (e.g. I²C HS5-540XMS) without the device type
        assert name_list[2] == device.name.split(' ')[1]


def test_is_removed(device):
    assert device.is_removed is False


def test_trig_in_cnt(device):
    assert type(device.trig_in_cnt) is int


def test_trig_ins(device):
    assert len(device.trig_ins) is device.trig_in_cnt
    for trig_in in device.trig_ins:
        assert type(trig_in) is TriggerInput


def test_trig_in_id(device):
    for trig_in_id in TriggerInput.TRIGGER_IDS:
        try:
            index = device.trig_in_by_id(trig_in_id)
            # If the id is supported by the device, a valid integer has to be returned. If not, 0xffff is returned.
            assert (index in range(device.trig_in_cnt)) | (index == 0xffff)
        except OSError as err:
            # If the device has no trigger inputs, an OSError is raised.
            assert str(err) == "[-2]: NOT_SUPPORTED"


def test_trig_out_cnt(device):
    assert type(device.trig_out_cnt) is int


def test_trig_outs(device):
    assert len(device.trig_outs) is device.trig_out_cnt
    for trig_out in device.trig_outs:
        assert type(trig_out) is TriggerOutput


def test_trig_out_id(device):
    for trig_out_id in TriggerOutput.TRIGGER_IDS:
        try:
            index = device.trig_out_by_id(trig_out_id)
            # If the id is supported by the device, a valid integer has to be returned. If not, 0xffff is returned.
            assert (index in range(device.trig_out_cnt)) | (index == 0xffff)
        except OSError as err:
            # If the device has no trigger outputs, an OSError is raised.
            assert str(err) == "[-2]: NOT_SUPPORTED"
