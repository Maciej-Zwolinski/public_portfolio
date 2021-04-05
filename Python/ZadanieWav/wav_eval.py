import sys
import os
import argparse
import logging
import copy

import utils

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def generate_low_regions(file_name):
    """Returns a list of 'low' regions boundries"""
    number_of_channels, sample_rate, data = utils.wav_to_array(file_name)
    low_regions = list()
    for span in args.span:
        density_data = utils.avg_zerolike_density(data, span=span)
        edges_list = utils.list_rising_and_falling_edges(density_data, span=span)
        clean_edges = utils.edge_cleanup(edges_list, sample_rate)
        low_regions.append(copy.deepcopy(clean_edges))

    return low_regions, number_of_channels


def boundry_stability_check(low_regions, number_of_channels):
    """Returns boundaries that are stable across all spans"""
    while len(low_regions) > 1:
        for channel_number in range(number_of_channels):
            i = 0
            while i < len(low_regions[0][channel_number]):
                if not (low_regions[0][channel_number][i] in low_regions[1][channel_number][:]):
                    low_regions[0][channel_number].pop(i)
                else:
                    i += 1
            low_regions[1].pop(channel_number)
        low_regions.pop(1)

    return low_regions


def set_flags(stable_boundaries, number_of_channels):
    """Sets corruption flags for channels"""
    flags = list()
    for channel_number in range(number_of_channels):
        if stable_boundaries[0][channel_number]:
            flags.append(0)
        else:
            flags.append(1)

    return flags


def main(args):
    logger = logging.getLogger(__name__)
    logger.debug(args.span)
    assert len(args.span) > 2, "Span too short, at least 2 elements required"

    for file_name in os.listdir(args.datadir):
        if file_name.endswith('.wav'):
            low_regions, number_of_channels = generate_low_regions(os.path.join(args.datadir, file_name))
            stable_boundaries = boundry_stability_check(low_regions, number_of_channels)
            flags = set_flags(stable_boundaries, number_of_channels)

            if (1 in flags) and (0 not in flags):
                logger.info(f'[{file_name}][valid]')
                continue
            elif (1 in flags) and (0 in flags):
                out = f'[{file_name}][partially valid]'
            else:
                out = f'[{file_name}][invalid]'

            for k in range(number_of_channels):
                if flags[k] == 1:
                    out += '[NaN]'
                else:
                    out += f'[{stable_boundaries[0][k][0][0]}]'

            logger.info(f"{out}")

    os.system("pause")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--datadir',
        help='Directory to be checked for .wav file_names. Default "./"',
        default='./')
    parser.add_argument(
        '--span',
        nargs='+',
        type=int,
        help='list of spans across which we check for stability',
        default=[30, 40, 50, 60])
    args = parser.parse_args()

    sys.exit(main(args))
