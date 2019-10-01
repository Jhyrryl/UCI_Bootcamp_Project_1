import pandas as pd
import json

import sys
import os
from pathlib import Path

base_data_path = os.path.join('.', 'Data')
base_path = Path(base_data_path)

accident_ids = {}
accidents = []

def fixTime( time_str ):
    dt = time_str.split(" ")
    newTime = dt[0][-4:] + "/" + dt[0][0:-5] + " " + dt[1]
    sys.stdout.write(newTime+"\n")
    sys.stdout.flush()
    return newTime

state_paths = [x for x in base_path.iterdir() if x.is_dir()]
for state in state_paths:
    city_paths = [y for y in state.iterdir() if y.is_dir()]
    for city in city_paths:
        file_paths = [z for z in city.iterdir() if not z.is_dir()]
        for file in file_paths:
            # print(file)
            data = pd.read_json(file)
            for item in data['TRAFFIC_ITEMS']['TRAFFIC_ITEM']:
                item_id = item['TRAFFIC_ITEM_ID']
                orig_id = item['ORIGINAL_TRAFFIC_ITEM_ID']
                if not orig_id in accident_ids:
                    accident_ids[orig_id] = []
                accident_ids[orig_id].append(item)

for item_id, incidents in accident_ids.items():
    last = None
    last_time = ''
    for incident in incidents:
        t = fixTime(incident['END_TIME'])
        if t > last_time:
            last = incident
            last_time = t
    last['END_TIME'] = t
    last['START_TIME'] = fixTime(last['START_TIME'])
    last['ENTRY_TIME'] = fixTime(last['ENTRY_TIME'])
    last['RELATED_ITEM_COUNT'] = len(incidents)
    accidents.append(last)

print(f"{len(accidents)} found")

data_path = os.path.join('.', 'Resources', 'accidents.json')
with open(data_path, 'w') as outfile:
    json.dump(accidents, outfile)

