import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

from ..measurement.utils.analysis_utils import calc_frequency
from ..measurement.utils.gui_utils import def_input
import line_fit

measured_fs, sigmas = {}, {}

directory = def_input('directory to scan', default='data/freq_test/')
root = def_input('waveform file root', default='waveform')

for filename in os.listdir('data/freq_test/'):
    if filename.startswith(root):
        fin = open(directory + filename)
        print(filename)
        
        exp_f = float(filename[len(root):-4])

        sampling_interval = fin.readline().split(' = ')[1]
        sampling_interval = 1e-6 * float(sampling_interval.split(' ')[0])
        
        concat_data = []

        fin.readline()  # skip one line
        for line in fin.readlines():
            # concatenate all the data
            concat_data += [float(datum) for datum in line.split(', ')]

        spectrum = np.fft.fft(np.array(concat_data))
        freqs = np.fft.fftfreq(len(concat_data), sampling_interval)

        mes_f = calc_frequency(freqs, spectrum)
        print(mes_f)
        measured_fs[exp_f] = mes_f
        sigmas[exp_f] = abs(freqs[2]-freqs[1])

        fin.close()

print(len(measured_fs), len(sigmas))
# print(type(expected_fs[0]), type(measured_fs[0]), type(sigmas[0]))

# turn the dicts into arrays
expected_fs = sorted(measured_fs.keys())
measured_fs = np.array([measured_fs[exp_f] for exp_f in expected_fs])
sigmas = np.array([sigmas[exp_f] for exp_f in expected_fs])
ys = abs(measured_fs - expected_fs)

# a relative errors plot
fig, ax = plt.subplots(figsize=(12, 8))
matplotlib.rcParams.update({'errorbar.capsize': 5})
ax.errorbar(expected_fs, ys/expected_fs, yerr=sigmas/expected_fs, fmt='+', markersize=15)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Expected Frequency (Hz)', fontsize=20)
ax.set_ylabel('Relative error in produced frequency', fontsize=20)
ax.tick_params(labelsize=18)

# and an absolute plot
fig1, ax1 = plt.subplots(figsize=(12, 8))
ax1.errorbar(expected_fs, ys, yerr=sigmas, fmt='+', markersize=15)

# fit lines:
regions = [(2, 6), (7, 14)]
for (imin, imax) in regions:
    # extract the x, y and sigma values
    xval = np.log10(expected_fs[imin:imax+1])
    yval = np.log10(ys[imin:imax+1])
    errval = np.log10(sigmas[imin:imax+1])

    ((m, c), (sigm, sigc)) = line_fit.fit(xval, yval, errs=errval)
    print("\nSection [{0:d} - {1:d}]. Slope {2:.4f} +/- {3:.4f};\tIntercept {4:.4f} +/- {5:.4f}".format(imin, imax, m, sigm, c, sigc))

    yfit = [m * x + c for x in xval]
    ax1.plot(np.power(10, xval), np.power(10, yfit), '-')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Expected Frequency (Hz)', fontsize=20)
ax1.set_ylabel('Error in produced frequency (Hz)', fontsize=20)
ax1.tick_params(labelsize=18)

plt.show()

saveopt = def_input('Save figures? (y/n)', default='n')
if saveopt == 'y':
    name_root = def_input('Filename root?', default='arduino_freq')
    fig.savefig('docs/%s_rel.pdf' % name_root, bbox_inches='tight')
    fig1.savefig('docs/%s_abs.pdf' % name_root, bbox_inches='tight')
