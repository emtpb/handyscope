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

    # See api doc, macro "TRIGGER_IO_ID"
    TRIGGER_IDS = {"EXT 1":                 0 << 24 | 3 << 20 | 1 << 8 | 0,
                   "EXT 2":                 0 << 24 | 3 << 20 | 2 << 8 | 0,
                   "EXT 3":                 0 << 24 | 3 << 20 | 3 << 8 | 0,
                   "Generator start":       0 << 24 | 2 << 20 | 0 << 8 | 0,
                   "Generator stop":        0 << 24 | 2 << 20 | 0 << 8 | 1,
                   "Generator new period":  0 << 24 | 2 << 20 | 0 << 8 | 2}

    def __init__(self, dev_handle, trig_in_idx):
        self._dev_handle = dev_handle
        self._idx = trig_in_idx

    @property
    def is_available(self):
        return libtiepie.DevTrInIsAvailable(self._dev_handle, self._idx) == 1

    @property
    def trigger_id(self):
        raw_id = libtiepie.DevTrInGetId(self._dev_handle, self._idx)
        for key in self.TRIGGER_IDS:
            if self.TRIGGER_IDS[key] == raw_id:
                return key

        raise ValueError("Unknown trigger input id %d" % raw_id)

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
    def kinds_available(self):
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
        """Check if the oscilloscope trigger input caused a trigger.

        Only valid for oscilloscope trigger inputs, otherwise always False is returned.

        Returns:
            bool: True if trigger input belongs to an oscilloscope and is triggered, false otherwise.
        """
        try:
            result = libtiepie.ScpTrInIsTriggered(self._dev_handle, self._idx) == 1
        except IOError as err:
            if str(err) == "[-3]: INVALID_HANDLE":
                result = False
            else:
                raise

        return result
