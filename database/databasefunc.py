import pymysql.cursors
from database.in_csv import InCsv

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


def add_column(table: str, name_column: str, path: str, telegramid: int) -> None:
    """
    Создаёт столбец и вносит данные из path в строку по telegramid
    добавляет путь до ГС или Фото в БД (в данном случае)
    table таблица, в которую добавить
    name_column название столбца
    path - что добавить в ячейку
    telegramid - telegramid пользователя
    """

    with connection.cursor() as cursor:
        connection.begin()  # позволяет обновить данные из mariadb (что бы когда добавили данные в phpmyadmin, то он
        # их увидел)

        request = f'ALTER TABLE test.{table} ADD COLUMN IF NOT EXISTS {name_column} VARCHAR (100)'
        print(request)
        cursor.execute(request)
        connection.commit()

        request = f"UPDATE `{table}` SET `{name_column}` = '{path}' WHERE `{table}`.`telegramid` = {telegramid}"
        print(request)
        cursor.execute(request)
        connection.commit()


def add_user(telegramid: int, table: str) -> bool:
    """
    add new user
    :param telegramid: id in tg
    :return: True if create new user, False if the user exists
    """
    with connection.cursor() as cursor:
        connection.begin()  # позволяет обновить данные из mariadb (что бы когда добавили данные в phpmyadmin, то он
        # их увидел)
        request = f"SELECT * FROM test.{table} WHERE telegramid = '{telegramid}';"
        print(request)
        cursor.execute(request)
        user_mariadb = cursor.fetchall()
        print(user_mariadb)

        if len(user_mariadb) != 0:
            return False
        request = f"INSERT IGNORE INTO test.{table} (telegramid) VALUES ({telegramid});"
        print(request)
        cursor.execute(request)
        connection.commit()
        return True


def mysql_in_csv(table: str) -> None:
    """
    from mysql export in csv
    :param table: table from mysql
    :return: None
    """
    with connection.cursor() as cursor:
        connection.begin()  # позволяет обновить данные из mariadb (что бы когда добавили данные в phpmyadmin, то он
        # их увидел)
        request = f"SELECT * FROM test.{table};"
        print(request)
        cursor.execute(request)
        user_mariadb = cursor.fetchall()
        # print(user_mariadb)
        print([column for column in user_mariadb[0]])
        InCsv(f'database/data/data_{table}.csv', fieldnames=[column for column in user_mariadb[0]]).write(list(user_mariadb))
