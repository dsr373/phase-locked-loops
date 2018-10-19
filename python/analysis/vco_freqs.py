import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import csv

from ..measurement.utils.gui_utils import def_input

FONTSIZE = 20

# the measurements are dictionaries from the expected_v to arrays of the measured values
v_in = {}
f_out = {}
results = {}

with open('data/vco/vco_R1M.tsv') as fin:
    reader = csv.reader(fin, delimiter='\t')
    reader.next()   # skip first row - those are the headings

    for row in reader:
        # construct the measurements dict
        exp_v = float(row[0])
        v_A = float(row[2])
        f_B = float(row[4])

        if exp_v in v_in.keys():
            v_in[exp_v].append(v_A)
            f_out[exp_v].append(f_B)
        else:
            v_in[exp_v] = [v_A]
            f_out[exp_v] = [f_B]

xs, ys, sigX, sigY = [], [], [], []
for exp_v in v_in.keys():
    xs.append(np.mean(v_in[exp_v]))
    ys.append(np.mean(f_out[exp_v]))
    sigX.append(np.std(v_in[exp_v]))
    sigY.append(np.std(f_out[exp_v]))

fig, ax = plt.subplots(figsize=(12, 8))
matplotlib.rcParams.update({'errorbar.capsize': 5})
ax.errorbar(xs, ys, yerr=sigY, xerr=sigX, fmt='+', markersize=8)

ax.set_title('Output of VCO', fontsize=FONTSIZE)
ax.set_xlabel('Input Voltage (V)', fontsize=FONTSIZE)
ax.set_ylabel('Output Frequency (Hz)', fontsize=FONTSIZE)
ax.tick_params(labelsize=FONTSIZE-4)
ax.set_xlim(left=-0.1, right=5.1)
plt.show()

saveopt = def_input('Save figure? (y/n)', default='n')
if saveopt == 'y':
    figname = raw_input('file name: ')
    fig.savefig('docs/%s.pdf' % figname, bbox_inches='tight')
