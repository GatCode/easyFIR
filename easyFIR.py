#!/usr/bin/env python3

from scipy.signal import lfilter, firwin, freqz
import matplotlib.pyplot as plt
from numpy import genfromtxt
from math import pi
import numpy as np
import sys
import csv

# ------------------------------------------------------------------------------
# ONLY CHANGE THE FOLLOWING 5 PARAMETERS
# ------------------------------------------------------------------------------
filter_type = 3 # 1 = Lowpass, 2 = Highpass, 3 = Bandpass, 4 = Bandstop
filter_order = 300 # number of coefficients in the output String
sampling_frequency = 800 # in Hz
cutoff_frequency_1 = 40 # in Hz
cutoff_frequency_2 = 60 # in Hz - only needed if Bandpass filter selected

# ------------------------------------------------------------------------------
# DO NOT CHANGE SOMETHING BELOW
# ------------------------------------------------------------------------------
def createLowpassFilter(order, fs, fc):
    w_c = 2 * fc / fs
    return firwin(order, w_c, window='hamming', pass_zero='lowpass')

def createHighpassFilter(order, fs, fc):
    w_c = 2 * fc / fs
    return firwin(order, w_c, window='hamming', pass_zero='highpass')

def createBandpassFilter(order, fs, fc_1, fc_2):
    w_c_1 = 2 * fc_1 / fs
    w_c_2 = 2 * fc_2 / fs
    return firwin(order, [w_c_1, w_c_2], window='hamming', pass_zero='bandpass')

def createBandstopFilter(order, fs, fc_1, fc_2):
    w_c_1 = 2 * fc_1 / fs
    w_c_2 = 2 * fc_2 / fs
    return firwin(order, [w_c_1, w_c_2], window='hamming', pass_zero='bandstop')

# idea copied from:
# https://en.wikipedia.org/wiki/Finite_impulse_response
# https://stackoverflow.com/questions/20917019/how-to-implement-a-filter-like-scipy-signal-lfilter
def applyFilter(data, coefficients):
    N = len(coefficients)
    res = []
    for n,_ in enumerate(data):
        y = 0
        for i in range(N):
            if n < i:
                break
            y += coefficients[i] * data[n-i]
        res.append(y)
    return res

# Read CSV Data
yAxis = genfromtxt(str(sys.argv[1]), delimiter=',', dtype=None)
xAxis = [i for i in range(len(yAxis))]
plt.subplot(3, 1, 1)
plt.plot(xAxis,yAxis)
plt.title('easyFIR\n', fontweight='bold')
plt.xlabel('Samples over time')
plt.ylabel('Amplitude')

# Create Filter
filterCoefficients = []
if filter_type == 1:
    filterCoefficients = createLowpassFilter(filter_order, sampling_frequency, cutoff_frequency_1)
elif filter_type == 2:
    filterCoefficients = createHighpassFilter(filter_order, sampling_frequency, cutoff_frequency_1)
elif filter_type == 3:
    filterCoefficients = createBandpassFilter(filter_order, sampling_frequency, cutoff_frequency_1, cutoff_frequency_2)
else:
    filterCoefficients = createBandstopFilter(filter_order, sampling_frequency, cutoff_frequency_1, cutoff_frequency_2)

output = "{"
for coefficient in filterCoefficients:
    output = output + "{0:.20f}".format(coefficient) + ","
output = output[:-1]
output = output + "}"
print(output)

# Frequency Resonse
plt.subplot(3, 1, 2)
w, h = freqz(filterCoefficients)
w = sampling_frequency * w / (2 * pi)
h_db = 20 * np.log10(abs(h))
plt.plot(w, h_db)
plt.xlabel('Frequency (Hz)\n')
plt.ylabel('Magnitude (db)')
plt.grid('on')

# Filtered Signal:
plt.subplot(3, 1, 3)
yAxisFiltered = applyFilter(yAxis, filterCoefficients)
plt.plot(xAxis, yAxisFiltered)
plt.xlabel('Samples over time')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
