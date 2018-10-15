def set_as_time(axes):
    axes.set_title('Time Domain')
    axes.set_xlabel('Time (s)')
    axes.set_ylabel('Voltage (V)')
    axes.set_ylim(bottom=-1, top=7)

def set_as_freq(axes):
    axes.set_title('Fourier Domain')
    axes.set_xlabel('Frequency (Hz)')
    axes.set_ylabel('Intensity')
