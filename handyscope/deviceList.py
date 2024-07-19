from handyscope.library import libtiepie

from datetime import date
import ctypes


class DeviceList:
    """This class provides access to the device list maintained by libtiepie.

    Attributes:
        ID_KINDS (dict): dict which maps readable representations of id kinds
                         to their int version
        PRODUCT_IDS (dict): dict which maps readable representations of product
                            ids to their int version
        DEVICE_TYPES (dict): dict which maps readable representations of
                             device types to their int version
    """

    ID_KINDS = {"product id":    1,
                "index":         2,
                "serial number": 4}

    PRODUCT_IDS = {"none":       0,
                   "combined":   2,
                   "HS3":       13,
                   "HS4":       15,
                   "HP3":       18,
                   "HS4D":      20,
                   "HS5":       22,
                   "HS6":       24,
                   "HS6D":      25}

    DEVICE_TYPES = {"Osc": 1,
                    "Gen": 2,
                    "I2C": 4}

    def __init__(self):
        """Constructor for class DeviceList."""
        # Fill the device list
        libtiepie.LstUpdate()

    @property
    def device_cnt(self):
        """Get device count.

        Returns:
            int: device count
        """
        return libtiepie.LstGetCount()

    def can_open_device(self, instr_id, id_kind="index", device_type="Osc"):
        """Check whether a device can be opened.

        Args:
            instr_id (int or str): Device list index, product ID
                                   (listed in dict PRODUCT_IDS) or
                                   serial number.
            id_kind (str): The kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device
                           list index.
            device_type (str): The type of the device
                               (listed in dict DEVICE_TYPES),
                               defaults to oscilloscope.

        Returns:
            bool: True, if the device can be opened.
        """
        # translate id kind & device type str to int
        id_kind_int = self.ID_KINDS[id_kind]
        device_type_int = self.DEVICE_TYPES[device_type]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        return libtiepie.LstDevCanOpen(id_kind_int,
                                       instr_id_int, device_type_int) == 1

    def get_vendor_id(self, instr_id, id_kind="index"):
        """Get the vendor id of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            int: vendor id
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the vendor id
        vendor_id = libtiepie.LstDevGetVendorId(id_kind_int, instr_id_int)

        return vendor_id

    def get_product_id(self, instr_id, id_kind="index"):
        """Get the product id of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            int: product id
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the product id
        product_id = libtiepie.LstDevGetProductId(id_kind_int, instr_id_int)

        return product_id

    def get_driver_version(self, instr_id, id_kind="index"):
        """Get the driver version of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            str: driver version
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the driver version
        driver_version = libtiepie.LstDevGetDriverVersion(id_kind_int,
                                                          instr_id_int)

        return version_to_str(driver_version)

    def get_recommended_driver_version(self, instr_id, id_kind="index"):
        """Get the recommended driver version of the device.

        Not tested.
        
        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            str: recommended driver version
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the driver version
        driver_version = libtiepie.LstDevGetRecommendedDriverVersion(
            id_kind_int, instr_id_int)

        return version_to_str(driver_version)

    def get_firmware_version(self, instr_id, id_kind="index"):
        """Get the firmware version of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            str: firmware version
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the firmware version
        firmware_version = libtiepie.LstDevGetFirmwareVersion(id_kind_int,
                                                              instr_id_int)

        return version_to_str(firmware_version)

    def get_recommended_firmware_version(self, instr_id, id_kind="index"):
        """Get the recommended firmware version of the device.
        
        Not tested.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            str: recommended firmware version
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the firmware version
        firmware_version = libtiepie.LstDevGetRecommendedFirmwareVersion(
            id_kind_int, instr_id_int)

        return version_to_str(firmware_version)

    def get_calibration_date(self, instr_id, id_kind="index"):
        """Get the calibration date of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            :py:class:`datetime.date`: calibration date
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        # get the calibration date
        raw_date = libtiepie.LstDevGetCalibrationDate(id_kind_int,
                                                      instr_id_int)

        split_date = date(raw_date >> 16, (raw_date >> 8) & 0xff,
                          raw_date & 0xff)
        return split_date

    def get_device_name(self, instr_id, id_kind="index"):
        """Get the full name of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            str: full device name
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of device name string
        str_len = libtiepie.LstDevGetName(id_kind_int, instr_id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstDevGetName(id_kind_int, instr_id, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_name_short(self, instr_id, id_kind="index"):
        """Get the short name of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            str: short device name
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of device name string
        str_len = libtiepie.LstDevGetNameShort(id_kind_int, instr_id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstDevGetNameShort(id_kind_int,
                                     instr_id,
                                     str_buffer,
                                     str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_name_shortest(self, instr_id, id_kind="index"):
        """Get the shortest name of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            str: shortest device name
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of device name string
        str_len = libtiepie.LstDevGetNameShortest(id_kind_int, instr_id,
                                                  None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstDevGetNameShortest(id_kind_int, instr_id, str_buffer,
                                        str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_serial_no(self, instr_id, id_kind="index"):
        """Get the serial number of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            int: serial number
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get the serial number
        serial_no = libtiepie.LstDevGetSerialNumber(id_kind_int, instr_id)

        return serial_no

    def get_contained_serial_no(self, instr_id, id_kind="index"):
        """Get serial numbers of devices in a contained device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            tuple: serial numbers of the devices
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of list
        serial_len = libtiepie.LstDevGetContainedSerialNumbers(id_kind_int,
                                                               instr_id,
                                                               None, 0)
        # initialize uint32 array
        serial_numbers = (ctypes.c_uint32 * serial_len)()

        # write the actual data to the array
        libtiepie.LstDevGetContainedSerialNumbers(id_kind_int, instr_id,
                                                  serial_numbers, serial_len)

        # convert to a normal python list
        serial_numbers = list(serial_numbers)

        return tuple(serial_numbers)

    def get_ipv4_address(self, instr_id, id_kind="index"):
        """Get the IP address of an instrument.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            int: IP address
        """
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        ip_v4_addr = libtiepie.LstDevGetIPv4Address(id_kind_int, instr_id_int)

        return ip_v4_addr

    def get_ip_port(self, instr_id, id_kind="index"):
        """Get the IP Port number of the instrument.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            int: IP port
        """
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        ip_port = libtiepie.LstDevGetIPPort(id_kind_int, instr_id_int)

        return ip_port

    def is_connected_to_server(self, instr_id, id_kind="index"):
        """Get whether the device is connected to a server.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            bool: True, if the device is connected to a server.
        """
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        return libtiepie.LstDevHasServer(id_kind_int, instr_id_int) == 1

    def get_device_types(self, instr_id, id_kind="index"):
        """Get the device types of an instrument.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.

        Returns:
            dict: key: type (as listed in DEVICE_TYPES), value: True/False.
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get the device types
        dev_types = libtiepie.LstDevGetTypes(id_kind_int, instr_id)

        # check for every possible type and store in dict
        type_dict = {"Osc": False,
                     "Gen": False,
                     "I2C": False}
        for key in self.DEVICE_TYPES:
            if dev_types & self.DEVICE_TYPES[key]:
                type_dict[key] = True

        return type_dict

    def get_overview(self):
        """Return a list with information on all connected instruments (index,
        name, serial number and device types).

        Returns:
            tuple: Tuple of dicts with info on connected instruments.
        """
        instr_list = []
        for idx in range(self.device_cnt):
            instr_info = {"Index":      idx,
                          "Name":       self.get_device_name_short(idx),
                          "SerNo":      self.get_device_serial_no(idx),
                          "DevTypes":   self.get_device_types(idx)}
            instr_list.append(instr_info)

        return tuple(instr_list)

    def get_overview_str(self):
        """Return a string with information on all connected instruments
        (index, name, serial number and device types).

        Returns:
            str: Information on connected instruments.
        """
        instr_str = ""
        for instr_info in self.get_overview():
            instr_str += "%d:\t%s\t%d\t%s\n" % (instr_info["Index"],
                                                instr_info["Name"],
                                                instr_info["SerNo"],
                                                instr_info["DevTypes"])

        return instr_str

    def __str__(self):
        """Return a (more or less) human-readable representation of the
        instruments in the device list.

        Returns:
            str: Instruments in the device list and info on them.
        """
        return self.get_overview_str()

    def open_device(self, instr_id, id_kind="index", device_type="Osc"):
        """Open a device (of device_type) of an instrument (with given id) and
        return the device handle.

        Args:
            instr_id (int or str): Device list index, product ID (listed
                                   in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id (listed in
                           dict ID_KINDS), defaults to device list index.
            device_type (str): the type of the device (listed in dict
                               DEVICE_TYPES), defaults to oscilloscope.

        Returns:
            handle (:py:class:`ctypes.c_uint32`): device handle
        """
        # translate id kind & device type str to int
        id_kind_int = self.ID_KINDS[id_kind]
        device_type_int = self.DEVICE_TYPES[device_type]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        return libtiepie.LstOpenDevice(id_kind_int, instr_id_int,
                                       device_type_int)

    def get_channel_count_cb(self, instr_id, contained_serial_no,
                             id_kind="index"):
        """Get the amount of channels of a contained oscilloscope in a combined
        instrument.

        Args:
            instr_id (int or str): Device list index, product ID (listed
                                   in dict PRODUCT_IDS) or serial number.
            id_kind (str): The kind of the given instr_id (listed in dict
                           ID_KINDS), defaults to device list index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.

        Returns:
            int: Channel count of the device
        """
        # translate id kind & device type str to int
        id_kind_int = self.ID_KINDS[id_kind]
        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        return libtiepie.LstCbScpGetChannelCount(id_kind_int, instr_id_int,
                                                 contained_serial_no)

    def get_product_id_cb(self, instr_id, contained_serial_no,
                          id_kind="index"):
        """Get the product id of a contained device in a combined instrument.

        Args:
            instr_id (int or str): Device list index, product ID (listed
                                   in dict PRODUCT_IDS) or serial number.
            id_kind (str): The kind of the given instr_id (listed in dict
                           ID_KINDS), defaults to device list index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.

        Returns: Product id of the device.
        """
        # translate id kind & device type str to int
        id_kind_int = self.ID_KINDS[id_kind]
        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        return libtiepie.LstCbDevGetProductId(id_kind_int, instr_id_int,
                                              contained_serial_no)

    def get_vendor_id_cb(self, instr_id, contained_serial_no,
                         id_kind="index"):
        """Get the vendor_id of a contained device in a combined instrument.

        Args:
            instr_id (int or str): Device list index, product ID (listed
                                   in dict PRODUCT_IDS) or serial number.
            id_kind (str): The kind of the given instr_id (listed in dict
                           ID_KINDS), defaults to device list index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.

        Returns:
            int: vendor id of the device.
        """
        # translate id kind & device type str to int
        id_kind_int = self.ID_KINDS[id_kind]
        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        return libtiepie.LstCbDevGetVendorId(id_kind_int, instr_id_int,
                                             contained_serial_no)

    def get_device_name_cb(self, instr_id, contained_serial_no,
                           id_kind="index"):
        """Get the full name of a contained device in a combined instrument.

        Args:
            instr_id (int or str): Device list index, product ID (listed
                                   in dict PRODUCT_IDS) or serial number.
            id_kind (str): The kind of the given instr_id (listed in dict
                           ID_KINDS), defaults to device list index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.

        Returns:
            str: full device name of the device
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of device name string
        str_len = libtiepie.LstCbDevGetName(id_kind_int, instr_id,
                                            contained_serial_no, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstCbDevGetName(id_kind_int, instr_id, contained_serial_no,
                                  str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_name_short_cb(self, instr_id, contained_serial_no,
                                 id_kind="index"):
        """Get the short name of a contained device in a combined instrument.

        Args:
            instr_id (int or str): Device list index, product ID (listed
                                   in dict PRODUCT_IDS) or serial number.
            id_kind (str): The kind of the given instr_id (listed in dict
                           ID_KINDS), defaults to device list index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.

        Returns:
            str: short device name
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of device name string
        str_len = libtiepie.LstCbDevGetNameShort(id_kind_int, instr_id,
                                                 contained_serial_no, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstCbDevGetNameShort(id_kind_int, instr_id,
                                       contained_serial_no,
                                       str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_name_shortest_cb(self, instr_id, contained_serial_no,
                                    id_kind="index"):
        """Get the shortest name of a contained device in a combined
        instrument.

        Args:
            instr_id (int or str): Device list index, product ID (listed
                                   in dict PRODUCT_IDS) or serial number.
            id_kind (str): The kind of the given instr_id (listed in dict
                           ID_KINDS), defaults to device list index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.
        Returns:
            str: shortest device name of the device
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of device name string
        str_len = libtiepie.LstCbDevGetNameShortest(id_kind_int, instr_id,
                                                    contained_serial_no,
                                                    None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstCbDevGetNameShortest(id_kind_int, instr_id,
                                          contained_serial_no, str_buffer,
                                          str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_driver_version_cb(self, instr_id, contained_serial_no,
                              id_kind="index"):
        """Get the driver version of a contained device in a combined
        instrument.

        Not tested.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.
        Returns:
            str: driver version of the device
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the driver version
        driver_version = libtiepie.LstCbDevGetDriverVersion(id_kind_int,
                                                            instr_id_int,
                                                            contained_serial_no)

        return version_to_str(driver_version)

    def get_firmware_version_cb(self, instr_id, contained_serial_no,
                             id_kind="index"):
        """Get the firmware version of a contained device in a combined
        instrument.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number.
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index.
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.

        Returns:
            str: firmware version of the device
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id
        # get the firmware version
        firmware_version = libtiepie.LstCbDevGetFirmwareVersion(id_kind_int,
                                                                instr_id_int,
                                                                contained_serial_no)

        return version_to_str(firmware_version)

    def get_calibration_date_cb(self, instr_id, contained_serial_no,
                                id_kind="index"):
        """Get the calibration date of the device.

        Args:
            instr_id (int): Device list index, product ID
                            (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id
                           (listed in dict ID_KINDS), defaults to device list
                           index
            contained_serial_no (int): Serial number of the desired device
                                       contained in the combined device.

        Returns:
            :py:class:`datetime.date`: calibration date of the device
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # Translate instr_id to int, if it is a product id str
        if id_kind == "product id":
            instr_id_int = self.PRODUCT_IDS[instr_id]
        else:
            instr_id_int = instr_id

        # get the calibration date
        raw_date = libtiepie.LstCbDevGetCalibrationDate(id_kind_int,
                                                        instr_id_int,
                                                        contained_serial_no)

        split_date = date(raw_date >> 16, (raw_date >> 8) & 0xff, raw_date & 0xff)
        return split_date


def version_to_str(raw_version):
    """Convert a raw version int in TiePie's format to a nice string.

    Args:
        raw_version (int): concatenated version numbers as int in TiePie's format

    Returns:
        str: version number as str
    """
    return '.'.join([str((raw_version >> (idx * 16)) & 0xffff) for idx in range(3, -1, -1)])


# Instantiate class to make it available via import. Thus only one instance 
# exists (singleton design pattern).
device_list = DeviceList()
