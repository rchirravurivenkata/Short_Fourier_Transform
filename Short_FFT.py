#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Discrete Fourier Transform for sensor data to observe trends in the respiratory rate

Created on Wed Apr 17 14:15:19 2019

@author: rcvenkata

"""

## Dependent packages
from __future__ import division

import pandas

import sys

import matplotlib.pyplot as plt

from skimage import util

import numpy as np 

from scipy import fftpack

import operator


## Take in a file from command line



a = pandas.read_csv(sys.stdin, sep=",")

data = a[['timestamp', ' rresp']].dropna()

## Convert timestamp variable to time in seconds

data.iloc[:, 0] = data.iloc[:, 0]/1024   ### Divide by 1024 to convert to seconds
    
data.iloc[:, 0] = data.iloc[:, 0] - data.iloc[0,0]  ### Subtract the entire timestamp column with the first time period to start the time from 0.0 sec


## we will first plot the data using amplitude vs time. 
    
fig, axis = plt.subplots()
axis.plot(data.iloc[:,0],data.iloc[:, 1] )
axis.set_xlabel('Time in seconds')
axis.set_ylabel('Amplitude of the signal')

fig.savefig('Raw_signal_figure.pdf') ## Raw signal vs time figure is saved in the working directory

### Averaging the windows 


windowSize = 1500 ## which is around 30 seconds of samples as our framerate is 50 hertz

slices = util.view_as_windows(np.array(data.iloc[:, 1]), window_shape=(windowSize,), step=1)


slices_time = util.view_as_windows(np.array(data.iloc[:, 0]), window_shape=(windowSize,), step=1)

### Center each slice 

slices2 = slices.copy()

for i in range(len(slices2)):

    slices2[i] = slices2[i] - slices2[i].mean()
    
## Convert time to hertz/frequency (within windows)
    
  ## divide by 50 as 1 hertz is 50


counts = range(1, len(slices2[1])+1)
counts= [x/50 for x in counts]



## Loop to identify dominant frequencies across each window and save it along with its corresponding time


maxFreqs = []
times = []
for i in range(len(slices2)):
    
    spectrum = abs(np.fft.fft(slices2[i], axis=0)) ## Make a spectrum
    peakInd = np.argmax(spectrum[0:750])
    maxFreqs.append(counts[peakInd])
    times.append(slices_time[i][peakInd])


## Plotting dominant frequencies across time
        
fig = plt.figure(figsize=(20,15))
ax=plt.subplot() 
ax.set_ylim()
ax.plot( times, maxFreqs)
ax.set_xlabel('time (s)')
ax.set_ylabel('frequency (Hz)')

fig.savefig('Dominant_frequency_across_time_plot.pdf')

