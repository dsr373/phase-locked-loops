from pico_utils import *

ps = open_pico()
configure_channel(ps, 'A')
(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1)
dataarr = getData(ps, nSamples, channels='AB')
dataA, dataB = dataarr[0], dataarr[1]
ps.stop()
ps.close()

dataTimeAxis = np.arange(nSamples) * sampling_interval

# Uncomment following for call to .show() to not block
# plt.ion()

fig, ax = plt.subplots()
ax.plot(dataTimeAxis, dataA, label="Clock")
ax.grid(True, which='major')
ax.set_title("Picoscope 2000 waveforms")
ax.set_ylabel("Voltage (V)")
ax.set_xlabel("Time (ms)")
ax.legend()
plt.show()
