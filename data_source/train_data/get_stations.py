import pandas as pd
import requests
import json 
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


df = pd.read_csv('./train_data.csv')

df_airport = pd.read_csv('./airport_coordinates.csv')

origin_airport = df['Origin Airport'].unique()

filtered_df = df_airport[df_airport['airport'].isin(origin_airport)]


## convert above to a dictionary ##
airport_dict = filtered_df.set_index('airport').T.to_dict('list')

# # # Get station data ## 

def get_stations_for_airports(coord):
    url = "https://meteostat.p.rapidapi.com/stations/nearby"
    querystring = {"lat": coord[0],"lon":coord[1]}
    headers = {
	"X-RapidAPI-Key": os.environ.get('METEOSTAT_API_KEY'),
	"X-RapidAPI-Host": "meteostat.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = json.loads(response.text)
    print(response_json['data'])
    return response_json['data'][0]['id']

stations_info = {}
for airport, coords in airport_dict.items():
    print(airport)
    print('\n------------------\n')
    station_id = get_stations_for_airports(coords)
    stations_info[airport] = station_id


# Written the Airport stations to a json file #
## Write to a json file ## 
with open('stations_info.json', 'w') as fp:
    json.dump(stations_info, fp, indent=4)



