from numpy import fft
from scipy import interpolate, optimize
import numpy as np
import matplotlib.pyplot as plt

def basic_frequency(freqs, spectrum):
    """
    Return the frequency corresponding to the peak in the spectrum data
    """
    return freqs[np.argmax(spectrum[1:])]

def calc_frequency(freqs, raw_spectrum):
    """
    :param freqs: array of frequency values, same size as spectrum
    :param raw_spectrum: array of intensity values, usually the output of a fourier transform. Must be same size as freqs
    Find the top frequency in the spectrum by interpolating the spectrum around the largest peak
    """
    
    spectrum = np.abs(raw_spectrum)
    # find the location of the top frequency, but remove 0 as it's not relevant
    i = np.argmax(spectrum[1:]) + 1
    # take di points either side of x. 3 points => can interpolate a quadratic
    di = 1
    idxs = [i-j for j in range(di, 0, -1)] + [i] + [i+j+1 for j in range(di)]
    xs = [freqs[i] for i in idxs]
    ys = [spectrum[i] for i in idxs]

    print('indices %s' % idxs)
    print('frequencies %s' % xs)
    print('spectrum %s' % ys)

    # interpolate
    poly = interpolate.BarycentricInterpolator(xs, ys)
    res = optimize.fmin(lambda x : -poly(x), freqs[i], disp=False)
    return abs(res[0])
