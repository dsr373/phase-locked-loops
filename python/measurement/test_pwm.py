import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency
from utils.gui_utils import set_as_freq, set_as_time, def_input

fontsize = 20

# set constants
mult = int(def_input('Number of cycles', default=50))
# set expected frequency of Arduino
frequency = 980
voltages = np.linspace(1, 5, num=101)

data_dir = 'data/pwm/'
name_root = def_input('Filename root', default='pwm')
fout = open(data_dir + name_root + '.tsv', 'w')
wvout = open('%swaveforms/%s_wv.csv' % (data_dir, name_root), 'w')

fout.write('expected V\tf_A (Hz)\tV_A\tsigma_V_A\tf_B (Hz)\tV_B\tsigma_V_B\n')

# fire up the scope
ps = open_pico()
configure_channel(ps, 'A')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)

(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1/frequency, multiplicity=mult)

# set up the plot
plt.ion()
plt.tight_layout()
fig, [ax, ax1] = plt.subplots(nrows=2, ncols=1, figsize=(12,9))
set_as_time(ax, fontsize=fontsize)
set_as_freq(ax1, fontsize=fontsize)
ax.set_ylim(top=7, bottom=2)
ax1.set_xlim(left=-4*frequency, right=4*frequency)

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

plt.show()

for v in voltages:
    # send duty cycle to arduino
    print("Sending stuff to ARDUINO")
    duty_cycle = v * 255 / 5
    send_command(duty_cycle=duty_cycle)
    configure_channel(ps, 'B', VRange=2*v)

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

    print("FrequencyA = %f Hz;\tv_A = %f +/- %f V" % (freqA, meanA, sigA))
    print("FrequencyB = %f Hz;\tv_B = %f +/- %f V" % (freqB, meanB, sigB))
    fout.write('%.3f\t%.4f\t%.5f\t%.5f\t%.4f\t%.5f\t%.5f\n' % (v, freqA, meanA, sigA, freqB, meanB, sigB))
    wvout.write('expected voltage = %.3f V\n' % v)
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
