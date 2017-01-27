from tiepie.library import libtiepie


class OscilloscopeChannel:
    @property
    def _idx(self):
        return None

    @property
    def connector_type(self):
        return libtiepie.ScpChGetConnectorType()

    @property
    def is_differential(self):
        return libtiepie.ScpChIsDifferential()

    @property
    def impedance(self):
        return libtiepie.ScpChGetImpedance()

    @property
    def couplings_available(self):
        return libtiepie.ScpChGetCouplings()

    @property
    def coupling(self):
        return libtiepie.ScpChGetCoupling()

    @coupling.setter
    def coupling(self, value):
        libtiepie.ScpChSetCoupling(value)

    @property
    def is_enabled(self):
        return libtiepie.ScpChGetEnabled()

    @is_enabled.setter
    def is_enabled(self, value):
        libtiepie.ScpChSetEnabled(value)

    @property
    def probe_gain(self):
        return libtiepie.ScpChGetProbeGain()

    @probe_gain.setter
    def probe_gain(self, value):
        libtiepie.ScpChSetProbeGain(value)

    @property
    def probe_offset(self):
        return libtiepie.ScpChGetProbeOffset()

    @probe_offset.setter
    def probe_offset(self, value):
        libtiepie.ScpChSetProbeOffset(value)

    @property
    def auto_range(self):
        return libtiepie.ScpChGetAutoRanging()

    @auto_range.setter
    def auto_range(self, value):
        libtiepie.ScpChSetAutoRanging(value)

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
        return libtiepie.ScpChTrGetEnabled()

    @trig_enabled.setter
    def trig_enabled(self, value):
        libtiepie.ScpChTrSetEnabled(value)

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
