from telethon import TelegramClient
import os
from dotenv import load_dotenv
import asyncio
from connecting import db_connection
import pandas as pd
from sql import query


async def repeat(interval, func, *args, **kwargs):
    """Run func every interval seconds.

    If func has not finished before *interval*, will run again
    immediately when the previous iteration finished.

    *args and **kwargs are passed as the arguments to func.
    """
    while True:
        await asyncio.gather(
            func(*args, **kwargs),
            asyncio.sleep(interval),
        )


load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('current', int(api_id), api_hash)
try:
    secs = int(input('Введите количество времени (секунд) спустя которое скрипт будет повторятся: '))
except Exception as e:
    print(e)
    exit()


async def task1():
    try:
        df = pd.read_sql(query, con=db_connection)
        db_connection.dispose()
        df.drop('id_contact', axis=1)
        df = df.groupby('Админ').agg({'telegram': 'first',
                                      'Переводчик': ', '.join}).reset_index()
        backslash = "\n"
        list_of_jsn = df.to_dict(orient='records')

        for dct in list_of_jsn:
            await client.send_message(dct['telegram'],
                                      f'Привет, у тебя есть переводчики, '
                                      f'не имеющие баланса уже более 3-х дней и их надо уволить через сферу, '
                                      f'либо отписать мне, почему это делать не надо :{backslash}-'
                                      f' {dct["Переводчик"].replace(",", "," + backslash + "-")}.')
            await asyncio.sleep(2.5)
        print(f'Отправлено {len(list_of_jsn)} админу(ам)')
    except Exception as err:
        print(err)
        exit()


async def main():
    t1 = asyncio.ensure_future(repeat(secs, task1))
    await t1


with client:
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt as e:
        print(e)
        exit()
