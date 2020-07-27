import psycopg2 
import pandas as pd
import pandas.io.sql as sqlio
from python.figure import vis
import json
from settings import DATABASE_URL

class database():
    '''
    Class that will connect to the database and
    retrieve all available data 
    the class will also allow for inserting data into the database
    '''
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()

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
        df = pd.DataFrame(records)
        df.columns = ['Region', 'Country', 'State', 'City', 'Month', 'Day', 'Year',
       'AvgTemperature']
        return vis(df).create_vis()
        
    def get_dict(self):
        with open('app/region_country.json') as f:
            region_country = json.load(f)
        with open('app/country_city.json') as f:
            country_city = json.load(f)
        with open('app/state_city.json') as f:
            state_city = json.load(f)
        return region_country, country_city, state_city