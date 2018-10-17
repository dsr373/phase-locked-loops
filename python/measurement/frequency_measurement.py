import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData, alt_configure_sampling
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency
from utils.gui_utils import set_as_freq, set_as_time

sep = '=' * 15

# fire up the scope
ps = open_pico()
configure_channel(ps, 'A')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

# the frequencies to test
frequencies = [(2**i) for i in range(4, 17)]
numRuns = 5
mult = 100

# open the data file
fout = open('data/freq_test/run5_fine.tsv', 'w')
fout.write('i\texpected (Hz)\tmeasured (Hz)\n')

for (fid, f) in enumerate(frequencies):
    print('\n\n%s %d. testing %.1f Hz %s' % (sep, fid, f, sep))

    wvout = open('data/freq_test/fine_waveform%.1f.csv' % f, 'w')

    # send half-period to arduino
    half_p_us = 5e5/f  # in microseconds
    print("Sending stuff to ARDUINO")
    send_command(half_p=half_p_us)

    (sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p_us/1e6, multiplicity=mult)

    wvout.write('sampling_interval = %.4f ms\n\n' % (sampling_interval * 1e3))

    for run in range(numRuns):
        # read signal
        dataA = getData(ps, nSamples, channel='A')
        wvout.write(', '.join(map(str, dataA)) + '\n')
    
        # do the FT
        spectrum = np.fft.fft(np.array(dataA), nSamples)
        freqs = np.fft.fftfreq(nSamples, sampling_interval)

        f_measured = calc_frequency(freqs, spectrum)
        print('FrequencyA = %f Hz' % f_measured)
        fout.write('%d\t%.5f\t%.5f\n' % (fid*numRuns+run, f, f_measured))
    
    wvout.close()

ps.stop()
ps.close()
fout.close()
