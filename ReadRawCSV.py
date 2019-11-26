#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:46:43 2017
@author: xiukunzhao

Function to read raw emfit files (csv file). 
Input: a valid emfit raw-*.csv file
Output: "data_dict", a dictionary containing all the data in the file, indexed by the headers.

"""

## Define a function to read raw csv file
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

## Read data
my_data = get_data('Data/raw-1500524529.csv')
# print(my_data.keys())    # print all the header names
Id = list(my_data.get('id'))
DeviceId = list(my_data.get('device_id'))
PresenceId = list(my_data.get('presence_id'))
StartDate = list(my_data.get('start_date'))

LowBand = list(my_data.get('data_lo_band'))     # print the first 10 elements of the 'data_hi_band' field               
HighBand = list(my_data.get('data_hi_band'))
IntgrRectRR = list(my_data.get('data_intgr_rect_rr'))   

Apnea = list(my_data.get('apnea_markers'))
NocalcBand = list(my_data.get('nocalc_bands'))
PeriodicResp = list(my_data.get('data_periodic_resp'))
StartTS = list(my_data.get('start_ts'))

#print(Id)
#print(DeviceId)
#print(PresenceId)
#print(StartDate)
#print(Apnea)
#print(NocalcBand)
#print(PeriodicResp)
#print(StartTS)

from datetime import datetime
DT = datetime.fromtimestamp(1500524529)  # 1500613701,  1500524529

               
## Plot
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
#import plotly.plotly as py
#import plotly.tools as tls

#fig = plt.figure(figsize=(8, 6), dpi=80)   
fig = plt.figure(1)
plt.title('raw data start from %s' %(DT))
plt.subplot(311)
plt.plot(LowBand,'r-')  
# ax.set_ylim(createLimits(margin,Vab))
plt.ylabel('Low Band')
#plt.xlim([0,5000])
#plt.ylim([-200,200])
plt.subplot(312)
plt.plot(HighBand,'b')
plt.ylabel('High Band')
#plt.xlim([0,5000])
#plt.ylim([-500,500])
plt.subplot(313)
plt.plot(IntgrRectRR,'g')
plt.ylabel('Rectified Band')
#plt.xlim([0,5000])
#plt.ylim([0,1000])

print(len(LowBand))
print(len(HighBand))
print(len(IntgrRectRR))

fig = plt.figure(5)
plt.plot(range(0,len(LowBand)*2,2),LowBand)
plt.plot(range(0,len(HighBand)),HighBand)
plt.plot(range(0,len(IntgrRectRR)*50,50),IntgrRectRR)


import numpy as np
#LB = np.zeros(len(LowBand)*2)
#LB[0:len(LowBand)*2:2]=LowBand[:]
LB = LowBand[0::25]
HB = HighBand[0::50]
RB = IntgrRectRR
np.corrcoef([LB,HB,RB])
#fig = plt.figure(6)
#plt.plot(LB)
#plt.plot(HB)
#plt.plot(RB)

fig = plt.figure(7)
plt.plot(LowBand[200000:215000])


#fig = plt.figure(2)
#plt.title('raw data start from %s' %(DT))
#line1, = plt.plot(LowBand,'r-',label="Low Band")  
#plt.plot(HighBand,'b',label="High Band")
#plt.plot(IntgrRectRR,'g',label="Rectified Band")
#plt.xlim([0,50000])
#plt.ylim([-10,10])
#plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

#fig = plt.figure(3)
#plt.title('raw data start from %s' %(DT))
#plt.subplot(211)
#plt.plot(LowBand,'r-')  
#plt.ylabel('Low Band')
#plt.xlim([300000,305000])
#plt.ylim([-10,10])
#plt.subplot(212)
#plt.plot(HighBand,'b')
#plt.ylabel('High Band')
#plt.xlim([300000,305000])
#plt.ylim([-10,10])
#
#fig = plt.figure(4)
#plt.title('raw data')
#line1, = plt.plot(LowBand,'r-',label="Low Band") 
#plt.plot(HighBand,'b',label="High Band")
#plt.xlim([300000,305000])
#plt.ylim([-20,20])
#plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})




#fig = plt.gcf()
#plotly_fig = tls.mpl_to_plotly(fig)
#plotly_fig['layout']['title'] = 'Simple Subplot Example Title'
#plotly_fig['layout']['margin'].update({'t':10000000})


# plt.plot(HighBand)            # plot



        
               