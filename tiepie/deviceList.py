from tiepie.library import libtiepie
import ctypes


class DeviceList:
    """This class provides access to the device list maintained by libtiepie.

    Attributes:
        ID_KINDS (dict): dict which maps readable representations of id kinds to their int version
        PRODUCT_IDS (dict): dict which maps readable representations of product ids to their int version
        DEVICE_TYPES (dict): dict which maps readable representations of device types to their int version
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

    def get_device_name(self, instr_id, id_kind="index"):
        """Get the full name of the device.

        Args:
            instr_id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS), defaults to device list index

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
            instr_id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS), defaults to device list index

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
        libtiepie.LstDevGetNameShort(id_kind_int, instr_id, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_name_shortest(self, instr_id, id_kind="index"):
        """Get the shortest name of the device.

        Args:
            instr_id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            str: shortest device name
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get length of device name string
        str_len = libtiepie.LstDevGetNameShortest(id_kind_int, instr_id, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.LstDevGetNameShortest(id_kind_int, instr_id, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    def get_device_serial_no(self, instr_id, id_kind="index"):
        """Get the serial number of the device.

        Args:
            instr_id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            int: serial number
        """
        # translate id kind str to int
        id_kind_int = self.ID_KINDS[id_kind]

        # get the serial number
        serial_no = libtiepie.LstDevGetSerialNumber(id_kind_int, instr_id)

        return serial_no

    def get_device_types(self, instr_id, id_kind="index"):
        """Get the the device types of an instrument.

        Args:
            instr_id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given id (listed in dict ID_KINDS), defaults to device list index

        Returns:
            dict: key: type (as listed in DEVICE_TYPES), value: True/False
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

    def _open_device(self, instr_id, id_kind="index", device_type="Osc"):
        """Open a device (of device_type) of an instrument (with given id) and return the device handle.

        Args:
            instr_id (int): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS), defaults to device list index
            device_type (str): the type of the device (listed in dict DEVICE_TYPES), defaults to oscilloscope

        Returns:
            handle (:py:class:`ctypes.c_uint32`): device handle
        """
        # translate id kind & device type str to int
        id_kind_int = self.ID_KINDS[id_kind]
        device_type_int = self.DEVICE_TYPES[device_type]

        return libtiepie.LstOpenDevice(id_kind_int, instr_id, device_type_int)
