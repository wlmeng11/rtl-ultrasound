#!/usr/bin/env python3
#
# Copyright (C) 2018 William Meng
#
# This file is part of rtlsdr_ultrasound
#
# rtlsdr_ultrasound is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rtlsdr_ultrasound is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rtlsdr_ultrasound.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import *
from scipy.signal import resample
from scipy.signal import hilbert
import time
from datetime import datetime

sdr = RtlSdr()

# configure device
sdr.set_direct_sampling(2) # directly sample Q channel
sdr.center_freq = 8e6
sdr.sample_rate = 2.4e6
sdr.gain = 'auto'

center_freq = sdr.center_freq
sample_rate = sdr.sample_rate
print("center freq = {}".format(center_freq))
print("sample rate = {}".format(sample_rate))
print("gain = {}".format(sdr.gain))


# read samples
samples = sdr.read_samples(256*512)
sdr.close()

# save samples to disk with timestamp
timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
np.save("rtlsdr_timedomain_samples_{}".format(timestamp), samples)

upsampling_factor = 10
resampled = resample(samples, len(samples) * upsampling_factor)
fs = sdr.sample_rate * upsampling_factor
Ts = 1e6/fs # time per sample after resampling, in microseconds
print("fs = {}".format(fs))
print("Ts = {}".format(Ts))
t = np.array([ x * Ts for x in range(len(resampled))])

#I = np.real(resampled)
#Q = np.imag(resampled)
envelope = np.abs(resampled)
#LO_cos = np.cos(2.0*np.pi*center_freq*t)
#LO_sin = np.sin(2.0*np.pi*center_freq*t)
#RF = I*LO_cos - Q*LO_sin

#plt.plot(t, I, label="I")
#plt.plot(t, Q, label="Q")
#plt.plot(t, RF, label="RF")
plt.plot(t, envelope, label="envelope")
plt.xlabel('t (microseconds)')
plt.ylabel('amplitude')
plt.title("HackRF --> RTL SDR center_freq=%d MHz sample_rate=%2f Msps" %
          (center_freq/1.0e6, sample_rate/1.0e6))
plt.legend()
plt.show()
