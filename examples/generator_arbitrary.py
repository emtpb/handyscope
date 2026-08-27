"""
Example script to generate and output a Gaussian-modulated sinusoidal pulse
using the HS5 arbitrary waveform generator.
"""

from handyscope import Generator
import numpy as np
import scipy.signal as sci


f_c = 0.8e6       # Center frequency in Hz
f_s = 100e6       # Sampling frequency in Hz
duration = 30e-6  # Pulse duration in s

# Create time vector and generate Gaussian-modulated pulse
t = np.arange(-duration/2, duration/2, 1/f_s)
pulse = sci.gausspulse(t, fc=f_c, bw=0.7, bwr=-6)

# Normalize pulse amplitude to ±1
pulse /= np.max(np.abs(pulse))

# Configure HS5 arbitrary waveform generator
gen = Generator("HS5")
gen.mode = "burst count"
gen.signal_type = "arbitrary"
gen.amplitude = 12
gen.freq_mode = "signal"
gen.burst_cnt = 1

# Set frequency according to waveform length and sampling rate
gen.freq = f_s / len(pulse)

# Upload waveform and start output
gen.is_out_on = True
gen.arb_data(pulse)
gen.start()
