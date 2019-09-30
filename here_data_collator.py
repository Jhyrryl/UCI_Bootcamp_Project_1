import pandas as pd
import json

import os
from pathlib import Path

base_data_path = os.path.join('.', 'Data')
base_path = Path(base_data_path)

accident_ids = {}
accidents = []

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
                if not item_id in accident_ids:
                    accident_ids[item_id] = True
                    accidents.append(item)

print(f"{len(accidents)} found")

data_path = os.path.join('.', 'Resources', 'accidents.json')
with open(data_path, 'w') as outfile:
    json.dump(accidents, outfile)

