from tiepie.library import libtiepie
from tiepie.device import Device
import ctypes


class I2CHost(Device):
    """Class for an I2CHost.

    An I2CHost is the I2C bus master included in Handyscopes. It is accessible via external connectors (D-Sub).
    """
    _device_type = "I2C"

    def __init__(self, instr_id, id_kind="product id"):
        """Constructor for an I2C host.

        Args:
            instr_id (int or str): Device list index, product ID (listed in dict PRODUCT_IDS) or serial number
            id_kind (str): the kind of the given instr_id (listed in dict ID_KINDS)
        """
        super().__init__(instr_id, id_kind, self._device_type)

    @property
    def clock_freq_max(self):
        """Get the maximum available clock frequency of the I2C clock line.

        Returns:
            int: maximum clock frequency in Hz
        """
        return libtiepie.I2CGetSpeedMax(self._dev_handle)

    @property
    def clock_freq(self):
        """Get or set the current I2C clock frequency in Hz."""
        return libtiepie.I2CGetSpeed(self._dev_handle)

    @clock_freq.setter
    def clock_freq(self, value):
        libtiepie.I2CSetSpeed(self._dev_handle, value)

    def is_internal_address(self, address):
        """Check if given address is used internally.

        Args:
            address (int): I2C address

        Returns:
            bool: True, if given address is internally used; False otherwise.
        """
        return libtiepie.I2CIsInternalAddress(self._dev_handle, address) == 1

    def read(self, address, no_bytes, send_stop=True):
        """Read the given number of bytes from the given address.

        Args:
            address   (int):  I2C address
            no_bytes  (int):  Number of bytes to read
            send_stop (bool): Whether to send a stop bit (defaults to True).

        Returns:
            list of int: List with the received bytes.
        """
        buffer = (ctypes.c_uint8 * no_bytes)()
        libtiepie.I2CRead(self._dev_handle, address, ctypes.byref(buffer), no_bytes, send_stop)
        return list(buffer)

    def read_byte(self, address):
        """Read one byte from the given address.

        Args:
            address (int): I2C address

        Returns:
            int: The received byte.
        """
        buffer = ctypes.c_uint8()
        libtiepie.I2CReadByte(self._dev_handle, address, ctypes.byref(buffer))
        return buffer.value

    def read_word(self, address):
        """Read one word from the given address.

        Args:
            address (int): I2C address

        Returns:
            int: The received word.
        """
        buffer = ctypes.c_uint16()
        libtiepie.I2CReadWord(self._dev_handle, address, ctypes.byref(buffer))
        return buffer.value

    def write(self, address, data, send_stop=True):
        """Write the given data to the address.

        Args:
            address     (int):          I2C address
            data        (list of int):  List of bytes to be writen
            send_stop   (bool):         Whether to send a stop bit (defaults to True).

        Returns:
            bool: True if write succeeded, False otherwise.
        """
        data_len = len(data)
        buffer = (ctypes.c_uint8 * data_len)(*data)
        result = libtiepie.I2CWrite(self._dev_handle, address, ctypes.byref(buffer), data_len, send_stop)

        return result == 1

    def write_byte(self, address, data_byte):
        """Write the given byte to the address.

        Args:
            address   (int): I2C address
            data_byte (int): Data byte to be writen

        Returns:
            bool: True if write succeeded, False otherwise.
        """
        result = libtiepie.I2CWriteByte(self._dev_handle, address, data_byte)

        return result == 1

    def write_byte_byte(self, address, data_byte1, data_byte2):
        """Write the two given bytes to the address.

        Args:
            address    (int): I2C address
            data_byte1 (int): First byte to be writen
            data_byte2 (int): Second byte to be writen

        Returns:
            bool: True if write succeeded, False otherwise.
        """
        result = libtiepie.I2CWriteByteByte(self._dev_handle, address, data_byte1, data_byte2)

        return result == 1

    def write_word(self, address, data_word):
        """Write the given word to the address.

        Args:
            address   (int): I2C address
            data_word (int): Data word to write

        Returns:
            bool: True if write succeeded, False otherwise.
        """
        result = libtiepie.I2CWriteWord(self._dev_handle, address, data_word)

        return result == 1

    def write_byte_word(self, address, data_byte, data_word):
        """Write the given byte and the given word to the address.

        Args:
            address   (int): I2C address
            data_byte (int): Data byte to write
            data_word (int): Data word to write

        Returns:
            bool: True if write succeeded, False otherwise.
        """
        result = libtiepie.I2CWriteByteWord(self._dev_handle, address, data_byte, data_word)

        return result == 1

    def scan(self):
        """Scan for available nodes on the bus.

        Returns:
            tuple of int: valid addresses
        """
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
