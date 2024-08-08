# Исключены дожи. Счинаются как бар на повышение с маленьким телом

from pathlib import Path
import pandas as pd
import sqlite3
import numpy as np
import sys

sys.dont_write_bytecode = True


# Параметры по которым будут производиться расчеты величины теней и тела свечи
PERIOD = 20  # Период для подсчета значений квантилей.
QUAN_MIN = 0.25  # Нижняя граница ниже которой параметр считается маленьким.
QUAN_MAX = 0.75  # Веерхняя граница выше которой параметр считается большим.


# def candle_code(open, close, size_hi, size_body, size_lo, q_hi_min, q_hi_max, q_body_min, q_body_max, q_lo_min, q_lo_max) -> str:
#     """
#     Кодирование свечей по Лиховидову
#     """
#     code_str: str = ''  # Строка в которую будем собирать код свечи
#     # Свеча на понижение (медвежья)
#     if open > close:  # Свеча на понижение (медвежья)
#         code_str += '0'
#         # Для тела медвежьей свечи
#         if size_body > q_body_max:  # 00 - медвежья свеча с телом больших размеров
#             code_str += '00'
#         elif size_body >= q_body_min:  # 01 - медвежья свеча с телом средних размеров
#             code_str += '01'
#         elif size_body > 0.0:  # 10 - медвежья свеча с телом небольших размеров
#             code_str += '10'
#         # Для верхней тени медвежьей свечи
#         if size_hi > q_hi_max:  # 11 - верхняя тень больших размеров
#             code_str += '11'
#         elif size_hi >= q_hi_min:  # 10 - верхняя тень средних размеров
#             code_str += '10'
#         elif size_hi > 0.0:  # 01 - верхняя тень небольших размеров
#             code_str += '01'
#         else:  # 00 - верхняя тень отсутствует
#             code_str += '00'
#         # Для нижней тени медвежьей свечи
#         if size_lo > q_lo_max:  # 00 - нижняя тень больших размеров
#             code_str += '00'
#         elif size_lo >= q_lo_min:  # 01 - нижняя тень средних размеров
#             code_str += '01'
#         elif size_lo > 0.0:  # 10 - нижняя тень небольших размеров
#             code_str += '10'
#         else:  # 11 - нижняя тень отсутствует
#             code_str += '11'
#     # Свеча на повышение (бычья)
#     elif open < close:  # Свеча на повышение (бычья)
#         code_str += '1'
#         # Для тела бычьей свечи
#         if size_body > q_body_max:  # 11 - бычья свеча с телом больших размеров.
#             code_str += '11'
#         elif size_body >= q_body_min:  # 10 - бычья свеча с телом средних размеров
#             code_str += '10'
#         elif size_body > 0.0:  # 01 - бычья свеча с телом небольших размеров
#             code_str += '01'
#         # Для верхней тени бычьей свечи
#         if size_hi > q_hi_max:  # 11 - верхняя тень больших размеров
#             code_str += '11'
#         elif size_hi >= q_body_min:  # 10 - верхняя тень средних размеров
#             code_str += '10'
#         elif size_hi > 0.0:  # 01 - верхняя тень небольших размеров
#             code_str += '01'
#         else:  # 00 - верхняя тень отсутствует
#             code_str += '00'
#         # Для нижней тени бычьей свечи
#         if size_lo > q_lo_max:  # 00 - нижняя тень больших размеров
#             code_str += '00'
#         elif size_lo >= q_lo_min:  # 01 - нижняя тень средних размеров
#             code_str += '01'
#         elif size_lo > 0.0:  # 10 - нижняя тень небольших размеров
#             code_str += '10'
#         else:  # 11 - нижняя тень отсутствует
#             code_str += '11'
            
