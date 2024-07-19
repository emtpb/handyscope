from handyscope.library import libtiepie
import ctypes


class TriggerOutput:

    __slots__ = ("_dev_handle", "_idx")

    TRIGGER_EVENTS = {
        "unknown": 0,
        "Generator start": 1,
        "Generator stop": 2,
        "Generator new period": 4,
        "Oscilloscope running": 8,
        "Oscilloscope triggered": 16,
        "manual": 32,
    }

    # see api doc, macro "TRIGGER_IO_ID"
    TRIGGER_IDS = {
        "EXT 1": 0 << 24 | 3 << 20 | 1 << 8 | 0,
        "EXT 2": 0 << 24 | 3 << 20 | 2 << 8 | 0,
        "EXT 3": 0 << 24 | 3 << 20 | 3 << 8 | 0,
    }

    def __init__(self, dev_handle, trig_out_idx):
        self._dev_handle = dev_handle
        self._idx = trig_out_idx

    @property
    def is_enabled(self):
        return libtiepie.DevTrOutGetEnabled(self._dev_handle, self._idx) == 1

    @is_enabled.setter
    def is_enabled(self, value):
        libtiepie.DevTrOutSetEnabled(self._dev_handle, self._idx, value)

    @property
    def trigger_id(self):
        raw_id = libtiepie.DevTrOutGetId(self._dev_handle, self._idx)
        for key in self.TRIGGER_IDS:
            if self.TRIGGER_IDS[key] == raw_id:
                return key

        raise ValueError("Unknown trigger output id %d" % raw_id)

    @property
    def name(self):
        # get length of name string
        str_len = libtiepie.DevTrOutGetName(
            self._dev_handle, self._idx, None, 0
        )

        # initialize mutable string buffer
        str_buffer = ctypes.create_string_buffer(str_len)

        # write the actual name to the buffer
        libtiepie.DevTrOutGetName(
            self._dev_handle, self._idx, str_buffer, str_len
        )

        # convert to a normal python string
        name = str_buffer.value.decode("utf-8")

        return name

    @property
    def events_available(self):
        raw_events = libtiepie.DevTrOutGetEvents(self._dev_handle, self._idx)
        _events = []

        # if no trigger evvents are available, return unknown
        if raw_events == self.TRIGGER_EVENTS["unknown"]:
            _events.append("unknown")
        # else do a detailed analysis...
        else:
            # ... by iterating over every possible kind...
            for key in self.TRIGGER_EVENTS:
                # ... and ignoring "unknown" (already handled above)
                if key == "unknown":
                    pass
                elif raw_events & self.TRIGGER_EVENTS[key] == self.TRIGGER_EVENTS[key]:
                    _events.append(key)

        return _events

    @property
    def event(self):
        raw_event = libtiepie.DevTrOutGetEvent(self._dev_handle, self._idx)
        for key in self.TRIGGER_EVENTS:
            if raw_event == self.TRIGGER_EVENTS[key]:
                return key

        raise ValueError("Unknown trigger output event: %d" % raw_event)

    @event.setter
    def event(self, value):
        libtiepie.DevTrOutSetEvent(
            self._dev_handle, self._idx, self.TRIGGER_EVENTS[value]
        )

    def force_trig(self):
        return libtiepie.DevTrOutTrigger(self._dev_handle, self._idx) == 1
