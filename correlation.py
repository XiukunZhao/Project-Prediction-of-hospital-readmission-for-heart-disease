#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 20:40:18 2017
@author: xiukunzhao

This file is used to check the correlation between raw data and time series data

"""

######### Load raw data #########

import GetRawData

#RawData = GetRawData.GetRawData('Data/raw-1500524529.csv') # 5072 07/19
RawData = GetRawData.GetRawData('Data/raw-1500615438.csv') # 5072 07/20

LowBand = list(RawData.get('data_lo_band'))     # print the first 10 elements of the 'data_hi_band' field               
HighBand = list(RawData.get('data_hi_band'))
IntgrRectRR = list(RawData.get('data_intgr_rect_rr'))   

# StartDate = RawData.get('start_date')
StartT = RawData.get('start_ts')


########### Load time series data ###########

import pandas as pd
import numpy as np

# vitals = pd.read_csv('Data/device-5072-presence-2017-07-19--21.22-05.13/device-5072-presence-2017-07-19--21.22-05.13-vitals.csv') 
vitals = pd.read_csv('Data/device-5072-presence-2017-07-20--22.37-08.06/device-5072-presence-2017-07-20--22.37-08.06-vitals.csv') 
HR = vitals.hr  
RR = vitals.rr  
MR = vitals.act
VTime = vitals.timestamp
NVTime = VTime-int(StartT)

#bedexits = pd.read_csv('Data/device-5072-presence-2017-07-19--21.22-05.13/device-5072-presence-2017-07-19--21.22-05.13-bedexits.csv') 
bedexits = pd.read_csv('Data/device-5072-presence-2017-07-20--22.37-08.06/device-5072-presence-2017-07-20--22.37-08.06-bedexits.csv') 
BTimeStart = bedexits.get('start_timestamp')
BTimeEnd = bedexits.get('end_timestamp')
NBTimeStart = BTimeStart-int(StartT)
NBTimeEnd = BTimeEnd-int(StartT)

#sleepclasses = pd.read_csv('Data/device-5072-presence-2017-07-19--21.22-05.13/device-5072-presence-2017-07-19--21.22-05.13-sleepclasses.csv') 
sleepclasses = pd.read_csv('Data/device-5072-presence-2017-07-20--22.37-08.06/device-5072-presence-2017-07-20--22.37-08.06-sleepclasses.csv') 
SCTime = sleepclasses.get('timestamp')
SC = sleepclasses.get('sleep_class')
NSCTime = SCTime -int(StartT)

#tossnturns = pd.read_csv('Data/device-5072-presence-2017-07-19--21.22-05.13/device-5072-presence-2017-07-19--21.22-05.13-tossnturns.csv') 
tossnturns = pd.read_csv('Data/device-5072-presence-2017-07-20--22.37-08.06/device-5072-presence-2017-07-20--22.37-08.06-tossnturns.csv') 
TTime = tossnturns.get('timestamp')
NTTime = TTime-int(StartT)

############ Cross Correlation ##########
#
#import scipy
#
#IR=IntgrRectRR[::8]
#RB=IR[0:len(MR)]
##np.corrcoef([MR,RB])
#scipy.correlate(MR,RB)

########## Plot ############

import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
#import numpy as np

fig = plt.figure(1,figsize=(20,15),dpi=100)   # all data (raw data and HR, RR, MR)
plt.subplot(411) # raw data
plt.title('Comparison between raw data and HR, RR, MR (2017-07-20)')
line1, = plt.plot((np.arange(0,len(LowBand)*2,2))/100,LowBand,'r-',label="Low Band")
plt.plot((np.arange(0,len(HighBand)))/100,HighBand,'b-',label="High Band")
plt.plot((np.arange(0,len(IntgrRectRR)*50,50))/100,IntgrRectRR,'g-',label="Rectified Band")
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.ylabel('raw data')
plt.subplot(412) # HR data
plt.ylabel('heart rate')
line1, = plt.plot(NVTime,HR,'m-',label="HR")
plt.subplot(413) # RR data
plt.plot(NVTime,RR,'y-',label="RR")
plt.ylabel('breath rate')
plt.subplot(414) # MR data
plt.plot(NVTime,MR,'g-',label="MR")
plt.ylabel('movement rate')
plt.xlabel('time (sec)')


OutBed = np.zeros(int(NVTime[-1:]))
for i in range(len(NBTimeStart)):
    OutBed[NBTimeStart[i]:NBTimeEnd[i]] = 1
TT = np.zeros(int(NVTime[-1:]))
for i in range(len(NTTime)):
    TT[NTTime[i]] = 1

fig = plt.figure(2,figsize=(15,10),dpi=100)   # all data (raw data and bedexits, tossnturns)
plt.subplot(311) # raw data
plt.title('Comparison between raw data and bedexits, tossnturns (2017-07-20)')
line1, = plt.plot((np.arange(0,len(LowBand)*2,2))/100,LowBand,'r-',label="Low Band")
plt.plot((np.arange(0,len(HighBand)))/100,HighBand,'b-',label="High Band")
#plt.plot((np.arange(0,len(IntgrRectRR)*50,50))/10,IntgrRectRR,'g-',label="Rectified Band")
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.ylabel('raw data')
plt.subplot(312) # bedexits (0: in bed, 1: exit from bed)
plt.ylabel('bedexits')
plt.plot(OutBed,'m-')
plt.subplot(313) # tossnturns (0: stable, 1: activity)
plt.plot(TT,'y-')
plt.ylabel('tossnturns')
plt.xlabel('time (sec)')


SS = np.zeros(int(NVTime[-1:]))
for i in range(len(NSCTime)-1):
    if SC[i] == 4:
         SS[NSCTime[i]:NSCTime[i+1]] = 4
    elif SC[i]==3:
         SS[NSCTime[i]:NSCTime[i+1]] = 3
    elif SC[i]==2:
         SS[NSCTime[i]:NSCTime[i+1]] = 2
    elif SC[i]==1:
         SS[NSCTime[i]:NSCTime[i+1]] = 1

fig = plt.figure(3,figsize=(15,10),dpi=100)   # all data (raw data and sleep stage)
plt.subplot(211) # raw data
plt.title('Comparison between raw data and sleep stage (2017-07-20)')
line1, = plt.plot((np.arange(0,len(LowBand)*2,2))/100,LowBand,'r-',label="Low Band")
plt.plot((np.arange(0,len(HighBand)))/100,HighBand,'b-',label="High Band")
#plt.plot((np.arange(0,len(IntgrRectRR)*50,50))/10,IntgrRectRR,'g-',label="Rectified Band")
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.ylabel('raw data')
plt.subplot(212) # sleep stage (4: awake, 3: REM, 2: light, 1: deep)
plt.ylabel('sleep stage')
plt.plot(SS,'g-')
plt.xlabel('time (sec)')
#
#
##fig = plt.figure(4)   # part of data
##plt.subplot(411) # raw data
##plt.title('Comparison between raw data and HR, RR, MR')
##line1, = plt.plot((np.arange(0,len(LowBand)*2,2))/100,LowBand,'r-',label="Low Band")
##plt.plot((np.arange(0,len(HighBand)))/100,HighBand,'b-',label="High Band")
##plt.xlim([7200,10800])
##plt.ylim([0,10800])
##plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
##plt.ylabel('raw data')
##plt.subplot(412) # HR data
##plt.ylabel('heart rate')
##plt.plot(NVTime,HR,'r-',label="HR")
##plt.xlim([7200,10800])
##plt.subplot(413) # RR data
##plt.plot(NVTime,RR,'b-',label="RR")
##plt.ylabel('breath rate')
##plt.xlim([7200,10800])
##plt.subplot(414) # MR data
##plt.plot(NVTime,MR,'g-',label="MR")
##plt.ylabel('movement rate')
##plt.xlim([7200,10800])


