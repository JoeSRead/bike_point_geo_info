import requests
import json
import pandas as pd
import numpy as np
import pickle
from datetime import datetime



class BikeTimes():
    def __init__(self):
        self.date = datetime.now()
        self.hour = self.date.hour
        self.minute = self.date.minute
        self.url = 'https://api.tfl.gov.uk/Place/Type/BikePoint'
        self.data = requests.get(self.url).json()
        
    def save_data(self):
        with open(f'./bike_data_{self.hour}_{self.minute}.json', 'w+') as f:
            f.write(json.dumps(self.data, sort_keys = True, indent = 4))
    
    def create_df(self):
        bikes_list = []
        
        for i in range(len(self.data)):
            name = self.data[i]['commonName']
            num_bikes = int(self.data[i]['additionalProperties'][-3]['value'])
            num_empty = int(self.data[i]['additionalProperties'][-2]['value'])
            num_docks = int(self.data[i]['additionalProperties'][-1]['value'])
            lat = self.data[i]['lat']
            lon = self.data[i]['lon']
            faulty = True if num_docks - num_empty - num_bikes > 0 else False
            num_faulty = num_docks - num_empty - num_bikes
            
            bike_dict = {'name': name,
                         'num_bikes': num_bikes,
                         'num_empty': num_empty,
                         'num_docks': num_docks,
                         'coords': (lat,lon),
                         'faulty': faulty,
                         'num_faulty': num_faulty}
    
            bikes_list.append(bike_dict)
        self.df = pd.DataFrame(bike_list)
    
    def 

class GeoGetter():
    def __init__(self):
        self.url = 'http://www.datasciencetoolkit.org/coordinates2statistics/'
    
    def create_df(self, dataframe):
        geo_list = []
        for i in range(len(dataframe)):
            lat = dataframe['coords'][i][0]
            lon = dataframe['coords'][i][1]
            data = requests.get(f"http://www.datasciencetoolkit.org/coordinates2statistics/{lat}%2c{lon}",
                                     params = {'statistics': 'population_density,elevation'}
                                     ).json()
            elevation = data[0]['statistics']['elevation']['value']
            pop_dens = data[0]['statistics']['population_density']['value']
            
            geo_dict = {'coords': dataframe['coords'][i],
                        'elevation': elevation,
                        'pop_dens': pop_dens}
            
            geo_list.append(geo_dict)
            
        self.df = pd.DataFrame(geo_list).set_index('coords')
        
    def add_hill_data(self):
        hill_list = []
        for n in range(len(self.df)):
            lat_n = self.df.index[n][0]
            lon_n = self.df.index[n][1]
            elev_list = []
            for i in range(len(self.df)):
                lat_i = self.df.index[i][0]
                lon_i = self.df.index[i][1]
                bol = ((lat_n-lat_i)**2 + (lon_n - lon_i)**2 < 0.000005)
                if bol:
                    elev_list.append(self.df.iloc[i].elevation)
            hill = (self.df.iloc[n].elevation > np.mean(elev_list))
            hill_list.append(hill)
        
        self.df['hill'] = hill_list
    
    def add_pop_data(self, quantile = 0.75):
        self.df['high_pop'] = self.df.pop_dens > self.df.pop_dens.quantile(quantile)
    
    def get_df(self):
        return self.df
        
        
        
        
        
        
        
        
        
        