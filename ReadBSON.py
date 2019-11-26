#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 17:46:33 2017
@author: xiukunzhao

Function to read structured json and bson files. 
Input: a valid emfits hk-*.json file or hk-*.bson.

"""

## Read json file
import json           
db = json.load(open('hk-body-masses.metadata.json'))
len(db)
list(db.get('indexes'))[0]

## Read bson file
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['test']
collection = db.emfits
import pprint
pprint.pprint(collection.find_one())
collection.count()       # count documents
list(collection.index_information())   # show id










"""
This is function to export feature from mongodb bson
input: device id
output: Feature
"""
from pymongo import MongoClient
import pprint
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

def get_feature_from_mongo(device):

    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client['test']
    collection = db.emfits

    
    sttime = np.array([])
    avg_hr = np.array([])
    avg_rr = np.array([])
    tossnturn = np.array([])
    min_hr = np.array([])
    max_hr = np.array([])
    min_rr = np.array([])
    max_rr = np.array([])
    hrv_rmssd_ev = np.array([])
    hrv_rmssd_mo = np.array([])
    count =0
    for record in collection.find({"device":device}):
        if count==0:
##            print(record.keys())
##            rmssddata = np.array(record.get('hrv_rmssd_data'))
##            print(rmssddata[1])
 
            count = count+1 
        sttime = np.append(sttime,record.get('from'))
        
        avg_hr = np.append(avg_hr,record.get('avg_hr'))

        max_hr = np.append(max_hr,record.get('max_hr'))
        min_hr = np.append(min_hr,record.get('min_hr'))
        hrv_rmssd_mo = np.append(hrv_rmssd_mo,record.get('hrv_rmssd_morning'))
        hrv_rmssd_ev = np.append(hrv_rmssd_ev,record.get('hrv_rmssd_evening'))
        
        avg_rr = np.append(avg_rr,record.get('avg_rr'))
        max_rr = np.append(max_rr,record.get('max_rr'))
        min_rr = np.append(min_rr,record.get('min_rr'))

        tossnturn = np.append(tossnturn,record.get('tossnturn_count'))

##       





        
    Feature = np.zeros((len(avg_hr),10))
    idx = np.argsort(sttime)
    Feature[:,0] = sttime[idx]
    Feature[:,1] = avg_hr[idx]
    Feature[:,2] = max_hr[idx]
    Feature[:,3] = min_hr[idx]
    Feature[:,4] = hrv_rmssd_mo[idx]
    Feature[:,5] = hrv_rmssd_ev[idx]
    Feature[:,6] = avg_rr[idx]
    Feature[:,7] = max_rr[idx]
    Feature[:,8] = min_rr[idx]
    Feature[:,9] = tossnturn[idx]

    Times =  []

    for i in range(len(Feature[:,0])):
        start = datetime.datetime.fromtimestamp(Feature[i,0])
        Times.append(start.date())
    
    
    return Feature,Times





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:46:33 2017
@author: Shixin Xu
Function to read  bson files. 
Input:  *.bson.
"""

 

## Read bson file
from pymongo import MongoClient
import pprint
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dplt
import mongofeature
from mpl_toolkits.mplot3d import Axes3D

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['test']
collection = db.emfits

Feature1,Times1 = mongofeature.get_feature_from_mongo("00123A")
plt.ion()
plt.figure(1)

plt.subplot(3,1,1)
plt.title('EMFIT Device 00123A Trend')
dates = dplt.date2num(Times1)
plt.plot_date(dates,Feature1[:,1],'go-',label='Mean-HR')
plt.plot_date(dates,Feature1[:,2],'r-',label='Max-HR')
plt.plot_date(dates,Feature1[:,3],'b-',label='Min-HR')
plt.fill_between(dates, Feature1[:,3], Feature1[:,2], color='grey', alpha='0.5')

plt.ylabel('HR')
plt.legend()
plt.subplot(3,1,2)
 
