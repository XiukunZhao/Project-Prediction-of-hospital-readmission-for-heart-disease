#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:44:51 2017
@author: xiukunzhao

This file is used to find the relationship between peaks of raw signal and heart rate, breath rate

"""

######### Load raw data #########

import GetRawData

RawData = GetRawData.GetRawData('Data/raw-1500524529.csv')

LowBand = list(RawData.get('data_lo_band'))     # print the first 10 elements of the 'data_hi_band' field               
HighBand = list(RawData.get('data_hi_band'))
IntgrRectRR = list(RawData.get('data_intgr_rect_rr'))   

# StartDate = RawData.get('start_date')
StartT = RawData.get('start_ts')


########### Load time series data ###########

import pandas as pd
import numpy as np
#import math

vitals = pd.read_csv('Data/device-5072-presence-2017-07-19--21.22-05.13/device-5072-presence-2017-07-19--21.22-05.13-vitals.csv') 
HR = vitals.hr  
RR = vitals.rr  
MR = vitals.act
VTime = vitals.timestamp
NVTime = VTime-int(StartT)

##### function for find local min and max
#
##def get_localMaxMin(wlen,x):
###    from collections import defaultdict
##    localMin = []
##    localMax = []
##    for i in range(wlen,len(x)-wlen):
##        a = x[i-wlen:i+wlen+1]
##        if (x[i]>=np.amax(a)):
##            localMax.append(i)
##            #plt.plot(widx[i],x[i],'ro')
##        elif(x[i]<=np.amin(a)):
##            localMin.append(i)
##            #plt.plot(widx[i],x[i],'k*')
##    return localMin,localMax
#
##### function for find breath rate by using low band data 
#def get_br(staridx,wsize,fsl,data_low):
#    
#    maxhr = 70 # estimate breath rate
#    fsl_1 = 1/50
#    wlen = int(60/maxhr/fsl_1)
#    endidx = staridx +wsize/fsl
#    
##    widx = np.linspace(0,wsize,wsize/fsl)
#    x =  data_low[int(staridx):int(endidx)]
#    localMin = []
#    localMax = []
#    for i in range(wlen,len(x)-wlen):
#        a = x[i-wlen:i+wlen+1]
#        if (x[i]>=np.amax(a)):
#            localMax.append(i)
#            #plt.plot(widx[i],x[i],'ro')
#        elif(x[i]<=np.amin(a)):
#            localMin.append(i)
#    
#    num_max = len(localMax)
#    num_min = len(localMin)
#     
#    br = math.floor(50*60/wsize*(num_max+num_min)/2)
#
#    return br
# 
#    
######extract breath rate from low band data ########
######### chose a window data
#    
#
#maxhr = 70 # estimate breath rate
##wsize = 60 # size of window (s)
# ## size of neighbour for local max and mix
#
##staridx = 3*3600/fsl
##endidx = staridx +wsize/fsl;
##widx = np.linspace(0,wsize,wsize/fsl)
#
#br=get_br(3*3600*50,3000,1,LowBand)
#print(br)

####### Sliding window (Low Band) ##########

# import peakdetect
from libs import detect_peaks

def sliding_window(fseq, window_size = 3000, moving_size = 200):
    WinNum = int((len(fseq) - window_size)/moving_size + 1)
    feature_matrix = np.zeros((WinNum,6))
    
    for i in range(int((len(fseq) - window_size)/moving_size + 1)):
#        yield fseq[i*moving_size:i*moving_size+window_size]
         feature_matrix[i,0] = np.mean(fseq[i*moving_size:i*moving_size+window_size])
         feature_matrix[i,1] = np.std(fseq[i*moving_size:i*moving_size+window_size])
  #       p1 = peakdetect.peakdet(fseq[i*moving_size:i*moving_size+window_size], 30)
  #       feature_matrix[i,2] = math.floor((len(p1[0])+len(p1[1]))/2)
  #       new_p = get_br(0,window_size,1,fseq[i*moving_size:i*moving_size+window_size])
  #       feature_matrix[i,3] = new_p
         p2 = detect_peaks.detect_peaks(fseq[i*moving_size:i*moving_size+window_size], mph=3, mpd=120)
         feature_matrix[i,2] = len(p2)  
         feature_matrix[i,3] = max(fseq[i*moving_size:i*moving_size+window_size])
         feature_matrix[i,4] = min(fseq[i*moving_size:i*moving_size+window_size])
         a = 0
         b = 0
         for j in range(i*moving_size,i*moving_size+window_size):
             a+=fseq[j]**2
         for j in range(len(p2)):   
             b+=fseq[p2[j]]**2
         feature_matrix[i,5] = b/a*100
         
    return feature_matrix

signal = LowBand#[300000:315000]
Feature = sliding_window(signal)#,1000,100)
#for seq in sliding_window(signal):     # print all features
#    print(seq)


######## Sliding window (High Band) ##########
#
## import peakdetect
#from libs import detect_peaks
#
#def sliding_window(fseq, window_size = 3000, moving_size = 200):
#    WinNum = int((len(fseq) - window_size)/moving_size + 1)
#    feature_matrix = np.zeros((WinNum,4))
#    
#    for i in range(int((len(fseq) - window_size)/moving_size + 1)):
##        yield fseq[i*moving_size:i*moving_size+window_size]
#         feature_matrix[i,0] = np.mean(fseq[i*moving_size:i*moving_size+window_size])
#         feature_matrix[i,1] = np.std(fseq[i*moving_size:i*moving_size+window_size])
#  #       p1 = peakdetect.peakdet(fseq[i*moving_size:i*moving_size+window_size], 30)
#  #       feature_matrix[i,2] = math.floor((len(p1[0])+len(p1[1]))/2)
#  #       new_p = get_br(0,window_size,1,fseq[i*moving_size:i*moving_size+window_size])
#  #       feature_matrix[i,3] = new_p
#         p2 = detect_peaks.detect_peaks(fseq[i*moving_size:i*moving_size+window_size], mph=2, mpd=60)
#         feature_matrix[i,2] = len(p2)          
#         
#    return feature_matrix
#
#signal = HighBand#[300000:315000]
#Feature = sliding_window(signal,6000,400)
##for seq in sliding_window(signal):     # print all features
##    print(seq)



########## Plot ##############

import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

#fig = plt.figure(1)
#line1, = plt.plot(np.arange(0,len(RR)*4,4),Feature[len(Feature[:,2])-len(RR)-1:-1,2],'r-',label="our method")
#plt.plot(np.arange(0,len(RR)*4,4),RR,'b-',label="emfit's method")
#plt.title('Comparison of breath rate between two methods')
#plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
#plt.ylabel('breath rate')
#plt.xlabel('time (sec)')


#fig = plt.figure(2)
#line1, = plt.plot(np.arange(0,len(HR)*4,4),HR,'b-',label="emfit's method")
#plt.plot(np.arange(0,len(HR)*4,4),Feature[len(Feature[:,2])-len(HR)-1:-1,2],'r-',label="our method")
#plt.title('Comparison of heart rate between two methods')
#plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
#plt.ylabel('heart rate')
#plt.xlabel('time (sec)')


fig = plt.figure(3)
plt.scatter(Feature[:,0],Feature[:,1])
plt.xlabel('mean')
plt.ylabel('standard deviation')
plt.title('Feature within each sliding window')

fig = plt.figure(4)
plt.scatter(Feature[:,3],Feature[:,4])
plt.xlabel('maximal amplitude of positive peaks')
plt.ylabel('maximal amplitude of negative peaks')
plt.title('Feature within each sliding window')

fig = plt.figure(5)
plt.scatter(Feature[:,2],Feature[:,5])
plt.xlabel('the number of cycles')
plt.ylabel('energy stored in positive peaks (%)')
plt.title('Feature within each sliding window')
