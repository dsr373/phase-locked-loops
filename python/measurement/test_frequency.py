from serial_utils import ser
from pico_utils import *

ps = open_pico()
configure_channel(ps, 'A')
configure_channel(ps, 'B')
(sampling_interval, nSamples, maxSamples) = configure_sampling(ps, 1)
dataarr = getData(ps, nSamples, channels='AB')
dataA, dataB = dataarr[0], dataarr[1]
ps.stop()
ps.close()