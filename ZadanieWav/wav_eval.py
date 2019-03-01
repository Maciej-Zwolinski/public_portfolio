import sys
import os
import argparse
import logging
import copy

import utils

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def gen_low_regions(file):
    """Returns a list of 'low' regions boundries"""
    n_channel,sample_rate,data=utils.wav_to_array(file)
    p=list()
    for span in args.span:
        x=utils.avg_zerolike_density(data,span=span)
        h=utils.edge_detection(x,span=span)
        g=utils.edge_cleanup(h,sample_rate)
        p.append(copy.deepcopy(g))

    return p

def boundry_stability_check(p):
    """Returns boundries that are stable across all spans"""
    while len(p)>1:
        for k in range(n_channel):
            i=0
            while i < len(p[0][k]):
                if not (p[0][k][i] in p[1][k][:]):
                    p[0][k].pop(i)
                else: i+=1
            p[1].pop(k)
        p.pop(1)

    return p

def set_flags(p, n_channels):
    """Sets corruption flags for channels"""
    flg=list()
    for k in range(n_channel):
        if len(p[0][k])==0:
            flg.append(1)
        else: flg.append(0)

    return flg
    

def main(args):
    path=args.datadir
    assert len(args.span)<2, "Span too short, at least 2 elements required"

    for file in os.listdir(path):
        if file.endswith('.wav'):
            p = gen_low_regions(file)
            p = boundry_stability_check(p)
            flg = set_flags(p, n_channels)

            if (1 in flg) and not(0 in flg):
                out=f'[{file}][valid]'
                print(out)
                continue
            elif (1 in flg) and (0 in flg):
                out=f'[{file}][partially valid]'
            else: 
                out=f'[{file}][invalid]'

            for k in range(n_channel):
                if flg[k]==1:
                    out+='[NaN]'
                else:
                    out+=f'{p[0][k][0][0]}'

            logger = logging.getLogger(__name__)
            logger.info(f"{out}")

    os.system("pause")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir',
                        help='Directory to be chaecked for .wav files. Default "./"',
                        default ='./')
    parser.add_argument('--span',
                        nargs='+',
                        type=int,
                        help='list of spans across which we check for stability',
                        default = [30,40,50,60])
    args = parser.parse_args()

    sys.exit(main(args))
