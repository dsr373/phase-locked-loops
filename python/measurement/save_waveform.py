import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, alt_configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency
from utils.gui_utils import set_as_freq, set_as_time, def_input

# set constants
frequency = float(def_input('Frequency in Hz', default=50))
phase_diff = int(def_input('Phase difference in deg', default=90))
mult = int(def_input('Number of cycles', default=10))
half_p_us = 5e5/frequency  # in microseconds

# send half-period to arduino
print("Sending stuff to ARDUINO")
send_command(half_p=half_p_us, phase_diff=phase_diff)

# read signal
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p_us/1e6, multiplicity=mult)

dataA = getData(ps, nSamples, channel='A')
dataB = getData(ps, nSamples, channel='B')
ps.stop()
ps.close()

# do the FT
spectrum = np.fft.fft(np.array(dataA), nSamples)
spectrumB = np.fft.fft(np.array(dataB), nSamples)
freqs = np.fft.fftfreq(nSamples, sampling_interval)

print("FrequencyA = %f Hz" % calc_frequency(freqs, spectrum))
print("FrequencyB = %f Hz" % calc_frequency(freqs, spectrumB))

# plot the real signal
t = np.linspace(0, sampling_interval*nSamples, num=nSamples)
fig, [ax, ax1] = plt.subplots(nrows=2, ncols=1, figsize=(12,9))

set_as_time(ax)
ax.plot(t, dataA, label='A')
ax.plot(t, dataB, label='B')
ax.legend()

# plot the FT'ed signal
set_as_freq(ax1)
ax1.plot(freqs, abs(spectrum), label='A')
ax1.plot(freqs, abs(spectrumB), label='B')
ax1.set_xlim(left=-4*frequency, right=4*frequency)
ax1.legend()

plt.tight_layout()
plt.show()

saveopt = def_input('Save data? a=ch A, b=ch B, f=figure', default='')
if 'a' in saveopt or 'b' in saveopt:
    outfile = raw_input('waveform filename: ')
    with open('data/'+outfile, 'w') as fout:
        fout.write('sampling_interval = %.4e us\n\n' % (sampling_interval * 1e6))
        if 'a' in saveopt:
            fout.write('A\n' + ', '.join(map(str, dataA)) + '\n\n')
        if 'b' in saveopt:
            fout.write('B\n' + ', '.join(map(str, dataB)) + '\n\n')

if 'f' in saveopt:
    outfile = raw_input('figure filename: ')
    fig.savefig('docs/'+outfile, bbox_inches='tight')
