# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 19:05:55 2019

@author: thecu
"""

import json
import pandas as pd
from datetime import datetime, timedelta
# read file
with open('Resources/accidents.json', 'r') as myfile:
    data=myfile.read()
    
obj = json.loads(data)

originalid=[]
IDlist=[]
criticality=[]
lat=[]
lng=[]
starttimes=[]
endtimes=[]
duration=[]
vehiclecalled=[]
roadclosed=[]


#date conversion
starttimeconv=[]
endtimeconv=[]
duration=[]
durationtoseconds=[]


for i in range(0, len(obj),1):
    IDlist.append(obj[i]["TRAFFIC_ITEM_ID"])
    originalid.append(obj[i]["ORIGINAL_TRAFFIC_ITEM_ID"])
    criticality.append(obj[i]['CRITICALITY']['DESCRIPTION'])
    lat.append(obj[i]['LOCATION']['GEOLOC']['ORIGIN']['LATITUDE'])
    lng.append(obj[i]['LOCATION']['GEOLOC']['ORIGIN']['LONGITUDE'])
    starttimes.append(obj[i]['START_TIME'])
    endtimes.append(obj[i]['END_TIME'])
    vehiclecalled.append(obj[i]['TRAFFIC_ITEM_DETAIL']['INCIDENT']['RESPONSE_VEHICLES'])
    roadclosed.append(obj[i]['TRAFFIC_ITEM_DETAIL']['ROAD_CLOSED'])
    
    #datetime conversions
    starttimeconv.append(datetime.strptime(starttimes[i], '%Y/%m/%d %X'))
    endtimeconv.append(datetime.strptime(endtimes[i], '%Y/%m/%d %X'))
    duration.append(endtimeconv[i]-starttimeconv[i])
    durationtoseconds.append(duration[i].total_seconds())
    
    
summarydf=pd.DataFrame.from_dict({"ID":IDlist,
                                  "Criticality":criticality,
                                  "Latitude":lat,
                                  "Longitude":lng,
                                  "Start_time":starttimes,
                                  "End_time": endtimes,
                                  "Duration_(seconds)":durationtoseconds,
                                  "Vehicle_response":vehiclecalled ,
                                  "Road_closure":roadclosed})
    
summarydf.to_json("Resources/CleanedData.json")