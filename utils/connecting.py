import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql

try:
    load_dotenv()
    user = os.getenv('DB_USR')
    password = os.getenv('DB_PASSWRD')
    host = os.getenv('DB_HOST')
    database = os.getenv('DATABASE')

    db_connection_str = f'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4'
    db_connection = create_engine(db_connection_str)
except Exception as e:
    print('Error has occurred:')
    input(str(e) + '\n Press enter to continue...')
    exit()
