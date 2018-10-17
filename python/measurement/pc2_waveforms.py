import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, alt_configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency
from utils.gui_utils import set_as_freq, set_as_time, def_input

fontsize = 20

# set constants
frequency = float(def_input('Frequency in Hz', default=50))
mult = int(def_input('Number of cycles', default=10))
phase_diffs = [0, 30, 45, 60, 90, 135, 170, 180, 190, 225, 270, 315, 350]
half_p_us = 5e5/frequency  # in microseconds

fig_dir = 'docs/pc2/'
data_dir = 'data/pc2/waveforms/'
name_root = def_input('Filename root:', default='deg')

fout = open(data_dir+name_root+'_wv.csv', 'w')

# send half-period to arduino
print("Sending stuff to ARDUINO")
send_command(half_p=half_p_us)

# fire up the scope
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p_us/1e6, multiplicity=mult)
t = np.linspace(0, sampling_interval*nSamples, num=nSamples)

for phase in phase_diffs:
    send_command(phase_diff=phase)

    dataA = getData(ps, nSamples, channel='A')
    dataB = getData(ps, nSamples, channel='B')

    fout.write('phase difference = %d deg\n' % phase)
    fout.write('A\n' + ', '.join(map(str, dataA)) + '\n\n')
    fout.write('B\n' + ', '.join(map(str, dataB)) + '\n\n')

    # # do the FT
    # spectrum = np.fft.fft(np.array(dataA), nSamples)
    # spectrumB = np.fft.fft(np.array(dataB), nSamples)
    # freqs = np.fft.fftfreq(nSamples, sampling_interval)

    # print("FrequencyA = %f Hz" % calc_frequency(freqs, spectrum))
    # print("FrequencyB = %f Hz" % calc_frequency(freqs, spectrumB))

    # plot the real signal
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,8))

    set_as_time(ax, fontsize=fontsize)
    ax.plot(t, dataA, label='A')
    ax.plot(t, dataB, label='B')
    ax.legend(fontsize=fontsize)

    # plot the FT'ed signal
    # set_as_freq(ax1)
    # ax1.plot(freqs, abs(spectrum), label='A')
    # ax1.plot(freqs, abs(spectrumB), label='B')
    # ax1.set_xlim(left=-4*frequency, right=4*frequency)
    # ax1.legend()

    plt.tight_layout()
    fig.savefig('%s%s%d.pdf' % (fig_dir, name_root, phase), bbox_inches='tight')
