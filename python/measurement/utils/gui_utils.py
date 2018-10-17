def set_as_time(axes, fontsize=20):
    # axes.set_title('Time Domain', fontsize=fontsize)
    axes.set_xlabel('Time (s)', fontsize=fontsize)
    axes.set_ylabel('Voltage (V)', fontsize=fontsize)
    axes.tick_params(labelsize=(fontsize-2))
    axes.set_ylim(bottom=-1, top=7)

def set_as_freq(axes, fontsize=20):
    axes.set_title('Fourier Domain', fontsize=fontsize)
    axes.set_xlabel('Frequency (Hz)', fontsize=fontsize)
    axes.set_ylabel('Intensity', fontsize=fontsize)
    axes.tick_params(labelsize=fontsize-2)

def def_input(prompt, default='0'):
    default = str(default)
    s_in = raw_input(prompt + ' [%s]: ' % default)
    if not s_in:
        return default
    else:
        return s_in
