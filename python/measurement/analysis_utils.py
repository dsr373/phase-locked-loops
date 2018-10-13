from numpy import fft
from scipy import interpolate, optimize
import numpy as np

def basic_frequency(freqs, spectrum):
    """
    Return the frequency corresponding to the peak in the spectrum data
    """
    return freqs[np.argmax(spectrum[1:])]

def frequency(freqs, spectrum):
    """
    :param freqs: array of frequency values, same size as spectrum
    :param spectrum: array of intensity values, usually the output of a fourier transform. Must be same size as freqs
    Find the top frequency in the spectrum by interpolating the spectrum around the largest peak
    """
    
    # find the location of the top frequency, but remove 0 as it's not relevant
    i = np.argmax(spectrum[1:])
    # take a point either side of x. 3 points => can interpolate a quadratic
    idxs = [i-1, i, i+1]
    xs = freqs[idxs]
    ys = spectrum[idxs]

    # interpolate
    f = interpolate.interp1d(xs, ys, kind='quadratic')
    # maximise
    res = optimize.fmin(lambda x: -f(x), freqs[i])

    # the second return value is the extreme value of the function
    return -res[1]
