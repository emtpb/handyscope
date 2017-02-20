

class TestDevice:
    def setup_class(self):
        from tiepie.device import Device
        self.device = Device("HS5", "product id", "Osc")

    def test_driver_ver(self):
        ver_list = self.device.driver_ver.split('.')
        assert len(ver_list) == 4
        for element in ver_list:
            assert element.isdigit()

    def test_firmware_ver(self):
        ver_list = self.device.firmware_ver.split('.')
        assert len(ver_list) == 4
        for element in ver_list:
            assert element.isdigit()

    def test_calibration_date(self):
        import datetime

        assert type(self.device.calibration_date) is datetime.date

    def test_serial_no(self):
        assert type(self.device.serial_no) is int
        assert self.device.serial_no >= 0

    def test_product_id(self):
        from tiepie.deviceList import DeviceList

        product_id = self.device.product_id
        assert type(product_id) is str
        # Check if it is a valid key
        assert product_id in DeviceList.PRODUCT_IDS

    def test_device_type(self):
        from tiepie.deviceList import DeviceList

        device_type = self.device.device_type
        assert type(device_type) is str
        # Check if it is a valid key
        assert device_type in DeviceList.DEVICE_TYPES

    def test_short_name(self):
        from tiepie.deviceList import DeviceList

        name = self.device.short_name
        assert type(name) is str
        # Short name corresponds to product names -> look it up in the dict
        assert name in DeviceList.PRODUCT_IDS

    def test_name(self):
        name = self.device.name
        name_list = name.split('-')
        assert len(name_list) == 2
        # first part of name is the short name
        assert name_list[0] == self.device.short_name

    def test_long_name(self):
        name = self.device.long_name
        name_list = name.split(' ')
        assert len(name_list) == 2
        # first part of long name is always the manufacturer name
        assert name_list[0] == "Handyscope"
        # second part of long name is the name
        assert name_list[1] == self.device.name

    def test_is_removed(self):
        assert self.device.is_removed is False

    def test_trig_in_cnt(self):
        assert isinstance(self.device.trig_in_cnt, int)

    def test_trig_ins(self):
        assert len(self.device.trig_ins) is self.device.trig_in_cnt
