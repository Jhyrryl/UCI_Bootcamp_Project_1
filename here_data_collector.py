import pandas as pd
import json

import os
import time
import sys

import asyncio
import aiohttp

from config import here_app_id, here_app_code

cities_path = os.path.join(".", "Resources", "top_us_cities_by_population.csv")
cities_csv = pd.read_csv(cities_path)
cities = pd.DataFrame(cities_csv)

base_data_path = os.path.join(".", "Data")
for ndx, row in cities.iterrows():
    data_path = os.path.join(base_data_path, row['State'], row['City'], "")
    os.makedirs(data_path, exist_ok=True)

def saveJson(base_data_path, city, state, data):
    file = f"{time.time()}.json"
    data_path = os.path.join(base_data_path, state, city, file)
    with open(data_path, 'w') as outfile:
        json.dump(data, outfile)

async def main():
    url = "https://traffic.api.here.com/traffic/6.3/incidents.json"
    params = {'type': 'accident', 'app_code': here_app_code, 'app_id': here_app_id}
    async with aiohttp.ClientSession() as session:
        for ndx, row in cities.iterrows():
            loc = f"\n{row['City']}, {row['State']}"
            sys.stdout.write(loc)
            params['prox'] = f"{row['Lat']},{row['Lng']},10000"
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                if 'TRAFFIC_ITEMS' in data:
                    count = len(data['TRAFFIC_ITEMS']['TRAFFIC_ITEM'])
                    if count == 1:
                        sys.stdout.write(f"...1 accident")
                    else:
                        sys.stdout.write(f"...{count} accidents")
                    saveJson(base_data_path, row['City'], row['State'], data)
            sys.stdout.flush()
            await asyncio.sleep(0.25)

asyncio.run(main())