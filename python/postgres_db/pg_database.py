import psycopg2 
import pandas as pd
import pandas.io.sql as sqlio
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

    def retrieve(self):
        query = '''
        SELECT * FROM city_temp;
        '''
        # self.cursor.execute(query)
        # return self.cursor.fetchall()
        return sqlio.read_sql_query(query, self.conn)

    def insert(self):
        #nothing rn
        return