from api.bybit import BitGetApi
import requests
from datetime import datetime, timedelta
from  strategy.btc_4 import Crypto

# получаем все открытые ордера на бирже, после чего добавляем их в массив
# vse_ordera = BitGetApi().orders()['result']['list']
# coll_orders = len(vse_ordera)

# coll = BitGetApi().coll_orders()
# print(coll)

#
# print(vse_ordera)
# # order_ids = []
# # for v in vse_ordera:
# #     order_id = v['orderId']
# #     order_ids.append(order_id)
# s = BitGetApi().order_ids()
# print(s)

################################################################
#
# def get_btc_price_at_time(target_datetime):
#     # Форматируем дату для API
#     date_str = target_datetime.strftime('%d-%m-%Y')
#     response = requests.get(f'https://api.coingecko.com/api/v3/coins/bitcoin/history',
#                             params={'date': date_str, 'localization': 'false'})
#
#     if response.status_code == 200:
#         data = response.json()
#         if 'market_data' in data and 'current_price' in data['market_data']:
#             price = data['market_data']['current_price']['usd']
#             return price
#     return None
#
# # Устанавливаем дату и время
# target_datetime = datetime(2024, 12, 31, 12, 35)
#
# for num in range(30):
#     # Получаем курс BTC
#     target_datetime = target_datetime - timedelta(minutes=5)
#     # target_datetime = target_datetime - timedelta(days=1)
#     # print(target_datetime)
#     btc_price = get_btc_price_at_time(target_datetime)
#
#     # Выводим результат
#     if btc_price is not None:
#         print(f"Курс BTC на {target_datetime.strftime('%d.%m.%Y %H:%M')} составляет {btc_price} USD")
#     else:
#         print("Не удалось получить курс BTC.")

###################################3

def fetch_historical_data():
    # url = 'https://api.bybit.com/v5/market/kline'
    # params = {
    #     'category': 'spot',
    #     'symbol': 'BTCUSDT',
    #     'interval': 5,  # Интервал в минутах
    #     # 'limit': 90000,    # Максимальное количество записей за один запрос
    #     'from': int((datetime.now() - timedelta(days=10)).timestamp())  # Данные за последний день
    # }
    # response = requests.get(url, params=params).json()
    # return response['result']['list']
    ##########################3
    url = 'https://api.bybit.com/v5/market/kline?category=spot&symbol=BTCUSDT&interval=5&limit=1000&start=1704127200000'
    response = requests.get(url).json()['result']['list']

    return response

# Получаем исторические данные и заполняем базу данных
historical_data = fetch_historical_data()
# print(historical_data)

for entry in historical_data:
    timestamp = datetime.fromtimestamp(int(entry[0][:-3]))  # Конвертация в datetime
    # price = entry['close']  # Закрывающая цена

    print(timestamp)


#
# const baseUrl = 'https://api.bybit.com'; // Базовый URL для API Bybit
# const symbol = 'BTCUSDT'; // Символ для отслеживания
#
#
# // Асинхронная функция для получения ATR (Average True Range)
# async function getATR(symbol, interval = 'D', limit = 14) {
#     try {
#         // Выполняет GET-запрос к API Bybit для получения данных Kline
#         const response = await axios.get(`${baseUrl}/v5/market/kline`, {
#             params: {
#                 category: 'spot', // Указывает категорию: 'spot', 'linear' или 'inverse'
#                 symbol: symbol,   // Указывает символ для получения данных (например, BTCUSDT)
#                 interval: interval, // Интервал времени для каждого Kline (например, 'D' для дневного)
#                 limit: limit + 1 // +1 чтобы включить предыдущее закрытие
#             }
#         }


session = HTTP(
            testnet=False,
            demo=True,
            api_key=api_key,
            api_secret=api_secret,
        )

session.place_order(
            category="spot",
            symbol=para,
            side="Sell",  # Shell Buy
            orderType="Limit",  # Market Limit
            qty=qty,
            price=price_shell,
            marketUnit='quoteCoin' #baseCoin  quoteCoin для передачи суммы в котируем валюте
        )