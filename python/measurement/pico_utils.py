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

def configure_channel(ps, ch_name):
    # the setChannel command will chose the next largest amplitude
    channelRange = ps.setChannel(ch_name, 'DC', VRange=10, VOffset=0.0, enabled=True, BWLimited=False, probeAttenuation=10)
    print("Chosen channel %s range = %d" % (ch_name, channelRange))
    # set the trigger
    ps.setSimpleTrigger(ch_name, 1.0, 'Falling', timeout_ms=100, enabled=True)


def configure_sampling(ps, desired_duration):
    print("\n" + "="*15 + " SAMPLING " + "="*15)

    obs_duration = 3.0 * desired_duration
    sampling_interval = obs_duration / 4096

    (actualSamplingInterval, nSamples, maxSamples) = ps.setSamplingInterval(sampling_interval, obs_duration)
    print("Sampling interval = %f ms" % (actualSamplingInterval * 1E3))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    return (actualSamplingInterval, nSamples, maxSamples)


def getData(ps, nSamples, channel='A'):
    ps.runBlock()
    ps.waitReady()
    print("Done waiting for trigger on %s" % channel)
    return ps.getDataV(channel, nSamples, returnOverflow=False)
