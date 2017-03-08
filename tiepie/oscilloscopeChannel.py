from tiepie.library import libtiepie


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
    def couplings(self):
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
        return libtiepie.ScpChGetRanges()

    @property
    def range(self):
        return libtiepie.ScpChGetRange()

    @range.setter
    def range(self, value):
        libtiepie.ScpChSetRange(value)

    @property
    def trig_enabled(self):
        return libtiepie.ScpChTrGetEnabled(self._dev_handle, self._idx) == 1

    @trig_enabled.setter
    def trig_enabled(self, value):
        libtiepie.ScpChTrSetEnabled(self._dev_handle, self._idx, value)

    @property
    def trig_kinds_available(self):
        return libtiepie.ScpChTrGetKinds()

    @property
    def trig_kind(self):
        return libtiepie.ScpChTrGetKind()

    @trig_kind.setter
    def trig_kind(self, value):
        libtiepie.ScpChTrSetKind(value)

    @property
    def trig_lvl_cnt(self):
        return libtiepie.ScpChTrGetLevelCount()

    @property
    def trig_lvl(self):
        return libtiepie.ScpChTrGetLevel()

    @trig_lvl.setter
    def trig_lvl(self, value):
        libtiepie.ScpChTrSetLevel(value)

    @property
    def trig_hysteresis_cnt(self):
        return libtiepie.ScpChTrGetHysteresisCount()

    @property
    def trig_hysteresis(self):
        return libtiepie.ScpChTrGetHysteresis()

    @trig_hysteresis.setter
    def trig_hysteresis(self, value):
        libtiepie.ScpChTrSetHysteresis(value)

    @property
    def trig_conditions_available(self):
        return libtiepie.ScpChTrGetConditions()

    @property
    def trig_condition(self):
        return libtiepie.ScpChTrGetCondition()

    @trig_condition.setter
    def trig_condition(self, value):
        libtiepie.ScpChTrSetCondition(value)

    @property
    def trig_time_cnt(self):
        return libtiepie.ScpChTrGetTimeCount()

    @property
    def trig_time(self):
        return libtiepie.ScpChTrGetTime()

    @trig_time.setter
    def trig_time(self, value):
        libtiepie.ScpChTrSetTime(value)

    @property
    def trig_is_available(self):
        return libtiepie.ScpChHasTrigger()

    @trig_is_available.setter
    def trig_is_available(self, value):
        libtiepie.ScpChTrIsAvailable(value)

    @property
    def is_available(self):
        return libtiepie.ScpChIsAvailable()

    @property
    def is_connection_test_available(self):
        return libtiepie.ScpChHasConnectionTest()

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
