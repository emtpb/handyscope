"""This Module demonstrates the burst count mode of the signal generator.

When the generator is started the generator generates a specified number of
periods of the selected signal. When the required number of periods is reached,
the generator stops automatically and the output will go to the selected
Offset. In order to visualize the generated signal you need to connect the
output of the handyscope with an input from an external oscilloscope.
"""
from handyscope import Generator
import time

gen = Generator("HS5")  # Initialize HS5 generator device

gen.mode = "burst count"
gen.signal_type = "sine"
gen.amplitude = 2  # 2 V
gen.freq = 1e6  # 1e6 Hz
gen.offset = 1  # 1 V
gen.burst_cnt = int(5e6)  # Duration of signal is equivalent to 5 seconds

gen.is_out_on = True

gen.start()
time.sleep(10)  # Wait 10 seconds before python script terminates