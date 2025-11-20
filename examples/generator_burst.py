"""This module demonstrates the burst count mode of the signal generator.

When the generator is started the generator generates a specified number of
periods of the selected signal. When the required number of periods is reached,
the generator stops automatically and the output will go to the selected
offset. In order to visualize the generated signal you need to connect the
output of the handyscope with an input from an external oscilloscope.
"""
import time

from handyscope import Generator


gen = Generator("HS5")  # Initialize HS5 generator device

gen.mode = "burst count"
gen.signal_type = "sine"
gen.amplitude = 2  # 2 V
gen.freq = 50  # 50 Hz
gen.offset = 1  # 1 V
gen.burst_cnt = 10  # Duration of signal is equivalent to 0.2 seconds

gen.is_out_on = True

gen.start()
# Output offset for another 0.5 seconds by keeping python script running
time.sleep(0.5)
