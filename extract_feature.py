#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:44:51 2017
@author: xiukunzhao

This file is used to extract features from raw data and calculate 
the heart rate and the breath rate.

Input: raw data and time series data
Output: features within windows and HR, RR comparison 

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

####### Sliding window (Low Band) ##########

# import peakdetect
from libs import detect_peaks

def sliding_window(fseq, window_size = 3000, moving_size = 200):
    WinNum = int((len(fseq) - window_size)/moving_size + 1)
    feature_matrix = np.zeros((WinNum,9))
    
    for i in range(int((len(fseq) - window_size)/moving_size + 1)):
#        yield fseq[i*moving_size:i*moving_size+window_size]
         feature_matrix[i,0] = np.mean(fseq[i*moving_size:i*moving_size+window_size])  # mean
         fseq[i*moving_size:i*moving_size+window_size] = np.subtract(fseq[i*moving_size:i*moving_size+window_size],feature_matrix[i,0])
         feature_matrix[i,1] = np.var(fseq[i*moving_size:i*moving_size+window_size])   # var
         feature_matrix[i,2] = np.mean(np.abs(np.subtract(fseq[i*moving_size:i*moving_size+window_size-1],fseq[i*moving_size+1:i*moving_size+window_size])))   # v
  #       p1 = peakdetect.peakdet(fseq[i*moving_size:i*moving_size+window_size], 30)
  #       feature_matrix[i,2] = math.floor((len(p1[0])+len(p1[1]))/2)
  #       new_p = get_br(0,window_size,1,fseq[i*moving_size:i*moving_size+window_size])
  #       feature_matrix[i,3] = new_p
         p2 = detect_peaks.detect_peaks(fseq[i*moving_size:i*moving_size+window_size], mph=3, mpd=120)
         feature_matrix[i,3] = len(p2)  # peak number (cycle)
         feature_matrix[i,4] = max(fseq[i*moving_size:i*moving_size+window_size])  # max amplitude
         feature_matrix[i,5] = min(fseq[i*moving_size:i*moving_size+window_size])  # min amplitude
         feature_matrix[i,6] = np.mean(np.abs((p2[1:len(p2)]-p2[0:len(p2)-1])))# average of peak distance
         feature_matrix[i,7] = np.std(np.abs((p2[1:len(p2)]-p2[0:len(p2)-1])))/feature_matrix[i,6] # CV of peak distance
         a = 0
         b = 0
         for j in range(i*moving_size,i*moving_size+window_size):
             a+=fseq[j]**2
         for j in range(len(p2)):   
             b+=fseq[p2[j]]**2
         feature_matrix[i,8] = b/a*100
         
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

fig = plt.figure(1, figsize=(20,10),dpi=80)
line1, = plt.plot(np.arange(0,len(RR)*4,4),Feature[len(Feature[:,3])-len(RR)-1:-1,3],'r-',label="our method")
plt.plot(np.arange(0,len(RR)*4,4),RR,'b-',label="emfit's method")
plt.title('Comparison of breath rate between two methods')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.ylabel('breath rate')
plt.xlabel('time (sec)')

#
#fig = plt.figure(2,figsize=(20,10),dpi=80)
#line1, = plt.plot(np.arange(0,len(HR)*4,4),HR,'b-',label="emfit's method")
#plt.plot(np.arange(0,len(HR)*4,4),Feature[len(Feature[:,3])-len(HR)-1:-1,3],'r-',label="our method")
#plt.title('Comparison of heart rate between two methods')
#plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
#plt.ylabel('heart rate')
#plt.xlabel('time (sec)')


fig = plt.figure(3)
plt.scatter(Feature[:,0],Feature[:,1])
plt.xlabel('mean')
plt.ylabel('variance')
plt.title('Feature within each sliding window')

fig = plt.figure(4)
plt.scatter(Feature[:,3],Feature[:,2])
plt.xlabel('the number of cycles')
plt.ylabel('variation')
plt.title('Feature within each sliding window')

fig = plt.figure(5)
plt.scatter(Feature[:,4],Feature[:,8])
plt.xlabel('maximal amplitude of positive peaks')
plt.ylabel('energy stored in positive peaks (%)')
plt.title('Feature within each sliding window')

fig = plt.figure(6)
plt.scatter(Feature[:,6],Feature[:,7])
plt.xlabel('average of distances between two successive positive peaks')
plt.ylabel('coefficient of variation of peak distances')
plt.title('Feature within each sliding window')


########## PCA ############

from sklearn.preprocessing import StandardScaler
F_std = StandardScaler().fit_transform(Feature)
mean_vec = np.mean(F_std, axis=0)
cov_mat = np.cov(F_std.T)
eig_vals, eig_vecs = np.linalg.eig(cov_mat)

for ev in eig_vecs:
    np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
       
tot = sum(eig_vals)
var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp) 

with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(6, 4))

    plt.bar(range(9), var_exp, alpha=0.5, align='center',
            label='individual explained variance')
    plt.step(range(9), cum_var_exp, where='mid',
             label='cumulative explained variance')
    plt.ylabel('Explained variance ratio')
    plt.xlabel('Principal components')
    plt.legend(loc='best')
    plt.tight_layout()


