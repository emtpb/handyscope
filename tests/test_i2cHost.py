import pytest

test_address = 0x09


def test_clock_freq_max(i2c):
    assert type(i2c.clock_freq_max) is float
    assert i2c.clock_freq_max > 0


def test_clock_freq(i2c):
    # Test getter
    assert type(i2c.clock_freq) is float
    assert i2c.clock_freq > 0

    # Test setter
    freqs = [i2c.clock_freq_max/4, i2c.clock_freq_max]
    for freq in freqs:
        i2c.clock_freq = freq
        assert i2c.clock_freq == freq


def test_is_internal_address(i2c):
    # Check if at least one address is internal
    assert any(i2c.is_internal_address(addr) for addr in range(0x08, 0x77))


def test_read(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.read(test_address, 1)
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_read_byte(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.read_byte(test_address)
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_read_word(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.read_word(test_address)
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_write(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.write(test_address, [0x00, 0x01])
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_write_byte(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.write_byte(test_address, 0x00)
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_write_byte_byte(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.write_byte_byte(test_address, 0x00, 0x01)
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_write_word(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.write_word(test_address, 0x0001)
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_write_byte_word(i2c):
    # Try to read an address, should raise error, because no device is connected
    with pytest.raises(OSError) as err:
        i2c.write_byte_word(test_address, 0x0001, 0x02)
        assert err.value.args[0] == "[-14]: NO_ACKNOWLEDGE"


def test_scan(i2c):
    # Assumption: no devices connected
    addresses = i2c.scan()
    assert type(addresses) is tuple
    assert len(addresses) is 0
