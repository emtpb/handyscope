from tiepie.library import libtiepie
from tiepie.device import Device
import ctypes


class I2CHost(Device):
    _device_type = "I2C"

    def __init__(self, instr_id, id_kind="product id"):
        super().__init__(instr_id, id_kind, self._device_type)

    @property
    def clock_freq_max(self):
        return libtiepie.I2CGetSpeedMax(self._dev_handle)

    @property
    def clock_freq(self):
        return libtiepie.I2CGetSpeed(self._dev_handle)

    @clock_freq.setter
    def clock_freq(self, value):
        libtiepie.I2CSetSpeed(self._dev_handle, value)

    def is_internal_address(self, address):
        return libtiepie.I2CIsInternalAddress(self._dev_handle, address) == 1

    def read(self, address, no_bytes, send_stop=True):
        buffer = (ctypes.c_uint8 * no_bytes)()
        libtiepie.I2CRead(self._dev_handle, address, ctypes.byref(buffer), no_bytes, send_stop)
        return list(buffer)

    def read_byte(self, address):
        buffer = ctypes.c_uint8()
        libtiepie.I2CReadByte(self._dev_handle, address, ctypes.byref(buffer))
        return buffer.value

    def read_word(self, address):
        buffer = ctypes.c_uint16()
        libtiepie.I2CReadWord(self._dev_handle, address, ctypes.byref(buffer))
        return buffer.value

    def write(self, address, data, send_stop=True):
        data_len = len(data)
        buffer = (ctypes.c_uint8 * data_len)(*data)
        libtiepie.I2CWrite(self._dev_handle, address, ctypes.byref(buffer), data_len, send_stop)

    def write_byte(self, address, data_byte):
        libtiepie.I2CWriteByte(self._dev_handle, address, data_byte)

    def write_byte_byte(self, address, data_byte1, data_byte2):
        libtiepie.I2CWriteByteByte(self._dev_handle, address, data_byte1, data_byte2)

    def write_word(self, address, data_word):
        libtiepie.I2CWriteWord(self._dev_handle, address, data_word)

    def write_byte_word(self, address, data_byte, data_word):
        libtiepie.I2CWriteByteWord(self._dev_handle, address, data_byte, data_word)
