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
        result = libtiepie.I2CWrite(self._dev_handle, address, ctypes.byref(buffer), data_len, send_stop)

        return result == 1

    def write_byte(self, address, data_byte):
        result = libtiepie.I2CWriteByte(self._dev_handle, address, data_byte)

        return result == 1

    def write_byte_byte(self, address, data_byte1, data_byte2):
        result = libtiepie.I2CWriteByteByte(self._dev_handle, address, data_byte1, data_byte2)

        return result == 1

    def write_word(self, address, data_word):
        result = libtiepie.I2CWriteWord(self._dev_handle, address, data_word)

        return result == 1

    def write_byte_word(self, address, data_byte, data_word):
        result = libtiepie.I2CWriteByteWord(self._dev_handle, address, data_byte, data_word)

        return result == 1

    def scan(self):
        valid_addresses = []

        # Only check allowed addresses: "Two groups of eight addresses (0000 XXX and 1111 XXX) are reserved"
        # `see official I2C-bus specification and user manual <http://www.nxp.com/documents/user_manual/UM10204.pdf>`_
        for address in range(0x08, 0x77):
            if self.is_internal_address(address):
                continue
            else:
                try:
                    self.write(address, [])
                except OSError as err:
                    # If no ACK was received, there is no device listening on this address
                    if err.args[0] == "[-15]: NO_ACKNOWLEDGE":
                        continue
                # If code didn't raise an exception, i.e. ACK was received, address is valid!
                valid_addresses.append(address)

        return tuple(valid_addresses)
