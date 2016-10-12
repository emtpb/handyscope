from tiepie.library import Library
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

    DEVICE_TYPES = {"oscilloscope": 1,
                    "generator": 2,
                    "i2chost": 4}

    def __init__(self):
        self.libInst = Library()

        # Fill the device list
        self.libInst.libtiepie.LstUpdate()

    @property
    def device_count(self):
        """Get device count

        Returns:
            int: device count
        """
        return self.libInst.libtiepie.LstGetCount()

    def get_device_name(self, id, id_kind=ID_KINDS["index"]):
        """Get the full name of the device.

        Args:
            id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (int): the kind of the given id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            str: full device name
        """
        # get length of device name string
        str_len = self.libInst.libtiepie.LstDevGetName(id_kind, id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        self.libInst.libtiepie.LstDevGetName(id_kind, id, str_buffer, str_len)

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
        str_len = self.libInst.libtiepie.LstDevGetNameShort(id_kind, id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        self.libInst.libtiepie.LstDevGetNameShort(id_kind, id, str_buffer, str_len)

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
        str_len = self.libInst.libtiepie.LstDevGetNameShortest(id_kind, id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        self.libInst.libtiepie.LstDevGetNameShortest(id_kind, id, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name
