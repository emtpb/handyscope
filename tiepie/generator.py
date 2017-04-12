from tiepie.library import libtiepie
from tiepie.device import Device
import ctypes


class Generator(Device):
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
        super().__init__(instr_id, id_kind, self._device_type)

    @property
    def connector_type(self):
        raw_type = libtiepie.GenGetConnectorType(self._dev_handle)
        for key in self.CONNECTOR_TYPES:
            if raw_type == self.CONNECTOR_TYPES[key]:
                return key

        raise ValueError("Unknown connector type: %d" % raw_type)

    @property
    def is_differential(self):
        return libtiepie.GenIsDifferential(self._dev_handle) == 1

    @property
    def impedance(self):
        return libtiepie.GenGetImpedance(self._dev_handle)

    @property
    def resolution(self):
        return libtiepie.GenGetResolution(self._dev_handle)

    @property
    def out_min(self):
        return libtiepie.GenGetOutputValueMin(self._dev_handle)

    @property
    def out_max(self):
        return libtiepie.GenGetOutputValueMax(self._dev_handle)

    @property
    def is_controllable(self):
        return libtiepie.GenIsControllable(self._dev_handle) == 1

    @property
    def status(self):
        raw_status = libtiepie.GenGetStatus(self._dev_handle)

        for key, value in self.GENERATOR_STATUSES.items():
            if raw_status & value == value:
                return key

        raise ValueError("Unknown generator status: %d" % raw_status)

    @property
    def is_out_on(self):
        return libtiepie.GenGetOutputOn(self._dev_handle) == 1

    @is_out_on.setter
    def is_out_on(self, value):
        libtiepie.GenSetOutputOn(self._dev_handle, value)

    @property
    def is_out_inv(self):
        return libtiepie.GenGetOutputInvert(self._dev_handle) == 1

    @is_out_inv.setter
    def is_out_inv(self, value):
        libtiepie.GenSetOutputInvert(self._dev_handle, value)

    def start(self):
        return libtiepie.GenStart(self._dev_handle) == 1

    def stop(self):
        return libtiepie.GenStop(self._dev_handle) == 1

    @property
    def signal_types_available(self):
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
        return libtiepie.GenGetAmplitudeMin(self._dev_handle)

    @property
    def amplitude_max(self):
        return libtiepie.GenGetAmplitudeMax(self._dev_handle)

    @property
    def amplitude(self):
        return libtiepie.GenGetAmplitude(self._dev_handle)

    @amplitude.setter
    def amplitude(self, value):
        libtiepie.GenSetAmplitude(self._dev_handle, value)

    @property
    def amplitude_ranges_available(self):
        list_len = libtiepie.GenGetAmplitudeRanges(self._dev_handle, None, 0)

        buffer = (ctypes.c_double * list_len)()

        libtiepie.GenGetAmplitudeRanges(self._dev_handle, ctypes.byref(buffer), list_len)

        return tuple(buffer)

    @property
    def amplitude_range(self):
        return libtiepie.GenGetAmplitudeRange(self._dev_handle)

    @amplitude_range.setter
    def amplitude_range(self, value):
        libtiepie.GenSetAmplitudeRange(self._dev_handle, value)

    @property
    def is_amplitude_autorange(self):
        return libtiepie.GenGetAmplitudeAutoRanging(self._dev_handle) == 1

    @is_amplitude_autorange.setter
    def is_amplitude_autorange(self, value):
        libtiepie.GenSetAmplitudeAutoRanging(self._dev_handle, value)

    @property
    def offset_min(self):
        return libtiepie.GenGetOffsetMin(self._dev_handle)

    @property
    def offset_max(self):
        return libtiepie.GenGetOffsetMax(self._dev_handle)

    @property
    def offset(self):
        return libtiepie.GenGetOffset(self._dev_handle)

    @offset.setter
    def offset(self, value):
        libtiepie.GenSetOffset(self._dev_handle, value)

    @property
    def freq_min(self):
        return libtiepie.GenGetFrequencyMin(self._dev_handle)

    @property
    def freq_max(self):
        return libtiepie.GenGetFrequencyMax(self._dev_handle)

    @property
    def freq(self):
        return libtiepie.GenGetFrequency(self._dev_handle)

    @freq.setter
    def freq(self, value):
        libtiepie.GenSetFrequency(self._dev_handle, value)

    @property
    def freq_modes_available(self):
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
        raw_mode = libtiepie.GenGetFrequencyMode(self._dev_handle)

        for key, value in self.FREQUENCY_MODES.items():
            if raw_mode & value == value:
                return key

        raise ValueError("Unknown frequency mode: %d" % raw_mode)

    @freq_mode.setter
    def freq_mode(self, value):
        libtiepie.GenSetFrequencyMode(self._dev_handle, self.FREQUENCY_MODES[value])

    @property
    def phase_min(self):
        return libtiepie.GenGetPhaseMin(self._dev_handle) * 360

    @property
    def phase_max(self):
        return libtiepie.GenGetPhaseMax(self._dev_handle) * 360

    @property
    def phase(self):
        return libtiepie.GenGetPhase(self._dev_handle) * 360

    @phase.setter
    def phase(self, value):
        libtiepie.GenSetPhase(self._dev_handle, value/360)

    @property
    def symmetry_min(self):
        return libtiepie.GenGetSymmetryMin(self._dev_handle)

    @property
    def symmetry_max(self):
        return libtiepie.GenGetSymmetryMax(self._dev_handle)

    @property
    def symmetry(self):
        return libtiepie.GenGetSymmetry(self._dev_handle)

    @symmetry.setter
    def symmetry(self, value):
        libtiepie.GenSetSymmetry(self._dev_handle, value)

    @property
    def pulse_width_min(self):
        return libtiepie.GenGetWidthMin(self._dev_handle)

    @property
    def pulse_width_max(self):
        return libtiepie.GenGetWidthMax(self._dev_handle)

    @property
    def pulse_width(self):
        return libtiepie.GenGetWidth(self._dev_handle)

    @pulse_width.setter
    def pulse_width(self, value):
        libtiepie.GenSetWidth(self._dev_handle, value)

    @property
    def arb_data_length_min(self):
        return libtiepie.GenGetDataLengthMin(self._dev_handle)

    @property
    def arb_data_length_max(self):
        return libtiepie.GenGetDataLengthMax(self._dev_handle)

    @property
    def arb_data_length(self):
        return libtiepie.GenGetDataLength(self._dev_handle)

    def arb_data(self, value_list):
        list_len = len(value_list)

        if list_len == 0:
            pointer = None
        else:
            buffer = (ctypes.c_float * list_len)(*value_list)
            pointer = ctypes.byref(buffer)

        libtiepie.GenSetData(self._dev_handle, pointer, list_len)

    @property
    def modes_native_available(self):
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
        return libtiepie.GenIsBurstActive(self._dev_handle) == 1

    @property
    def burst_cnt_min(self):
        return libtiepie.GenGetBurstCountMin(self._dev_handle)

    @property
    def burst_cnt_max(self):
        return libtiepie.GenGetBurstCountMax(self._dev_handle)

    @property
    def burst_cnt(self):
        return libtiepie.GenGetBurstCount(self._dev_handle)

    @burst_cnt.setter
    def burst_cnt(self, value):
        libtiepie.GenSetBurstCount(self._dev_handle, value)

    @property
    def burst_sample_cnt_min(self):
        return libtiepie.GenGetBurstSampleCountMin(self._dev_handle)

    @property
    def burst_sample_cnt_max(self):
        return libtiepie.GenGetBurstSampleCountMax(self._dev_handle)

    @property
    def burst_sample_cnt(self):
        return libtiepie.GenGetBurstSampleCount(self._dev_handle)

    @burst_sample_cnt.setter
    def burst_sample_cnt(self, value):
        libtiepie.GenSetBurstSegmentCount(self._dev_handle, value)

    @property
    def burst_segment_cnt_min(self):
        return libtiepie.GenGetBurstSegmentCountMin(self._dev_handle)

    @property
    def burst_segment_cnt_max(self):
        return libtiepie.GenGetBurstSegmentCountMax(self._dev_handle)

    @property
    def burst_segment_cnt(self):
        return libtiepie.GenGetBurstSegmentCount(self._dev_handle)

    @burst_segment_cnt.setter
    def burst_segment_cnt(self, value):
        libtiepie.GenSetBurstSegmentCount(self._dev_handle, value)
