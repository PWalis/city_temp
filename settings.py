from dotenv import load_dotenv
import os 
load_dotenv(verbose=True)

DB_PASSWORD = os.getenv('DB_PASSWORD')
