from tiepie.library import libtiepie
from tiepie.device import Device
from tiepie.oscilloscopeChannel import OscilloscopeChannel
import ctypes
import time
import numpy as np


class Oscilloscope(Device):
    """Class for an oscilloscope.

    Attributes:
        MEASURE_MODES (dict): dict which maps measure modes as strs to their libtiepie int version
        AUTO_RESOLUTIONS (dict): dict which maps auto resolutions as strs to their libtiepie int version
        CLOCK_SOURCES (dict): dict which maps clock sources as strs to their libtiepie int version
        CLOCK_OUTPUTS (dict): dict which maps clock outputs as strs to their libtiepie int version
        CONNECTION_STATES (dict): dict which maps connection states as strs to their libtiepie int version
    """
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
        """Constructor for an oscilloscope.

        Args:
            instr_id (int or str): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS)
        """
        super().__init__(instr_id, id_kind, self._device_type)

        # Initialize channels
        self._channels = tuple(OscilloscopeChannel(self._dev_handle, ch_idx) for ch_idx in range(self.channel_cnt))

    @property
    def channel_cnt(self):
        """Get the channel count.

        Returns:
            int: The channel count
        """
        return libtiepie.ScpGetChannelCount(self._dev_handle)

    @property
    def channels(self):
        """Tuple of all channels.

        Returns:
            tuple: Tuple of oscilloscope channels (:py:class:`tiepie.oscilloscopeChannel.OscilloscopeChannel`)
        """
        return self._channels

    def _get_sample_cnts(self):
        """Get information on the sample counts.

        The recorded samples are divided in pre and post samples. If multiple triggers occur in a short time, not all
        pre samples might be valid. This method calculates the start count and the total number of valid samples.

        Returns:
            tuple: sample start count and valid sample count as ints
        """
        # Calc number of valid samples
        if self.measure_mode == 'block':
            post_sample_cnt = round((1.0 - self.pre_sample_ratio) * self.record_length)
            valid_sample_cnt = post_sample_cnt + self.valid_pre_sample_cnt
            # Calc sample start count
            sample_start_cnt = self.record_length - valid_sample_cnt
        else:
            sample_start_cnt = 0
            valid_sample_cnt = self.record_length

        return sample_start_cnt, valid_sample_cnt

    def retrieve(self, channel_nos=None):
        """Retrieve measured samples.

        Previously to retrieving data, a measurement has to be started.
        If no channel numbers are given, all enabled channels are retrieved.

        Args:
            channel_nos (list): (optional) iterable with channel numbers to retrieve, or None

        Returns:
            list: List with entries for each channel. An entry contains None, if the channel is disabled, otherwise
                  a list of samples.
        """
        # If no channel numbers are given, get the active ones
        if channel_nos is None:
            channel_nos = []
            for channel in self.channels:
                if channel.is_enabled:
                    channel_nos.append(channel._idx + 1)
        # Else check that the given channels are enabled
        else:
            for channel_no in channel_nos:
                if self.channels[channel_no-1].is_enabled is False:
                    raise ValueError("The given channel %d is not enabled. It has to be enabled before " % channel_no
                                     + "oscilloscope.start() is called to get valid values!")

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
        """Retrieve measured samples of channel 1.

        Previously to retrieving data, a measurement has to be started.

        Returns:
            list: List with an entry for channel 1. The entry contains None, if channel 1 is disabled, otherwise
                  a list of samples.
        """
        # Check availability
        if self.channels[0].is_enabled:
            # Get number of valid samples
            sample_start_cnt, valid_sample_cnt = self._get_sample_cnts()

            # Init buffer
            buffer = (ctypes.c_float * valid_sample_cnt)()

            libtiepie.ScpGetData1Ch(self._dev_handle, buffer, sample_start_cnt, valid_sample_cnt)

            # Cast ctypes float array to normal python list
            data = list(buffer)

            return [data]
        else:
            return [None]

    def retrieve_ch1_ch2(self):
        """Retrieve measured samples of channel 1 and 2.

        Previously to retrieving data, a measurement has to be started.

        Returns:
            list: List with entries for each channel. An entry contains None, if the channel is disabled, otherwise
                  a list of samples.
        """
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
        """Retrieve measured samples of channel 1, 2 and 3.

        Previously to retrieving data, a measurement has to be started.

        Returns:
            list: List with entries for each channel. An entry contains None, if the channel is disabled, otherwise
                  a list of samples.
        """
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
        """Retrieve measured samples of channel 1, 2, 3 and 4.

        Previously to retrieving data, a measurement has to be started.

        Returns:
            list: List with entries for each channel. An entry contains None, if the channel is disabled, otherwise
                  a list of samples.
        """
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
        """Get the count of valid pre samples.

        Returns:
            int: Count of valid pre samples.
        """
        return libtiepie.ScpGetValidPreSampleCount(self._dev_handle)

    def start(self):
        """Start a measurement.

        Returns:
            bool: True if successful, False otherwise.
        """
        return libtiepie.ScpStart(self._dev_handle) == 1

    def stop(self):
        """Stop a measurement.

        Returns:
            bool: True if successful, False otherwise.
        """
        return libtiepie.ScpStop(self._dev_handle) == 1

    def force_trig(self):
        """Force a trigger.

        Returns:
            bool: True if successful, False otherwise.
        """
        return libtiepie.ScpForceTrigger(self._dev_handle) == 1

    @property
    def measure_modes_available(self):
        """Get the available measure modes.

        Returns:
            tuple: Available measure modes (keys of :py:attr:`tiepie.oscilloscope.Oscilloscope.MEASURE_MODES`)
        """
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

        return tuple(_modes)

    @property
    def measure_mode(self):
        """Get or set the current measure mode (keys of :py:attr:`tiepie.oscilloscope.Oscilloscope.MEASURE_MODES`)"""
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
        """Check if the oscilloscope is running.

        Returns:
            bool: Truef if oscilloscope is running, False otherwise.
        """
        return libtiepie.ScpIsRunning(self._dev_handle) == 1

    @property
    def is_triggered(self):
        """Check if the oscilloscope is triggered.

        Returns:
            bool: True if oscilloscope is triggered, False otherwise.
        """
        return libtiepie.ScpIsTriggered(self._dev_handle) == 1

    @property
    def is_timeout_trig(self):
        """Check if the oscilloscope is triggered by a timeout.

        Returns:
            bool: True if oscilloscope is triggered by a timeout, False otherwise.
        """
        return libtiepie.ScpIsTimeOutTriggered(self._dev_handle) == 1

    @property
    def is_force_trig(self):
        """Check if the trigger of the oscilloscope is forced.

        Returns:
            bool: True if trigger is forced, False otherwise.
        """
        return libtiepie.ScpIsForceTriggered(self._dev_handle) == 1

    @property
    def is_data_ready(self):
        """Check if data is ready.

        Returns:
            bool: True if data ready, False otherwise.
        """
        return libtiepie.ScpIsDataReady(self._dev_handle) == 1

    @property
    def is_data_overflow(self):
        """Check if there is a data overflow.

        Returns:
            bool: True if data overflow, False otherwise.
        """
        return libtiepie.ScpIsDataOverflow(self._dev_handle) == 1

    @property
    def resolutions_available(self):
        """Get available ADC resolutions.

        Returns:
            tuple: Available ADC resolutions in bits.
        """
        # get length of list
        res_len = libtiepie.ScpGetResolutions(self._dev_handle, None, 0)

        # initialize uint8 array
        res = (ctypes.c_uint8 * res_len)()

        # write the actual data to the array
        libtiepie.ScpGetResolutions(self._dev_handle, ctypes.byref(res), res_len)

        # convert to a normal python list
        res = list(res)

        return tuple(res)

    @property
    def resolution(self):
        """Get or set the current ADC resolution in bit."""
        return libtiepie.ScpGetResolution(self._dev_handle)

    @resolution.setter
    def resolution(self, value):
        libtiepie.ScpSetResolution(self._dev_handle, value)

    @property
    def is_resolution_enhanced(self):
        """Check if the ADC resolution is enhanced.

        Returns:
            bool: True if ADC resolution is enhanced, False otherwise.
        """
        return libtiepie.ScpIsResolutionEnhanced(self._dev_handle) == 1

    @property
    def auto_resolutions_available(self):
        """Get available auto resolutions.

        Returns:
            tuple: Available auto resolutions (keys of :py:attr:`tiepie.oscilloscope.Oscilloscope.AUTO_RESOLUTIONS`)
        """
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

        return tuple(_res)

    @property
    def auto_resolution(self):
        """Get or set the current auto resolution mode (key of
        :py:attr:`tiepie.oscilloscope.Oscilloscope.AUTO_RESOLUTIONS`)
        """
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
        """Get available clock sources.

        Returns:
            tuple: Available clock sources (keys of :py:attr:`tiepie.oscilloscope.Oscilloscope.CLOCK_SOURCES`)
        """
        raw_srcs = libtiepie.ScpGetClockSources(self._dev_handle)
        srcs = []

        if raw_srcs == self.CLOCK_SOURCES["unknown"]:
            srcs.append("unknown")
        else:
            for key, value in self.CLOCK_SOURCES.items():
                if key == "unknown":
                    continue
                else:
                    if raw_srcs & value == value:
                        srcs.append(key)

        return tuple(srcs)

    @property
    def clock_source(self):
        """Get or set the current clock source (key of :py:attr:`tiepie.oscilloscope.Oscilloscope.CLOCK_SOURCES`)
        """
        src = libtiepie.ScpGetClockSource(self._dev_handle)
        for key, value in self.CLOCK_SOURCES.items():
            if src == value:
                return key

        raise ValueError("Unknown clock source: %d" % src)

    @clock_source.setter
    def clock_source(self, value):
        libtiepie.ScpSetClockSource(self._dev_handle, self.CLOCK_SOURCES[value])

    @property
    def clock_outputs_available(self):
        """Get available clock outputs.

        Returns:
            tuple: Available clock outputs (keys of :py:attr:`tiepie.oscilloscope.Oscilloscope.CLOCK_OUTPUTS`)
        """
        raw_outs = libtiepie.ScpGetClockOutputs(self._dev_handle)
        outs = []

        if raw_outs == self.CLOCK_OUTPUTS["unknown"]:
            outs.append("unknown")
        else:
            for key, value in self.CLOCK_OUTPUTS.items():
                if key == "unknown":
                    pass
                else:
                    if raw_outs & value == value:
                        outs.append(key)

        return tuple(outs)

    @property
    def clock_output(self):
        """Get or set the current clock output (key of :py:attr:`tiepie.oscilloscope.Oscilloscope.CLOCK_OUTPUTS`)"""
        out = libtiepie.ScpGetClockOutput(self._dev_handle)
        for key, value in self.CLOCK_OUTPUTS.items():
            if out == value:
                return key

        raise ValueError("Unknown clock output: %d" % out)

    @clock_output.setter
    def clock_output(self, value):
        libtiepie.ScpSetClockOutput(self._dev_handle, self.CLOCK_OUTPUTS[value])

    @property
    def sample_freq_max(self):
        """Get the maximum sample frequency in Hz.

        Returns:
            float: Maximum sample frequency in Hz
        """
        return libtiepie.ScpGetSampleFrequencyMax(self._dev_handle)

    @property
    def sample_freq(self):
        """Get or set the current sample frequency in Hz."""
        return libtiepie.ScpGetSampleFrequency(self._dev_handle)

    @sample_freq.setter
    def sample_freq(self, value):
        libtiepie.ScpSetSampleFrequency(self._dev_handle, value)

    @property
    def record_length_max(self):
        """Get the maximum record length (number of samples).

        Returns:
            int: Maximum record length
        """
        return libtiepie.ScpGetRecordLengthMax(self._dev_handle)

    @property
    def record_length(self):
        """Get or set the current record length (number of samples)."""
        return libtiepie.ScpGetRecordLength(self._dev_handle)

    @record_length.setter
    def record_length(self, value):
        libtiepie.ScpSetRecordLength(self._dev_handle, value)

    @property
    def pre_sample_ratio(self):
        """Get or set the pre sample ratio.

        The pre sample ratio is a float between 0 and 1 and defines how many samples should be recorded before the
        trigger point."""
        return libtiepie.ScpGetPreSampleRatio(self._dev_handle)

    @pre_sample_ratio.setter
    def pre_sample_ratio(self, value):
        libtiepie.ScpSetPreSampleRatio(self._dev_handle, value)

    @property
    def segment_cnt_max(self):
        """Get the maximum available segment count.

        Returns:
            int: Maximum available segment count
        """
        return libtiepie.ScpGetSegmentCountMax(self._dev_handle)

    @property
    def segment_cnt(self):
        """Get or set the current segment count."""
        return libtiepie.ScpGetSegmentCount(self._dev_handle)

    @segment_cnt.setter
    def segment_cnt(self, value):
        libtiepie.ScpSetSegmentCount(self._dev_handle, value)

    @property
    def trig_timeout(self):
        """Get or set the trigger timeout in seconds.

        0 forces a trigger immediately after a measurement is started, -1 will wait infinitely for a trigger."""
        return libtiepie.ScpGetTriggerTimeOut(self._dev_handle)

    @trig_timeout.setter
    def trig_timeout(self, value):
        libtiepie.ScpSetTriggerTimeOut(self._dev_handle, value)

    @property
    def is_trig_delay_available(self):
        """Check if trigger delay is available.

        Returns:
            bool: True if trigger delay is available, False otherwise.
        """
        return libtiepie.ScpHasTriggerDelay(self._dev_handle) == 1

    @property
    def trig_delay_max(self):
        """Get the maximum available trigger delay in seconds.

        Returns:
            float: Maximum available trigger delay in seconds.
        """
        return libtiepie.ScpGetTriggerDelayMax(self._dev_handle)

    @property
    def trig_delay(self):
        """Get or set the current trigger delay in seconds."""
        return libtiepie.ScpGetTriggerDelay(self._dev_handle)

    @trig_delay.setter
    def trig_delay(self, value):
        libtiepie.ScpSetTriggerDelay(self._dev_handle, value)

    @property
    def is_trig_holdoff_available(self):
        """Check if trigger holdoff is available.

        Returns:
            bool: True if trigger holdoff is available, False otherwise.
        """
        return libtiepie.ScpHasTriggerHoldOff(self._dev_handle) == 1

    @property
    def trig_holdoff_max(self):
        """Get the maximum available trigger holdoff in seconds.

        Returns:
            float: Maximum available trigger holdoff on seconds.
        """
        return libtiepie.ScpGetTriggerHoldOffCountMax(self._dev_handle)

    @property
    def trig_holdoff(self):
        """Get or set the current trigger holdoff in seconds."""
        return libtiepie.ScpGetTriggerHoldOffCount(self._dev_handle)

    @trig_holdoff.setter
    def trig_holdoff(self, value):
        libtiepie.ScpSetTriggerHoldOffCount(self._dev_handle, value)

    @property
    def is_trig_available(self):
        """Check if trigger is available.

        Returns:
            bool: True if trigger is available, False otherwise.
        """
        return libtiepie.ScpHasTrigger(self._dev_handle) == 1

    @property
    def is_connection_test_available(self):
        """Check if connection test is available.

        Returns:
            bool: True if connection test is available, False otherwise.
        """
        return libtiepie.ScpHasConnectionTest(self._dev_handle) == 1

    def start_connection_test(self):
        """Start a connection test.

        Returns:
            bool: True if test started successfully, False otherwise.
        """
        return libtiepie.ScpStartConnectionTest(self._dev_handle) == 1

    @property
    def is_connection_test_completed(self):
        """Check if connection test is completed.

        Returns:
            bool: True if connection test is completed, False otherwise.
        """
        return libtiepie.ScpIsConnectionTestCompleted(self._dev_handle) == 1

    @property
    def connection_test_data(self):
        """Get connection test data.

        Returns:
            tuple: Tuple with the test result of each channel (key of
                   :py:attr:`tiepie.oscilloscope.Oscilloscope.CONNECTION_STATES`)
        """
        # Initialize uint8 array
        data = (ctypes.c_uint8 * self.channel_cnt)()

        # Write the actual data to the array
        libtiepie.ScpGetConnectionTestData(self._dev_handle, ctypes.byref(data), self.channel_cnt)

        # Convert to a normal python list
        data = list(data)

        # Evaluate
        data_evaluated = []
        for element in data:
            result = None

            # Try to look up the element
            for key, value in self.CONNECTION_STATES.items():
                if element == value:
                    result = key

            # If found append it to the output
            if result is not None:
                data_evaluated.append(result)
            # Else throw an exception
            else:
                raise ValueError("Unknown connection state: %d" % element)

        return tuple(data_evaluated)

    def test_connection(self):
        """Perform a connection test.

        Returns:
            tuple: Tuple with the test result of each channel (key of
                   :py:attr:`tiepie.oscilloscope.Oscilloscope.CONNECTION_STATES`)
        """
        if self.is_connection_test_available:
            res = self.start_connection_test()
            if res is False:
                raise IOError("Connection test could not be started.")

            while not self.is_connection_test_completed:
                time.sleep(0.1)

            return self.connection_test_data
        else:
            return None

    def measure(self):
        """Perform a single shot measurement.

        Utility function which starts a measurement. When measurement data is ready, it is retrieved
        and returned.

        Returns:
            list: List with entries for each channel. An entry contains None, if the channel is disabled, otherwise
                  a list of samples.
        """
        # Start measurement
        self.start()

        # Wait until measurement is finished
        while not self.is_data_ready:
            time.sleep(0.1)

        # Get data
        data = self.retrieve()

        return data

    @property
    def time_vector(self):
        """Get a time vector according to the current oscilloscope settings.

        Returns:
            :class:`numpy.ndarray`: Time vector
        """
        return np.linspace(0, 1/self.sample_freq*self.record_length, num=self.record_length, endpoint=False)