#     # Дожи
#     else:  # Дожи
#         if size_hi > size_lo:  # Верхняя тень больше, медвежий дожи
#             code_str += '011'
#         else:  # Верхняя тень меньше, бычий дожи
#             code_str += '100'
#         # Для верхней тени дожи
#         if size_hi > q_hi_max:  # 11 - верхняя тень больших размеров
#             code_str += '11'
#         elif size_hi >= q_hi_min:  # 10 - верхняя тень средних размеров
#             code_str += '10'
#         elif size_hi > 0.0:  # 01 - верхняя тень небольших размеров
#             code_str += '01'
#         else:  # 00 - верхняя тень отсутствует
#             code_str += '00'
#         # Для нижней тени дожи
#         if size_lo > q_hi_max:  # 00 - нижняя тень больших размеров
#             code_str += '00'
#         elif size_lo >= q_lo_min:  # 01 - нижняя тень средних размеров
#             code_str += '01'
#         elif size_lo > 0.0:  # 10 - нижняя тень небольших размеров
#             code_str += '10'
#         else:  # 11 - нижняя тень отсутствует
#             code_str += '11'
#     return code_str

def candle_code(open, close, size_hi, size_body, size_lo, q_hi_min, q_hi_max, q_body_min, q_body_max, q_lo_min, q_lo_max) -> str:
    """
    Кодирование свечей по Лиховидову без дожи.
    """
    code_str: str = ''  # Строка в которую будем собирать код свечи
    # Свеча на понижение (медвежья)
    if open > close:  # Свеча на понижение (медвежья)
        code_str += '0'
        # Для тела медвежьей свечи
        if size_body > q_body_max:  # 00 - медвежья свеча с телом больших размеров
            code_str += '00'
        elif size_body >= q_body_min:  # 01 - медвежья свеча с телом средних размеров
            code_str += '01'
        elif size_body >= 0.0:  # 10 - медвежья свеча с телом небольших размеров
            code_str += '10'
        # Для верхней тени медвежьей свечи
        if size_hi > q_hi_max:  # 11 - верхняя тень больших размеров
            code_str += '11'
        elif size_hi >= q_hi_min:  # 10 - верхняя тень средних размеров
            code_str += '10'
        elif size_hi >= 0.0:  # 01 - верхняя тень небольших размеров
            code_str += '01'
        else:  # 00 - верхняя тень отсутствует
            code_str += '00'
        # Для нижней тени медвежьей свечи
        if size_lo > q_lo_max:  # 00 - нижняя тень больших размеров
            code_str += '00'
        elif size_lo >= q_lo_min:  # 01 - нижняя тень средних размеров
            code_str += '01'
        elif size_lo >= 0.0:  # 10 - нижняя тень небольших размеров
            code_str += '10'
        else:  # 11 - нижняя тень отсутствует
            code_str += '11'
    # Свеча на повышение (бычья)
    else:  # Свеча на повышение (бычья)
        code_str += '1'
        # Для тела бычьей свечи
        if size_body > q_body_max:  # 11 - бычья свеча с телом больших размеров.
            code_str += '11'
        elif size_body >= q_body_min:  # 10 - бычья свеча с телом средних размеров
            code_str += '10'
        elif size_body >= 0.0:  # 01 - бычья свеча с телом небольших размеров
            code_str += '01'
        # Для верхней тени бычьей свечи
        if size_hi > q_hi_max:  # 11 - верхняя тень больших размеров
            code_str += '11'
        elif size_hi >= q_body_min:  # 10 - верхняя тень средних размеров
            code_str += '10'
        elif size_hi >= 0.0:  # 01 - верхняя тень небольших размеров
            code_str += '01'
        else:  # 00 - верхняя тень отсутствует
            code_str += '00'
        # Для нижней тени бычьей свечи
        if size_lo > q_lo_max:  # 00 - нижняя тень больших размеров
            code_str += '00'
        elif size_lo >= q_lo_min:  # 01 - нижняя тень средних размеров
            code_str += '01'
        elif size_lo >= 0.0:  # 10 - нижняя тень небольших размеров
            code_str += '10'
        else:  # 11 - нижняя тень отсутствует
            code_str += '11'

    return code_str

