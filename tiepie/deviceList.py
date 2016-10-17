from tiepie.library import libtiepie
import ctypes


class DeviceList:
    """This class provides access to the device list maintained by libtiepie.

    Attributes:
        ID_KINDS (dict): dict which maps readable representations of id kinds to their int version
        PRODUCT_IDS (dict): dict which maps readable representations of product ids to their int version
        DEVICE_TYPES (dict): dict which maps readable representations of device types to their int version
        libInst (:py:class:`.library.Library`): instance of Library to access libtiepie
    """

    ID_KINDS = {"product id": 0,
                "index": 2,
                "serial number": 4}

    PRODUCT_IDS = {"none": 0,
                   "combined": 2,
                   "HS4": 15,
                   "HP3": 18,
                   "HS4D": 20,
                   "HS5": 22}

    DEVICE_TYPES = {"Osc": 1,
                    "Gen": 2,
                    "I2C": 4}

    def __init__(self):
        # Fill the device list
        libtiepie.LstUpdate()

    @property
    def device_count(self):
        """Get device count

        Returns:
            int: device count
        """
        return libtiepie.LstGetCount()

    def get_device_name(self, id, id_kind=ID_KINDS["index"]):
        """Get the full name of the device.

        Args:
            id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (int): the kind of the given id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            str: full device name
        """
        # get length of device name string
        str_len = libtiepie.LstDevGetName(id_kind, id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstDevGetName(id_kind, id, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_name_short(self, id, id_kind=ID_KINDS["index"]):
        """Get the short name of the device.

        Args:
            id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (int): the kind of the given id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            str: short device name
        """
        # get length of device name string
        str_len = libtiepie.LstDevGetNameShort(id_kind, id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstDevGetNameShort(id_kind, id, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_name_shortest(self, id, id_kind=ID_KINDS["index"]):
        """Get the shortest name of the device.

        Args:
            id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (int): the kind of the given id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            str: shortest device name
        """
        # get length of device name string
        str_len = libtiepie.LstDevGetNameShortest(id_kind, id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstDevGetNameShortest(id_kind, id, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_serial_no(self, id, id_kind=ID_KINDS["index"]):
        """Get the serial number of the device.

        Args:
            id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (int): the kind of the given id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            int: serial number
        """
        # get the serial number
        serial_no = libtiepie.LstDevGetSerialNumber(id_kind, id)

        return serial_no

    def get_device_types(self, id, id_kind=ID_KINDS["index"]):
        """Get the the device types of an instrument.

        Args:
            id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (int): the kind of the given id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            dict: key: type (as listed in DEVICE_TYPES), value: True/False
        """
        # get the device types
        dev_types = libtiepie.LstDevGetTypes(id_kind, id)

        # check for every possible type and store in dict
        type_dict = {"Osc": False,
                     "Gen": False,
                     "I2C": False}
        for key in self.DEVICE_TYPES:
            if dev_types & self.DEVICE_TYPES[key]:
                type_dict[key] = True

        return type_dict

    def __str__(self):
        """Return a (more or less) human-readable representation of the instruments in the device list.

        Returns:
            str: Instruments in the device list
        """
        dev_list = ""
        for idx in range(self.device_count):
            dev_list += "%d:\t%s\t%d\t%s\n" % (idx, self.get_device_name_short(idx), self.get_device_serial_no(idx),
                                               str(self.get_device_types(idx)))

        return dev_list
