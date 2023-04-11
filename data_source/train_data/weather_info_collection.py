import pandas as pd 
import json
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
import requests
import logging

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.DEBUG,filename='valdata.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')


df_weather_delay = pd.read_csv('./weather_delay.csv')

df_train_data = pd.read_csv('../../evaluation/val_data(Apr 12-15).csv')

with open('stations_info.json') as json_file:
    stations_info = json.load(json_file)

headers = {
    "X-RapidAPI-Key": os.environ.get('METEOSTAT_API_KEY'),
    "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
}

meta_data_daily = {"date": "Date UTC /Day","tavg": "Average Temperature(Celcius) /Day", "tmin": "Minimum Temperature(Celcius) /Day", "tmax": "Maximum Temperature(Celcius) /Day", "prcp": "Daily Precipitation(mm) /Day", "snow": "Maximum Snowfall(mm) /Day", "wdir": "Wind Direction(Degrees) /Day", "wspd": "Wind Speed(km/h) /Day", "wpgt": "Peak Wind Gust(km/h) /Day", "pres": "Atmospheric Pressure(hPa) /Day", "tsun": "Sunshine Duration(m) /Day"}

meta_data_hourly = {"time": "Time UTC /Hour", "temp": "Temperature(Celcius) /Hour", "dwpt": "Dew Point(Celcius) /Hour", "rhum": "Relative Humidity(%) /Hour", "prcp": "Precipitation(mm) /Hour", "snow": "Snowfall(mm) /Hour", "wdir": "Wind Direction(Degrees) /Hour", "wspd": "Wind Speed(km/h) /Hour", "wpgt": "Peak Wind Gust(km/h) /Hour", "pres": "Atmospheric Pressure(hPa) /Hour", "tsun": "Sunshine Duration(m) /Hour", "coco": "Weather Code /Hour"}

weather_dict_code = {
    1: 'Clear',
    2: 'Fair',
    3: 'Cloudy',
    4: 'Overcast',
    5: 'Fog',
    6: 'Freezing Fog',
    7: 'Light Rain',
    8: 'Rain',
    9: 'Heavy Rain',
    10: 'Freezing Rain',
    11: 'Heavy Freezing Rain',
    12: 'Sleet',
    13: 'Heavy Sleet',
    14: 'Light Snowfall',
    15: 'Snowfall',
    16: 'Heavy Snowfall',
    17: 'Rain Shower',
    18: 'Heavy Rain Shower',
    19: 'Sleet Shower',
    20: 'Heavy Sleet Shower',
    21: 'Snow Shower',
    22: 'Heavy Snow Shower',
    23: 'Lightning',
    24: 'Hail',
    25: 'Thunderstorm',
    26: 'Heavy Thunderstorm',
    27: 'Storm'
}



def get_weather_per_day_station_statistics(row):
    """
    Get weather meta data for each date
    """
    date = row['Date (MM/DD/YYYY)']
    date_record = {}
    # Parse the input date string using strptime() and convert it to the desired format using strftime()
    new_date_string = datetime.strptime(str(date), '%m/%d/%Y').strftime('%Y-%m-%d')
    airport_station_id = stations_info.get(row['Origin Airport'])
    url =f"https://meteostat.p.rapidapi.com/stations/daily?station={airport_station_id}&start={new_date_string}&end={new_date_string}&units=metric"
    response = requests.request("GET", url, headers=headers)
    response_json = json.loads(response.text)
    logging.debug(response_json)
    date_weather =  response_json['data'][0]
    for key, value in date_weather.items():
        if key in meta_data_daily:
            date_record[meta_data_daily[key]] = value
    return date_record


## Iterate over the entire dataset and get weather data for each date ##
for index, row in df_train_data.iterrows():
    logging.debug(f"Processing row {index} of {len(df_train_data)}")
    date_record = get_weather_per_day_station_statistics(row)
    for key, value in date_record.items():
        df_train_data.loc[index, key] = value

## Use this for correlation of flights arrival time vs actual weather data ##
df_train_data.to_csv('val_data_with_daily_weather_data.csv', index=False)


# ## Iterate over each row and get weather data for each date ##
# for index, row in df_weather_delay.iterrows():
#     logging.info(f"Processing row {index} of {len(df_weather_delay)}")
#     date_record = get_weather_per_day_station_statistics(row)
#     for key, value in date_record.items():
#         df_weather_delay.loc[index, key] = value


# ## Use this for correlation of flights getting delayed by weather vs actual weather data ##
# df_weather_delay.to_csv('weather_delay_with_daily_weather_data.csv', index=False)
        






