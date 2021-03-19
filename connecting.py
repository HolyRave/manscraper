import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql

load_dotenv()
user = os.getenv('USER')
password = os.getenv('PASSWRD')
host = os.getenv('HOST')

db_connection_str = f'mysql+pymysql://{user}:{password}@{host}/{host}?charset=utf8mb4'
db_connection = create_engine(db_connection_str)
