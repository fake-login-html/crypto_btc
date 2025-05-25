import time
from  strategy.btc_4 import Crypto

def main():

    while True:
        # получаем актуальный курс
        try:
            latest_price = Crypto().scrape()
        except:
            latest_price = Crypto().scrape()
        # проверяем цену за крайние сутки, если она была выше 4 поцентов, отправляем сигнал
        Crypto().CheckProc(latest_price)
        # сверяем прогнозы с текущим курсом
        Crypto().CheckPrognoz(latest_price)

        time.sleep(60*5) # спим 5 минут

if __name__ == "__main__":
    main()









