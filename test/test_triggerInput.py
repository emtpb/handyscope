import pytest
import warnings
from tiepie.device import Device
from tiepie.triggerInput import TriggerInput


class TestTriggerInput:
    def setup_class(self):
        self.device = Device("HS5", "product id", "Osc")
        if len(self.device.trig_ins) is 0:
            warnings.warn("This device has no trigger outputs, thus a full test cannot be performed.")

    def test_is_available(self):
        for trig_in in self.device.trig_ins:
            assert type(trig_in.is_available) is bool

    def test_is_triggered(self):
        for trig_in in self.device.trig_ins:
            assert type(trig_in.is_triggered) is bool

    def test_is_enabled(self):
        # Test getter
        for trig_in in self.device.trig_ins:
            assert type(trig_in.is_enabled) is bool

        # Test setter by changing the value and reading it back
        for trig_in in self.device.trig_ins:
            trig_in.is_enabled = True
            assert trig_in.is_enabled is True
            trig_in.is_enabled = False
            assert trig_in.is_enabled is False

    def test_name(self):
        for trig_in in self.device.trig_ins:
            assert type(trig_in.name) is str
            assert trig_in.name in TriggerInput.TRIGGER_IDS

    def test_kinds(self):
        for trig_in in self.device.trig_ins:
            for kind in trig_in.kinds:
                assert kind in trig_in.TRIGGER_KINDS

    def test_kind(self):
        # Test getter
        for trig_in in self.device.trig_ins:
            # If there are multiple kinds available, the chosen kind can be retrieved
            if trig_in.kinds != ["unknown"]:
                assert trig_in.kind in trig_in.TRIGGER_KINDS
            # Else (no known kinds), accessing the chosen kind raises an OSError
            else:
                with pytest.raises(OSError):
                    trig_in.kind

        # Test setter by changing the value and reading it back
        for trig_in in self.device.trig_ins:
            # If there are multiple kinds available, the chosen kind can be retrieved
            if trig_in.kinds != ["unknown"]:
                # Test every available kind
                for kind in trig_in.kinds:
                    # Set the value
                    trig_in.kind = kind
                    # Read it back & compare
                    assert trig_in.kind == kind
            # Else (no known kinds), accessing the chosen kind raises an OSError
            else:
                with pytest.raises(OSError):
                    trig_in.kind = "unknown"

    def test_trigger_id(self):
        for trig_in in self.device.trig_ins:
            trig_id = trig_in.trigger_id
            assert trig_id in TriggerInput.TRIGGER_IDS
