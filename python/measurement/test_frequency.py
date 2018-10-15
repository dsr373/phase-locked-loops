import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency

# set constants
frequency = float(raw_input('Enter frequency (Hz): '))
half_p_us = 5e5/frequency  # in microseconds

# send half-period to arduino
print("Sending stuff to ARDUINO")
send_command(half_p=half_p_us)

# read signal
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
# configure_channel(ps, 'B')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p_us/1e6)

dataA = getData(ps, nSamples, channel='A')
ps.stop()
ps.close()

# do the FT
spectrum = np.fft.fft(np.array(dataA), nSamples)
freqs = np.fft.fftfreq(nSamples, sampling_interval)

print("Frequency = %f Hz" % calc_frequency(freqs, spectrum))

# write to file
with open('data/real2.csv', 'w') as fout:
    fout.write('nSamples = %d\n' % nSamples)
    fout.write('sampling_interval = %d us\n\n' % (sampling_interval*1e6))
    for i, datum in enumerate(dataA):
        fout.write('%d, %f\n' % (i, datum))


with open('data/fourier2.csv', 'w') as fout:
    for (f, i) in zip(freqs, abs(spectrum)):
        fout.write('%f, %f\n' % (f, i))

# plot the real signal
fig1, ax1 = plt.subplots()
ax1.plot(np.linspace(0, sampling_interval*nSamples, num=nSamples), dataA)

# plot the FT'ed signal
fig, ax = plt.subplots()
ax.plot(freqs, abs(spectrum))
ax.set_xlim(left=-200, right=200)
plt.show()
