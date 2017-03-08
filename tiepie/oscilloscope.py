from tiepie.library import libtiepie
from tiepie.device import Device
from tiepie.deviceList import DeviceList
from tiepie.oscilloscopeChannel import OscilloscopeChannel
import ctypes


class Oscilloscope(Device):
    MEASURE_MODES = {"unknown": 0,
                     "stream":  1,
                     "block":   2}

    AUTO_RESOLUTIONS = {"unknown":     0,
                        "disabled":    1,
                        "native only": 2,
                        "all":         4}

    _device_type = "Osc"

    def __init__(self, instr_id, id_kind="product id"):
        super().__init__(instr_id, id_kind, self._device_type)

        # Initialize channels
        self._channels = [OscilloscopeChannel(self._dev_handle, ch_idx) for ch_idx in range(self.channel_count)]

    @property
    def channel_count(self):
        return libtiepie.ScpGetChannelCount(self._dev_handle)

    @property
    def channels(self):
        return self._channels

    def retrieve(self):
        libtiepie.ScpGetData()

    def retrieve_ch1(self):
        libtiepie.ScpGetData1Ch()

    def retrieve_ch1_ch2(self):
        libtiepie.ScpGetData2Ch()

    def retrieve_ch1_ch2_ch3(self):
        libtiepie.ScpGetData3Ch()

    def retrieve_ch1_ch2_ch3_ch4(self):
        libtiepie.ScpGetData4Ch()

    @property
    def valid_pre_sample_cnt(self):
        return libtiepie.ScpGetValidPreSampleCount(self._dev_handle)

    def start(self):
        return libtiepie.ScpStart(self._dev_handle) == 1

    def stop(self):
        return libtiepie.ScpStop(self._dev_handle) == 1

    def force_trig(self):
        return libtiepie.ScpForceTrigger(self._dev_handle) == 1

    @property
    def measure_modes(self):
        raw_modes = libtiepie.ScpGetMeasureModes(self._dev_handle)
        _modes = []

        # If no measure modes are available, return unknown
        if raw_modes == self.MEASURE_MODES["unknown"]:
            _modes.append("unknown")
        # Else do a detailed analysis...
        else:
            # ... by iterating over every possible kind...
            for key in self.MEASURE_MODES:
                # ... and ignoring "unknown" (already handled above)
                if key == "unknown":
                    pass
                elif raw_modes & self.MEASURE_MODES[key] == self.MEASURE_MODES[key]:
                    _modes.append(key)

        return _modes

    @property
    def measure_mode(self):
        mode_int = libtiepie.ScpGetMeasureMode(self._dev_handle)
        for key in self.MEASURE_MODES:
            if mode_int == self.MEASURE_MODES[key]:
                return key

        raise ValueError("Unknown measure mode: %d" % mode_int)

    @measure_mode.setter
    def measure_mode(self, value):
        libtiepie.ScpSetMeasureMode(self._dev_handle, self.MEASURE_MODES[value])

    @property
    def is_running(self):
        return libtiepie.ScpIsRunning(self._dev_handle) == 1

    @property
    def is_triggered(self):
        return libtiepie.ScpIsTriggered(self._dev_handle) == 1

    @property
    def is_timeout_trig(self):
        return libtiepie.ScpIsTimeoutTriggered(self._dev_handle) == 1

    @property
    def is_force_trig(self):
        return libtiepie.ScpIsForceTriggered(self._dev_handle) == 1

    @property
    def is_data_ready(self):
        return libtiepie.ScpIsDataReady(self._dev_handle) == 1

    @property
    def is_data_overflow(self):
        return libtiepie.ScpIsDataOverflow(self._dev_handle) == 1

    @property
    def resolutions(self):
        # get length of list
        res_len = libtiepie.ScpGetResolutions(self._dev_handle, None, 0)

        # initialize uint8 array
        res = (ctypes.c_uint8 * res_len)()

        # write the actual data to the array
        libtiepie.ScpGetResolutions(self._dev_handle, ctypes.byref(res), res_len)

        # convert to a normal python list
        res = list(res)

        return res

    @property
    def resolution(self):
        return libtiepie.ScpGetResolution(self._dev_handle)

    @resolution.setter
    def resolution(self, value):
        libtiepie.ScpSetResolution(self._dev_handle, value)

    @property
    def is_resolution_enhanced(self):
        return libtiepie.ScpIsResolutionEnhanced(self._dev_handle) == 1

    @property
    def auto_resolutions(self):
        raw_res = libtiepie.ScpGetAutoResolutionModes(self._dev_handle)
        _res = []

        # If no auto resolution modes are available, return unknown
        if raw_res == self.AUTO_RESOLUTIONS["unknown"]:
            _res.append("unknown")
        # Else do a detailed analysis...
        else:
            # ... by iterating over every possible kind...
            for key in self.AUTO_RESOLUTIONS:
                # ... and ignoring "unknown" (already handled above)
                if key == "unknown":
                    pass
                elif raw_res & self.AUTO_RESOLUTIONS[key] == self.AUTO_RESOLUTIONS[key]:
                    _res.append(key)

        return _res

    @property
    def auto_resolution(self):
        raw_res = libtiepie.ScpGetAutoResolutionMode(self._dev_handle)
        for key, value in self.AUTO_RESOLUTIONS.items():
            if raw_res == value:
                return key

        raise ValueError("Unknown auto resolution mode: %d" % raw_res)

    @auto_resolution.setter
    def auto_resolution(self, value):
        libtiepie.ScpSetAutoResolutionMode(self._dev_handle, self.AUTO_RESOLUTIONS[value])

    @property
    def clock_sources_available(self):
        return libtiepie.ScpGetClockSources()

    @property
    def clock_source(self):
        return libtiepie.ScpGetClockSource()

    @clock_source.setter
    def clock_source(self, value):
        libtiepie.ScpSetClockSource(value)

    @property
    def clock_outputs_available(self):
        return libtiepie.ScpGetClockOutputs()

    @property
    def clock_output(self):
        return libtiepie.ScpGetClockOutput()

    @clock_output.setter
    def clock_output(self, value):
        libtiepie.ScpSetClockOutput(value)

    @property
    def sample_freq_max(self):
        return libtiepie.ScpGetSampleFrequencyMax()

    @property
    def sample_freq(self):
        return libtiepie.ScpGetSampleFrequency()

    @sample_freq.setter
    def sample_freq(self, value):
        libtiepie.ScpSetSampleFrequency(value)

    @property
    def record_length_max(self):
        return libtiepie.ScpGetRecordLengthMax()

    @property
    def record_length(self):
        return libtiepie.ScpGetRecordLength()

    @record_length.setter
    def record_length(self, value):
        libtiepie.ScpSetRecordLength(value)

    @property
    def pre_sample_ratio(self):
        return libtiepie.ScpGetPreSampleRatio()

    @pre_sample_ratio.setter
    def pre_sample_ratio(self, value):
        libtiepie.ScpSetPreSampleRatio(value)

    @property
    def segment_cnt_max(self):
        return libtiepie.ScpGetSegmentCountMax()

    @property
    def segment_cnt(self):
        return libtiepie.ScpGetSegmentCount()

    @segment_cnt.setter
    def segment_cnt(self, value):
        libtiepie.ScpSetSegmentCount(value)

    @property
    def trig_timeout(self):
        return libtiepie.ScpGetTriggerTimeOut()

    @trig_timeout.setter
    def trig_timeout(self, value):
        libtiepie.ScpSetTriggerTimeOut(value)

    @property
    def is_trig_delay_available(self):
        return libtiepie.ScpHasTriggerDelay()

    @property
    def trig_delay_max(self):
        return libtiepie.ScpGetTriggerDelayMax()

    @property
    def trig_delay(self):
        return libtiepie.ScpGetTriggerDelay()

    @trig_delay.setter
    def trig_delay(self, value):
        libtiepie.ScpSetTriggerDelay(value)

    @property
    def is_trig_holdoff_available(self):
        return libtiepie.ScpHasTriggerHoldOff()

    @property
    def trig_holdoff_max(self):
        return libtiepie.ScpGetTriggerHoldOffCountMax()

    @property
    def trig_holdoff(self):
        return libtiepie.ScpGetTriggerHoldOff()

    @trig_holdoff.setter
    def trig_holdoff(self, value):
        libtiepie.ScpSetTriggerHoldOff(value)

    @property
    def is_trig_available(self):
        return libtiepie.ScpHasTrigger()

    @property
    def is_connection_test_available(self):
        return libtiepie.ScpHasConnectionTest()

    def start_connection_test(self):
        libtiepie.ScpStartConnectionTest()

    @property
    def is_connection_test_completed(self):
        return libtiepie.ScpIsConnectionTestCompleted()

    @property
    def connection_test_data(self):
        return libtiepie.ScpGetConnectionTestData()

    def test_connection(self):
        pass