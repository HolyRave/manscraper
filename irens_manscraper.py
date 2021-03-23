from telethon.sync import TelegramClient, errors
import os
from dotenv import load_dotenv
import asyncio
from utils.connecting import db_connection
import pandas as pd
from utils.sql import query
from datetime import datetime


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


try:
    load_dotenv()
except Exception as e:
    print("Проверьте .env файл, скорее всего с ним какая-то ошибка")
    input(str(e) + '\n Press enter to continue...')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
secs = int(input('Введите количество времени (секунд) спустя которое скрипт будет повторятся: '))
client = TelegramClient('current', int(api_id), api_hash)
client.connect()
if not client.is_user_authorized():
    phone_number = input('Enter phone: ')
    client.send_code_request(phone_number)
    try:
        client.sign_in(phone_number, input('Enter code: '))
    except errors.SessionPasswordNeededError:
        client.sign_in(password=input('Enter password: '))

with client as client:
    async def task1():
        try:
            df = pd.read_sql(query, con=db_connection)
            db_connection.dispose()
            df.drop('id_contact', axis=1)
            df = df.groupby('Админ').agg({'telegram': 'first',
                                          'Переводчик': ', '.join}).reset_index()
            list_of_jsn = df.to_dict(orient='records')

            backslash = "\n"
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            for dct in list_of_jsn:
                try:
                    await client.send_message(dct['telegram'],
                                              f'Привет, у тебя есть переводчики, '
                                              f'не имеющие баланса уже более 3-х дней и их надо уволить через сферу, '
                                              f'либо отписать мне, почему это делать не надо :{backslash}-'
                                              f' {dct["Переводчик"].replace(",", "," + backslash + "-")}.')
                    await asyncio.sleep(2.5)
                except Exception as E:
                    print('Error has occurred:')
                    input(str(E) + '\n Press enter to continue...')
                    exit()
            print(f'- {current_time} Отправлено {len(list_of_jsn)} админам(у)')

        except Exception as err:
            print('Error has occurred:')
            input(str(err) + '\n Press enter to continue...')
            exit()


    async def main():
        try:
            t1 = asyncio.ensure_future(repeat(secs, task1))
            await t1
        except KeyboardInterrupt:
            input("Program has finished, enter to continue... ")
            exit()


    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt as e:
        input("Program has finished, enter to continue... ")
        exit()
    except Exception as e:
        print('Error has occurred:')
        input(str(e) + '\n Press enter to continue...')
        exit()
