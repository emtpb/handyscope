from tiepie.library import libtiepie
from tiepie.deviceList import device_list
from tiepie.triggerInput import TriggerInput
from tiepie.triggerOutput import TriggerOutput
from datetime import date
import ctypes


class Device:
    """Base class for devices.

    This class contains methods common to all devices of an instrument, like name and serial number. A device is e.g. an
    oscilloscope or a generator, whereas an instrument is e.g. the whole 'HS5'.
    """

    def __init__(self, instr_id, id_kind, device_type):
        """Constructor for class Device.

        Args:
            instr_id (int or str): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS)
            device_type (str): the type of the device (listed in dict DEVICE_TYPES)
        """
        self._dev_handle = device_list.open_device(instr_id, id_kind, device_type)

        self._trig_ins = []
        for idx in range(self.trig_in_cnt):
            self._trig_ins.append(TriggerInput(self._dev_handle, idx))

        self._trig_outs = []
        for idx in range(self.trig_out_cnt):
            self._trig_outs.append(TriggerOutput(self._dev_handle, idx))

    @property
    def driver_ver(self):
        """Get the driver version in the format Major.Minor.Release.Build

        Returns:
            str: driver version in the format Major.Minor.Release.Build
        """
        raw_version = libtiepie.DevGetDriverVersion(self._dev_handle)
        return version_to_str(raw_version)

    @property
    def firmware_ver(self):
        """Get the firmware version in the format Major.Minor.Release.Build

        Returns:
            str: firmware version in the format Major.Minor.Release.Build
        """
        raw_version = libtiepie.DevGetFirmwareVersion(self._dev_handle)
        return version_to_str(raw_version)

    @property
    def calibration_date(self):
        """Get the calibration date

        Returns:
            :py:class:`datetime.date`: calibration date
        """
        raw_date = libtiepie.DevGetCalibrationDate(self._dev_handle)
        split_date = date(raw_date >> 16, (raw_date >> 8) & 0xff, raw_date & 0xff)
        return split_date

    @property
    def serial_no(self):
        """Get the serial number

        Returns:
            int: serial number
        """
        return libtiepie.DevGetSerialNumber(self._dev_handle)

    @property
    def product_id(self):
        """Get the product id as human readable string (key of :py:attr:`tiepie.deviceList.DeviceList.PRODUCT_IDS`)

        Returns:
            str: product id
        """
        id_int = libtiepie.DevGetProductId(self._dev_handle)

        # Lookup id in the dict
        for key in device_list.PRODUCT_IDS:
            if device_list.PRODUCT_IDS[key] == id_int:
                # Return human readable string, i.e. the key name
                return key

        # If code hasn't returned yet, product id wasn't found
        raise ValueError("Unknown product id: %s" % id_int)

    @property
    def device_type(self):
        """Get the device type as human readable string (key of :py:attr:`tiepie.deviceList.DeviceList.DEVICE_TYPES`)

        Returns:
            str: device type
        """
        type_int = libtiepie.DevGetType(self._dev_handle)

        # Lookup type in the dict
        for key in device_list.DEVICE_TYPES:
            if device_list.DEVICE_TYPES[key] == type_int:
                # Return human readable string, i.e. the key name
                return key

        # If code hasn't returned yet, device type wasn't found
        raise ValueError("Unknown device type: %s" % type_int)

    @property
    def long_name(self):
        """Get the long name of the device.

        Returns:
            str: long device name (e.g. "Handyscope HS5-530XMS")
        """
        # get length of device name string
        str_len = libtiepie.DevGetName(self._dev_handle, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.DevGetName(self._dev_handle, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    @property
    def name(self):
        """Get the name of the device.

        Returns:
            str: device name (e.g. "HS5-530XMS")
        """
        # get length of device name string
        str_len = libtiepie.DevGetNameShort(self._dev_handle, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.DevGetNameShort(self._dev_handle, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    @property
    def short_name(self):
        """Get the short name of the device.

        Returns:
            str: short device name (e.g. "HS5")
        """
        # get length of device name string
        str_len = libtiepie.DevGetNameShortest(self._dev_handle, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual device name to the buffer
        libtiepie.DevGetNameShortest(self._dev_handle, str_buffer, str_len)

        # convert to a normal python string
        dev_name = str_buffer.value.decode('utf-8')

        return dev_name

    @property
    def is_removed(self):
        """Check if device is removed.

        Returns:
            bool: True if removed, False otherwise.
        """
        return libtiepie.DevIsRemoved(self._dev_handle) == 1

    def dev_close(self):
        """Close the device.
        """
        libtiepie.DevClose(self._dev_handle)

    @property
    def trig_ins(self):
        """List of all trigger inputs.

        Returns:
            list: list of :py:class:`tiepie.triggerInput.TriggerInput`
        """
        return self._trig_ins

    @property
    def trig_in_cnt(self):
        """Count of available trigger inputs.

        Returns:
            int: count of trigger inputs
        """
        try:
            return libtiepie.DevTrGetInputCount(self._dev_handle)
        except OSError as err:
            # DevTrGetInputCount raises NOT_SUPPORTED OSError, if the device has no trigger inputs
            if str(err) == "[-2]: NOT_SUPPORTED":
                return 0
            else:
                # Something other than "not supported" happened -> rethrow error
                raise err

    def trig_in_by_id(self, trig_in_id):
        id_int = TriggerInput.TRIGGER_IDS[trig_in_id]
        return libtiepie.DevTrGetInputIndexById(self._dev_handle, id_int)

    @property
    def trig_outs(self):
        """List of available trigger outputs.

        Returns:
            list: list of :py:class:`tiepie.triggerOutput.TriggerOutput`
        """
        return self._trig_outs

    @property
    def trig_out_cnt(self):
        """Count of available trigger outputs.

        Returns:
            int: count of trigger outputs
        """
        try:
            return libtiepie.DevTrGetOutputCount(self._dev_handle)
        except OSError as err:
            # DevTrGetOutputCount raises NOT_SUPPORTED OSError, if the device has no trigger outputs
            if str(err) == "[-2]: NOT_SUPPORTED":
                return 0
            else:
                # Something other than "not supported" happened -> rethrow error
                raise err

    def trig_out_by_id(self, trig_out_id):
        """Get trigger output index by its ID.

        Args:
            trig_out_id (str): ID of the trigger output as in :py:attr:`tiepie.triggerOutput.TriggerOutput.TRIGGER_IDS`

        Returns:
            int: index of the requested trigger output
        """
        id_int = TriggerOutput.TRIGGER_IDS[trig_out_id]
        return libtiepie.DevTrGetOutputIndexById(self._dev_handle, id_int)


def version_to_str(raw_version):
    """Convert a raw version int in TiePie's format to a nice string.

    Args:
        raw_version (int): concatenated version numbers as int in TiePie's format

    Returns:
        str: version number as str
    """
    return '.'.join([str((raw_version >> (idx * 16)) & 0xffff) for idx in range(3,-1,-1)])
