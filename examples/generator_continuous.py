"""This module demonstrates the continuous mode of the signal generator.

In continuous mode, the generator continuously generates the selected signal
until the generator is stopped. Starting the generator is done using the
function "start()". Stopping the generator is done using the function "stop()".
The current period of the signal that is being generated is not finished, the
output will go immediately to the selected offset. In order to visualize the
generated signal you need to connect the output of the handyscope with an input
from an external oscilloscope.
"""
import time

from handyscope import Generator


gen = Generator("HS5")  # Initialize HS5 generator device

gen.mode = "continuous"
gen.signal_type = "sine"
gen.amplitude = 2  # 2 V
gen.freq = 50  # 50 Hz
gen.offset = 1  # 1 V

gen.is_out_on = True

gen.start()
time.sleep(1)  # 1 second to generate the signal

gen.stop()
# Output offset for another second by keeping python script running
time.sleep(1)
