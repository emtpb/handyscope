from tiepie.library import libtiepie
from tiepie.device import Device
from tiepie.deviceList import DeviceList
from tiepie.oscilloscopeChannel import OscilloscopeChannel


class Oscilloscope(Device):
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
        return libtiepie.ScpGetValidPreSampleCount()

    @property
    def data_range(self):
        return libtiepie.ScpChGetDataValueRange()

    @property
    def data_range_min(self):
        return libtiepie.ScpChGetDataValueMin()

    @property
    def data_range_max(self):
        return libtiepie.ScpChGetDataValueMax()

    def start(self):
        libtiepie.ScpStart()

    def stop(self):
        libtiepie.ScpStop()

    def force_trig(self):
        libtiepie.ScpForceTrigger()

    @property
    def measure_modes_available(self):
        return libtiepie.ScpGetMeasureModes()

    @property
    def measure_mode(self):
        return libtiepie.ScpGetMeasureMode()

    @measure_mode.setter
    def measure_mode(self, value):
        libtiepie.ScpSetMeasureMode(value)

    @property
    def is_running(self):
        return libtiepie.ScpIsRunning()

    @property
    def is_triggered(self):
        return libtiepie.ScpIsTriggered()

    @property
    def is_timeout_trig(self):
        return libtiepie.ScpIsTimeoutTriggered()

    @property
    def is_force_trig(self):
        return libtiepie.ScpIsForceTriggered()

    @property
    def is_data_ready(self):
        return libtiepie.ScpIsDataReady()

    @property
    def is_data_overflow(self):
        return libtiepie.ScpIsDataOverflow()

    @property
    def resolutions_availabe(self):
        return libtiepie.ScpGetResolutions()

    @property
    def resolution(self):
        return libtiepie.ScpGetResolution()

    @resolution.setter
    def resolution(self, value):
        libtiepie.ScpSetResolution(value)

    @property
    def is_resolution_enhanced(self):
        return libtiepie.ScpIsResolutionEnhanced()

    @property
    def auto_resolutions_available(self):
        return libtiepie.ScpGetAutoResolutionModes()

    @property
    def auto_resolution(self):
        return libtiepie.ScpGetAutoResolutionMode()

    @auto_resolution.setter
    def auto_resolution(self, value):
        libtiepie.ScpSetAutoResolutionMode(value)

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