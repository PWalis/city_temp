import psycopg2 
import pandas as pd
import pandas.io.sql as sqlio
from python.figure import vis
import json
from settings import DATABASE_URL, DB_PASSWORD

class database():
    '''
    Class that will connect to the database and
    retrieve all available data 
    the class will also allow for inserting data into the database
    '''
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()
        self.df = pd.DataFrame()

    def filter(self, Region, Country, State, City):
        query_1 = """
        select * from city_temp
        where ("Region", "Country", "State", "City")  
        in ((%s, %s, %s, %s));
        """
        query_2 = """
        select * from city_temp
        where ("Region", "Country", "City")  
        in ((%s, %s, %s));
        """
        values_1 = [Region, Country, State, City]
        values_2 = [Region, Country, City]
        if Country == 'US':
            try:
                self.cursor.execute(query_1, values_1)
                records = self.cursor.fetchall()
            except Exception as e:
                print('Error: ', e)
                self.conn.rollback()
        else:
            try:
                self.cursor.execute(query_2, values_2)
                records = self.cursor.fetchall()
            except Exception as e:
                print('Error: ', e)
                self.conn.rollback()
        if len(records) != 0:      
            df = pd.DataFrame(records)
            df.columns = ['Region', 'Country', 'State', 'City', 'AvgTemperature', 'Date']
            self.update_df(df)
            return vis(df).create_vis()
        else:
            self.update_df(pd.DataFrame)
            return vis(pd.DataFrame).create_vis()
        
    def get_dict(self):
        with open('app_dicts/region_country.json') as f:
            region_country = json.load(f)
        with open('app_dicts/country_city.json') as f:
            country_city = json.load(f)
        with open('app_dicts/state_city.json') as f:
            state_city = json.load(f)
        return region_country, country_city, state_city

    def get_stats(self):
        df = self.df
        if df.empty == False:
            stats = df['AvgTemperature'].describe()
            count = stats.iloc[0]
            minimum = df['AvgTemperature'].min()
            maxmimum = df['AvgTemperature'].max()
            min_date = df[df['AvgTemperature']==minimum]['Date'].iloc[0]
            max_date = df[df['AvgTemperature']==maxmimum]['Date'].iloc[0]
            min_string = f'{minimum} {min_date}'
            max_string = f'{maxmimum} {max_date}'
            return count, min_string, max_string
        else:
            return 0, ' ', ' '
    
    def update_df(self, df):
        self.df = df
        
