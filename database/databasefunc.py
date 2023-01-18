import pymysql.cursors

import aioschedule
import asyncio
from create_bot import bot
from typing import List, Dict
from aiogram.utils.exceptions import BotBlocked


def connection_with_mariadb() -> None:
    """Connect to the database"""
    global connection
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='',
                                 database='test',
                                 cursorclass=pymysql.cursors.DictCursor)

    print('Maria db connected OK')


def add_voice(name_column: str, path: str, telegramid: int) -> None:
    """добавляет путь до ГС в БД"""

    with connection.cursor() as cursor:
        connection.begin()  # позволяет обновить данные из mariadb (что бы когда добавили данные в phpmyadmin, то он
        # их увидел)

        request = f'ALTER TABLE test.audio ADD COLUMN IF NOT EXISTS {name_column} VARCHAR (100)'
        print(request)
        cursor.execute(request)
        connection.commit()

        request = f"UPDATE `audio` SET `{name_column}` = '{path}' WHERE `audio`.`telegramid` = {telegramid}"
        print(request)
        cursor.execute(request)
        connection.commit()


def add_user(telegramid: int) -> bool:
    """
    add new user
    :param telegramid: id in tg
    :return: True if create new user, False if the user exists
    """
    with connection.cursor() as cursor:
        connection.begin()  # позволяет обновить данные из mariadb (что бы когда добавили данные в phpmyadmin, то он
        # их увидел)
        request = f"SELECT * FROM test.audio WHERE telegramid = '{telegramid}';"
        print(request)
        cursor.execute(request)
        user_mariadb = cursor.fetchall()
        print(user_mariadb)

        if len(user_mariadb) != 0:
            return False
        request = f"INSERT IGNORE INTO test.audio (telegramid) VALUES ({telegramid});"
        print(request)
        cursor.execute(request)
        connection.commit()
        return True
