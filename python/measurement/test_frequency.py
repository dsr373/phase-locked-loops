import matplotlib.pyplot as plt
import numpy as np
import serial

from pico_utils import open_pico, configure_channel, configure_sampling, getData

# send half-period to arduino
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.write("10000")

ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2)
dataarr = getData(ps, nSamples, channels='A')
dataA = dataarr[0]
ps.stop()
ps.close()

spectrum = np.fft.fft(np.array(dataA), nSamples)
freqs = np.fft.fftfreq(nSamples, sampling_interval)

with open('data/real.csv', 'w') as fout:
    fout.write('nSamples = %d\n' % nSamples)
    fout.write('sampling_interval = %d\n\n' % sampling_interval)
    for i, datum in enumerate(dataA):
        fout.write('%d, %f\n' % (i, datum))


with open('data/fourier.csv', 'w') as fout:
    for (f, i) in zip(freqs, abs(spectrum)):
        fout.write('%f, %f\n' % (f, i))

fig, ax = plt.subplots()
ax.plot(freqs, abs(spectrum))
ax.set_xlim(left=-2, right=100)
plt.show()
