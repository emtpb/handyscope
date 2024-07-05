==========
Handyscope
==========

Handyscope provides a Python interface to the mobile USB-oscilloscopes made by TiePie.

This package is inspired by `python-libtiepie <https://www.tiepie.com/en/libtiepie-sdk/python>`_
and acts as an alternative. The main differences are the following:


1. **python-libtiepie** has some constants defined, which can be used to set properties like signal type. However, the user needs to know the names of these constants and they cannot be printed due to actually being numerical (binary) values. In **handyscope**, the values are given as strings and an overview of the available strings is provided in an additional property.
2. The error check is performed automatically after every method call.
3. More easier way of opening of devices.

Example of setting and getting the signal type in **python-libtiepie**::

    # Set the signal type to triangle
    gen.signal_type = libtiepie.ST_TRIANGLE
    # Prints 0x00000010
    print(gen.signal_type)

Example of setting and getting the signal type in **handyscope**::

    # Prints the tuple ('sine', 'triangle', 'square', 'DC', 'noise', 'arbitrary', 'pulse')
    print(gen.signal_types_available)
    # Set the signal type to triangle
    gen.signal_type = "triangle"
    # Prints "triangle"
    print(gen.signal_type)
    
Example of opening a generator device from **python-libtiepie**::

    import libtiepie

    # Search for devices:
    libtiepie.device_list.update()

    # Try to open a generator:
    gen = None
    for item in libtiepie.device_list:
        if item.can_open(libtiepie.DEVICETYPE_GENERATOR):
            gen = item.open_generator()
            if gen:
                break

Example of opening a generator device using **handyscope**::

    from handyscope import Generator

    gen = Generator("HS5") 


Features
--------

* Uses `libtiepie <https://www.tiepie.com/en/libtiepie-sdk>`_
* Provides access to oscilloscope, signal generator and I2C interface features
* Works with Windows and Linux

Installation
------------

To install the Handyscope Interface, run this command in your terminal:

$ pip install handyscope

Note that usage in Windows will require the `TiePie USB driver
version 8.1.9 <https://download.tiepie.com/Drivers/DriverInstall-USB_v8.1.9.exe>`_

Usage
-----

Example for using an oscilloscope device::

    from handyscope import Oscilloscope
    # To initialize as HS3 oscilloscope device
    osc = Oscilloscope("HS3")
    # Set the range of the channels to 4 Volts
    osc.channels[0].range = 4
    osc.channels[1].range = 4
    # Set the trigger kind to rising edge
    osc.channels[0].trig_kind = "rising"
    # Enable the trigger
    osc.channels[0].trig_enabled= True
    # Disable the trigger timeout
    osc.trig_timeout = -1
    # Set record length and sampling frequency
    osc.record_length = 62500
    osc.sample_freq = 100000
    # Start measuring and get the data
    data = osc.measure()


Example for using a generator device::

    from handyscope import Generator
    # To initialize as HS3 generator device
    gen = Generator("HS3")
    # Set the signal type to a sinus wave
    gen.signal_type = "sine"
    # Set the amplitude to 2 Volts
    gen.amplitude = 2
    # Set the frequency to 100 Hz
    gen.freq = 100
    # Enable the output
    gen.is_out_on = True
    # Start the generator
    gen.start()
