from database import db_btc

from api.bybit import BitGetApi
import requests
from datetime import datetime, timedelta

from database.db_btc import DataBase
from  strategy.btc_4 import Crypto

import pandas as pd
import json
import requests
import sys
from datetime import datetime as dt
import os
import numpy


symbol= 'BTCUSDT' # sys.argv[1]
limit_price = 288 #100
interval= 5 #sys.argv[2]
from_date= '01-01-2024'#sys.argv[3]
# to_date= '01-01-2025' #sys.argv[4]
to_date= '01-01-2025'
payload={}
headers = {}

#Convert string to datetime
s_dt = dt.strptime(from_date, '%d-%m-%Y')
#Initialize epoch
epoch = dt.utcfromtimestamp(0)
#Get your difference from epoch in ms
global start_epoch_time
start_epoch_time = int((s_dt - dt.utcfromtimestamp(0)).total_seconds()*1000)
#print(start_epoch_time)

#Convert string to datetime
e_dt = dt.strptime(to_date, '%d-%m-%Y')
epoch = dt.utcfromtimestamp(0)
global end_epoch_time
end_epoch_time = int((e_dt - dt.utcfromtimestamp(0)).total_seconds()*1000)
#print(end_epoch_time)

def fetch_historical_data(url):

    # url = 'https://api.bybit.com/v5/market/kline?category=spot&symbol=BTCUSDT&interval=5&limit=1000&start=1704127200000'

    moneta = {}
    response = requests.get(url).json()['result']['list']
    for entry in response:
        timestamp = datetime.fromtimestamp(int(entry[0][:-3]))  # Конвертация в datetime

        # данные для бд
        moneta['date'] = timestamp
        moneta['price'] = entry[4]
        moneta['moneta'] = 'BTC'

        #########################
        if int(entry[0][:-3]) <= start_epoch_time:

            DataBase().price_add_test(moneta)
            print(moneta)
        # print(timestamp, entry[4])

    # return response


while (start_epoch_time < end_epoch_time):
    url = "https://api.bybit.com/v5/market/kline?category=spot&symbol=" + symbol + "&interval=" + str(interval) + "&limit=" + str(limit_price) + "&start=" + str(start_epoch_time)
    print(url)
    fetch_historical_data(url)

    response = requests.request("GET", url, headers=headers, data=payload)
    data=json.loads(response.text)
    json_data=data['result']['list']

    start_epoch_time=int(start_epoch_time + ( 60 * 1000 * 1000 ))