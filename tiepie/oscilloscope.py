from tiepie.library import libtiepie
from tiepie.device import Device
from tiepie.deviceList import DeviceList
from tiepie.oscilloscopeChannel import OscilloscopeChannel
import ctypes
import time


class Oscilloscope(Device):
    MEASURE_MODES = {"unknown": 0,
                     "stream":  1,
                     "block":   2}

    AUTO_RESOLUTIONS = {"unknown":     0,
                        "disabled":    1,
                        "native only": 2,
                        "all":         4}

    CLOCK_SOURCES = {"unknown":  0,
                     "external": 1,
                     "internal": 2}

    CLOCK_OUTPUTS = {"unknown":  0,
                     "disabled": 1,
                     "sample":   2,
                     "fixed":    4}

    CONNECTION_STATES = {"undefined":    0,
                         "connected":    1,
                         "disconnected": 2}

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

    def _get_sample_cnts(self):
        # Calc number of valid samples
        post_sample_cnt = round((1.0 - self.pre_sample_ratio) * self.record_length)
        valid_sample_cnt = post_sample_cnt + self.valid_pre_sample_cnt
        # Calc sample start count
        sample_start_cnt = self.record_length - valid_sample_cnt

        return sample_start_cnt, valid_sample_cnt

    def retrieve(self, channel_nos=None):
        # If no channel numbers are given, get the active ones
        if channel_nos is None:
            channel_nos = []
            for channel in self.channels:
                if channel.is_enabled:
                    channel_nos.append(channel._idx + 1)

        # Check that there is at least one entry in channel_nos
        if not channel_nos:
            raise ValueError("No channel is enabled for measurement or the supplied channel number list is empty.")

        # Get number of valid samples
        sample_start_cnt, valid_sample_cnt = self._get_sample_cnts()

        # Initialize buffer
        channel_cnt = max(channel_nos)
        buffers = [None] * channel_cnt
        pointer_array = libtiepie.HlpPointerArrayNew(channel_cnt)
        for idx in range(channel_cnt):
            if idx+1 in channel_nos:
                buffers[idx] = (ctypes.c_float * valid_sample_cnt)()
                libtiepie.HlpPointerArraySet(pointer_array, idx, ctypes.byref(buffers[idx]))

        libtiepie.ScpGetData(self._dev_handle, pointer_array, channel_cnt, sample_start_cnt, valid_sample_cnt)

        # Free pointer array
        libtiepie.HlpPointerArrayDelete(pointer_array)

        # Cast ctypes float array to normal python lists
        data = [None if channel_data is None else list(channel_data) for channel_data in buffers]

        return data

    def retrieve_ch1(self):
        # Check availability
        if self.channels[0].is_enabled:
            # Get number of valid samples
            sample_start_cnt, valid_sample_cnt = self._get_sample_cnts()

            # Init buffer
            buffer = (ctypes.c_float * valid_sample_cnt)()

            libtiepie.ScpGetData1Ch(self._dev_handle, buffer, sample_start_cnt, valid_sample_cnt)

            # Cast ctypes float array to normal python list
            data = list(buffer)

            return data
        else:
            return None

    def retrieve_ch1_ch2(self):
        # Get number of valid samples
        sample_start_cnt, valid_sample_cnt = self._get_sample_cnts()

        # Init buffers list for channel 1 & 2
        buffers = [None] * 2

        for idx in range(len(buffers)):
            # Check availability
            if idx < len(self.channels):
                if self.channels[idx].is_enabled:
                    buffers[idx] = (ctypes.c_float * valid_sample_cnt)()

        libtiepie.ScpGetData2Ch(self._dev_handle, *buffers, sample_start_cnt, valid_sample_cnt)

        # Cast ctypes float array to normal python lists
        data = [None if channel_data is None else list(channel_data) for channel_data in buffers]

        return data

    def retrieve_ch1_ch2_ch3(self):
        # Get number of valid samples
        sample_start_cnt, valid_sample_cnt = self._get_sample_cnts()

        # Init buffers list for channel 1 & 2
        buffers = [None] * 3

        for idx in range(len(buffers)):
            # Check availability
            if idx < len(self.channels):
                if self.channels[idx].is_enabled:
                    buffers[idx] = (ctypes.c_float * valid_sample_cnt)()

        libtiepie.ScpGetData3Ch(self._dev_handle, *buffers, sample_start_cnt, valid_sample_cnt)

        # Cast ctypes float array to normal python lists
        data = [None if channel_data is None else list(channel_data) for channel_data in buffers]

        return data

    def retrieve_ch1_ch2_ch3_ch4(self):
        # Get number of valid samples
        sample_start_cnt, valid_sample_cnt = self._get_sample_cnts()

        # Init buffers list for channel 1 & 2
        buffers = [None] * 4

        for idx in range(len(buffers)):
            # Check availability
            if idx < len(self.channels):
                if self.channels[idx].is_enabled:
                    buffers[idx] = (ctypes.c_float * valid_sample_cnt)()

        libtiepie.ScpGetData4Ch(self._dev_handle, *buffers, sample_start_cnt, valid_sample_cnt)

        # Cast ctypes float array to normal python lists
        data = [None if channel_data is None else list(channel_data) for channel_data in buffers]

        return data

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
    def measure_modes_available(self):
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
    def resolutions_available(self):
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
    def auto_resolutions_available(self):
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
        raw_srcs = libtiepie.ScpGetClockSources(self._dev_handle)
        srcs = []

        if raw_srcs == self.CLOCK_SOURCES["unknown"]:
            srcs.append("unknown")
        else:
            for key, value in self.CLOCK_SOURCES.items():
                if value == "unknown":
                    pass
                else:
                    if raw_srcs & value == value:
                        srcs.append(key)

        return srcs

    @property
    def clock_source(self):
        src = libtiepie.ScpGetClockSource(self._dev_handle)
        for key, value in self.CLOCK_SOURCES:
            if src == value:
                return key

        raise ValueError("Unknown clock source: %d" % src)

    @clock_source.setter
    def clock_source(self, value):
        libtiepie.ScpSetClockSource(self._dev_handle, self.CLOCK_SOURCES[value])

    @property
    def clock_outputs_available(self):
        raw_outs = libtiepie.ScpGetClockOutputs(self._dev_handle)
        outs = []

        if raw_outs == self.CLOCK_OUTPUTS["unknown"]:
            outs.append("unknown")
        else:
            for key, value in self.CLOCK_OUTPUTS.items():
                if value == "unknown":
                    pass
                else:
                    if raw_outs & value == value:
                        outs.append(key)

        return outs

    @property
    def clock_output(self):
        out = libtiepie.ScpGetClockOutput(self._dev_handle)
        for key, value in self.CLOCK_OUTPUTS:
            if out == value:
                return key

        raise ValueError("Unknown clock output: %d" % out)

    @clock_output.setter
    def clock_output(self, value):
        libtiepie.ScpSetClockOutput(self._dev_handle, self.CLOCK_OUTPUTS[value])

    @property
    def sample_freq_max(self):
        return libtiepie.ScpGetSampleFrequencyMax(self._dev_handle)

    @property
    def sample_freq(self):
        return libtiepie.ScpGetSampleFrequency(self._dev_handle)

    @sample_freq.setter
    def sample_freq(self, value):
        libtiepie.ScpSetSampleFrequency(self._dev_handle, value)

    @property
    def record_length_max(self):
        return libtiepie.ScpGetRecordLengthMax(self._dev_handle)

    @property
    def record_length(self):
        return libtiepie.ScpGetRecordLength(self._dev_handle)

    @record_length.setter
    def record_length(self, value):
        libtiepie.ScpSetRecordLength(self._dev_handle, value)

    @property
    def pre_sample_ratio(self):
        return libtiepie.ScpGetPreSampleRatio(self._dev_handle)

    @pre_sample_ratio.setter
    def pre_sample_ratio(self, value):
        libtiepie.ScpSetPreSampleRatio(self._dev_handle, value)

    @property
    def segment_cnt_max(self):
        return libtiepie.ScpGetSegmentCountMax(self._dev_handle)

    @property
    def segment_cnt(self):
        return libtiepie.ScpGetSegmentCount(self._dev_handle)

    @segment_cnt.setter
    def segment_cnt(self, value):
        libtiepie.ScpSetSegmentCount(self._dev_handle, value)

    @property
    def trig_timeout(self):
        return libtiepie.ScpGetTriggerTimeOut(self._dev_handle)

    @trig_timeout.setter
    def trig_timeout(self, value):
        libtiepie.ScpSetTriggerTimeOut(self._dev_handle, value)

    @property
    def is_trig_delay_available(self):
        return libtiepie.ScpHasTriggerDelay(self._dev_handle) == 1

    @property
    def trig_delay_max(self):
        return libtiepie.ScpGetTriggerDelayMax(self._dev_handle)

    @property
    def trig_delay(self):
        return libtiepie.ScpGetTriggerDelay(self._dev_handle)

    @trig_delay.setter
    def trig_delay(self, value):
        libtiepie.ScpSetTriggerDelay(self._dev_handle, value)

    @property
    def is_trig_holdoff_available(self):
        return libtiepie.ScpHasTriggerHoldOff(self._dev_handle)

    @property
    def trig_holdoff_max(self):
        return libtiepie.ScpGetTriggerHoldOffCountMax(self._dev_handle)

    @property
    def trig_holdoff(self):
        return libtiepie.ScpGetTriggerHoldOff(self._dev_handle)

    @trig_holdoff.setter
    def trig_holdoff(self, value):
        libtiepie.ScpSetTriggerHoldOff(self._dev_handle, value)

    @property
    def is_trig_available(self):
        return libtiepie.ScpHasTrigger(self._dev_handle) == 1

    @property
    def is_connection_test_available(self):
        return libtiepie.ScpHasConnectionTest(self._dev_handle) == 1

    def start_connection_test(self):
        return libtiepie.ScpStartConnectionTest(self._dev_handle) == 1

    @property
    def is_connection_test_completed(self):
        return libtiepie.ScpIsConnectionTestCompleted(self._dev_handle) == 1

    @property
    def connection_test_data(self):
        # Initialize uint8 array
        data = (ctypes.c_uint8 * self.channel_count)()

        # Write the actual data to the array
        libtiepie.ScpGetConnectionTestData(self._dev_handle, ctypes.byref(data), self.channel_count)

        # Convert to a normal python list
        data = list(data)

        # Evaluate
        data_evaluated = []
        for element in data:
            for key, value in self.CONNECTION_STATES.items():
                if element == value:
                    data_evaluated.append(key)
                else:
                    raise ValueError("Unknown connection state: %d" % element)

        return data_evaluated

    def test_connection(self):
        if self.is_connection_test_available:
            res = self.start_connection_test()
            if res is False:
                raise IOError("Connection test could not be started.")

            while not self.is_connection_test_completed:
                pass

            return self.connection_test_data
        else:
            return None

    def measure(self):
        # Start measurement
        self.start()

        # Wait until measurement is finished
        while not self.is_data_ready:
            time.sleep(0.01)

        # Get data
        data = self.retrieve()

        return data
