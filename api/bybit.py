import time
from config import *

from pybit.unified_trading import HTTP

class BitGetApi:

    def __init__(self):
        #api_key = ''
        #api_secret = ''

        self.session = HTTP(
            testnet=False,
            demo=True,
            api_key=api_key,
            api_secret=api_secret,
        )

    # колличество монеты на аккаунте
    def qty_account(self, coin): # coin="USDT"
        summ_usdt = self.session.get_wallet_balance(accountType="UNIFIED", coin=coin)['result']['list'][0]['coin'][0]['equity'] #result
        return summ_usdt

    # покупка по рынку
    def buy(self, qty, para): # para='TONUSDT'
        buy_order = self.session.place_order(
            category="spot",
            symbol=para,
            side="Buy", #Shell Buy
            orderType="Market", #Market Limit
            qty=qty,
            # marketUnit='quoteCoin' #для передачи суммы в котируем валюте
        )

        id_order = buy_order['result']['orderId']
        return id_order

    # продажа по рынку
    def shell(self, qty, para): # para='TONUSDT'

        Shell_order = self.session.place_order(
            category="spot",
            symbol=para,
            side="Sell", #Shell Buy
            orderType="Market", #Market Limit
            qty=qty
        )
        return Shell_order

    # покупка по лимиту
    def buy_limit(self, qty, price_by, para): # para='TONUSDT'
        buy_order = self.session.place_order(
            category="spot",
            symbol=para,
            side="Buy", #Shell Buy
            orderType="Limit", #Market Limit
            qty=qty,
            price=price_by,
            # marketUnit='quoteCoin' #baseCoin  quoteCoin для передачи суммы в котируем валюте
        )

        id_order = buy_order['result']['orderId']
        return id_order

    # продажа по лимиту
    def shell_limit(self, qty, price_shell, para):  # para='TONUSDT'

        shell_order = self.session.place_order(
            category="spot",
            symbol=para,
            side="Sell",  # Shell Buy
            orderType="Limit",  # Market Limit
            qty=qty,
            price=price_shell,
            marketUnit='quoteCoin' #baseCoin  quoteCoin для передачи суммы в котируем валюте
        )

        id_order = shell_order['result']['orderId']
        return id_order

    # все открытые ордера
    def orders(self):
        open_orders = self.session.get_open_orders(category='spot')#, orderId=1827778601341422848)
        return open_orders

    # все ID открытых ордеров(для проверки в базе)
    def order_ids(self):
        open_orders = self.session.get_open_orders(category='spot')['result']['list']
        order_ids = []
        for op in open_orders:
            order_id = op['orderId']
            order_ids.append(order_id)

        return order_ids

    # конкретный ордер
    def inf_order(self, order_id=1827812391233260800):

        price_buy = self.session.get_open_orders(category='spot', orderId=order_id)['result']['list'][0]['basePrice']
        sum_order = self.session.get_open_orders(category='spot', orderId=order_id)['result']['list'][0]['cumExecQty']

        return sum_order

    # сумма пары
    def last_price(self, para="TONUSDT"):
        price = self.session.get_tickers(category="inverse",
                                    symbol=para,
                                    )['result']['list'][0]['lastPrice']
        return price

    def coll_orders(self):
        vse_ordera = BitGetApi().orders()['result']['list']
        cl_orders = len(vse_ordera)

        return cl_orders

#     def test_orders(self):
#
#         list_BTC = self.session.get_order_history(
#             category="spot",
#             symbol='BTCUSDT',
#             limit=1,
#         )['result']['list']
#
#         print(list_BTC)
#
# BitGetApi().test_orders()
# --------------------------------------------------------------------------------

def ton_bybit(qty_buy, price_shell): # para=ВАЛЮТНАЯ ПАРА, qty_buy=КОЛЛИЧЕСТВО USDT ДЛЯ ПОКУПКИ, price_shell=КУРС ПРОДАЖИ

    para = 'TONUSDT'

    # покупаем по рынку
    order_buy = BitGetApi().buy(qty=qty_buy, para=para)
    # по ид ордера узнаем сумму купленной валюты
    qty_shell = BitGetApi().inf_order(order_buy)

    # оставляем 2 символа после запятой или оставляем как есть
    qty_shell = str(float(qty_shell) - (float(qty_shell) / 1000))
    qty_shell = qty_shell.split('.')
    if len(qty_shell) == 2: qty_shell = qty_shell[0] + '.' + qty_shell[1][:2]
    else: qty_shell = qty_shell[0]

    # ставим ордер на продажу
    order_id = BitGetApi().shell_limit(qty=qty_shell, price_shell=price_shell, para=para)

    return order_id

# ton_bybit(qty_buy=10, price_shell=7.25)
# BitGetApi().shell(para='TONUSDT',qty=4842.20)


def btc_bybit(qty_buy, price_shell):  # para=ВАЛЮТНАЯ ПАРА, qty_buy=КОЛЛИЧЕСТВО USDT ДЛЯ ПОКУПКИ, price_shell=КУРС ПРОДАЖИ

    para = 'BTCUSDT'

    # покупаем по рынку
    order_buy = BitGetApi().buy(qty=qty_buy, para=para)
    # по ид ордера узнаем сумму купленной валюты
    qty_shell = BitGetApi().inf_order(order_buy)

    # оставляем 6 символов после запятой или оставляем как есть
    qty_shell = str(float(qty_shell) - (float(qty_shell) / 1000))
    qty_shell = qty_shell.split('.')
    if len(qty_shell) == 2: qty_shell = qty_shell[0] + '.' + qty_shell[1][:6]
    else: qty_shell = qty_shell[0]

    # ставим ордер на продажу
    order_id = BitGetApi().shell_limit(qty=qty_shell, price_shell=price_shell, para=para)

    return order_id


# btc_bybit(10000, 99000)
# BitGetApi().shell_limit(qty=0.0001, price_shell=99000, para='BTCUSDT')

# btc_bybit(qty_buy=100, price_shell=95000)
# BitGetApi().shell(para='BTCUSDT',qty=0.001070)



# -----------------------------------------------------------------
# para='TONUSDT'
# # покупаем по рынку
# order_buy = BitGetApi().buy(qty=10, para=para)
# # по ид ордера узнаем сумму купленной валюты
# sum_buy = BitGetApi().inf_order(order_buy)
# # продаем купленную валюту по рынку
# order_shell = BitGetApi().shell(qty=sum_buy, para=para)