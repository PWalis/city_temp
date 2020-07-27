from python.data import data
from python.mysql_db.database import database as db
from app.app import app 

server = app.run_server(debug=False)
