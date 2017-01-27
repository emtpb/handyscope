from tiepie.library import libtiepie


class I2CHost:
    @property
    def clock_freq_max(self):
        return libtiepie.I2CGetSpeedMax()

    @property
    def clock_freq(self):
        return libtiepie.I2CGetSpeed()

    @clock_freq.setter
    def clock_freq(self, value):
        libtiepie.I2CSetSpeed(value)

    def is_internal_address(self):
        libtiepie.I2CIsInternalAddress()

    def read(self):
        libtiepie.I2CRead()

    def read_byte(self):
        libtiepie.I2CReadByte()

    def read_word(self):
        libtiepie.I2CReadWord()

    def write(self):
        libtiepie.I2CWrite()

    def write_byte(self):
        libtiepie.I2CWriteByte()

    def write_word(self):
        libtiepie.I2CWriteWord()

    def write_byte_word(self):
        libtiepie.I2CWriteByteWord()