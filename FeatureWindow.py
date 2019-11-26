#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:06:07 2017
@author: xiukunzhao

This file is used to analyze features based on the raw csv file. We want to link 
the features from raw data to some concrete data feature (e.g., heart rate), and 
we are also interested in digging new features. 

Sliding windows include features: mean, SD, peak number, amplitude, energy, ...

Input: raw-*.csv file
Output: feature table and figures showing raw data and features

"""

######## Define a function to read the raw csv file ##########

def get_data(emfit_raw_file):
    from collections import defaultdict
    data_dict = defaultdict(list)
        
    with open(emfit_raw_file, 'r') as f: 
        header = f.readline().strip('\r\n').split(',')
        data = f.readline().strip('\r\n').split(',')
    
    idx = 0
    for item in data:
        if (('[' not in item) and (']' not in item)):
            data_dict[header[idx]].append(item)
            if len(data_dict[header[idx]]) == 1:
                idx+=1
        else:
            if '[' in item:
                data_dict[header[idx]].append(item.strip('['))
            else:
                data_dict[header[idx]].append(item.strip(']'))
                idx+=1
    for k,v in data_dict.items(): 
        if len(v) == 1:
            data_dict[k] = v[0]
        else:
            data_dict[k] = map(float,v)
    
    return data_dict


######## Read data ###########

RawData = get_data('Data/raw-1500524529.csv')

LowBand = list(RawData.get('data_lo_band'))     # print the first 10 elements of the 'data_hi_band' field               
HighBand = list(RawData.get('data_hi_band'))
IntgrRectRR = list(RawData.get('data_intgr_rect_rr'))   

StartDate = RawData.get('start_date')
StartTS = RawData.get('start_ts')
#print(StartDate)
#print(StartTS)

from datetime import datetime
import pytz

tz1 = pytz.timezone('US/Eastern')     # Toronto
tz2 = pytz.timezone('US/Pacific')     # San Francisco
DT = datetime.fromtimestamp(1500524529, tz2) 


######## Sliding window ##########

import numpy as np
import peakdetect

def window(fseq, window_size = 1000, moving_size = 100):
    WinNum = int((len(fseq) - window_size)/moving_size + 1)
    Feature = np.zeros((WinNum,6))
    
    for i in range(int((len(fseq) - window_size)/moving_size + 1)):
#        yield fseq[i*moving_size:i*moving_size+window_size]
         Feature[i,0] = np.mean(fseq[i*moving_size:i*moving_size+window_size])
         Feature[i,1] = np.std(fseq[i*moving_size:i*moving_size+window_size])
         p = peakdetect.peakdet(fseq[i*moving_size:i*moving_size+window_size], 60)
         Feature[i,2] = len(p[0])
         Feature[i,3] = len(p[1])
         Feature[i,4] = max(fseq[i*moving_size:i*moving_size+window_size])
         a = 0
         for j in range(i*moving_size,i*moving_size+window_size):
             a+=fseq[j]**2
         Feature[i,5] = (np.sum(p[0]**2)+np.sum(p[1]**2))/a*100
         
    return Feature

signal = LowBand[300000:301500]
#signalH = HighBand[600000:603000:2]
#Feature = window(signal, 500)
for seq in window(signal, 500):
    print(seq)

X = np.abs(signal)/len(signal)*2
Y = np.abs(np.fft.fft(X,len(signal)))


######### Plot ###########
#
#import matplotlib.pyplot as plt
#from matplotlib.legend_handler import HandlerLine2D
#  
#peaks = peakdetect.peakdet(signal, 60)
#peaksH = peakdetect.peakdet(signalH, 60)
#PositiveP = peaks[0]
#NegativeP = peaks[1]
#PositivePH = peaksH[0]
#NegativePH = peaksH[1]
#fig = plt.figure(1)
#plt.title('part of raw data (30 second window)')
#line1, = plt.plot(LowBand[300000:301500],'r-',label="Low Band")
#plt.plot(HighBand[600000:603000:2],'b-',label="High Band")
#plt.plot(PositiveP[:,0],PositiveP[:,1],'og')
#plt.plot(NegativeP[:,0],NegativeP[:,1],'oy')
#plt.plot(PositivePH[:,0],PositivePH[:,1],'oc')
#plt.plot(NegativePH[:,0],NegativePH[:,1],'om')
##plt.plot(IntgrRectRR[12000:12060],'g-',label="Rectified Band")
#plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})





        
               