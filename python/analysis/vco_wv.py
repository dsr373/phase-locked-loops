import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import csv

from ..measurement.utils.gui_utils import def_input
from ..measurement.utils.analysis_utils import calc_frequency

fin = open('data/vco/waveforms/vco2_wv.csv', 'r')

v_As, s_As, f_Bs, s_Bs = [], [], [], []
current_A_means = []
current_B_freqs = []

# the first thing the file should have is the dt
line = fin.readline()
dt = float(line.split(' = ')[1].split(' ')[0]) * 1e-6

# the second line is the first v_in
line = fin.readline()
run_key = float(line.split(' = ')[1].split(' ')[0])

flgA, flgB = False, False

for line in fin:

    if flgA:
        # this line is A channel data, i.e. input
        flgA = False
        dataA = map(float, line.split(', '))
        current_A_means.append(np.mean(dataA))

    if flgB:
        # this line is B channel data, i.e. output
        flgB = False
        dataB = map(float, line.split(', '))
        current_B_freqs += dataB

    if line.startswith('input voltage = '):
        current_key = float(line.split(' = ')[1].split(' ')[0])
        if current_key != run_key:
            # the run is over
            # save your processed data to globals, then empty the lists
            v_As.append(np.mean(current_A_means))
            s_As.append(np.std(current_A_means))

            x_spec = np.fft.fftfreq(len(current_B_freqs), dt)
            y_spec = np.fft.fft(current_B_freqs)
            f_Bs.append(calc_frequency(x_spec, y_spec))
            s_Bs.append(abs(x_spec[2]-x_spec[1]))

            current_A_means, current_B_concat = [], []
            run_key = current_key
    
    elif line == 'A\n':
        # the next line is an A signal
        flgA = True
    
    elif line == 'B\n':
        # the next line is a B signal
        flgB = True

fig, ax = plt.subplots(figsize=(12, 8))
matplotlib.rcParams.update({'errorbar.capsize': 5})
ax.errorbar(v_As, f_Bs, xerr=s_As, yerr=s_Bs, fmt='+', markersize=8)

ax.set_title('Output of VCO', fontsize=20)
ax.set_xlabel('Input Voltage (V)', fontsize=20)
ax.set_ylabel('Output Frequency (Hz)', fontsize=20)

plt.show()

saveopt = def_input('Save figure? (y/n)', default='n')
if saveopt == 'y':
    figname = raw_input('file name: ')
    fig.savefig('docs/%s.pdf' % figname, bbox_inches='tight')
