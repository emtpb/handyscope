from tiepie.library import libtiepie


class Generator:
    @property
    def connector_type(self):
        return libtiepie.GenGetConnectorType()

    @property
    def is_differential(self):
        return libtiepie.GenIsDifferential()

    @property
    def impedance(self):
        return libtiepie.GenGetImpedance()

    @property
    def resolution(self):
        return libtiepie.GenGetResolution()

    @property
    def out_min(self):
        return libtiepie.GenGetOutputValueMin()

    @property
    def out_max(self):
        return libtiepie.GenGetOutputValueMax()

    @property
    def is_controllable(self):
        return libtiepie.GenIsControllable()

    @property
    def status(self):
        return libtiepie.GenGetStatus()

    @property
    def is_out_on(self):
        return libtiepie.GenGetOutputOn()

    @is_out_on.setter
    def is_out_on(self, value):
        libtiepie.GenSetOutputOn(value)

    @property
    def is_out_inv(self):
        return libtiepie.GenGetOutputInvert()

    @is_out_inv.setter
    def is_out_inv(self, value):
        libtiepie.GenSetOutputInvert(value)

    def start(self):
        libtiepie.GenStart()

    def stop(self):
        libtiepie.GenStop()

    @property
    def signal_types_available(self):
        return libtiepie.GenGetSignalTypes()

    @property
    def signal_type(self):
        return libtiepie.GenGetSignalType()

    @signal_type.setter
    def signal_type(self, value):
        libtiepie.GenSetSignalType(value)

    @property
    def amplitude_min(self):
        return libtiepie.GenGetAmplitudeMin()

    @property
    def amplitude_max(self):
        return libtiepie.GenGetAmplitudeMax()

    @property
    def amplitude(self):
        return libtiepie.GenGetAmplitude()

    @amplitude.setter
    def amplitude(self, value):
        libtiepie.GenSetAmplitude(value)

    @property
    def amplitude_ranges_available(self):
        return libtiepie.GenGetAmplitudeRanges()

    @property
    def amplitude_range(self):
        return libtiepie.GenGetAmplitudeRange()

    @amplitude_range.setter
    def amplitude_range(self, value):
        libtiepie.GenSetAmplitudeRange(value)

    @property
    def is_amplitude_autorange(self):
        return libtiepie.GenGetAmplitudeAutoRanging()

    @is_amplitude_autorange.setter
    def is_amplitude_autorange(self, value):
        libtiepie.GenSetAmplitudeAutoRanging(value)

    @property
    def offset_min(self):
        return libtiepie.GenGetOffsetMin()

    @property
    def offset_max(self):
        return libtiepie.GenGetOffsetMax()

    @property
    def offset(self):
        return libtiepie.GenGetOffset()

    @offset.setter
    def offset(self, value):
        libtiepie.GenSetOffset(value)

    @property
    def freq_min(self):
        return libtiepie.GenGetFrequencyMin()

    @property
    def freq_max(self):
        return libtiepie.GenGetFrequencyMax()

    @property
    def freq(self):
        return libtiepie.GenGetFrequency()

    @freq.setter
    def freq(self, value):
        libtiepie.GenSetFrequency(value)

    @property
    def freq_modes_available(self):
        return libtiepie.GenGetFrequencyModes()

    @property
    def freq_mode(self):
        return libtiepie.GenGetFrequencyMode()

    @freq_mode.setter
    def freq_mode(self, value):
        libtiepie.GenSetFrequencyMode(value)

    @property
    def phase_min(self):
        return libtiepie.GenGetPhaseMin()

    @property
    def phase_max(self):
        return libtiepie.GenGetPhaseMax()

    @property
    def phase(self):
        return libtiepie.GenGetPhase()

    @phase.setter
    def phase(self, value):
        libtiepie.GenSetPhase(value)

    @property
    def symmetry_min(self):
        return libtiepie.GenGetSymmetryMin()

    @property
    def symmetry_max(self):
        return libtiepie.GenGetSymmetryMax()

    @property
    def symmetry(self):
        return libtiepie.GenGetSymmetry()

    @symmetry.setter
    def symmetry(self, value):
        libtiepie.GenSetSymmetry(value)

    @property
    def pulse_width_min(self):
        return libtiepie.GenGetWidthMin()

    @property
    def pulse_width_max(self):
        return libtiepie.GenGetWidthMax()

    @property
    def pulse_width(self):
        return libtiepie.GenGetWidth()

    @pulse_width.setter
    def pulse_width(self, value):
        libtiepie.GenSetWidth(value)

    @property
    def arb_data_length_min(self):
        return libtiepie.GenGetDataLengthMin()

    @property
    def arb_data_length_max(self):
        return libtiepie.GenGetDataLengthMax()

    @property
    def arb_data_length(self):
        return libtiepie.GenGetDataLength()

    @property
    def arb_data(self):
        return None

    @arb_data.setter
    def arb_data(self, value):
        libtiepie.GenSetData(value)

    @property
    def modes_native_available(self):
        return libtiepie.GenGetModesNative()

    @property
    def modes_available(self):
        return libtiepie.GenGetModes()

    @property
    def mode(self):
        return libtiepie.GenGetMode()

    @mode.setter
    def mode(self, value):
        libtiepie.GenSetMode(value)

    @property
    def is_burst_active(self):
        return libtiepie.GenIsBurstActive()

    @property
    def burst_cnt_min(self):
        return libtiepie.GenGetBurstCountMin()

    @property
    def burst_cnt_max(self):
        return libtiepie.GenGetBurstCountMax()

    @property
    def burst_cnt(self):
        return libtiepie.GenGetBurstCount()

    @burst_cnt.setter
    def burst_cnt(self, value):
        libtiepie.GenSetBurstCount(value)

    @property
    def burst_sample_cnt_min(self):
        return libtiepie.GenGetBurstSampleCountMin()

    @property
    def burst_sample_cnt_max(self):
        return libtiepie.GenGetBurstSampleCountMax()

    @property
    def burst_sample_cnt(self):
        return libtiepie.GenGetBurstSampleCount()

    @burst_sample_cnt.setter
    def burst_sample_cnt(self, value):
        libtiepie.GenSetBurstSegmentCount(value)

    @property
    def burst_segment_cnt_min(self):
        return libtiepie.GenGetBurstSegmentCountMin()

    @property
    def burst_segment_cnt_max(self):
        return libtiepie.GenGetBurstSegmentCountMax()

    @property
    def burst_segment_cnt(self):
        return libtiepie.GenGetBurstSegmentCount()

    @burst_segment_cnt.setter
    def burst_segment_cnt(self, value):
        libtiepie.GenSetBurstSegmentCount(value)
