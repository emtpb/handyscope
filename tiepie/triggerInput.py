import ctypes
from tiepie.library import libtiepie


class TriggerInput:
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

    def __init__(self, dev_handle, trig_in_idx):
        self._dev_handle = dev_handle
        self._idx = trig_in_idx

    @property
    def is_available(self):
        return libtiepie.DevTrInIsAvailable(self._dev_handle, self._idx) == 1

    @property
    def _tiid(self):
        # TODO implement dict, if necessary
        return libtiepie.DevTrInGetId(self._dev_handle, self._idx)

    @property
    def name(self):
        # get length of name string
        str_len = libtiepie.DevTrInGetName(self._dev_handle, self._idx, None, 0)

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual name to the buffer
        libtiepie.DevTrInGetName(self._dev_handle, self._idx, str_buffer, str_len)

        # convert to a normal python string
        name = str_buffer.value.decode('utf-8')

        return name

    @property
    def kinds(self):
        # TODO check handling of "unknown"
        raw_kinds = libtiepie.DevTrInGetKinds(self._dev_handle, self._idx)
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
    def kind(self):
        raw_kind = libtiepie.DevTrInGetKind(self._dev_handle, self._idx)
        for key in self.TRIGGER_KINDS:
            if raw_kind == self.TRIGGER_KINDS[key]:
                return key

        raise ValueError("Unknown trigger kind: %d" % raw_kind)

    @kind.setter
    def kind(self, value):
        libtiepie.DevTrInSetKind(self._dev_handle, self._idx, self.TRIGGER_KINDS[value])

    @property
    def is_enabled(self):
        return libtiepie.DevTrInGetEnabled(self._dev_handle, self._idx) == 1

    @is_enabled.setter
    def is_enabled(self, value):
        libtiepie.DevTrInSetEnabled(self._dev_handle, self._idx, value)

    @property
    def is_triggered(self):
        return libtiepie.ScpTrInIsTriggered(self._dev_handle, self._idx) == 1