def run(df):
    df.columns = map(str.lower, df.columns)  # Название колонок в нижний регистр
    
    # Подсчет размеров теней и тела свечи
    df['size_hi'] = df.apply(lambda x: abs(x.high - x.open), axis=1)
    df['size_body'] = df.apply(lambda x: abs(x.open - x.close), axis=1)
    df['size_lo'] = df.apply(lambda x: abs(x.open - x.low), axis=1)
    
    # Подсчет и запись в колонки заданных по условию квантилей для теней и тела свечи
    df['q_hi_min'] = df.size_hi.rolling(window=PERIOD).quantile(QUAN_MIN)  # Минимальный заданный квантиль для верхней тени свечи
    df['q_hi_max'] = df.size_hi.rolling(window=PERIOD).quantile(QUAN_MAX)  # Максимальный заданный квантиль для верхней тени свечи
    df['q_body_min'] = df.size_body.rolling(window=PERIOD).quantile(QUAN_MIN)
    df['q_body_max'] = df.size_body.rolling(window=PERIOD).quantile(QUAN_MAX)
    df['q_lo_min'] = df.size_lo.rolling(window=PERIOD).quantile(QUAN_MIN)
    df['q_lo_max'] = df.size_lo.rolling(window=PERIOD).quantile(QUAN_MAX)
    
    df = df.dropna().reset_index(drop=True)
    
    # Добавление колонки кода свечи
    df['candle_code'] = df.apply(lambda x: candle_code(
        x.open,
        x.close,
        x.size_hi,
        x.size_body,
        x.size_lo,
        x.q_hi_min,
        x.q_hi_max,
        x.q_body_min,
        x.q_body_max,
        x.q_lo_min,
        x.q_lo_max
        ), axis=1)  # Заполняем столбец candle_code

    df['up/down'] = df[['open', 'close']].apply(lambda x: 1 if (x.close > x.open) else 0, axis=1)  # Добавление колонки напрвления свечи
    # df['prev_cc'] = df.candle_code.shift(-1)  # Добавление колонки кода предыдущей свечи
    # df = df[['tradedate', 'open', 'low', 'high', 'close', 'up/down', 'candle_code', 'prev_cc']]
    df = df[['tradedate', 'size_body', 'open', 'low', 'high', 'close', 'up/down', 'candle_code']]
    df = df.dropna().reset_index(drop=True)
    
    # # Создание фичей из candle code предыдущей свечи
    # for i in range(7):
    #     df[f'f_{i}'] = df.apply(lambda x: int(x.prev_cc[i]), axis=1)
        
    # Создание фичей из candle code текущей свечи
    for i in range(7):
        df[f'f_{i}'] = df.apply(lambda x: int(x.candle_code[i]), axis=1)
        
    df.columns = map(str.upper, df.columns)  # Название колонок в верхний регистр
    
    return df


if __name__ == '__main__':
    tiker: str = 'RTS'
    db_path: Path = Path(fr'c:\Users\Alkor\gd\data_quote_db\{tiker}_futures_options_day_pj1.db')

    # Подключение к базе данных
    conn = sqlite3.connect(db_path)

    # Чтение данных из БД в DataFrame
    df_f = pd.read_sql_query("SELECT `TRADEDATE`, `OPEN`, `LOW`, `HIGH`, `CLOSE`, `OPENPOSITION`, `SHORTNAME`, `LSTTRADE` FROM Futures", conn)

    # Закрытие соединения
    conn.close()

    df_f[['TRADEDATE', 'LSTTRADE']] = df_f[['TRADEDATE', 'LSTTRADE']].apply(pd.to_datetime)

    df_f['next_name'] = df_f.SHORTNAME.shift(-1)  # Добавление колонки с именем следующей свечи

    # Фильтрация строк, где значения в столбцах SHORTNAME и next_name равны (исключение переходов контракта)
    df_f = df_f[df_f['SHORTNAME'] == df_f['next_name']]

    # print(df_f.to_string(max_rows=4, max_cols=10))
    df_f = df_f.dropna()
    # df_f[['next_ud']] = df_f[['next_ud']].astype(int)

    # Сортировка по полю даты и сброс индекса
    df_f = df_f.sort_values(by='TRADEDATE').reset_index(drop=True)
    df_f = df_f[['TRADEDATE', 'OPEN', 'LOW', 'HIGH', 'CLOSE']]
    
    df_f = run(df_f)

    # Вывод DataFrame
    print(df_f.to_string(max_rows=10, max_cols=20))
    print(df_f.shape)

    