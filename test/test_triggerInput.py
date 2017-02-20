import pytest


class TestTriggerInput:
    def setup_class(self):
        from tiepie.device import Device
        self.device = Device("HS5", "product id", "Osc")

    def test_is_available(self):
        for trig_in in self.device.trig_ins:
            assert isinstance(trig_in.is_available, bool)

    def test_is_triggered(self):
        for trig_in in self.device.trig_ins:
            assert isinstance(trig_in.is_triggered, bool)

    def test_is_enabled(self):
        # Test getter
        for trig_in in self.device.trig_ins:
            assert isinstance(trig_in.is_enabled, bool)

        # Test setter by changing the value and reading it back
        for trig_in in self.device.trig_ins:
            trig_in.is_enabled = True
            assert trig_in.is_enabled is True
            trig_in.is_enabled = False
            assert trig_in.is_enabled is False

    def test_name(self):
        known_names = ["EXT 1", "EXT 2", "EXT 3", "Generator start", "Generator stop", "Generator new period"]

        for trig_in in self.device.trig_ins:
            assert isinstance(trig_in.name, str)
            assert trig_in.name in known_names

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
