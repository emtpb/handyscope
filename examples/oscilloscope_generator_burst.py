"""This module demonstrates the oscilloscope for burst signals.

A burst signal is generated to demonstrate how this signal can be recorded
using the built-in oscilloscope of the device.

It is important to note that channel 1 is used and that you need to connect
channel 1 to the signal generator of the device. You can observe the signal
using the internal oscilloscope by having a look at the given plot.
Additionaly an external oscilloscope can be used as well.
"""
import time

import matplotlib.pyplot as plt

from handyscope import Generator
from handyscope import Oscilloscope


gen = Generator("HS5")  # Initialize HS5 generator device

gen.mode = "burst count"
gen.signal_type = "sine"
gen.amplitude = 2  # 2 V
gen.freq = 1e6  # 1 MHz
gen.burst_cnt = 10  # Duration of signal is equivalent to 10 microseconds
gen.is_out_on = True

osc = Oscilloscope("HS5")  # Initialize HS5 oscilloscope device

osc.trig_timeout = -1  # Disable trigger timeout

osc.channels[0].is_enabled = True  # Enable channel 1
osc.channels[0].is_trig_enabled = True
osc.channels[0].trig_kind = "rising"
osc.channels[0].trig_lvl_mode = "absolute"
osc.channels[0].trig_lvl = (1,)  # 1 V (Must be given as tuple)
osc.channels[0].range = 4  # 4 V
osc.pre_sample_ratio = 0.1

osc.sample_freq = 20 * gen.freq
osc.record_length = int(1e-4 * osc.sample_freq)  # Measure for 100 microseconds

osc.start()  # Start measurement

time.sleep(0.3)  # Delay to ensure oscilloscope is armed
gen.start()  # Start generator

while not osc.is_data_ready:
    time.sleep(0.1)

gen.stop()

data = osc.retrieve()[0]  # Data from channel 1
t = osc.time_vector

plt.figure()
plt.plot(t, data)
plt.title("Burst signal recorded by oscilloscope")
plt.xlabel("$t$ in s")
plt.ylabel("$u$ in V")
plt.grid()
plt.autoscale(enable="True", axis="x", tight=True)
plt.show()
