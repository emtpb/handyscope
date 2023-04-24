from handyscope.triggerInput import TriggerInput
from handyscope.triggerOutput import TriggerOutput


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
    from handyscope.deviceList import DeviceList

    product_id = device.product_id
    assert type(product_id) is str
    # Check if it is a valid key
    assert product_id in DeviceList.PRODUCT_IDS


def test_device_type(device):
    from handyscope.deviceList import DeviceList

    device_type = device.device_type
    assert type(device_type) is str
    # Check if it is a valid key
    assert device_type in DeviceList.DEVICE_TYPES


def test_short_name(device):
    from handyscope.deviceList import DeviceList

    name = device.short_name
    assert type(name) is str
    # For "Osc" and "I2C": Short name corresponds to product names -> look it up in the dict.
    # Attention: This is just an assumption made while working with the HS5 and libtiepie 0.6.3.
    if device.device_type in ["Osc", "I2C"]:
        assert name in DeviceList.PRODUCT_IDS
    # For "Gen": Short name consist out of "AWG " + product name. Attention: This is just an assumption made while
    # working with the HS5 and libtiepie 0.5 / 0.6.3.
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
    assert len(name_list) == 2
    # first part of long name is always the manufacturer name
    assert name_list[0] == "Handyscope"
    # second part of long name is the name
    assert name_list[1] == device.name


def test_is_battery_available(device):
    assert device.is_battery_available == False


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
