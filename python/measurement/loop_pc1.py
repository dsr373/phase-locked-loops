import matplotlib.pyplot as plt
import numpy as np
from time import sleep

from utils.pico_utils import open_pico, configure_channel, configure_sampling, alt_configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency
from utils.gui_utils import set_as_freq, set_as_time, def_input

FONTSIZE = 20
SEP = '=' * 20

# set constants
input_frequencies = np.arange(1000, 3000, step=25)
mult = int(def_input('Number of cycles', default=50))
numRuns = int(def_input('Number of runs', default=10))
name_root = def_input('Filename root', default='loop_pc1')
data_dir = 'data/loop/'

# open the files and write a heading
fout = open(data_dir+name_root+'.tsv', 'w')
wvout = open('{0}waveforms/{1}_wv.csv'.format(data_dir, name_root), 'w')

fout.write('f_in\tmean_A (V)\tf_A (Hz)\tmean_B (V)\tf_B (Hz)\n')

# setup the plot
plt.ion()
fig, [ax, ax1] = plt.subplots(nrows=2, ncols=1, figsize=(12,9))
set_as_time(ax, fontsize=FONTSIZE)
set_as_freq(ax1, fontsize=FONTSIZE)
plt.tight_layout()

# fire up the scope
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
ps.setSimpleTrigger('B', 1.0, 'Falling', timeout_ms=100, enabled=True)

old_f = int(1e3)

for freq in input_frequencies:
    print('\n{0} Testing at: {1:.3e} Hz {2}'.format(SEP, freq, SEP))

    # smoothly vary the freq
    # for f in np.arange(old_f, freq, step=5.0):
    #     send_command(half_p=5e5/f)
    #     sleep(0.25)
    # old_f = freq

    # send frequency to arduino
    half_p_us = 5e5/freq    # in microseconds
    print("Sending stuff to ARDUINO")
    send_command(half_p=half_p_us)
    sleep(0.5)

    (sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1.0/freq, multiplicity=mult)
    t = np.linspace(0, sampling_interval*nSamples, num=nSamples)
    ax.set_xlim(left=t[0], right=t[-1])
    ax1.set_xlim(left=-4*freq, right=4*freq)

    wvout.write('sampling interval = {0} us\n'.format(sampling_interval * 1e6))

    for i in range(numRuns):
        # take data
        dataA = getData(ps, nSamples, channel='A')
        dataB = getData(ps, nSamples, channel='B')
        mean_A = np.mean(dataA)
        mean_B = np.mean(dataB)

        # save waveforms
        wvout.write('A\n' + ', '.join(map(str, dataA)) + '\n\n')
        wvout.write('B\n' + ', '.join(map(str, dataB)) + '\n\n')

        # do the FT
        spectrumA = np.fft.fft(np.array(dataA), nSamples)
        spectrumB = np.fft.fft(np.array(dataB), nSamples)
        freqs = np.fft.fftfreq(nSamples, sampling_interval)
        f_B = calc_frequency(freqs, spectrumB)
        f_A = calc_frequency(freqs, spectrumA)
        print("FrequencyA = %f Hz" % f_A)
        print("FrequencyB = %f Hz" % f_B)

        # save the datapoint
        fout.write('{f_in:.4f}\t{mean_A:.5f}\t{f_A:.4f}\t{mean_B:.5f}\t{f_B:.4f}\n'.format(f_in=freq, mean_A=mean_A, f_A=f_A, mean_B=mean_B, f_B=f_B))

        # plot the real signal
        while ax.lines:
            ax.lines.pop()
        ax.plot(t, dataA, label='A', color='C0')
        ax.plot(t, dataB, label='B', color='C1')

        # plot the FT'ed signal
        while(ax1.lines):
            ax1.lines.pop()
        ax1.plot(freqs, abs(spectrumA), label='A', color='C0')
        ax1.plot(freqs, abs(spectrumB), label='B', color='C1')
        plt.pause(0.01)
