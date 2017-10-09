import time
import numpy as np
import json
import os, inspect
from scipy.signal import gausspulse


def _intersample_peak(signal):
    """
    Calculate position of maximum of the given signal

    Args:
        signal: The signal to use.

    Returns:
        float: Position of the maximum.

    """
    signal = np.absolute(signal)
    pos_max = np.argmax(signal)
    pos_max += 0.5 * (signal[pos_max - 1] - signal[pos_max + 1]) / \
               (signal[pos_max - 1] - 2 * signal[pos_max] + signal[pos_max + 1])
    return pos_max


def _load_sync_offset_config():
    """
    Load the known sync offset config.

    Returns:
        dict: Sync offset to Handyscopes.

    """
    path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    if os.name == 'nt':
        path += '\\'
    elif os.name == 'posix':
        path += '/'
    else:
        raise ValueError("Unknown operating system found")
    with open(path+'config.json', 'r') as cfg_file:
        config = json.load(cfg_file)
    return config


def _measurement(gen, osz):
    """
    Take a single measurement on channel 1 and channel 2.

    Returns:
        list: Data of channel 1 and channel 2.

    """
    osz.start()
    gen.start()
    while not osz.is_data_ready:
        time.sleep(0.05)
    data = osz.retrieve_ch1_ch2()
    gen.stop()
    return data


def _save_sync_offset_config(new_config):
    """
    Save the new sync offset config.

    Args:
        new_config: The new config to save.

    """
    path = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    if os.name == 'nt':
        path += '\\'
    elif os.name == 'posix':
        path += '/'
    else:
        raise ValueError("Unknown operating system found")
    with open(path+'config.json', 'w') as cfg_file:
        json.dump(new_config, cfg_file, sort_keys=True, indent=4)


def calculate_sync_offset(gen, osz):
    """
    Calculate the sync offset between channel 1 and channel 2 for the current sample frequency of the oscilloscope
    and save it to file. Calculation is doe with a center frequency of 1 MHz, because there is no real difference for 
    reasonable center frequencies.  

    Args:
        gen: Generator to use.
        osz: Oscilloscope to use.

    Returns:
        float: The calculated sync offset.

    Raises:
        AttributeError: If user aborts the process.
        ValueError: If user gives invalid input.

    """
    print("No sync offset found in the database for the given device and sample frequency. Need to calculate it now. \n"
          "To do this the output channel of the handyscope has to be connected to both channel 1 and channel 2. \n"
          "Please change the assembly to look like this. Be careful to use BNC cables with the same length.")
    inp = input("Choices: \n"
                "c to continue the process, after you finished to rearrange the assembly \n"
                "a to abort the whole process")
    if inp == 'a':
        raise AttributeError("No snyc offset found and calculation was aborted")
    elif inp == 'c':
        # calculate input signal for generator
        t_c = gausspulse("cutoff", 1e6, 1.1, tpr=-40)
        steps = np.arange(-2 * t_c, 2 * t_c, 1 / osz.sample_freq)
        signal = gausspulse(steps, 1e6, 1.1)

        # settings for calculation and save old ones to restore them later
        old_gen_sig_type = gen.signal_type
        gen.signal_type = "arbitrary"
        old_gen_mode = gen.mode
        gen.mode = "burst count"
        old_gen_out_on = gen.is_out_on
        gen.is_out_on = True
        old_gen_burst_cnt = gen.burst_cnt
        gen.burst_cnt = 1
        gen.freq_mode = 'sample'
        old_gen_freq = gen.freq
        gen.freq = osz.sample_freq
        old_gen_amplitude = gen.amplitude
        gen.amplitude = 12
        old_gen_arb_data = gen.arb_data
        gen.arb_data(signal)
        old_osz_res = osz.resolution
        osz.resolution = 12
        old_osz_trig_timeout = osz.trig_timeout
        osz.trig_timeout = 5
        old_osz_ch0_range = osz.channels[0].range
        osz.channels[0].range = 20
        old_osz_ch1_range = osz.channels[1].range
        osz.channels[1].range = 20
        old_osz_ch0_trig_en = osz.channels[0].is_trig_enabled
        osz.channels[0].is_trig_enabled = 0
        old_osz_ch1_trig_en = osz.channels[1].is_trig_enabled
        osz.channels[1].is_trig_enabled = 0
        old_osz_trig_ins_3_en = osz.trig_ins[3].is_enabled
        osz.trig_ins[3].is_enabled = True
        old_osz_record_length = osz.record_length
        osz.record_length = signal.size

        def max_position():
            # retrieve data
            pos_max_ch1 = 0
            pos_max_ch2 = 0
            for mes in range(0, int(1e4)):
                data = _measurement(gen, osz)
                pos_max_ch1 += _intersample_peak(data[0])
                pos_max_ch2 += _intersample_peak(data[1])
                if mes % 500 == 0:
                    print("{} % done".format(int(mes/100)))
            print("100 % done")

            # calculate sync offset
            pos_max_ch1 /= 1e4
            pos_max_ch2 /= 1e4
            offset = pos_max_ch1 - pos_max_ch2
            return round(offset, 2)

        sync_offset = max_position()

        # save the newly calculated sync offset
        current = _load_sync_offset_config()
        try:
            current[str(osz.serial_no)][str(osz.sample_freq)] = sync_offset
        except KeyError:  # no values for this serial are available yet
            current[str(osz.serial_no)] = {str(osz.sample_freq): sync_offset}
        _save_sync_offset_config(current)

        # restore old settings
        gen.signal_type = old_gen_sig_type
        gen.burst_cnt = old_gen_burst_cnt
        gen.mode = old_gen_mode
        gen.is_out_on = old_gen_out_on
        gen.freq = old_gen_freq
        gen.amplitude = old_gen_amplitude
        gen.arb_data = old_gen_arb_data
        osz.resolution = old_osz_res
        osz.trig_timeout = old_osz_trig_timeout
        osz.channels[0].range = old_osz_ch0_range
        osz.channels[1].range = old_osz_ch1_range
        osz.channels[0].is_trig_enabled = old_osz_ch0_trig_en
        osz.channels[1].is_trig_enabled = old_osz_ch1_trig_en
        osz.trig_ins[3].is_enabled = old_osz_trig_ins_3_en
        osz.record_length = old_osz_record_length

        print("Sync offset was successfully calculated and saved for future use. Some variables of generator and "
              "oscilloscope were changed in the process, but should be restored. Eventually this was not done "
              "completely, so be carefully with the next results. \n"
              "Also consider uploading the new config file, for future consistency and easy use for other users of the "
              "same Handyscope.")
        inp = input("Choices: \n"
                    "c to continue with the normal measurement, after you rearranged the assembly back\n"
                    "a to abort the measurement, to adjust the settings.")
        if inp == 'a':
            raise AttributeError("Measurement aborted by user.")
        elif inp == 'c':
            return sync_offset
        else:
            raise ValueError("Invalid option given")
    else:
        raise ValueError("Invalid option given")


