from tiepie.library import libtiepie


class TriggerInput:
    @property
    def _idx(self):
        return None

    @property
    def is_available(self):
        return libtiepie.DevTrInIsAvailable()

    @property
    def _tiid(self):
        return libtiepie.DevTrInGetId()

    @property
    def name(self):
        return libtiepie.DevTrInGetName()

    @property
    def kinds(self):
        return libtiepie.DevTrInGetKinds()

    @property
    def kind(self):
        return libtiepie.DevTrInGetKind()

    @kind.setter
    def kind(self, value):
        libtiepie.DevTrInSetKind(value)

    @property
    def is_enabled(self):
        return libtiepie.DevTrInGetEnabled()

    @is_enabled.setter
    def is_enabled(self, value):
        libtiepie.DevTrInSetEnabled(value)

    def is_triggered(self):
        libtiepie.ScpTrInIsTriggered()
