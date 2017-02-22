from tiepie.triggerOutput import TriggerOutput
from tiepie.device import Device
import warnings


class TestTriggerOutput:
    def setup_class(self):
        self.device = Device("HS5", "product id", "Gen")
        if len(self.device.trig_outs) is 0:
            warnings.warn("This device has no trigger outputs, thus a full test cannot be performed.")

    def test_is_enabled(self):
        # test getter
        for trig_out in self.device.trig_outs:
            assert type(trig_out.is_enabled) is bool

        # test setter by changing the value and reading it back
        for trig_out in self.device.trig_outs:
            trig_out.is_enabled = True
            assert trig_out.is_enabled is True
            trig_out.is_enabled = False
            assert trig_out.is_enabled is False

    def test_trigger_id(self):
        for trig_out in self.device.trig_outs:
            assert trig_out.trigger_id in TriggerOutput.TRIGGER_IDS

    def test_name(self):
        for trig_out in self.device.trig_outs:
            # Names correspond to keys in TRIGGER_IDS
            assert trig_out.name in TriggerOutput.TRIGGER_IDS

    def test_events(self):
        for trig_out in self.device.trig_outs:
            for event in trig_out.events:
                assert event in TriggerOutput.TRIGGER_EVENTS

    def test_event(self):
        for trig_out in self.device.trig_outs:
            # test getter
            assert trig_out.event in TriggerOutput.TRIGGER_EVENTS

            # test setter by changing a value and reading it back
            # possible values are accessible via property events
            for event in trig_out.events:
                trig_out.event = event
                assert trig_out.event is event
