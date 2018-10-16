from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import time
from picoscope import ps2000
import pylab as plt
import numpy as np

def open_pico():
    print("Attempting to open Picoscope 2000...")

    ps = ps2000.PS2000()
    # Uncomment this line to use with the 2000a/2000b series
    # ps = ps2000a.PS2000a()

    print("Found the following picoscope:")
    print(ps.getAllUnitInfo())
    return ps

def configure_channel(ps, ch_name, VRange=10):
    # the setChannel command will chose the next largest amplitude
    channelRange = ps.setChannel(ch_name, 'DC', VRange=VRange, VOffset=0.0, enabled=True, BWLimited=False, probeAttenuation=10)
    print("Chosen channel %s range = %d" % (ch_name, channelRange))
    # set the trigger
    # ps.setSimpleTrigger(ch_name, 1.0, 'Falling', timeout_ms=100, enabled=True)
    return channelRange


def configure_sampling(ps, period, multiplicity=100):
    """
    Configure the sampling rate and the duration of a sample.
    :param period: the period of the signal, in seconds, or the duration if not periodic
    :param ps: the picoscope object
    :param multiplicity: the number of periods to capture
    """

    print("\n" + "="*15 + " SAMPLING " + "="*15)

    obs_duration = multiplicity * period
    sampling_interval = obs_duration / 4096

    (actualSamplingInterval, nSamples, maxSamples) = ps.setSamplingInterval(sampling_interval, obs_duration)
    print("Sampling interval = %f ms" % (actualSamplingInterval * 1E3))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    print('='*40 + '\n')
    return (actualSamplingInterval, nSamples, maxSamples)


def alt_configure_sampling(ps, signal_duration):
    """
    Configure the sampling rate and the duration of a sample. Use this when you need really fine frequency data.
    :param signal_duration: the period of the signal, in seconds
    :param ps: the picoscope object
    """

    print("\n" + "="*15 + " ALT SAMPLING " + "="*15)
    signal_freq = 1.0/signal_duration
    sample_freq = 10 * signal_freq
    nSamples = 4096

    (actualSamplingFreq, maxSamples) = ps.setSamplingFrequency(sample_freq, nSamples)
    print("Sampling frequency = %f Hz" % (actualSamplingFreq))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    print('='*44 + '\n')
    return (1.0/actualSamplingFreq, nSamples, maxSamples)


def getData(ps, nSamples, channel='A'):
    ps.runBlock()
    ps.waitReady()
    print("Done waiting for trigger")
    return ps.getDataV(channel, nSamples, returnOverflow=False)
