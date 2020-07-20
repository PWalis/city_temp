import sqlalchemy
import pandas as pd
from settings import DB_PASSWORD
class database():
    '''
    Class that will connect to the database and
    retrieve all available data 
    the class will also allow for inserting data into the database
    '''
    def __init__(self):
        creds = f'mysql://patrick:{DB_PASSWORD}@127.0.0.1/numerouno'
        self.engine = sqlalchemy.create_engine(creds)

    def retrieve(self):
        engine = self.engine
        return pd.read_sql_table('city_temp', engine, index_col='index')

    def insert(self):
        self.engine.execute()