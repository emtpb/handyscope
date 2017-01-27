from tiepie.library import libtiepie


class TriggerOutput:
    @property
    def _idx(self):
        return None

    @property
    def is_enabled(self):
        return libtiepie.DevTrOutGetEnabled()

    @is_enabled.setter
    def is_enabled(self, value):
        libtiepie.DevTrOutSetEnabled(value)

    @property
    def _toid(self):
        return libtiepie.DevTrOutGetId()

    @property
    def name(self):
        return libtiepie.DevTrOutGetName()
