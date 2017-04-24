import pytest
from tiepie.triggerOutput import TriggerOutput


def test_is_enabled(device):
    # test getter
    for trig_out in device.trig_outs:
        assert type(trig_out.is_enabled) is bool

    # test setter by changing the value and reading it back
    for trig_out in device.trig_outs:
        trig_out.is_enabled = True
        assert trig_out.is_enabled is True
        trig_out.is_enabled = False
        assert trig_out.is_enabled is False


def test_trigger_id(device):
    for trig_out in device.trig_outs:
        assert trig_out.trigger_id in TriggerOutput.TRIGGER_IDS


def test_name(device):
    for trig_out in device.trig_outs:
        # Names correspond to keys in TRIGGER_IDS
        assert trig_out.name in TriggerOutput.TRIGGER_IDS


def test_events_available(device):
    for trig_out in device.trig_outs:
        for event in trig_out.events_available:
            assert event in TriggerOutput.TRIGGER_EVENTS


def test_event(device):
    for trig_out in device.trig_outs:
        # test getter
        assert trig_out.event in TriggerOutput.TRIGGER_EVENTS

        # test setter by changing a value and reading it back
        # possible values are accessible via property events
        for event in trig_out.events_available:
            trig_out.event = event
            assert trig_out.event is event


def test_force_trig(device):
    for trig_out in device.trig_outs:
        trig_out.is_enabled = True
        # HS5 doesn't support forced output triggers
        with pytest.raises(IOError) as err:
            trig_out.force_trig()
            assert str(err) == "[-2]: NOT_SUPPORTED"
