# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 19:05:55 2019

@author: thecu
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from config import gkey
import requests
import time
import sys

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
states = []

url = "https://maps.googleapis.com/maps/api/geocode/json"
params = {'key': gkey}

for ndx, row in summarydf.iterrows():
    # print(row)
    lat_lng = f"{row['Latitude']},{row['Longitude']}"
    params['latlng'] = lat_lng
    response = requests.get(url,params).json()
    state = None
    for component in response['results'][0]['address_components']:
        # print(component)
        for t in component['types']:
            if t == "administrative_area_level_1":
                state = component['long_name']
                break
        if state != None:
            break

    states.append(state)
    sys.stdout.write(f"{ndx} - {state}\n")
    sys.stdout.flush()
    time.sleep(0.02)

summarydf['State'] = states
    
summarydf.to_json("Resources/CleanedData.json")


