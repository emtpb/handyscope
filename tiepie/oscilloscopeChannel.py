from tiepie.library import libtiepie
import ctypes


class OscilloscopeChannel:
    """Class for an oscilloscope channel.

    Attributes:
        CONNECTOR_TYPES (dict): dict which maps connector types as strs to their libtiepie int version
        COUPLINGS (dict): dict which maps couplings as strs to their libtiepie int version
        TRIGGER_KINDS (dict): dict which maps trigger kinds as strs to their libtiepie int version
        TRIGGER_CONDITIONS (dict): dict which maps trigger conditions as strs to their libtiepie int version
    """
    # See also Generator.CONNECTOR_TYPES
    CONNECTOR_TYPES = {"unknown":   0,
                       "BNC":       1,
                       "Banana":    2,
                       "Powerplug": 4}

    COUPLINGS = {"unknown":  0,
                 "V DC":     1,
                 "V AC":     2,
                 "A DC":     4,
                 "A AC":     8,
                 "Ohm":     16}

    # Note: OscilloscopeChannel.TRIGGER_KINDS is the same as TriggerInput.TRIGGER_KINDS, but defined seperately here
    # for perspicuity. In the API documentation there's the additional define "TKM_NONE", which has the same value as
    # the - according to the docs also valid - define "TK_UNKNOWN". Thus it is ignored here.
    TRIGGER_KINDS = {"unknown": 0,
                     "rising": 1,
                     "falling": 2,
                     "in window": 4,
                     "out window": 8,
                     "any": 16,
                     "enter window": 32,
                     "exit window": 64,
                     "pulsewidth positive": 128,
                     "pulsewidth negative": 256}

    TRIGGER_CONDITIONS = {"unknown": 0,
                          "none":    1,
                          "smaller": 2,
                          "larger":  4}

    TRIGGER_LVL_MODES = {"unknown":  0,
                         "relative": 1,
                         "absolute": 2}

    def __init__(self, dev_handle, ch_idx):
        """Constructor for an oscilloscope channel.

        Args:
            dev_handle (int): Libtiepie device handle
            ch_idx (int): Channel index
        """
        self._dev_handle = dev_handle
        self._idx = ch_idx

    @property
    def bandwidths_available(self):
        """Get available input bandwidths in Hz.

        Returns:
            tuple: Available input bandwidths in Hz.
        """
        # Get length of list
        ranges_len = libtiepie.ScpChGetBandwidths(self._dev_handle,
                                                  self._idx, None, 0)

        # Initialize double array
        bandwidths = (ctypes.c_double * ranges_len)()

        # Write the actual data to the array
        libtiepie.ScpChGetBandwidths(self._dev_handle, self._idx,
                                     ctypes.byref(bandwidths), ranges_len)

        # Convert to a normal python list
        bandwidths = tuple(bandwidths)

        return bandwidths

    @property
    def bandwidth(self):
        """Get or set the input bandwidth."""
        return libtiepie.ScpChGetBandwidth(self._dev_handle, self._idx)

    @bandwidth.setter
    def bandwidth(self, value):
        libtiepie.ScpChSetBandwidth(self._dev_handle, self._idx, value)

    @property
    def has_safe_ground(self):
        """Check whether the channel has a safe ground.

        Returns:
            bool: True if the channel has a safe ground.
        """
        return libtiepie.ScpChHasSafeGround(self._dev_handle, self._idx) == 1

    @property
    def safe_ground_enabled(self):
        """Get or set whether the safe ground is enabled."""
        return libtiepie.ScpChGetSafeGroundEnabled(self._dev_handle,
                                                   self._idx) == 1

    @safe_ground_enabled.setter
    def safe_ground_enabled(self, value):
        libtiepie.ScpChSetSafeGroundEnabled(self._dev_handle, self._idx, value)

    @property
    def safe_ground_threshold_min(self):
        """Get the minimum safe ground threshold current."""
        return libtiepie.ScpChGetSafeGroundThresholdMin(self._dev_handle,
                                                        self._idx)

    @property
    def safe_ground_threshold_max(self):
        """Get the maximum safe ground threshold current."""
        return libtiepie.ScpChGetSafeGroundThresholdMax(self._dev_handle,
                                                        self._idx)

    @property
    def safe_ground_threshold(self):
        """Get or set the safe ground threshold current."""
        return libtiepie.ScpChGetSafeGroundThreshold(self._dev_handle,
                                                     self._idx)

    @safe_ground_threshold.setter
    def safe_ground_threshold(self, value):
        libtiepie.ScpChSetSafeGroundThreshold(self._dev_handle, self._idx,
                                              value)

    def verify_safe_ground_threshold(self, threshold):
        """Verify if a threshold can be set.

        Args:
            threshold: Threshold to verify in Ampere.

        Returns:
            float: safe ground current that will be set.
        """
        return libtiepie.ScpChVerifySafeGroundThreshold(self._dev_handle, self._idx,
                                                        threshold)

    @property
    def connector_type(self):
        """Get the connector type.

        Returns:
            str: Connector type (key of :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.CONNECTOR_TYPES`)
        """
        raw_type = libtiepie.ScpChGetConnectorType(self._dev_handle, self._idx)
        for key in self.CONNECTOR_TYPES:
            if raw_type == self.CONNECTOR_TYPES[key]:
                return key

        raise ValueError("Unknown connector type: %d" % raw_type)

    @property
    def is_differential(self):
        """Check if the channel is differential.

        Returns:
            bool: True if channel is differential, False otherwise.
        """
        return libtiepie.ScpChIsDifferential(self._dev_handle, self._idx) == 1

    @property
    def impedance(self):
        """Get the channel's input impedance.

        Returns:
            float: The channel's input impedance
        """
        return libtiepie.ScpChGetImpedance(self._dev_handle, self._idx)

    @property
    def couplings_available(self):
        """Get available couplings.

        Returns:
            tuple: Available couplings (keys of :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.COUPLINGS`)
        """
        raw_couplings = libtiepie.ScpChGetCouplings(self._dev_handle, self._idx)
        _couplings = []

        # if no couplings are available, return unknown
        if raw_couplings == self.COUPLINGS["unknown"]:
            _couplings.append("unknown")
        # else do a detailed analysis...
        else:
            # ... by iterating over every possible coupling...
            for key in self.COUPLINGS:
                # ... and ignoring "unknown" (already handled above)
                if key == "unknown":
                    pass
                elif raw_couplings & self.COUPLINGS[key] == self.COUPLINGS[key]:
                    _couplings.append(key)

        return tuple(_couplings)

    @property
    def coupling(self):
        """Get or set the current coupling (key of
        :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.COUPLINGS`)."""
        raw_coupling = libtiepie.ScpChGetCoupling(self._dev_handle, self._idx)
        for key in self.COUPLINGS:
            if raw_coupling == self.COUPLINGS[key]:
                return key

        raise ValueError("Unknown coupling: %d" % raw_coupling)

    @coupling.setter
    def coupling(self, value):
        libtiepie.ScpChSetCoupling(self._dev_handle, self._idx, self.COUPLINGS[value])

    @property
    def is_enabled(self):
        """Get or set if the channel is enabled."""
        return libtiepie.ScpChGetEnabled(self._dev_handle, self._idx) == 1

    @is_enabled.setter
    def is_enabled(self, value):
        libtiepie.ScpChSetEnabled(self._dev_handle, self._idx, value)

    @property
    def probe_gain(self):
        """Get or set the probe gain."""
        return libtiepie.ScpChGetProbeGain(self._dev_handle, self._idx)

    @probe_gain.setter
    def probe_gain(self, value):
        libtiepie.ScpChSetProbeGain(self._dev_handle, self._idx, value)

    @property
    def probe_offset(self):
        """Get or set the probe offset in V."""
        return libtiepie.ScpChGetProbeOffset(self._dev_handle, self._idx)

    @probe_offset.setter
    def probe_offset(self, value):
        libtiepie.ScpChSetProbeOffset(self._dev_handle, self._idx, value)

    @property
    def is_auto_range(self):
        """Get or set if autoranging is enabled."""
        return libtiepie.ScpChGetAutoRanging(self._dev_handle, self._idx) == 1

    @is_auto_range.setter
    def is_auto_range(self, value):
        libtiepie.ScpChSetAutoRanging(self._dev_handle, self._idx, value)

    @property
    def ranges_available(self):
        """Get available ranges in V.

        Returns:
            tuple: Available ranges in V
        """
        # Get length of list
        ranges_len = libtiepie.ScpChGetRanges(self._dev_handle, self._idx, None, 0)

        # Initialize double array
        ranges = (ctypes.c_double * ranges_len)()

        # Write the actual data to the array
        libtiepie.ScpChGetRanges(self._dev_handle, self._idx, ctypes.byref(ranges), ranges_len)

        # Convert to a normal python list
        ranges = tuple(ranges)

        return ranges

    @property
    def range(self):
        """Get or set the current range in V."""
        return libtiepie.ScpChGetRange(self._dev_handle, self._idx)

    @range.setter
    def range(self, value):
        libtiepie.ScpChSetRange(self._dev_handle, self._idx, value)

    @property
    def is_max_range_reachable(self):
        """Check whether the maximum of the range is reachable.

        Returns:
            bool: True, if the maximum of the range is reachable,
                  False otherwise.
        """
        return libtiepie.ScpChIsRangeMaxReachable(self._dev_handle, self._idx) == 1

    @property
    def is_trig_enabled(self):
        """Get or set if the channel trigger is enabled."""
        return libtiepie.ScpChTrGetEnabled(self._dev_handle, self._idx) == 1

    @is_trig_enabled.setter
    def is_trig_enabled(self, value):
        libtiepie.ScpChTrSetEnabled(self._dev_handle, self._idx, value)

    @property
    def trig_kinds_available(self):
        """Get available trigger kinds.

        Returns:
            tuple: Available trigger kinds (keys of
                   :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.TRIGGER_KINDS`)
        """
        raw_kinds = libtiepie.ScpChTrGetKinds(self._dev_handle, self._idx)
        _kinds = []

        # If no trigger kinds are available, return unknown
        if raw_kinds == self.TRIGGER_KINDS["unknown"]:
            _kinds.append("unknown")
        # Else do a detailed analysis...
        else:
            # ...by iterating over every possible kind ...
            for key in self.TRIGGER_KINDS:
                # ...and ignoring "unknown" (already handled above)
                if key == "unknown":
                    pass
                elif raw_kinds & self.TRIGGER_KINDS[key] == self.TRIGGER_KINDS[key]:
                    _kinds.append(key)

        return tuple(_kinds)

    @property
    def trig_kind(self):
        """Get or set the current trigger kind (key of
        :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.TRIGGER_KINDS`)"""
        raw_kind = libtiepie.ScpChTrGetKind(self._dev_handle, self._idx)
        for key in self.TRIGGER_KINDS:
            if raw_kind == self.TRIGGER_KINDS[key]:
                return key

        raise ValueError("Unknown trigger kind: %d" % raw_kind)

    @trig_kind.setter
    def trig_kind(self, value):
        libtiepie.ScpChTrSetKind(self._dev_handle, self._idx, self.TRIGGER_KINDS[value])

    @property
    def trig_lvl_cnt(self):
        """Get the count of trigger levels.

        Returns:
            int: Count of trigger levels.
        """
        return libtiepie.ScpChTrGetLevelCount(self._dev_handle, self._idx)

    @property
    def trig_lvl(self):
        """Get or set the trigger levels.

        Value range depends on
        :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.trig_lvl_mode`.
        """
        _lvls = []
        for idx in range(self.trig_lvl_cnt):
            _lvls.append(libtiepie.ScpChTrGetLevel(self._dev_handle, self._idx, idx))
        return tuple(_lvls)

    @trig_lvl.setter
    def trig_lvl(self, iterable):
        for idx, value in enumerate(iterable):
            libtiepie.ScpChTrSetLevel(self._dev_handle, self._idx, idx, value)

    @property
    def trig_lvl_modes_available(self):
        """Get the available trigger level modes.

        Returns:
            tuple: Available trigger level modes (keys of
                   :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.TRIGGER_LVL_MODES`)
        """
        raw_modes = libtiepie.ScpChTrGetLevelModes(self._dev_handle, self._idx)
        _modes = []

        # If no trigger level modes are available, return unknown
        if raw_modes == self.TRIGGER_LVL_MODES["unknown"]:
            _modes.append("unknown")
        # Else do a detailed analysis...
        else:
            # ...by iterating over every possible kind ...
            for key in self.TRIGGER_LVL_MODES:
                # ...and ignoring "unknown" (already handled above)
                if key == "unknown":
                    pass
                elif raw_modes & self.TRIGGER_LVL_MODES[key] == self.TRIGGER_LVL_MODES[key]:
                    _modes.append(key)

        return tuple(_modes)

    @property
    def trig_lvl_mode(self):
        """Get or set the current trigger level mode.

        Possible trigger level modes are the keys of
        :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.TRIGGER_LVL_MODES`.
        """
        raw_mode = libtiepie.ScpChTrGetLevelMode(self._dev_handle, self._idx)
        for key, value in self.TRIGGER_LVL_MODES.items():
            if raw_mode == value:
                return key

        raise ValueError("Unknown trigger level mode: %d" % raw_mode)

    @trig_lvl_mode.setter
    def trig_lvl_mode(self, value):
        libtiepie.ScpChTrSetLevelMode(self._dev_handle, self._idx, self.TRIGGER_LVL_MODES[value])

    @property
    def trig_hysteresis_cnt(self):
        """Get the count of trigger hysteresises.

        Returns:
            int: Count of trigger hysteresises
        """
        return libtiepie.ScpChTrGetHysteresisCount(self._dev_handle, self._idx)

    @property
    def trig_hysteresis(self):
        """Get or set the trigger hysteresis."""
        _hyst = []
        for idx in range(self.trig_hysteresis_cnt):
            _hyst.append(libtiepie.ScpChTrGetHysteresis(self._dev_handle, self._idx, idx))

        return tuple(_hyst)

    @trig_hysteresis.setter
    def trig_hysteresis(self, iterable):
        for idx, value in enumerate(iterable):
            libtiepie.ScpChTrSetHysteresis(self._dev_handle, self._idx, idx, value)

    @property
    def trig_conditions_available(self):
        """Get the available trigger conditions.

        Returns:
            tuple: Available trigger conditions (keys of
                   :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.TRIGGER_CONDITIONS`)
        """
        raw_conds = libtiepie.ScpChTrGetConditions(self._dev_handle, self._idx)
        _conds = []

        # If no trigger conditions are available, return unknown
        if raw_conds == self.TRIGGER_CONDITIONS["unknown"]:
            _conds.append("unknown")
        # Else do a detailed analysis...
        else:
            # ...by iterating over every possible kind ...
            for key in self.TRIGGER_CONDITIONS:
                # ...and ignoring "unknown" (already handled above)
                if key == "unknown":
                    pass
                elif raw_conds & self.TRIGGER_CONDITIONS[key] == self.TRIGGER_CONDITIONS[key]:
                    _conds.append(key)

        return tuple(_conds)

    @property
    def trig_condition(self):
        """Get or set the current trigger condition (key of
        :py:attr:`tiepie.oscilloscopeChannel.OscilloscopeChannel.TRIGGER_CONDITIONS`)"""
        raw_cond = libtiepie.ScpChTrGetCondition(self._dev_handle, self._idx)
        for key, value in self.TRIGGER_CONDITIONS.items():
            if raw_cond == value:
                return key

        raise ValueError("Unknown trigger condition: %d" % raw_cond)

    @trig_condition.setter
    def trig_condition(self, value):
        libtiepie.ScpChTrSetCondition(self._dev_handle, self._idx, self.TRIGGER_CONDITIONS[value])

    @property
    def trig_time_cnt(self):
        """Get the count of trigger times.

        Returns:
            int: Count of trigger times
        """
        return libtiepie.ScpChTrGetTimeCount(self._dev_handle, self._idx)

    @property
    def trig_time(self):
        """Get or set the trigger times."""
        times = []

        for idx in range(self.trig_time_cnt):
            times.append(libtiepie.ScpChTrGetTime(self._dev_handle, self._idx, idx))

        return tuple(times)

    @trig_time.setter
    def trig_time(self, iterable):
        for idx, value in enumerate(iterable):
            libtiepie.ScpChTrSetTime(self._dev_handle, self._idx, idx, value)

    def verify_trig_time(self, trigger_times):
        """Verify if the desired trigger times can be set.

        Returns:
            tuple: Trigger times which have been set by the device.
        """
        set_trigger_times = []
        for idx, value in enumerate(trigger_times):
            trigger_time = libtiepie.ScpChTrVerifyTime(self._dev_handle,
                                                       self._idx, idx, value)
            set_trigger_times.append(trigger_time)
        return set_trigger_times

    @property
    def is_trig_available(self):
        """Check if trigger is available.

        Returns:
            bool: True if trigger is available, False otherwise.
        """
        # TODO Check if both function calls are necessary. To be on the safe side, currently both are called.
        # Check if trigger support is given under the currently selected measure mode
        measure_mode_ok = libtiepie.ScpChHasTrigger(self._dev_handle, self._idx) == 1
        # Check if trigger is available with current settings
        settings_ok = libtiepie.ScpChTrIsAvailable(self._dev_handle, self._idx) == 1

        return measure_mode_ok & settings_ok

    @property
    def is_triggered(self):
        """Check if the channel has been triggered.

        Returns:
            bool: True, if the channel has been triggered, False otherwise.
        """
        return libtiepie.ScpChTrIsTriggered(self._dev_handle, self._idx) == 1

    @property
    def is_available(self):
        """Check if channel is available.

        Returns:
            bool: True if channel is available, False otherwise.
        """
        return libtiepie.ScpChIsAvailable(self._dev_handle, self._idx) == 1

    @property
    def is_connection_test_available(self):
        """Check if connection test is available.

        Returns:
            bool: True if connection test is available, False otherwise.
        """
        return libtiepie.ScpChHasConnectionTest(self._dev_handle, self._idx) == 1

    @property
    def data_range(self):
        """Get the minimum and maximum values of the input range of the measured data.

        Returns:
            tuple: Minimum and maximum values of the input range as float
        """
        # Init floats
        range_min = ctypes.c_double()
        range_max = ctypes.c_double()

        # Get data
        libtiepie.ScpChGetDataValueRange(self._dev_handle, self._idx, ctypes.byref(range_min), ctypes.byref(range_max))

        # Get values and return them
        return range_min.value, range_max.value

    @property
    def data_range_min(self):
        """Get the minimum value of the input range of the measured data.

        Returns:
            float: Minimum value of the input range
        """
        return libtiepie.ScpChGetDataValueMin(self._dev_handle, self._idx)

    @property
    def data_range_max(self):
        """Get the maximum value of the input range of the measured data.

        Returns:
            float: Maximum value of the input range
        """
        return libtiepie.ScpChGetDataValueMax(self._dev_handle, self._idx)
