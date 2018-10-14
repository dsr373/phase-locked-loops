import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency

# set constants
frequency = float(raw_input('Enter frequency (Hz): '))
nRuns = int(raw_input('Number of runs: '))
half_p = 5e5/frequency  # in microseconds

# send half-period to arduino
print("Sending to ARDUINO")
send_command(half_p=half_p)

# set up scope
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p/1e6)
freqs = np.fft.fftfreq(nSamples, sampling_interval)

fig, [ax1, ax2] = plt.subplots(ncols=1, nrows=2)
v_line, = ax1.plot([i*sampling_interval for i in range(nSamples)], np.zeros(nSamples))
f_line, = ax2.plot(freqs, np.zeros(len(freqs)))

for i in range(nRuns):
    dataA = getData(ps, nSamples, channel='A')
    # do the FT
    spectrum = np.fft.fft(np.array(dataA), nSamples)

    fhz = calc_frequency(freqs, spectrum)
    print('Frequency: %f Hz' % fhz)

    v_line.update_ydata(dataA)
    f_line.update_ydata(spectrum)
    fig.canvas.draw()

ps.stop()
ps.close()