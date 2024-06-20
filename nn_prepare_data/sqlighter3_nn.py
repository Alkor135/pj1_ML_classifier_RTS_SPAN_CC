"""
Создание БД с таблицами All и Nearest при запуске скрипта.
При доступе из других модулей получает доступ к БД.
"""
from pathlib import Path
from typing import Any
import sqlite3

import pandas as pd


def create_tables(connection, cursor):
    """ Функция создания таблиц  в БД если их нет"""
    try:
        with connection:
            # cursor.execute('''DROP TABLE Futures''')
            # print("Удалена таблица 'Futures' из БД")
            cursor.execute('''CREATE TABLE if not exists `All_opt` (
                            `TRADEDATE`         DATE PRIMARY KEY UNIQUE NOT NULL,
                            `-22500`            REAL,
                            `-20000`            REAL,
                            `-17500`            REAL,
                            `-15000`            REAL,
                            `-12500`            REAL,
                            `-10000`            REAL,
                            `-7500`             REAL,
                            `-5000`             REAL,
                            `-2500`             REAL,
                            `0`                 REAL,
                            `2500`              REAL,
                            `5000`              REAL,
                            `7500`              REAL,
                            `10000`             REAL,
                            `12500`             REAL,
                            `15000`             REAL,
                            `17500`             REAL,
                            `20000`             REAL,
                            `22500`             REAL,
                            `zero_strike`       INTEGER NOT NULL,
                            `close`             REAL NOT NULL,
                            `low`               REAL NOT NULL,
                            `high`              REAL NOT NULL)'''
                           )
            cursor.execute('''CREATE TABLE if not exists `Nearest` (
                            `TRADEDATE`         DATE PRIMARY KEY UNIQUE NOT NULL,
                            `-22500`            REAL,
                            `-20000`            REAL,
                            `-17500`            REAL,
                            `-15000`            REAL,
                            `-12500`            REAL,
                            `-10000`            REAL,
                            `-7500`             REAL,
                            `-5000`             REAL,
                            `-2500`             REAL,
                            `0`                 REAL,
                            `2500`              REAL,
                            `5000`              REAL,
                            `7500`              REAL,
                            `10000`             REAL,
                            `12500`             REAL,
                            `15000`             REAL,
                            `17500`             REAL,
                            `20000`             REAL,
                            `22500`             REAL,
                            `zero_strike`       INTEGER NOT NULL,
                            `close`             REAL NOT NULL,
                            `low`               REAL NOT NULL,
                            `high`              REAL NOT NULL)'''
                           )
        print('Taблицы в БД созданы')
    except sqlite3.OperationalError as exception:
        print(f"Ошибка при создании БД: {exception}")


def non_empty_table_all_opt(connection, cursor):
    """Проверяем, есть ли записи в таблице 'All_opt' в базе"""
    with connection:
        return cursor.execute("SELECT count(*) FROM (select 1 from All_opt limit 1)").fetchall()[0][0]


def tradedate_nn_exists(connection, cursor, tradedate):
    """Проверяем, есть ли дата в таблице 'All_opt' в базе"""
    with connection:
        result = cursor.execute('SELECT * FROM `All_opt` WHERE `TRADEDATE` = ?', (tradedate,)).fetchall()
        return bool(len(result))


def add_tradedate_all(connection, cursor, tradedate, o_22500, o_20000, o_17500, o_15000, o_12500, o_10000,
                      o_7500, o_5000, o_2500, p_0, p_2500, p_5000, p_7500, p_10000, p_12500, p_15000, p_17500,
                      p_20000, p_22500, zero_strike, close, low, high):
    """Добавляет строку в таблицу `All_opt` """
    with connection:
        return cursor.execute(
            "INSERT INTO `All_opt` (`TRADEDATE`, `-22500`, `-20000`, `-17500`, `-15000`, `-12500`, `-10000`, `-7500`, "
            "`-5000`, `-2500`, `0`, `2500`, `5000`, `7500`, `10000`, `12500`, `15000`, `17500`, `20000`, `22500`, "
            "`zero_strike`, `close`, `low`, `high`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (tradedate, o_22500, o_20000, o_17500, o_15000, o_12500, o_10000, o_7500, o_5000, o_2500, p_0, p_2500,
             p_5000, p_7500, p_10000, p_12500, p_15000, p_17500, p_20000, p_22500, zero_strike, close, low, high))


def add_tradedate_nearest(connection, cursor, tradedate, o_22500, o_20000, o_17500, o_15000, o_12500, o_10000,
                          o_7500, o_5000, o_2500, p_0, p_2500, p_5000, p_7500, p_10000, p_12500, p_15000, p_17500,
                          p_20000, p_22500, zero_strike, close, low, high):
    """Добавляет строку в таблицу `Nearest` """
    with connection:
        return cursor.execute(
            "INSERT INTO `Nearest` (`TRADEDATE`, `-22500`, `-20000`, `-17500`, `-15000`, `-12500`, `-10000`, `-7500`, "
            "`-5000`, `-2500`, `0`, `2500`, `5000`, `7500`, `10000`, `12500`, `15000`, `17500`, `20000`, `22500`, "
            "`zero_strike`, `close`, `low`, `high`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (tradedate, o_22500, o_20000, o_17500, o_15000, o_12500, o_10000, o_7500, o_5000, o_2500, p_0, p_2500,
             p_5000, p_7500, p_10000, p_12500, p_15000, p_17500, p_20000, p_22500, zero_strike, close, low, high))


if __name__ == '__main__':  # Создание БД, если её не существует
    # Настройка базы данных
    tiker: str = 'RTS'
    path_bd_nn: Path = Path(r'c:\Users\Alkor\gd\data_quote_db')  # Папка с БД
    file_bd_nn: str = f'{tiker}_nn.db'

    if not path_bd_nn.is_dir():  # Если не существует папка под БД
        try:
            path_bd_nn.mkdir()  # Создание папки под БД
        except Exception as err:
            print(f'Ошибка создания каталога "{path_bd_nn}": {err}')

    connection: Any = sqlite3.connect(fr'{path_bd_nn}\{file_bd_nn}', check_same_thread=True)
    cursor: Any = connection.cursor()
    create_tables(connection, cursor)  # Создание таблиц в БД если их нет
