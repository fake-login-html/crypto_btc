# при падении на 4 процента, в течении 2 дней, поднимется на 2 процента
import requests
from database import db_ton as db
from api.bybit import ton_bybit
from api.bybit import BitGetApi
import datetime
from system import SendMessage, statistics


class Crypto:

    def __init__(self):
        self.moneta = {}

    # получаем актуальный курс монеты
    def ton_price(self):
        coins = 'the-open-network' # ton
        url = f'https://api.coingecko.com/api/v3/coins/{coins}'
        posts = requests.get(url=url).json()
        ton = posts['market_data']['current_price']['usd']
        print(f'Текущий курс TON: {ton}')
        return  ton

    # проверяем, удовлетворяет ли курс условиям
    def check_procent(self, last_price):

        # получаем все сигналы за крайние 2 дня
        signal = db.DataBase().signal_check()
        # если нет сигналов за крайние 2 дня, добавляем
        coll_orders = BitGetApi().coll_orders()
        if not signal:
            # максимальный курс за крайние 2 дня
            max_db = db.DataBase().price_check()[0][0]
            proc = 100 - ((last_price / max_db) * 100)
            print('[4.0] Разница от максимальной цены курса за крайние 2 дня',round(proc, 2))
            # если процент больше или равен 4, отправляем сигнал о покупке
            if proc >= 4 and coll_orders < 10:#4:
                Crypto().signal_add(last_price, proc)
        # если сигнал есть, проверяем, чтобы он был больше на 4 процента, от предыдущего
        else:
            # получаем значение крайнего сигнала
            signal_db =  signal[0][2] #[0][3] 15.11.2024
            # если оно больше 4 процентов, записываем его в бд
            proc = round(100 - ((last_price / signal_db) * 100), 2)
            print('[4.0] Разница от крайнего синала за 2 дня', round(proc, 2))
            if proc >= 4 and coll_orders < 10:#4:
                Crypto().signal_add(last_price, proc)

    # добавляем актуальный курс в бд
    def moneta_add(self):
        self.moneta['price'] = Crypto().ton_price()
        self.moneta['date'] = datetime.datetime.now()
        self.moneta['moneta'] = 'TON'
        # добавляем в бд
        db.DataBase().price_add(self.moneta)

        return self.moneta['price']

    # добавляем сигнал в бд
    def signal_add(self, last_price, proc):

        self.moneta['price'] =last_price
        self.moneta['date'] = datetime.datetime.now()
        self.moneta['moneta'] = 'TON'
        self.moneta['signal'] = round(last_price + ((last_price / 100) * 2), 2)
        self.moneta['proc'] = proc

        # покупаем крипту по рынку и сразу ставим лимитный ордер на продажу
        order_id = ton_bybit(qty_buy=10000, price_shell=self.moneta['signal'])
        self.moneta['order_id'] = order_id

        # добавляем в бд
        db.DataBase().signal_add(self.moneta)

        sms = f'🛑 ВНИМАНИЕ!!! 🛑\n\n' \
            f'📚 В течении 48 часов {self.moneta['moneta']} упал на {round(self.moneta['proc'], 2)}% 📚 \n\n' \
            f'⬆️ Вход {self.moneta['price']} ⬆️ \n' \
            f'🔥 Продажа {self.moneta['signal']} (+2%) 🔥\n\n'\
            f'🕰 {self.moneta['date']} 🕰'

        SendMessage.Send(sms)
        # обновляем статитстику
        statistics.ref_stat()


    def CheckPrognoz(self, latest_price):

        # получаем все не закрытые прогнозы из бд
        signal = db.DataBase().itog_check()
        # получаем все не закрытые прогнозы с ByBit
        order_ids = BitGetApi().order_ids()
        # проверяем все актуальные прогнозы
        for s in signal:
            uuid = s[0] # ИД прогноза
            date = s[1]  # дата прогноза
            prognoz = s[3] # курс прогноза
            order_is = s[8] # id открытых лимитных ордеров

            # если на ByBit нет такого ордера а в бд есть, значит ордер выполнился(закрываем его в бд)
            if order_is not in order_ids:
                sms_prognoz = f'📈 🔥🔥🔥🔥 📈 \n📆 Прогноз от {date} \n🔥 Успешно выполнен \n🌪 По курсу {latest_price}'

                # вносим изменения в бд, об успешном прогнозе
                db.DataBase().update_signal(uuid)

                # отправляем сообщение
                SendMessage.Send(sms_prognoz)
                # обновляем статитстику
                statistics.ref_stat()