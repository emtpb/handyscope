def test_device_cnt(dev_list):
    assert type(dev_list.device_cnt) is int
    assert dev_list.device_cnt > 0


def test_can_open_device(dev_list):
    assert dev_list.can_open_device(0) is True


def test_get_firmware_version(dev_list):
    assert type(dev_list.get_firmware_version(0)) is str


def test_get_recommended_firmware_version(dev_list):
    assert type(dev_list.get_firmware_version(0)) is str


def test_get_device_name(dev_list):
    assert type(dev_list.get_device_name(0)) is str


def test_get_device_name_short(dev_list):
    assert type(dev_list.get_device_name_short(0)) is str


def test_get_device_name_shortest(dev_list):
    assert type(dev_list.get_device_name_shortest(0)) is str


def test_get_device_serial_no(dev_list):
    assert type(dev_list.get_device_serial_no(0)) is int


def test_get_device_types(dev_list):
    assert type(dev_list.get_device_types(0)) is dict
    for key, value in dev_list.get_device_types(0).items():
        assert key in dev_list.DEVICE_TYPES
        assert type(value) is bool


def test_get_overview(dev_list):
    assert type(dev_list.get_overview()) is tuple
    for element in dev_list.get_overview():
        assert type(element) is dict
        assert element["Index"] in range(dev_list.device_cnt)
        assert element["Name"] == dev_list.get_device_name_short(element["Index"])
        assert element["SerNo"] == dev_list.get_device_serial_no(element["Index"])
        assert element["DevTypes"] == dev_list.get_device_types(element["Index"])


def test_get_overview_str(dev_list):
    assert type(dev_list.get_overview_str()) is str


def test__str__(dev_list):
    assert str(dev_list) == dev_list.get_overview_str()


# Opening a device is tested when instantiating Oscilloscope, Generator and I2CHost
