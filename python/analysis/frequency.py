import numpy as np
import matplotlib.pyplot as plt
import csv

with open('data/freq_test/run2.tsv') as fin:
    reader = csv.reader(fin, delimiter='\t')
    reader.next()   # skip first row - those are the headings

    current_exp = 0
    measurements = {}

    for row in reader:
        cur_measured = float(row[2])
        cur_expected = float(row[1])
        if cur_expected not in measurements.keys():
            measurements[cur_expected] = [cur_measured]
        else:
            measurements[cur_expected].append(cur_measured)


expected_fs, measured_fs, sigmas = [], [], []
for exp_f in measurements.keys():
    expected_fs.append(exp_f)
    measured_fs.append(np.mean(measurements[exp_f]))
    sigmas.append(np.std(measurements[exp_f]))

expected_fs, measured_fs, sigmas = np.array(expected_fs), np.array(measured_fs), np.array(sigmas)

print(zip(expected_fs, measured_fs, sigmas))

fig, ax = plt.subplots(figsize=(12, 8))
ax.errorbar(expected_fs, abs(measured_fs-expected_fs)/expected_fs, yerr=sigmas/expected_fs, fmt='+', markersize=15, capthick=15)

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_title('Characteristic of Arduino as signal generator', fontsize=15)
ax.set_xlabel('Expected Frequency (Hz)', fontsize=15)
ax.set_ylabel('Relative error in produced frequency', fontsize=15)

plt.show()
