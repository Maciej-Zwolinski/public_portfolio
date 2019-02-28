# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 22:12:25 2019

@author: Maciej
"""
import numpy as np
import os

def wav_to_array(file_name):

    with open(file_name, "rb") as f:
        f.seek(16,0)
        n=int.from_bytes(f.read(4), byteorder='little')
        # print(n)
        f.seek(2,1)
        NumChannels = int.from_bytes(f.read(2), byteorder='little')
        f.seek(8,1)
        Byte_rate = int(int.from_bytes(f.read(2), byteorder='little')/NumChannels)
        # print(Byte_rate)
        f.seek(24,0)
        sample_rate=int.from_bytes(f.read(4), byteorder='little')
        #print(sample_rate)
        f.seek(16+n+8,0)
        data_l = int.from_bytes(f.read(4), byteorder='little')/Byte_rate
        # print(int(data_l/NumChannels))
        if Byte_rate==1: d_t=np.uint8
        elif Byte_rate==2: d_t=np.int16
        data=np.zeros((int(NumChannels),int(data_l/NumChannels)),dtype=d_t)
        for k in range(int(NumChannels)):
            for i in range(int(data_l/NumChannels)):
                data[k][i]= np.int16(int.from_bytes(f.read(Byte_rate), byteorder='little'))
        
    return NumChannels, int(data_l/NumChannels), sample_rate, data


def array_abs(data):
    x=np.zeros((data.shape[0],data.shape[1]), dtype=np.float32)
    for k in range(data.shape[0]):
        q=32768
        x[k][:]=np.float32(np.divide(data[k][:],q))

    return x

def array_relative(data):
    x=np.zeros((data.shape[0],data.shape[1]), dtype=np.float32)
    for k in range(data.shape[0]):
        q=np.amax([np.amax(data[k][:]),np.abs(np.amin(data[k][:]))])
        x[k][:]=np.float32(np.divide(data[k][:],q))

    return x

def avg_zerolike_density(data, margin=5, span=40):
    y=data.copy()
    for k in range(data.shape[0]):
        for l in range(data.shape[1]):
            y[k][l]=(abs(data[k][l])<=abs(margin))

    x=np.zeros((data.shape[0],data.shape[1]-span), dtype=np.float32)
    for k in range(x.shape[0]):
        for l in range(x.shape[1]):
            x[k][l]=np.float32(np.sum(y[k][ l : l+span ])/span)

    return x

def edge_detection(x,span=40):
    h=list()

    for k in range(x.shape[0]):
        flg=0
        g=list()
        for i in range(x.shape[1]-1):
            if (flg==0 and x[k][i]>=0.5):
                flg=1
                g.append(i+span//2)
            if (flg==1 and x[k][i]<0.5):
                flg=0
                g.append(i+span//2)
        h.append(g)

    return h

def edge_cleanup(h,sample_rate,tmax=0.1,suspend=100):
    for k in range(len(h)):
        g=h[k]
        f=list()
        l=list()
        for i in range(0,len(g),2):
            if g[i]!=g[-1]:
                t=g[i+1] - g[i]
                if t<tmax*sample_rate and t>suspend:
                    f.append([g[i], g[i+1]])
        # print(f)
        i=0
        while i <len(f)-1:
            if f[i+1][0]-f[i][1]<suspend:
                f[i][1]=f[i+1][1]
                f.pop(i+1)
            else: i+=1

        # print(f)
        i=0
        while i<len(f) and len(f)!=0:
            if f[i][1]-f[i][0]>tmax*sample_rate:
                f.pop(i)
            else: i+=1

        l.append(f)

    return l

'''
dev corner

     
n,l,sr,data=wav_to_array("D:/Python/Projekty/Samsung/nan-ai-file-2.wav") 
s=40  
x=avg_zerolike_density(data,span=s)
h=edge_detection(x,span=s)

g=edge_cleanup(h,sr)
print(g)
'''












