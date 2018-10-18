import matplotlib.pyplot as plt
import numpy as np
from time import sleep

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency
from utils.gui_utils import set_as_freq, set_as_time, def_input

fontsize = 20
sep = '=' * 15

# set constants
frequency = float(def_input('Expected frequency (Hz)', default=15e3))
mult = int(def_input('Number of cycles', default=50))
nRuns = int(def_input('Number of runs', default=10))
step_size = int(def_input('Step size', default=2))
# set expected frequency of Arduino
pwm_vals = np.arange(0, 255, step_size)

data_dir = def_input('Data directory', default='data/vco/')
name_root = def_input('Filename root', default='vco')
fout = open(data_dir + name_root + '.tsv', 'w')
wvout = open('%swaveforms/%s_wv.csv' % (data_dir, name_root), 'w')

fout.write('expected V\tf_A (Hz)\tV_A\tsigma_V_A\tf_B (Hz)\tV_B\tsigma_V_B\n')

# fire up the scope
ps = open_pico()
configure_channel(ps, 'B')
ps.setSimpleTrigger('B', 1.0, 'Falling', timeout_ms=100, enabled=True)

(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1.0/frequency, multiplicity=mult)

# set up the plot
plt.ion()
fig, [ax, ax1] = plt.subplots(nrows=2, ncols=1, figsize=(12,9))
set_as_time(ax, fontsize=fontsize)
set_as_freq(ax1, fontsize=fontsize)
ax.set_ylim(top=7, bottom=-2)
ax1.set_xlim(left=-4*frequency, right=4*frequency)
ax1.set_ylim(top=1e4, bottom=-10)

# make default plots
t = np.linspace(0, sampling_interval*nSamples, num=nSamples)
freqs = np.fft.fftfreq(nSamples, sampling_interval)

dataA = np.zeros(len(t))
dataB = np.zeros(len(t))
spectrumA = np.zeros(len(freqs))
spectrumB = np.zeros(len(freqs))

# plot the real signal
lineA, = ax.plot(t, dataA, label='A')
lineB, = ax.plot(t, dataB, label='B')

# plot the FT'ed signal
specA, = ax1.plot(freqs, abs(spectrumA), label='A')
specB, = ax1.plot(freqs, abs(spectrumB), label='B')

plt.tight_layout()

for duty_cycle in pwm_vals:
    v = 5.0 * duty_cycle / 255
    print(sep + ' Testing at %.2f V ' % v + sep)

    # send duty cycle to arduino
    print("Sending stuff to ARDUINO")
    send_command(duty_cycle=duty_cycle)

    # configure scope channel
    if v < 1:
        vRange = 1
    else:
        vRange = 2*v
    configure_channel(ps, 'A', VRange=vRange)
    sleep(0.5)

    for run in range(nRuns):
        # measure
        dataA = getData(ps, nSamples, channel='A')
        dataB = getData(ps, nSamples, channel='B')
        
        meanA = np.mean(dataA)
        meanB = np.mean(dataB)
        sigA = np.std(dataA)
        sigB = np.std(dataB)

        # do the FT
        spectrumA = np.fft.fft(np.array(dataA), nSamples)
        spectrumB = np.fft.fft(np.array(dataB), nSamples)
        freqA = calc_frequency(freqs, spectrumA)
        freqB = calc_frequency(freqs, spectrumB)

        print("FrequencyA = %.4e Hz;\tv_A = %f +/- %f V" % (freqA, meanA, sigA))
        print("FrequencyB = %.4e Hz;\tv_B = %f +/- %f V" % (freqB, meanB, sigB))
        fout.write('%.3f\t%.4f\t%.5f\t%.5f\t%.4f\t%.5f\t%.5f\n' % (v, freqA, meanA, sigA, freqB, meanB, sigB))
        wvout.write('input voltage = %.3f V\n' % v)
        wvout.write('A\n' + ', '.join(map(str, dataA)) + '\n\n')
        wvout.write('B\n' + ', '.join(map(str, dataB)) + '\n\n')

        # replot realtime
        lineA.set_ydata(dataA)
        lineB.set_ydata(dataB)
        specA.set_ydata(spectrumA)
        specB.set_ydata(spectrumB)
        plt.pause(0.01)

fout.close()
wvout.close()
ps.stop()
ps.close()