def get_sync_offset(gen, osz):
    """
    Get the sync offset for the given serial number and current sample frequency of the oscilloscope. 
    If unknown a new one will be calculated.

    Args:
        gen: The generator to use.
        osz: The oscilloscope to use.

    Returns:
        float: The sync offset of the oscilloscope.

    """
    config = _load_sync_offset_config()
    try:
        return config[str(osz.serial_no)][str(osz.sample_freq)]
    except KeyError:  # no sync offset known
        return calculate_sync_offset(gen, osz)


def measurement_jitter_free(gen, osz, gen_signal, n_avg, pause=0.1):
    """
    Take a measurement and calculate jitter free signal for channel 2. On channel 1 the input signal gets measured and
    on channel 2 the real measurement signal. This then gets corrected using the correlation between both channels,
    which results in jitter free values for channel 2.

    Args:
        gen: The generator to use.
        osz: The oscilloscope to use.
        gen_signal: The output signal of the generator.
        n_avg (int): Amount of measurements to be taken.
        pause (float): Pause between measurements in seconds.

    Returns:
        list: Values of channel 1.
        list: Values of channel 2.
        list: Jitter free values of channel 2.

    """
    ch_1 = []
    ch_2 = []
    jit_free = []
    # get the correct sync offset
    sync_offset = get_sync_offset(gen, osz)
    for mes in range(0, n_avg):
        # take one measurement
        data = _measurement(gen, osz)
        # calculate jitter free signal
        max_pos_x_0 = _intersample_peak(gen_signal)
        max_pos_channel_1 = _intersample_peak(data[0])
        # calculate difference and use the specific sync offset
        diff = max_pos_x_0 - max_pos_channel_1 + sync_offset
        # jitter free signal with 1d interpolation
        jitter_free_cur = np.interp(np.arange(len(data[1])) + diff, np.arange(len(data[1])), data[1])
        # append the current data to the overall
        ch_1.append(np.asanyarray(data[0]))
        ch_2.append(np.asanyarray(data[1]))
        jit_free.append(jitter_free_cur)
        time.sleep(pause)

    return ch_1, ch_2, jit_free
