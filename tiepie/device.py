from tiepie.library import libtiepie, CallbackObject
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
    EVENT_IDS = {'invalid': 0,
                 'object_removed': 1,
                 'osc_data_ready': 2,
                 'osc_data_overflow': 3,
                 'osc_connection_test_completed': 4,
                 'osc_triggered': 5,
                 'gen_burst_completed': 6,
                 'gen_control_label_changed': 7,
                 'osc_safe_ground_error': 9}

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

        self._obj_cb = None

    def generate_object_callback(self, event_ids, cb_funtions):
        """Generate and register callback functions for given event ids.

        Args:
            event_ids (list): Event ids for which the callback functions are given in cb_functions (see EVENT_IDS).
            cb_funtions (list): Callback functions. Length of list has to be identical with length of event_ids.
                                Each function has to have the following head: fun(p_data, value). 'p_data' is the data
                                provided by the event and 'value' a single value.

        Returns:

        """
        def default_cb(p_data, value):
            pass
        funs = {}
        for evt_id in self.EVENT_IDS.values():
            if evt_id in event_ids:
                idx = event_ids.index(evt_id)
                funs[evt_id] = cb_funtions[idx]
            else:
                funs[evt_id] = default_cb

        def object_callback(p_data, event_id, value):
            funs[event_id](p_data, value)
        self._obj_cb = CallbackObject(object_callback)
        libtiepie.ObjSetEventCallback(self._dev_handle, self._obj_cb, None)

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
    def vendor_id(self):
        """Get the vendor id of the device.

        Returns:
            int: Vendor id of the device.
        """
        return libtiepie.DevGetVendorId(self._dev_handle)

    @property
    def ipv4_address(self):
        """Get the IPv4 address of the device.

        Not tested.

        Returns:
            str: IPv4 address of the device.
        """
        return libtiepie.DevGetIPv4Address(self._dev_handle)

    @property
    def ip_port(self):
        """Get the IP Port number of the device.

        Returns:
            int: IP Port number of the device.
        """
        return libtiepie.DevGetIPPort(self._dev_handle)

    @property
    def calibration_token(self):
        """Get the calibration token of the device.

         Returns:
             str: calibration token of the device.
         """

        # get length of calibration token string
        str_len = libtiepie.DevGetCalibrationToken(self._dev_handle, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual calibration token to the buffer
        libtiepie.DevGetNameShortest(self._dev_handle, str_buffer, str_len)

        # convert to a normal python string
        token = str_buffer.value.decode('utf-8')

        return token

    @property
    def has_battery(self):
        """Check whether the device has a battery.

        Returns:
            bool: True if the device has a battery.
        """
        return libtiepie.DevHasBattery(self._dev_handle) == 1

    @property
    def battery_charge(self):
        """Get the current charge of the battery in percent.

        Returns:
            int: Battery charge in percent.
        """
        return libtiepie.DevGetBatteryCharge(self._dev_handle)

    @property
    def battery_time_to_empty(self):
        """Get the battery time until it is empty in minutes.

        Returns:
            int: Battery time in minutes.
        """
        return libtiepie.DevGetBatteryTimeToEmpty(self._dev_handle)

    @property
    def battery_time_to_full(self):
        """Get the battery time until it is fully charged in minutes .

        Returns:
            int: Battery time in minutes.
        """
        return libtiepie.DevGetBatteryTimeToFull(self._dev_handle)

    @property
    def battery_charger_connected(self):
        """Check whether the charger is connected to the device.

        Returns:
            bool: True if the charger is connected to the device.
        """
        return libtiepie.DevIsBatteryChargerConnected(self._dev_handle) == 1

    @property
    def battery_charging(self):
        """Check whether the battery is charging.

        Returns:
            bool: True if the battery is getting charged.
        """
        return libtiepie.DevIsBatteryCharging(self._dev_handle) == 1

    @property
    def battery_broken(self):
        """Check whether the device battery is broken.

        Returns:
            bool: True if the device battery is broken.
        """
        return libtiepie.DevIsBatteryBroken(self._dev_handle) == 1

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
        return libtiepie.ObjIsRemoved(self._dev_handle) == 1

    def close(self):
        """Close the device."""
        libtiepie.ObjClose(self._dev_handle)

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
    return '.'.join([str((raw_version >> (idx * 16)) & 0xffff) for idx in range(3, -1, -1)])
