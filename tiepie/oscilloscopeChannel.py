from tiepie.library import libtiepie
import ctypes


class OscilloscopeChannel:
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

    def __init__(self, dev_handle, ch_idx):
        self._dev_handle = dev_handle
        self._idx = ch_idx

    @property
    def connector_type(self):
        raw_type = libtiepie.ScpChGetConnectorType(self._dev_handle, self._idx)
        for key in self.CONNECTOR_TYPES:
            if raw_type == self.CONNECTOR_TYPES[key]:
                return key

        raise ValueError("Unknown connector type: %d" % raw_type)

    @property
    def is_differential(self):
        return libtiepie.ScpChIsDifferential(self._dev_handle, self._idx) == 1

    @property
    def impedance(self):
        return libtiepie.ScpChGetImpedance(self._dev_handle, self._idx)

    @property
    def couplings_available(self):
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

        return _couplings

    @property
    def coupling(self):
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
        return libtiepie.ScpChGetEnabled(self._dev_handle, self._idx) == 1

    @is_enabled.setter
    def is_enabled(self, value):
        libtiepie.ScpChSetEnabled(self._dev_handle, self._idx, value)

    @property
    def probe_gain(self):
        return libtiepie.ScpChGetProbeGain(self._dev_handle, self._idx)

    @probe_gain.setter
    def probe_gain(self, value):
        libtiepie.ScpChSetProbeGain(self._dev_handle, self._idx, value)

    @property
    def probe_offset(self):
        return libtiepie.ScpChGetProbeOffset(self._dev_handle, self._idx)

    @probe_offset.setter
    def probe_offset(self, value):
        libtiepie.ScpChSetProbeOffset(self._dev_handle, self._idx, value)

    @property
    def is_auto_range(self):
        return libtiepie.ScpChGetAutoRanging(self._dev_handle, self._idx) == 1

    @is_auto_range.setter
    def is_auto_range(self, value):
        libtiepie.ScpChSetAutoRanging(self._dev_handle, self._idx, value)

    @property
    def ranges_available(self):
        # Get length of list
        ranges_len = libtiepie.ScpChGetRanges(self._dev_handle, self._idx, None, 0)

        # Initialize double array
        ranges = (ctypes.c_double * ranges_len)()

        # Write the actual data to the array
        libtiepie.ScpChGetRanges(self._dev_handle, self._idx, ctypes.byref(ranges), ranges_len)

        # Convert to a normal python list
        ranges = list(ranges)

        return ranges

    @property
    def range(self):
        return libtiepie.ScpChGetRange(self._dev_handle, self._idx)

    @range.setter
    def range(self, value):
        libtiepie.ScpChSetRange(self._dev_handle, self._idx, value)

    @property
    def trig_enabled(self):
        return libtiepie.ScpChTrGetEnabled(self._dev_handle, self._idx) == 1

    @trig_enabled.setter
    def trig_enabled(self, value):
        libtiepie.ScpChTrSetEnabled(self._dev_handle, self._idx, value)

    @property
    def trig_kinds_available(self):
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

        return _kinds

    @property
    def trig_kind(self):
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
        return libtiepie.ScpChTrGetLevelCount(self._dev_handle, self._idx)

    @property
    def trig_lvl(self):
        _lvls = []
        for idx in range(self.trig_lvl_cnt):
            _lvls.append(libtiepie.ScpChTrGetLevel(self._dev_handle, self._idx, idx))
        return _lvls

    @trig_lvl.setter
    def trig_lvl(self, value_list):
        for idx in range(len(value_list)):
            libtiepie.ScpChTrSetLevel(self._dev_handle, self._idx, idx, value_list[idx])

    @property
    def trig_hysteresis_cnt(self):
        return libtiepie.ScpChTrGetHysteresisCount(self._dev_handle, self._idx)

    @property
    def trig_hysteresis(self):
        _hyst = []
        for idx in range(self.trig_hysteresis_cnt):
            _hyst.append(libtiepie.ScpChTrGetHysteresis(self._dev_handle, self._idx, idx))

        return _hyst

    @trig_hysteresis.setter
    def trig_hysteresis(self, value_list):
        for idx in range(self.trig_hysteresis_cnt):
            libtiepie.ScpChTrSetHysteresis(self._dev_handle, self._idx, idx, value_list[idx])

    @property
    def trig_conditions_available(self):
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

        return _conds

    @property
    def trig_condition(self):
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
        return libtiepie.ScpChTrGetTimeCount(self._dev_handle, self._idx)

    @property
    def trig_time(self):
        times = []

        for idx in range(self.trig_time_cnt):
            times.append(libtiepie.ScpChTrGetTime(self._dev_handle, self._idx, idx))

        return times

    @trig_time.setter
    def trig_time(self, value_list):
        for idx in range(self.trig_time_cnt):
            libtiepie.ScpChTrSetTime(self._dev_handle, self._idx, idx, value_list[idx])

    @property
    def trig_is_available(self):
        # TODO Check if both function calls are necessary. To be on the safe side, currently both are called.
        # Check if trigger support is given under the currently selected measure mode
        measure_mode_ok = libtiepie.ScpChHasTrigger(self._dev_handle, self._idx) == 1
        # Check if trigger is available with current settings
        settings_ok = libtiepie.ScpChTrIsAvailable(self._dev_handle, self._idx) == 1

        return measure_mode_ok & settings_ok

    @property
    def is_available(self):
        return libtiepie.ScpChIsAvailable(self._dev_handle, self._idx) == 1

    @property
    def is_connection_test_available(self):
        return libtiepie.ScpChHasConnectionTest(self._dev_handle, self._idx) == 1

    @property
    def data_range(self):
        # Init floats
        range_min = ctypes.c_double()
        range_max = ctypes.c_double()

        # Get data
        libtiepie.ScpChGetDataValueRange(self._dev_handle, self._idx, ctypes.byref(range_min), ctypes.byref(range_max))

        # Get values and return them
        return range_min.value, range_max.value

    @property
    def data_range_min(self):
        return libtiepie.ScpChGetDataValueMin(self._dev_handle, self._idx)

    @property
    def data_range_max(self):
        return libtiepie.ScpChGetDataValueMax(self._dev_handle, self._idx)
