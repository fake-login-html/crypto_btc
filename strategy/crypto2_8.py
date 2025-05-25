# при падении на 2.8 процента, в течении 1 дня, поднимется на 1,4 процента
from database import db_ton as db
from api.bybit import ton_bybit
import datetime
from system import SendMessage, statistics


class Crypto_2_8:

    def __init__(self):
        self.moneta = {}

    # проверяем, удовлетворяет ли курс условиям
    def check_procent(self, last_price):

        # получаем все сигналы за крайние 2 дня
        signal = db.DataBase().signal_check_2_8()
        # если нет сигналов за крайние 2 дня, добавляем
        if not signal:
            # максимальный курс за крайние сутки
            max_db = db.DataBase().price_check_2_8()[0][0]
            proc = 100 - ((last_price / max_db) * 100)
            print('[2.8] Разница от максимальной цены курса за крайние сутки',round(proc, 2))
            # если процент больше или равен 4, отправляем сигнал о покупке
            if proc >= 2.8:#4:
                Crypto_2_8().signal_add(last_price, proc)
        # если сигнал есть, проверяем, чтобы он был больше на 4 процента, от предыдущего
        else:
            # получаем значение крайнего сигнала
            signal_db =  signal[0][2] #[0][3] 15.11.2024
            # если оно больше 4 процентов, записываем его в бд
            proc = round(100 - ((last_price / signal_db) * 100), 2)
            print('[2.8] Разница от крайнего синала за 1 день', round(proc, 2))
            if proc >= 2.8:#4:
                Crypto_2_8().signal_add(last_price, proc)


    # добавляем сигнал в бд
    def signal_add(self, last_price, proc):

        self.moneta['price'] =last_price
        self.moneta['date'] = datetime.datetime.now()
        self.moneta['moneta'] = 'TON'
        self.moneta['signal'] = round(last_price + ((last_price / 100) * 1.4), 2)
        self.moneta['proc'] = proc

        # покупаем крипту по рынку и сразу ставим лимитный ордер на продажу
        order_id = ton_bybit(qty_buy=10000, price_shell=self.moneta['signal'])
        self.moneta['order_id'] = order_id

        # добавляем в бд
        db.DataBase().signal_add_2_8(self.moneta)

        sms = f'🛑 ВНИМАНИЕ!!! 🛑\n\n' \
            f'📚 В течении 48 часов {self.moneta['moneta']} упал на {round(self.moneta['proc'], 2)}% 📚 \n\n' \
            f'⬆️ Вход {self.moneta['price']} ⬆️ \n' \
            f'🔥 Продажа {self.moneta['signal']} (+1.4%) 🔥\n\n'\
            f'🕰 {self.moneta['date']} 🕰'

        # отправлем сообщение
        SendMessage.Send(sms)
        # обновляем статитстику
        statistics.ref_stat()
