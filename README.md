# UCI_Bootcamp_Project_1

## Data Collection & Cleaning Scripts
* here_data_collector.py was used to poll the here.com API.
* here_data_collator.py was used to filter and combine collected files.
* DataCleaner.py was used to extract raw data into a usable DataFrame.
  * reverse geocoding logic is also located in this script, but is currently commented out.

## Technical Requirements
* Accident Analysis.ipynb was the primary notebook that utilized Pandas to clean and format data.
* TrafficAccidentExlorationAndCleanup.ipynb is the required notebook describing the data exploration and cleanup process.
* DataAnalysisReport.ipynb is the required notebook illustrating the final data analysis.
* Matplotlib visualizations were saved as PNGs in the Charts folder.
* Optional API was the Incidents 6.2 Traffic API at here.com
  * https://developer.here.com/documentation/traffic/topics/request-constructing.html
* The presentation can be found summary can be found at:
  * https://prezi.com/bfgygwsquibe/traffic-accidents-across-the-us/?utm_campaign=share&utm_medium=copy

## Resources
* Input to the here_data_collector for polling the here.com API is found in Resources/top_us_cities_by_population.csv.
* Output data from executing here_data_collector.py was too extensive to include in the project.
* Output from the here_data_collator.py script can be found in Resources/accidents.json.
* Output from the DataCleaner.py script can be found in Resources/CleanedData.json.
* The state_population.csv was used to initialize the Pandas DataFrame onto which we hung all of our other data.

## Other
All other files/folders are either spikes to create visualizations, or the visualizations themselves. For example, Data Collection Map.ipynb was used to create Resources/accident_data_collection.png for use in presentation and required notebooks.
