======
TiePie
======

TiePie provides a Python interface to the mobile USB-oscilloscopes made by TiePie.

Features
--------

* Uses `libtiepie <https://www.tiepie.com/en/libtiepie-sdk>`_
* Provides access to oscilloscope, signal generator and I2C interface features
* Works with Windows and Linux

Installation
------------

To install the TiePie Interface, run this command in your terminal:

$ pip install tiepie

Note that usage in Windows will require the `TiePie USB driver
version 8.1.9 <https://download.tiepie.com/Drivers/DriverInstall-USB_v8.1.9.exe>`_

Usage
-----

Example for using an oscilloscope device::

    from tiepie import Oscilloscope
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
    # osc.trig_timeout = -1
    # Set record length and sampling frequency
    osc.record_length = 62500
    osc.sample_freq = 100000
    # Start measuring and get the data
    data = osc.measure()


Example for using a generator device::

    from tiepie import Generator
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
