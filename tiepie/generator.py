from tiepie.library import libtiepie
from tiepie.device import Device
import ctypes


class Generator(Device):
    """Class for a generator.

    Attributes:
        CONNECTOR_TYPES (dict): dict which maps connector types as strs to their libtiepie int version
        GENERATOR_STATUSES (dict): dict which maps generator statuses as strs to their libtiepie int version
        SIGNAL_TYPES (dict): dict which maps signal types as strs to their libtiepie int version
        FREQUENCY_MODES (dict): dict which maps frequency modes as strs to their libtiepie int version
        GENERATOR_MODES (dict): dict which maps generator modes as strs to their libtiepie int version
    """
    # See also OscilloscopeChannel.CONNECTOR_TYPES
    CONNECTOR_TYPES = {"unknown":   0,
                       "BNC":       1,
                       "Banana":    2,
                       "Powerplug": 4}

    GENERATOR_STATUSES = {"unknown":      0,
                          "stopped":      1,
                          "running":      2,
                          "burst active": 4,
                          "waiting":      8}

    SIGNAL_TYPES = {"unknown":      0,
                    "sine":         1,
                    "triangle":     2,
                    "square":       4,
                    "DC":           8,
                    "noise":       16,
                    "arbitrary":   32,
                    "pulse":       64}

    FREQUENCY_MODES = {"unknown":   0,
                       "signal":    1,
                       "sample":    2}

    GENERATOR_MODES = {"unknown":                          0,
                       "continuous":                       1,
                       "burst count":                      2,
                       "gated periods":                    4,
                       "gated":                            8,
                       "gated period start":              16,
                       "gated period finish":             32,
                       "gated run":                       64,
                       "gated run output":               128,
                       "burst sample count":             256,
                       "burst sample count output":      512,
                       "burst segment count":           1024,
                       "burst segment count output":    2048}
    
    _device_type = "Gen"

    def __init__(self, instr_id, id_kind="product id"):
        """Contructor for a generator.

        Args:
            instr_id (int or str): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS)
        """
        super().__init__(instr_id, id_kind, self._device_type)

    @property
    def connector_type(self):
        """Get the connector type.

        Returns:
            str: The connector type, key of :py:attr:`tiepie.generator.Generator.CONNECTOR_TYPES`
        """
        raw_type = libtiepie.GenGetConnectorType(self._dev_handle)
        for key, value in self.CONNECTOR_TYPES.items():
            if raw_type == value:
                return key

        raise ValueError("Unknown connector type: %d" % raw_type)

    @property
    def is_differential(self):
        """Check if output is differential.

        Returns:
            bool: True if differential, False otherwise.
        """
        return libtiepie.GenIsDifferential(self._dev_handle) == 1

    @property
    def impedance(self):
        """Get output impedance.

        Returns:
            float: Output impedance in Ohm.
        """
        return libtiepie.GenGetImpedance(self._dev_handle)

    @property
    def resolution(self):
        """Get DAC resolution.

        Returns:
            int: Resolution of the DAC in bits.
        """
        return libtiepie.GenGetResolution(self._dev_handle)

    @property
    def out_min(self):
        """Get minimum available output voltage.

        Returns:
            float: Minimum available output voltage in Volt.
        """
        return libtiepie.GenGetOutputValueMin(self._dev_handle)

    @property
    def out_max(self):
        """Get maximum available output voltage.

        Returns:
            float: Maximum available output voltage in Volt.
        """
        return libtiepie.GenGetOutputValueMax(self._dev_handle)

    @property
    def is_controllable(self):
        """Check if the generator is controllable.

        Returns:
            bool: True if controllable, False otherwise.
        """
        return libtiepie.GenIsControllable(self._dev_handle) == 1

    @property
    def status(self):
        """Get the current generator status.

        Returns:
            str: Generator status, key of :py:attr:`tiepie.generator.Generator.GENERATOR_STATUSES`
        """
        raw_status = libtiepie.GenGetStatus(self._dev_handle)

        for key, value in self.GENERATOR_STATUSES.items():
            if raw_status == value:
                return key

        raise ValueError("Unknown generator status: %d" % raw_status)

    @property
    def is_out_on(self):
        """Get or set if the generator output is enabled."""
        return libtiepie.GenGetOutputOn(self._dev_handle) == 1

    @is_out_on.setter
    def is_out_on(self, value):
        libtiepie.GenSetOutputOn(self._dev_handle, value)

    @property
    def is_out_inv(self):
        """Get or set if the generator output is inverted."""
        return libtiepie.GenGetOutputInvert(self._dev_handle) == 1

    @is_out_inv.setter
    def is_out_inv(self, value):
        libtiepie.GenSetOutputInvert(self._dev_handle, value)

    def start(self):
        """Start the generator.

        Returns:
            bool: True if successful, False otherwise.
        """
        return libtiepie.GenStart(self._dev_handle) == 1

    def stop(self):
        """Stop the generator.

        Returns:
            bool: True if successful, False otherwise.
        """
        return libtiepie.GenStop(self._dev_handle) == 1

    @property
    def signal_types_available(self):
        """Get available signal types.

        Returns:
            tuple: Available signal types, keys of :py:attr:`tiepie.generator.Generator.SIGNAL_TYPES`
        """
        raw_types = libtiepie.GenGetSignalTypes(self._dev_handle)
        _types = []

        if raw_types == self.SIGNAL_TYPES["unknown"]:
            _types.append("unknown")
        else:
            for key, value in self.SIGNAL_TYPES.items():
                if key == "unknown":
                    pass
                elif raw_types & value == value:
                    _types.append(key)

        return tuple(_types)

    @property
    def signal_type(self):
        """Get or set the currently active signal type."""
        raw_type = libtiepie.GenGetSignalType(self._dev_handle)

        for key, value in self.SIGNAL_TYPES.items():
            if raw_type == value:
                return key

        raise ValueError("Unknown signal type: %d" % raw_type)

    @signal_type.setter
    def signal_type(self, value):
        libtiepie.GenSetSignalType(self._dev_handle, self.SIGNAL_TYPES[value])

    @property
    def amplitude_min(self):
        """Get the minimum available amplitude.

        Returns:
            float: Miminum available amplitude in Volt.
        """
        return libtiepie.GenGetAmplitudeMin(self._dev_handle)

    @property
    def amplitude_max(self):
        """Get the maximum available amplitude.

        Returns:
            float: Maximum available amplitude in Volt.
        """
        return libtiepie.GenGetAmplitudeMax(self._dev_handle)

    @property
    def amplitude(self):
        """Get or set the amplitude in Volt."""
        return libtiepie.GenGetAmplitude(self._dev_handle)

    @amplitude.setter
    def amplitude(self, value):
        libtiepie.GenSetAmplitude(self._dev_handle, value)

    @property
    def amplitude_ranges_available(self):
        """Get the available amplitude ranges.

        Returns:
            tuple: Available amplitude ranges as floats in Volt.
        """
        list_len = libtiepie.GenGetAmplitudeRanges(self._dev_handle, None, 0)

        buffer = (ctypes.c_double * list_len)()

        libtiepie.GenGetAmplitudeRanges(self._dev_handle, ctypes.byref(buffer), list_len)

        return tuple(buffer)

    @property
    def amplitude_range(self):
        """Get or set the currently used amplitude range."""
        return libtiepie.GenGetAmplitudeRange(self._dev_handle)

    @amplitude_range.setter
    def amplitude_range(self, value):
        libtiepie.GenSetAmplitudeRange(self._dev_handle, value)

    @property
    def is_amplitude_autorange(self):
        """Get or set if amplitude autoranging is enabled."""
        return libtiepie.GenGetAmplitudeAutoRanging(self._dev_handle) == 1

    @is_amplitude_autorange.setter
    def is_amplitude_autorange(self, value):
        libtiepie.GenSetAmplitudeAutoRanging(self._dev_handle, value)

    @property
    def offset_min(self):
        """Get the minumum available offset.

        Returns:
            float: Minimum available offset in Volt.
        """
        return libtiepie.GenGetOffsetMin(self._dev_handle)

    @property
    def offset_max(self):
        """Get the maximum available offset.

        Returns:
            float: Maximum available offset in Volt.
        """
        return libtiepie.GenGetOffsetMax(self._dev_handle)

    @property
    def offset(self):
        """Get or set the current offset in Volt."""
        return libtiepie.GenGetOffset(self._dev_handle)

    @offset.setter
    def offset(self, value):
        libtiepie.GenSetOffset(self._dev_handle, value)

    @property
    def freq_min(self):
        """Get the minumum available frequency.

        Returns:
            float: Minimum available frequency in Hz.
        """
        return libtiepie.GenGetFrequencyMin(self._dev_handle)

    @property
    def freq_max(self):
        """Get the maximum available frequency.

        Returns:
            float: Maximum available frequency in Hz.
        """
        return libtiepie.GenGetFrequencyMax(self._dev_handle)

    @property
    def freq(self):
        """Get or set the currently used frequency in Hz."""
        return libtiepie.GenGetFrequency(self._dev_handle)

    @freq.setter
    def freq(self, value):
        libtiepie.GenSetFrequency(self._dev_handle, value)

    @property
    def freq_modes_available(self):
        """Get the available frequency modes.

        Returns:
            tuple: Available frequency modes, keys of :py:attr:`tiepie.generator.Generator.FREQUENCY_MODES`
        """
        raw_modes = libtiepie.GenGetFrequencyModes(self._dev_handle)
        _modes = []

        if raw_modes == self.FREQUENCY_MODES["unknown"]:
            _modes.append("unknown")
        else:
            for key, value in self.FREQUENCY_MODES.items():
                if key == "unknown":
                    pass
                elif raw_modes & value == value:
                    _modes.append(key)

        return tuple(_modes)

    @property
    def freq_mode(self):
        """Get or set the currently active frequency mode."""
        raw_mode = libtiepie.GenGetFrequencyMode(self._dev_handle)

        for key, value in self.FREQUENCY_MODES.items():
            if raw_mode == value:
                return key

        raise ValueError("Unknown frequency mode: %d" % raw_mode)

    @freq_mode.setter
    def freq_mode(self, value):
        libtiepie.GenSetFrequencyMode(self._dev_handle, self.FREQUENCY_MODES[value])

    @property
    def phase_min(self):
        """Get the minumum available signal phase.

        Returns:
            float: Minimum available signal phase in degree.
        """
        return libtiepie.GenGetPhaseMin(self._dev_handle) * 360

    @property
    def phase_max(self):
        """Get the maximum available signal phase.

        Returns:
            float: Maximum available signal phase in degree.
        """
        return libtiepie.GenGetPhaseMax(self._dev_handle) * 360

    @property
    def phase(self):
        """Get or set the signal phase in degree."""
        return libtiepie.GenGetPhase(self._dev_handle) * 360

    @phase.setter
    def phase(self, value):
        libtiepie.GenSetPhase(self._dev_handle, value/360)

    @property
    def symmetry_min(self):
        """Get the minimum available symmetry.

        The symmetry of a signal defines the ratio between the length of positive part of a period and the length of
        the negative part of a period of the generated signal.

        Returns:
            float: Minimum available symmetry, value between 0 and 1.
        """
        return libtiepie.GenGetSymmetryMin(self._dev_handle)

    @property
    def symmetry_max(self):
        """Get the maximum available symmetry.

        The symmetry of a signal defines the ratio between the length of positive part of a period and the length of
        the negative part of a period of the generated signal.

        Returns:
            float: Maximum available symmetry, value between 0 and 1.
        """
        return libtiepie.GenGetSymmetryMax(self._dev_handle)

    @property
    def symmetry(self):
        """Get or set the maximum available symmetry.

        The symmetry of a signal defines the ratio between the length of positive part of a period and the length of
        the negative part of a period of the generated signal.
        """
        return libtiepie.GenGetSymmetry(self._dev_handle)

    @symmetry.setter
    def symmetry(self, value):
        libtiepie.GenSetSymmetry(self._dev_handle, value)

    @property
    def pulse_width_min(self):
        """Get the minimum available pulse width.

        Available for signal type "pulse".

        Returns:
            float: Minimum available pulse width in seconds.
        """
        return libtiepie.GenGetWidthMin(self._dev_handle)

    @property
    def pulse_width_max(self):
        """Get the maximum available pulse width.

        Available for signal type "pulse".

        Returns:
            float: Maximum available pulse width in seconds.
        """
        return libtiepie.GenGetWidthMax(self._dev_handle)

    @property
    def pulse_width(self):
        """Get or set the pulse width in seconds.

        Available for signal type "pulse".
        """
        return libtiepie.GenGetWidth(self._dev_handle)

    @pulse_width.setter
    def pulse_width(self, value):
        libtiepie.GenSetWidth(self._dev_handle, value)

    @property
    def arb_data_length_min(self):
        """Get the minimum length (number of samples) of arbitrary data.

        Available for signal type "arbitrary".

        Returns:
            int: Minimum length of arbitrary data
        """
        return libtiepie.GenGetDataLengthMin(self._dev_handle)

    @property
    def arb_data_length_max(self):
        """Get the maximum length (number of samples) of arbitrary data.

        Available for signal type "arbitrary".

        Returns:
            int: Maximum length of arbitrary data
        """
        return libtiepie.GenGetDataLengthMax(self._dev_handle)

    @property
    def arb_data_length(self):
        """Get the length of the currently loaded arbitrary data.

        Available for signal type "arbitrary".

        Returns:
            int: Length of currently loaded arbitrary data.
        """
        return libtiepie.GenGetDataLength(self._dev_handle)

    def arb_data(self, value_list):
        """Fill the arbitrary data buffer of the generator.

        The values are normalized by the generator itself: The highest absolute value equals the set amplitude value,
        0 corresponds to the set offset value. If value_list is empty, the buffer gets cleared.

        Args:
            value_list (list): List with arbitrary data samples
        """
        list_len = len(value_list)

        if list_len == 0:
            pointer = None
        else:
            buffer = (ctypes.c_float * list_len)(*value_list)
            pointer = ctypes.byref(buffer)

        libtiepie.GenSetData(self._dev_handle, pointer, list_len)

    @property
    def modes_native_available(self):
        """Get the natively available generator modes.

        The natively available modes are the built-in modes of the generetator, independent of current settings.

        Returns:
            tuple: Available modes, keys of :py:attr:`tiepie.generator.Generator.GENERATOR_MODES`
        """
        raw_modes = libtiepie.GenGetModesNative(self._dev_handle)
        _modes = []

        if raw_modes == self.GENERATOR_MODES["unknown"]:
            _modes.append("unknown")
        else:
            for key, value in self.GENERATOR_MODES.items():
                if key == "unknown":
                    pass
                elif raw_modes & value == value:
                    _modes.append(key)

        return tuple(_modes)

    @property
    def modes_available(self):
        """Get the currently available generator modes.

        The currently available modes depend on the current generator settings.

        Returns:
            tuple: Available modes, keys of :py:attr:`tiepie.generator.Generator.GENERATOR_MODES`
        """
        raw_modes = libtiepie.GenGetModes(self._dev_handle)
        _modes = []

        if raw_modes == self.GENERATOR_MODES["unknown"]:
            _modes.append("unknown")
        else:
            for key, value in self.GENERATOR_MODES.items():
                if key == "unknown":
                    pass
                elif raw_modes & value == value:
                    _modes.append(key)

        return tuple(_modes)

    @property
    def mode(self):
        """Get or set the current generator mode (keys of :py:attr:`tiepie.generator.Generator.GENERATOR_MODES`).
        """
        raw_mode = libtiepie.GenGetMode(self._dev_handle)

        for key, value in self.GENERATOR_MODES.items():
            if raw_mode == value:
                return key

        raise ValueError("Unknown generator mode: %d" % raw_mode)

    @mode.setter
    def mode(self, value):
        libtiepie.GenSetMode(self._dev_handle, self.GENERATOR_MODES[value])

    @property
    def is_burst_active(self):
        """Check if a burst is active.

        Returns:
            bool: True if burst is active, False otherwise.
        """
        return libtiepie.GenIsBurstActive(self._dev_handle) == 1

    @property
    def burst_cnt_min(self):
        """Get the minimum available burst count.

        Available in generator burst modes.

        Returns:
            int: Minimum available burst count.
        """
        return libtiepie.GenGetBurstCountMin(self._dev_handle)

    @property
    def burst_cnt_max(self):
        """Get the maximum available burst count.

        Available in generator burst modes.

        Returns:
            int: Maximum available burst count.
        """
        return libtiepie.GenGetBurstCountMax(self._dev_handle)

    @property
    def burst_cnt(self):
        """Get or set the burst count.

        Available in generator burst modes.
        """
        return libtiepie.GenGetBurstCount(self._dev_handle)

    @burst_cnt.setter
    def burst_cnt(self, value):
        libtiepie.GenSetBurstCount(self._dev_handle, value)

    @property
    def burst_sample_cnt_min(self):
        """Get the minimum available burst sample count.

        Available in generator sample burst modes.

        Returns:
            int: Minimum available sample burst count.
        """
        return libtiepie.GenGetBurstSampleCountMin(self._dev_handle)

    @property
    def burst_sample_cnt_max(self):
        """Get the maximum available burst sample count.

        Available in generator sample burst modes.

        Returns:
            int: Maximum available sample burst count.
        """
        return libtiepie.GenGetBurstSampleCountMax(self._dev_handle)

    @property
    def burst_sample_cnt(self):
        """Get or set the burst sample count.

        Available in generator sample burst modes.
        """
        return libtiepie.GenGetBurstSampleCount(self._dev_handle)

    @burst_sample_cnt.setter
    def burst_sample_cnt(self, value):
        libtiepie.GenSetBurstSegmentCount(self._dev_handle, value)

    @property
    def burst_segment_cnt_min(self):
        """Get the minimum available burst segment count.

        Available in generator segment burst modes.

        Returns:
            int: Minimum available segment burst count.
        """
        return libtiepie.GenGetBurstSegmentCountMin(self._dev_handle)

    @property
    def burst_segment_cnt_max(self):
        """Get the maximum available burst segment count.

        Available in generator segment burst modes.

        Returns:
            int: Maximum available segment burst count.
        """
        return libtiepie.GenGetBurstSegmentCountMax(self._dev_handle)

    @property
    def burst_segment_cnt(self):
        """Get or set the burst segment count.

        Available in generator segment burst modes.
        """
        return libtiepie.GenGetBurstSegmentCount(self._dev_handle)

    @burst_segment_cnt.setter
    def burst_segment_cnt(self, value):
        libtiepie.GenSetBurstSegmentCount(self._dev_handle, value)
