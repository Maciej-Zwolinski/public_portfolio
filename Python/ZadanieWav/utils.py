import os
import logging
import numpy as np


def wav_to_array(file_name):
    """Reads .wav file and loads data into np.array"""

    logger = logging.getLogger(__name__)
    with open(file_name, "rb") as f:
        f.seek(16, 0)
        n = int.from_bytes(f.read(4), byteorder='little')
        logger.debug(n)
        f.seek(2, 1)
        number_of_channels = int.from_bytes(f.read(2), byteorder='little')
        f.seek(8, 1)
        byte_rate = int(int.from_bytes(f.read(2), byteorder='little') / number_of_channels)
        logger.debug(byte_rate)
        f.seek(24, 0)
        sample_rate = int.from_bytes(f.read(4), byteorder='little')
        logger.debug(sample_rate)
        f.seek(16 + n + 8, 0)
        data_length = int.from_bytes(f.read(4), byteorder='little') / byte_rate
        logger.debug(int(data_length/number_of_channels))
        if byte_rate == 1:
            data_type = np.uint8
        elif byte_rate == 2:
            data_type = np.int16
        else: raise ValueError(f'byte rate out of standard (1,2)')
        data = np.zeros(
            (int(number_of_channels), int(
                data_length / number_of_channels)), dtype=data_type)
        for k in range(int(number_of_channels)):
            for i in range(int(data_length / number_of_channels)):
                data[k][i] = np.int16(int.from_bytes(f.read(byte_rate), byteorder='little'))

    return number_of_channels, sample_rate, data


def array_abs(data):
    """Scales data by max value of a type"""

    scaled_array = np.zeros((data.shape[0], data.shape[1]), dtype=np.float32)
    for channel_number in range(data.shape[0]):
        q = 32768  # max int16 value
        scaled_array[channel_number][:] = np.float32(np.divide(data[channel_number][:], q))

    return scaled_array


def array_relative(data):
    """Scales data by maximal occurring value"""

    scaled_data = np.zeros((data.shape[0], data.shape[1]), dtype=np.float32)
    for channel_number in range(data.shape[0]):
        q = np.amax([np.amax(data[channel_number][:]), np.abs(np.amin(data[channel_number][:]))])
        scaled_data[channel_number][:] = np.float32(np.divide(data[channel_number][:], q))

    return scaled_data


def avg_zerolike_density(data, margin=5, span=40):
    """Calculates density of 'low' signal values within given span over entire data"""

    data_high_low = data.copy()
    for channel_number in range(data.shape[0]):
        for i in range(data.shape[1]):
            data_high_low[channel_number][i] = (abs(data[channel_number][i]) <= abs(margin))

    rolling_average_data = np.zeros((data.shape[0], data.shape[1] - span), dtype=np.float32)
    for channel_number in range(rolling_average_data.shape[0]):
        for i in range(rolling_average_data.shape[1]):
            rolling_average_data[channel_number][i] = np.float32(np.sum(data_high_low[channel_number][i: i + span]) / span)

    return rolling_average_data


def list_rising_and_falling_edges(rolling_average_data, span=40):
    """Detects edges between 'high' and 'low' signal regions"""

    edges_list = list()

    for channel_number in range(rolling_average_data.shape[0]):
        flg = 0
        edges_list[channel_number] = []
        for i in range(rolling_average_data.shape[1] - 1):
            if flg == 0 and rolling_average_data[channel_number][i] >= 0.5:
                flg = 1
                edges_list[channel_number].append(i + span // 2)
            elif flg == 1 and rolling_average_data[channel_number][i] < 0.5:
                flg = 0
                edges_list[channel_number].append(i + span // 2)

    return edges_list


def edge_cleanup(edge_list, sample_rate, tmax=0.1, suspend=100):
    """Pairs up rising and falling edges
       Concatenates neraby 'low' regions
       Checks if concatenated regions aren't too long"""

    clean_edge_data = []
    logger = logging.getLogger(__name__)
    for channel_number in range(len(edge_list)):
        channel_data = edge_list[channel_number]
        paired_edges = []

        for i in range(0, len(channel_data), 2):
            if channel_data[i] != channel_data[-1]:
                time_diff_in_samples = channel_data[i + 1] - channel_data[i]
                if tmax * sample_rate > time_diff_in_samples > suspend:
                    paired_edges.append([channel_data[i], channel_data[i + 1]])
        logger.debug(paired_edges)

        i = 0
        while i < len(paired_edges) - 1:
            if paired_edges[i + 1][0] - paired_edges[i][1] < suspend:
                paired_edges[i][1] = paired_edges[i + 1][1]
                paired_edges.pop(i + 1)
            else:
                i += 1

        logger.debug(paired_edges)
        i = 0
        while i < len(paired_edges) and paired_edges:
            if paired_edges[i][1] - paired_edges[i][0] > tmax * sample_rate:
                paired_edges.pop(i)
            else:
                i += 1

        clean_edge_data.append(paired_edges)

    return clean_edge_data
