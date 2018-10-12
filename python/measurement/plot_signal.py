import matplotlib.pyplot as plt
import numpy as np

from pico_utils import open_pico, configure_channel, configure_sampling, getData

ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1)
dataarr = getData(ps, nSamples, channels='AB')
dataA, dataB = dataarr[0], dataarr[1]
ps.stop()
ps.close()

dataTimeAxis = np.arange(nSamples) * sampling_interval

# Uncomment following for call to .show() to not block
# plt.ion()

fig, ax = plt.subplots()
ax.plot(dataTimeAxis, dataA, label="A")
ax.plot(dataTimeAxis, dataB, label="B")
# ax.grid(True, which='major')
ax.set_title("Picoscope 2000 waveforms")
ax.set_ylabel("Voltage (V)")
ax.set_xlabel("Time (ms)")
ax.legend()
plt.show()
