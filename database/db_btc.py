# НОВАЯ БД (POSTGRE)

import psycopg2
from datetime import datetime, timedelta

class DataBase:

    def __init__(self):

        # подключаемся к бд
        self.conn = psycopg2.connect(dbname='crypto', user='satoshi', password='satoshi', host='localhost')
        # создаем курсор
        self.cursor = self.conn.cursor()

    def price_add(self, moneta):
        # выполняем запрос
        self.cursor.execute(f"INSERT INTO public.price(\n" \
                       f"date, price, moneta)\n" \
                       f"VALUES ('{moneta['date']}', {moneta['price']}, '{moneta['moneta']}');")
        self.cursor.close()  # закрываем курсор
        self.conn.commit()  # сохраняем изменения
        self.conn.close()  # закрываем соединение

    def signal_add(self, moneta):
        # выполняем запрос
        self.cursor.execute(f"INSERT INTO public.signal(\n" \
                       f"date, price, prognoz, moneta, use, procent, order_id)\n" \
                       f"VALUES ('{moneta['date']}', {moneta['price']}, {moneta['signal']}, '{moneta['moneta']}', false, 2, '{moneta['order_id']}');")
        self.cursor.close()  # закрываем курсор
        self.conn.commit()  # сохраняем изменения
        self.conn.close()  # закрываем соединение

    def signal_add_2_8(self, moneta):
        # выполняем запрос
        self.cursor.execute(f"INSERT INTO public.signal(\n" \
                       f"date, price, prognoz, moneta, use, procent)\n" \
                       f"VALUES ('{moneta['date']}', {moneta['price']}, {moneta['signal']}, '{moneta['moneta']}', false, 1.4);")
        self.cursor.close()  # закрываем курсор
        self.conn.commit()  # сохраняем изменения
        self.conn.close()  # закрываем соединение

    def update_signal(self, uuid):
        # выполняем запрос
        date_now = datetime.now()
        self.cursor.execute(f"UPDATE signal set use = true, date_end = '{date_now}' where ids = '{uuid}';")
        self.cursor.close()  # закрываем курсор
        self.conn.commit()  # сохраняем изменения
        self.conn.close()  # закрываем соединение

    def price_check(self):
        # минус два дня от отекущего времени
        dm = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        # выполняем запрос
        self.cursor.execute(f"SELECT max(price) FROM price where date > '{dm}' and moneta = 'BTC';")
        price = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return price

    def price_check_3day(self):
        # минус два дня от отекущего времени
        dm = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        # выполняем запрос
        self.cursor.execute(f"SELECT max(price) FROM price where date > '{dm}' and moneta = 'BTC';")
        price = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return price

    def price_check_2_8(self):
        # минус два дня от отекущего времени
        dm = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        # выполняем запрос
        self.cursor.execute(f"SELECT max(price) FROM price where date > '{dm}' and moneta = 'BTC';")
        price = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return price

    def signal_check(self):
        # вычитаем из текущей даты 2 дня
        dm = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        # выполняем запрос
        self.cursor.execute(f"SELECT * FROM public.signal where date > '{dm}' and use = false and procent = {2} and moneta = 'BTC' ORDER by date desc LIMIT 1;")
        signal = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return signal

    def signal_check_3day(self):
        # вычитаем из текущей даты 3 дня
        dm = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        # выполняем запрос
        self.cursor.execute(f"SELECT * FROM public.signal where date > '{dm}' and use = false and procent = {2} and moneta = 'BTC_3day' ORDER by date desc LIMIT 1;")
        signal = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return signal

    def signal_check_2_8(self):
        # вычитаем из текущей даты 2 дня
        dm = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        # выполняем запрос
        self.cursor.execute(f"SELECT * FROM public.signal where date > '{dm}' and use = false and procent = '{1.4}' and moneta = 'BTC' ORDER by date desc LIMIT 1;")
        signal = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return signal

    def itog_check(self):
        # выполняем запрос
        self.cursor.execute(f"SELECT * FROM public.signal where  use = false and moneta = 'BTC'")
        signal = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return signal

    def statistics(self):
        # выполняем запрос
        self.cursor.execute(f"SELECT procent, moneta, use, prognoz FROM public.signal")
        statistic = self.cursor.fetchall()
        self.cursor.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение
        return statistic

######################## для отката стратегий ######################################

    # ДОБАВЛЯЕМ КУРСЫ ВАЛЮТ В БД
    def price_add_test(self, moneta):

        conn = psycopg2.connect(dbname='crypto_test', user='satoshi', password='satoshi', host='localhost')
        # создаем курсор
        cursor = conn.cursor()
        # выполняем запрос
        cursor.execute(f"INSERT INTO public.price(\n" \
                       f"date, price, moneta)\n" \
                       f"VALUES ('{moneta['date']}', {moneta['price']}, '{moneta['moneta']}');")
        cursor.close()  # закрываем курсор
        conn.commit()  # сохраняем изменения
        conn.close()  # закрываем соединение

