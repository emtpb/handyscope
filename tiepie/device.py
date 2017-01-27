from tiepie.library import libtiepie


class Device:
    def __init__(self, dev_handle):
        self._dev_handle = dev_handle

    def __del__(self):
        libtiepie.DevClose(self._dev_handle)

    @property
    def driver_ver(self):
        return libtiepie.DevGetDriverVersion()

    @property
    def firmware_ver(self):
        return libtiepie.DevGetFirmwareVersion()

    @property
    def calibration_date(self):
        return libtiepie.DevGetCalibrationDate()

    @property
    def serial_no(self):
        return libtiepie.DevGetSerialVersion()

    @property
    def product_id(self):
        return libtiepie.DevGetProductId()

    @property
    def device_type(self):
        return libtiepie.DevGetType()

    @property
    def long_name(self):
        return libtiepie.DevGetName()

    @property
    def name(self):
        return libtiepie.DevGetNameShort()

    @property
    def short_name(self):
        return libtiepie.DevGetNameShortest()

    @property
    def is_removed(self):
        return libtiepie.DevIsRemoved()

    def dev_close(self):
        libtiepie.DevClose()

    @property
    def trig_ins(self):
        return None

    @property
    def trig_in_cnt(self):
        return libtiepie.DevTrGetInputCount()

    def trig_in_by_id(self):
        libtiepie.DevTrGetInputIndexById()

    @property
    def trig_outs(self):
        return None

    @property
    def trig_out_cnt(self):
        return libtiepie.DevTrGetOutputCount()

    def trig_out_by_id(self):
        libtiepie.DevTrGetOutputIndexById()