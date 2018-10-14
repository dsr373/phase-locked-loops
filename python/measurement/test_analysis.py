from analysis_utils import frequency
import matplotlib.pyplot as plt
import numpy as np

with open('data/fourier.csv') as fin:
    lines = fin.readlines()
    lines = [[float(x) for x in line.split(',')] for line in lines]
    data = zip(*lines)
    freqs = list(data[0])
    spectrum = list(data[1])

print(freqs[0:6])
print(spectrum[0:6])

print('Frequency = %f Hz' % frequency(freqs, spectrum))
# frequency(freqs, spectrum)
