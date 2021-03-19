from telethon import TelegramClient
import os
from dotenv import load_dotenv
import asyncio
import time
from connecting import db_connection
import pandas as pd
from sql import query

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('current', int(api_id), api_hash)
try:
    secs = int(input('Введите количество времени спустя которое скрипт повторится'))
except Exception as e:
    print(e)
    exit()


async def main():
    try:
        # df = pd.read_csv('test.csv')
        df = pd.read_sql(query, con=db_connection)
        db_connection.dispose()
        df.drop('id_contact', axis=1)
        df = df.groupby('Админ').agg({'telegram': 'first',
                                      'Переводчик': ', '.join}).reset_index()
        print(df)

        backslash = "\n"
        list_of_jsn = df.to_dict(orient='records')
        for dct in list_of_jsn:
            await client.send_message(dct['telegram'],
                                      f'Привет, у тебя есть переводчики, '
                                      f'не имеющие баланса уже более 3-х дней и их надо уволить через сферу, '
                                      f'либо отписать мне, почему это делать не надо :{backslash}-'
                                      f' {dct["Переводчик"].replace(",",","+backslash+"-")}.')
            await asyncio.sleep(2.5)
    except Exception as e:
        print(e)
        exit()

with client:
    while 1:
        try:
            client.loop.run_until_complete(main())
            # noinspection PyUnboundLocalVariable
            time.sleep(secs=secs)
        except KeyboardInterrupt as e:
            print(e)
            exit()
