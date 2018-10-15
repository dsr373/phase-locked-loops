import matplotlib.pyplot as plt
import numpy as np

from utils.pico_utils import open_pico, configure_channel, configure_sampling, getData

ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)
(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1)
dataA = getData(ps, nSamples, channel='A')
dataB = getData(ps, nSamples, channel='B')
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
