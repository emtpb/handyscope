"""This Module demonstrates the continuous mode of the signal generator.

In continuous mode, the generator continuously generates the selected signal
until the generator is stopped. Starting the generator is done using the
function "start()". Stopping the generator is done using the function "stop()".
The current period of the signal that is being generated is not finished, the
output will go immediately to the selected Offset. In order to visualize the
generated signal you need to connect the output of the handyscope with an input
from an external oscilloscope.
"""
from handyscope import Generator
import time

gen = Generator("HS5")  # Initialize HS5 generator device

gen.mode = "continuous"
gen.signal_type = "sine"
gen.amplitude = 2  # 2 V
gen.freq = 1e6  # 1e6 Hz
gen.offset = 1  # 1 V

gen.is_out_on = True

gen.start()
time.sleep(10)  # 10 seconds to generate the signal

gen.stop()
time.sleep(2)  # Wait 2 seconds before python script terminates