import numpy as np
import os

def wav_to_array(file_name):
    """Reads .wav file and loads data into np.array"""

    with open(file_name, "rb") as f:
        f.seek(16,0)
        n=int.from_bytes(f.read(4), byteorder='little')
        # print(n)
        f.seek(2,1)
        num_channels = int.from_bytes(f.read(2), byteorder='little')
        f.seek(8,1)
        Byte_rate = int(int.from_bytes(f.read(2), byteorder='little')/num_channels)
        # print(Byte_rate)
        f.seek(24,0)
        sample_rate=int.from_bytes(f.read(4), byteorder='little')
        #print(sample_rate)
        f.seek(16+n+8,0)
        data_l = int.from_bytes(f.read(4), byteorder='little')/Byte_rate
        # print(int(data_l/num_channels))
        if Byte_rate==1: d_t=np.uint8
        elif Byte_rate==2: d_t=np.int16
        data=np.zeros((int(num_channels),int(data_l/num_channels)),dtype=d_t)
        for k in range(int(num_channels)):
            for i in range(int(data_l/num_channels)):
                data[k][i]= np.int16(int.from_bytes(f.read(Byte_rate), byteorder='little'))
        
    return num_channels, sample_rate, data


def array_abs(data):
    """Scales data by max value of a type"""
    
    x=np.zeros((data.shape[0],data.shape[1]), dtype=np.float32)
    for k in range(data.shape[0]):
        q=32768 #max int16 value
        x[k][:]=np.float32(np.divide(data[k][:],q))

    return x

def array_relative(data):
    """Scales data by maximal occuring value"""
    
    x=np.zeros((data.shape[0],data.shape[1]), dtype=np.float32)
    for k in range(data.shape[0]):
        q=np.amax([np.amax(data[k][:]),np.abs(np.amin(data[k][:]))])
        x[k][:]=np.float32(np.divide(data[k][:],q))

    return x

def avg_zerolike_density(data, margin=5, span=40):
    """Calculates density of 'low' signal values within given span over entire data"""
    
    data_copy=data.copy()
    for k in range(data.shape[0]):
        for l in range(data.shape[1]):
            data_copy[k][l]=(abs(data[k][l])<=abs(margin))

    x=np.zeros((data.shape[0],data.shape[1]-span), dtype=np.float32)
    for k in range(x.shape[0]):
        for l in range(x.shape[1]):
            x[k][l]=np.float32(np.sum(data_copy[k][ l : l+span ])/span)

    return x

def edge_detection(x,span=40):
    """Detects edges between 'high' and 'low' signal regions"""
    
    h=list()

    for k in range(x.shape[0]):
        flg=0
        g=list()
        for i in range(x.shape[1]-1):
            if (flg==0 and x[k][i]>=0.5):
                flg=1
                g.append(i+span//2)
            elif (flg==1 and x[k][i]<0.5):
                flg=0
                g.append(i+span//2)
        h.append(g)

    return h

def edge_cleanup(h,sample_rate,tmax=0.1,suspend=100):
    """Pairs up rising and falling edges
       Concatenates neraby 'low' regions
       Checks if concatenated regions aren't too long"""

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
