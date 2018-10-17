import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency

sep = '=' * 20
datadir = 'data/pc2/'

# the frequencies to test
frequencies = [(10**i) for i in range(1, 5)]
phase_shifts = np.arange(0, 361, 5)
numRuns = 10

# the output data in memory:
b_means = {}    # dict of tuples. each tuple has 2 arrays: 
                # meanB values and sigma values, one for each phaseshift

# fire up the scope
ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

# open the data file
fout = open(datadir + 'run2.tsv', 'w')
fout.write('i\tf_expected (Hz)\tphase_diff (deg)\tf_measured (Hz)\tmean A (V)\tmean B (V)\n')

for (fid, f) in enumerate(frequencies):
    print('\n\n' + sep*3)
    print('%s %d. testing at %.1f Hz %s' % (sep, fid, f, sep))
    print(sep*3)

    b_means[f] = ([], [])

    wvout = open(datadir + 'waveforms/waveform%d.csv' % (int(f)), 'w')

    # send half-period to arduino
    half_p_us = 5e5/f  # in microseconds
    print("Sending stuff to ARDUINO")
    send_command(half_p=half_p_us)

    (sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p_us/1e6, multiplicity=20)

    wvout.write('sampling_interval = %.5f ms\n\n' % (sampling_interval * 1e3))

    for (phid, phase) in enumerate(phase_shifts):
        print('\n%s %d.%d phase %d degrees %s' % (sep, fid, phid, phase, sep))

        print("Sending phase to ARDUINO")
        send_command(phase_diff=phase)

        at_this_phase = []

        wvout.write('\n\nphase_difference = %d degrees\n' % phase)

        for run in range(numRuns):
            # read signal
            dataA = getData(ps, nSamples, channel='A')
            dataB = getData(ps, nSamples, channel='B')

            # save the output waveforms
            wvout.write(', '.join(map(str, dataB)) + '\n')
        
            # measure the frequency of A
            spectrum = np.fft.fft(np.array(dataA), nSamples)
            freqs = np.fft.fftfreq(nSamples, sampling_interval)
            f_measured = calc_frequency(freqs, spectrum)

            # measure the means
            meanA = np.mean(dataA)
            meanB = np.mean(dataB)
            at_this_phase.append(meanB)

            # save the processed data
            print('FrequencyA = %f Hz;\tmeanA = %f V;\tmeanB = %f V' % (f_measured, meanA, meanB))
            fout.write('%d\t%.5f\t%d\t%.5f\t%.5f\t%.5f\n' % ((fid*len(phase_shifts) + phid)*numRuns+run, f, phase, f_measured, meanA, meanB))
        
        # output results at this phase
        mean_at_this_phase = np.mean(at_this_phase)
        sigma_at_this_phase = np.std(at_this_phase)
        
        print(sep*3)
        print('RESULTS: meanB = %f +/- %f V' % (mean_at_this_phase, sigma_at_this_phase))
        print(sep*3)

        b_means[f][0].append(mean_at_this_phase)
        b_means[f][1].append(sigma_at_this_phase)
    
    wvout.close()

ps.stop()
ps.close()
fout.close()

fig, ax = plt.subplots(figsize=(12,8))
matplotlib.rcParams.update({'errorbar.capsize': 5})
ax.set_title('Output of phase comparator 1', fontsize=15)
ax.set_xlabel('Phase difference (deg)', fontsize=15)
ax.set_ylabel('Average output (V)', fontsize=15)

for key in frequencies:
    ax.errorbar(phase_shifts, b_means[key][0], yerr=b_means[key][1], fmt='+', markersize=15, label=('%.1e Hz' % key))

ax.legend()
plt.show()
