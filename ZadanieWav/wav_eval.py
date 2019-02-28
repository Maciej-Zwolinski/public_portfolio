# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 20:28:28 2019

@author: Maciej
"""
import sys
import os
import argparse
import copy

import utils as U

def main(args):
    path=os.getcwd()+args.datadir
    if len(args.span)<2:
        s=[30,40,50,60]
    else: s=args.span
    for file in os.listdir(path):
        if file.endswith('.wav'):
            n,l,sr,data=U.wav_to_array(file)
            p=list()
            for span in s:
                x=U.avg_zerolike_density(data,span=span)
                h=U.edge_detection(x,span=span)
                g=U.edge_cleanup(h,sr)
                p.append(copy.deepcopy(g))

            while len(p)>1:
                for k in range(n):
                    i=0
                    while i < len(p[0][k]):
                        if not (p[0][k][i] in p[1][k][:]):
                            p[0][k].pop(i)
                        else: i+=1
                    p[1].pop(k)
                p.pop(1)

            flg=list()
            for k in range(n):
                if len(p[0][k])==0:
                    flg.append(1)
                else: flg.append(0)

            if (1 in flg) and not(0 in flg):
                out='[file without issues][{}]'.format(file)
                print(out)
                continue
            elif (1 in flg) and (0 in flg):
                out='[file partially corrupted][{}]'.format(file)
            else: 
                out='[corrupted file][{}]'.format(file)

            for k in range(n):
                if flg[k]==1:
                    out+='[NaN]'
                else:
                    out+='{}'.format(p[0][k][0])

            print(out)
      
    os.system("pause")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', help='Directory to be chaecked for .wav files. Default "../"', default ='')
    parser.add_argument('--span', help='list of spans across which we check for stability', default =[30,40,50,60])
    args = parser.parse_args()

    sys.exit(main(args))
