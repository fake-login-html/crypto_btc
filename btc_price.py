import time
from  strategy.btc_4 import Crypto
from  strategy.btc_long4_3day import Crypto as Crypto_3day

def main():

    while True:
        # получаем актуальный курс
        try:
            latest_price = Crypto().scrape()
        except:
            latest_price = Crypto().scrape()

        # 2 DAYS
        # проверяем цену за крайние сутки, если она была выше 4 поцентов, отправляем сигнал
        Crypto().CheckProc(latest_price)
        # сверяем прогнозы с текущим курсом
        Crypto().CheckPrognoz(latest_price)

        # 3 DAYS
        # проверяем цену за крайние сутки, если она была выше 4 поцентов, отправляем сигнал
        Crypto_3day().CheckProc(latest_price)
        # сверяем прогнозы с текущим курсом
        Crypto_3day().CheckPrognoz(latest_price)

        time.sleep(60*5) # спим 5 минут

if __name__ == "__main__":
    main()









