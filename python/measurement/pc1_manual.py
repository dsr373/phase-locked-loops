import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData
from utils.serial_utils import send_command
from utils.analysis_utils import calc_frequency

# set constants
frequency = float(raw_input('Enter frequency (Hz): '))
phase_diff = float(raw_input('Enter phase difference (deg): '))
nRuns = int(raw_input('Number of runs: '))
half_p_us = 5e5/frequency  # in microseconds

# send half-period to arduino
print("Sending to ARDUINO")
send_command(half_p=half_p_us, phase_diff=phase_diff)

# set up scope
print("\n\n")
ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)
(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 2*half_p_us/1e6, multiplicity=10)

# initialise the x axes
t = np.linspace(0, nSamples*sampling_interval, num=nSamples)

# set up plot -- does not work atm
plt.ion()
fig, [ax1, ax2] = plt.subplots(ncols=1, nrows=2)
va_line, = ax1.plot(t, np.zeros(nSamples))
vb_line, = ax1.plot(t, np.zeros(nSamples))
m_line, = ax2.plot(list(range(nRuns)), np.zeros(nRuns))
plt.show()

measured = []

for i in range(nRuns):
    dataA = getData(ps, nSamples, channel='A')
    dataB = getData(ps, nSamples, channel='B')
    # do the FT
    meanA = np.mean(dataA)
    mean = np.mean(dataB)
    print('\nRun %d' % i)
    print('Mean A: %f Volts;\tMean B: %f Volts' % (meanA, mean))

    measured.append(mean)

    va_line.set_ydata(dataA)
    vb_line.set_ydata(dataB)
    plt.draw()

print('='*15 + ' RESULTS ' + '='*15)
print('Measured mean B: %.5f V' % np.mean(measured))
print('Standard deviation: %.5f V' % np.std(measured))

ps.stop()
ps.close()
