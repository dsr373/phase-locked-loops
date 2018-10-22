import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from ..measurement.utils.gui_utils import def_input

FONTSIZE = 20

fin = open('data/loop/loop_pc1.tsv', 'r')

v_As, s_As, f_Bs, s_Bs = [], [], [], []
current_A_means = []
current_B_freqs = []

# the first line is the headings
fin.readline()
run_key = 0

for sline in fin:
    line = sline.strip().split('\t')
    current_key = float(line[0])
    if current_key != run_key:
        # the run has ended
        # process the data in this run
        if current_A_means:
            v_As.append(np.mean(current_A_means))
            f_Bs.append(np.mean(current_B_freqs))
            s_As.append(np.std(current_A_means))
            s_Bs.append(np.std(current_B_freqs))

        # setup for the new run
        run_key = current_key
        current_A_means = [float(line[2])]
        current_B_freqs = [float(line[4])]

    else:
        current_A_means.append(float(line[2]))
        current_B_freqs.append(float(line[4]))

fig, ax = plt.subplots(figsize=(12, 8))
matplotlib.rcParams.update({'errorbar.capsize': 5})
ax.errorbar(f_Bs, v_As, xerr=s_Bs, yerr=s_As, fmt='+', markersize=8)

ax.set_title('Output of VCO', fontsize=FONTSIZE)
ax.set_ylabel('Phase comparator average (V)', fontsize=FONTSIZE)
ax.set_xlabel('Input Frequency (Hz)', fontsize=FONTSIZE)

plt.show()

saveopt = def_input('Save figure? (y/n)', default='n')
if saveopt == 'y':
    figname = raw_input('file name: ')
    fig.savefig('docs/%s.pdf' % figname, bbox_inches='tight')
