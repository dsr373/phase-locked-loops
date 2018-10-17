import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import csv

from ..measurement.utils.gui_utils import def_input

# the measurements is a dictionary from the frequency to a dict
# the inner dict is from the phaseshift to an array of mean Bs
measurements = {}
results = {}

with open('data/pc2/run2.tsv') as fin:
    reader = csv.reader(fin, delimiter='\t')
    reader.next()   # skip first row - those are the headings

    for row in reader:
        # construct the measurements dict
        freq = float(row[1])
        phase = int(row[2])
        vB = float(row[-1])

        if freq in measurements.keys():
            if phase in measurements[freq].keys():
                measurements[freq][phase].append(vB)
            else:
                measurements[freq][phase] = [vB]
        else:
            measurements[freq] = {phase: [vB]}

for freq in measurements.keys():
    results[freq] = {}
    for phase in measurements[freq].keys():
        results[freq][phase] = (np.mean(measurements[freq][phase]), np.std(measurements[freq][phase]))

# all_freqs = sorted(list(results.keys()))
all_freqs = sorted(results.keys())

fig, ax = plt.subplots(figsize=(12, 8))
matplotlib.rcParams.update({'errorbar.capsize': 5})

for freq in all_freqs:
    xs, ys, sigmas = [], [], []
    for phase in results[freq].keys():
        xs.append(phase)
        ys.append(results[freq][phase][0])
        sigmas.append(results[freq][phase][1])

    ax.errorbar(xs, ys, yerr=sigmas, fmt='+', markersize=8, label='%.1e' % freq)

ax.set_title('Output of phase comparator 1', fontsize=15)
ax.set_xlabel('Phase difference (deg)', fontsize=15)
ax.set_ylabel('Average output (V)', fontsize=15)
ax.legend()

plt.show()

saveopt = def_input('Save figure? (y/n)', default='n')
if saveopt == 'y':
    figname = raw_input('file name: ')
    fig.savefig('docs/%s.pdf' % figname, bbox_inches='tight')
