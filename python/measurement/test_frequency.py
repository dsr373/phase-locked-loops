import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData
from utils.serial_utils import send_command

# set constants
frequency = float(raw_input('Enter frequency (Hz): '))
half_p = 5e5/frequency

# send half-period to arduino
print("Sending stuff to ARDUINO")
send_command(half_p=half_p)

# read signal
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')

(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p/1e6)

dataA = getData(ps, nSamples, channel='A')
ps.stop()
ps.close()

# do the FT
spectrum = np.fft.fft(np.array(dataA), nSamples)
freqs = np.fft.fftfreq(nSamples, sampling_interval)

# write to file
with open('data/real.csv', 'w') as fout:
    fout.write('nSamples = %d\n' % nSamples)
    fout.write('sampling_interval = %d\n\n' % sampling_interval)
    for i, datum in enumerate(dataA):
        fout.write('%d, %f\n' % (i, datum))


with open('data/fourier.csv', 'w') as fout:
    for (f, i) in zip(freqs, abs(spectrum)):
        fout.write('%f, %f\n' % (f, i))

# plot the FT'ed signal
fig, ax = plt.subplots()
ax.plot(freqs, abs(spectrum))
ax.set_xlim(left=-2, right=100)
plt.show()
