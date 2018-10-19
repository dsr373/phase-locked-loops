import matplotlib.pyplot as plt
import numpy as np
from time import sleep

from utils.pico_utils import open_pico, configure_channel, configure_sampling, alt_configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency
from utils.gui_utils import set_as_freq, set_as_time, def_input

fontsize = 20

# set constants
pwm = int(def_input('Duty cycle', default=128))
frequency = float(def_input('Expected Frequency (Hz)', default=1e4))
mult = int(def_input('Number of cycles', default=5))
numRuns = int(def_input('Number of runs', default=5))

fig_dir = 'docs/vco/current/'
data_dir = 'data/vco/current/'
name_root = def_input('Filename root', default='currents')

fout = open(data_dir+name_root+'_wv.csv', 'w')

# send cuty cycle to arduino
print("Sending stuff to ARDUINO")
send_command(duty_cycle=pwm)

# fire up the scope
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1.0/frequency, multiplicity=mult)
t = np.linspace(0, sampling_interval*nSamples, num=nSamples)

plt.ion()
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,8))
set_as_time(ax, fontsize=fontsize)

for i in range(numRuns):

    dataA = getData(ps, nSamples, channel='A')
    dataB = getData(ps, nSamples, channel='B')

    fout.write('run %d\n' % i)
    fout.write('A\n' + ', '.join(map(str, dataA)) + '\n\n')
    fout.write('B\n' + ', '.join(map(str, dataB)) + '\n\n')

    # # do the FT
    # spectrum = np.fft.fft(np.array(dataA), nSamples)
    # spectrumB = np.fft.fft(np.array(dataB), nSamples)
    # freqs = np.fft.fftfreq(nSamples, sampling_interval)

    # print("FrequencyA = %f Hz" % calc_frequency(freqs, spectrum))
    # print("FrequencyB = %f Hz" % calc_frequency(freqs, spectrumB))

    # plot the real signal
    while ax.lines:
        ax.lines.pop()
    ax.plot(t, dataA, label='A', color='C0')
    ax.plot(t, dataB, label='B', color='C1')
    ax.legend(fontsize=fontsize)
    plt.pause(0.01)

    # plot the FT'ed signal
    # set_as_freq(ax1)
    # ax1.plot(freqs, abs(spectrum), label='A')
    # ax1.plot(freqs, abs(spectrumB), label='B')
    # ax1.set_xlim(left=-4*frequency, right=4*frequency)
    # ax1.legend()

    plt.tight_layout()
    fig.savefig('%s%s%d.pdf' % (fig_dir, name_root, i), bbox_inches='tight')
