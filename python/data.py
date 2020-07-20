import pandas as pd 
import sqlalchemy 
from .mysql_db.database import database as db
from python.figure import vis

'''
This will contain the data class which will be responsible for
loading the data into a pandas data frame from the MySql database
it will load the data using sqlalchemy
'''

class data():
    '''
    Loading data and filtering data
    '''
    def __init__(self):
        self.data = db().retrieve()
        # self.data = pd.read_csv('./data/clean_city_temp.csv')

    def filter(self, region, country, state, city ):
        '''
        Filters the dataframe by unique values of each column 
        '''
        # make it so at least region, country and city are populated before filtering
        data_copy = self.data.copy()
        if region is not None:
            data_copy = data_copy[data_copy['Region']==region]
        if country is not None:
            data_copy = data_copy[data_copy['Country']==country]
        if state != 'None' and state != None:
            data_copy = data_copy[data_copy['State']==state]
        if city is not None:
            data_copy = data_copy[data_copy['City']==city]
        fig = vis(data_copy)
        return fig.create_vis()
            
    def get_dict(self):
        df = self.data
        region_country = {}
        keys = df['Region'].unique()
        for key in keys:
            countries = df[df['Region']==key]['Country'].unique()
            region_country.update({key:countries})
        
        country_city = {}
        keys = df['Country'].unique()
        for key in keys:
            if key != 'US':
                cities = df[df['Country']==key]['City'].unique()
                country_city.update({key:cities})
            elif key == 'US':
                states = df[df['Country']=='US']['State'].unique()
                country_city.update({key:states})
        
        state_city = {}
        keys = df['State'].unique()[1:]
        for key in keys:
            cities = df[df['State']==key]['City'].unique()
            state_city.update({key:cities})
        
        return region_country, country_city, state_city
