import requests
from database.db_btc import DataBase as db
from api.bybit import BitGetApi
from api.bybit import btc_bybit
from system import SendMessage, statistics
import datetime

class Crypto:

    def __init__(self):
        self.price = {}

    # получаем курс биткоина
    def scrape(self):
        # получаем актуальный курс BTC
        URL = 'https://blockchain.info/ru/ticker'
        response = requests.get(URL)
        response_json = response.json()
        latest_price = float(response_json["USD"]["last"])
        Crypto().PriceBd(latest_price)
        return float(response_json["USD"]["last"])


    # добавляем данные в таблицу прайс
    def PriceBd(self, last_price):
        self.price['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.price['price'] = last_price
        self.price['moneta'] = 'BTC'
        print("Последняя цена BTC: ", last_price)
        # добавляем в бд
        db().price_add(self.price)


    # добавляем данные в таблицу сигнал
    def SignalBd(self, last_price, proc):
        self.price['date'] = datetime.datetime.now()
        self.price['price'] = last_price
        self.price['signal'] = round(last_price + ((last_price / 100) * 2), 2)  # добавляем 2 процента к текущей сумме и округляем до сотых
        self.price['moneta'] = 'BTC'
        self.price['proc'] = proc

        # покупаем крипту по рынку и сразу ставим лимитный ордер на продажу
        order_id = btc_bybit(qty_buy=10000, price_shell=self.price['signal'])
        self.price['order_id'] = order_id

        # добавляем в бд
        db().signal_add(self.price)
        # отправляем сообщение в канал
        sms = f'🛑 ВНИМАНИЕ!!! 🛑\n\n' \
              f'📚 В течении 48 часов {self.price['moneta']} упал на {round(self.price['proc'], 2)}% 📚 \n\n' \
              f'⬆️ Вход {self.price['price']} ⬆️ \n' \
              f'🔥 Продажа {self.price['signal']} (+2%) 🔥\n\n' \
              f'🕰 {self.price['date']} 🕰'

        SendMessage.Send(sms)
        # обновляем статитстику
        statistics.ref_stat()



    # добавляем сигнал, если он удовлетворяет условия
    def CheckProc(self, last_price):

        # получаем все сигналы за крайние 2 дня
        signal = db().signal_check()

        # если нет сигналов за крайние 2 дня, добавляем
        coll_orders = BitGetApi().coll_orders()
        if not signal:
            # максимальный курс за крайние 2 дня
            max_db = db().price_check()[0][0]
            proc = 100 - ((last_price / max_db) * 100)
            print('Разница от максимальной цены курса за крайние 2 дня', round(proc, 2))
            # если процент больше или равен 4, отправляем сигнал о покупке
            if proc >= 4 and coll_orders < 10:  # 4:
                Crypto().SignalBd(last_price, proc)

        # если сигнал есть, проверяем, чтобы он был больше на 4 процента, от предыдущего
        else:
            # получаем значение крайнего сигнала
            signal_db = signal[0][2] #[0][3] 15.11.2024
            # если оно больше 4 процентов, записываем его в бд
            proc = round(100 - ((last_price / signal_db) * 100), 2)
            print('Разница от крайнего синала за 2 дня', round(proc, 2))
            if proc >= 4 and coll_orders < 10:  # 4:
                Crypto().SignalBd(last_price, proc)

        # SignalBd(last_price, proc)

    # проверяем курс валюты, с курсами прогнозов(если курс больше, отправляем сообщение и редактируем запись в бд)
    def CheckPrognoz(self, latest_price):

        # получаем все не закрытые прогнозы с ByBit
        order_ids = BitGetApi().order_ids()
        # получаем все не закрытые прогнозы из бд
        signal = db().itog_check()
        # проверяем все актуальные прогнозы
        for s in signal:
            ids = s[0]  # ИД прогноза
            date = s[1]  # дата прогноза
            prognoz = s[3]  # курс прогноза
            order_is = s[8] # id открытых лимитных ордеров

            # если на ByBit нет такого ордера а в бд есть, значит ордер выполнился(закрываем его в бд)
            if order_is not in order_ids:
                sms_prognoz = f'📈 🔥🔥🔥🔥 📈 \n📆 Прогноз от {date} \n🔥 Успешно выполнен по курсу {latest_price} 🌪'

                # вносим изменения в бд, об успешном прогнозе
                db().update_signal(ids)

                # отправляем сообщение
                SendMessage.Send(sms_prognoz)
                # обновляем статитстику
                statistics.ref_stat()