plt.plot_date(dates,Feature1[:,6],'go-',label='Mean-RR')
plt.plot_date(dates,Feature1[:,7],'r-',label='Max-RR')
plt.plot_date(dates,Feature1[:,8],'b-',label='Min-RR')
plt.fill_between(dates, Feature1[:,8], Feature1[:,7], color='grey', alpha='0.5')
plt.ylabel('RR')
plt.legend()
plt.subplot(3,1,3)
##plt.plot(np.arange(len(Feature1[:,9])),Feature1[:,9],'go-',label='Toss')
plt.plot_date(dates,Feature1[:,9],'go-',label='Toss')
plt.ylabel('Toss')
plt.xlabel('Time(day)')
plt.legend()


Feature2,Times2 = mongofeature.get_feature_from_mongo("1335A2")
Feature3,Times3 = mongofeature.get_feature_from_mongo("133B55")
Feature4,Times4 = mongofeature.get_feature_from_mongo("13232D")

##plt.figure(2)
##plt.plot(Feature1[:,1],Feature1[:,6],'ro',label='Device 00123A')
##plt.plot(Feature2[:,1],Feature2[:,6],'k*',label='Device 1335A2')
##plt.plot(Feature3[:,1],Feature3[:,6],'bs',label='Device 133B55')
##plt.plot(Feature4[:,1],Feature4[:,6],'g<',label='Device 13232D')
##plt.xlabel('HR')
##plt.ylabel('RR')
##plt.legend()
##
##plt.figure(3)
##plt.plot(Feature1[:,9],Feature1[:,6],'ro',label='Device 00123A')
##plt.plot(Feature2[:,9],Feature2[:,6],'k*',label='Device 1335A2')
##plt.plot(Feature3[:,9],Feature3[:,6],'bs',label='Device 133B55')
##plt.plot(Feature4[:,9],Feature4[:,6],'g<',label='Device 13232D')
##plt.xlabel('TOSS')
##plt.ylabel('RR')
##plt.legend()


fig = plt.figure(4)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(Feature1[:,1],Feature1[:,6],Feature1[:,9],c='r', marker='o')
ax.scatter(Feature2[:,1],Feature2[:,6],Feature2[:,9],c='k', marker='*')
ax.scatter(Feature3[:,1],Feature3[:,6],Feature3[:,9],c='b', marker='s')
ax.scatter(Feature4[:,1],Feature4[:,6],Feature4[:,9],c='g', marker='<')
ax.set_xlabel('HR')
ax.set_ylabel('RR')
ax.set_zlabel('TOSS')
ax.set_title('r:00123A; k:1335A2; b:133B55; g:13232D')
##plt.legend()

##plt.figure(4)
##plt.fill_between(np.arange(len(Feature1[:,1])), Feature1[:,3], Feature1[:,2], color='red', alpha='0.5')
##plt.fill_between(np.arange(len(Feature2[:,1])), Feature2[:,3], Feature2[:,2], color='black', alpha='0.5')
##plt.fill_between(np.arange(len(Feature3[:,1])), Feature3[:,3], Feature3[:,2], color='blue', alpha='0.5')
##plt.fill_between(np.arange(len(Feature4[:,1])), Feature4[:,3], Feature4[:,2], color='green', alpha='0.5')
##plt.xlabel('Time(day)')
##plt.ylabel('HR')
##plt.title('HR Range Comparison')
##plt.legend()
##
##plt.figure(5)
##plt.fill_between(np.arange(len(Feature1[:,6])), Feature1[:,8], Feature1[:,7], color='red', alpha='0.5')
##plt.fill_between(np.arange(len(Feature2[:,6])), Feature2[:,8], Feature2[:,7], color='black', alpha='0.5')
##plt.fill_between(np.arange(len(Feature3[:,6])), Feature3[:,8], Feature3[:,7], color='blue', alpha='0.5')
##plt.fill_between(np.arange(len(Feature4[:,6])), Feature4[:,8], Feature4[:,7], color='green', alpha='0.5')
##plt.xlabel('Time(day)')
##plt.ylabel('RR')
##plt.title('RR Range Comparison')
##plt.legend()

##plt.show()






