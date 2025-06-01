from database.db_btc import DataBase
from system import SendMessage
from api.bybit import BitGetApi

def ref_stat():
    coll_usdt = BitGetApi().qty_account(coin='USDT').split('.')[0]

    statistics = DataBase().statistics()
    # цикл для подсчета статистики успешный сигналов
    stat_all = {}
    stat_like = {}
    raznica = {}
    summa_procentov = {}
    for st in statistics:

        proc = st[0]
        moneta = st[1]
        use = st[2]
        names = moneta + '_' + str(proc) # ДЛЯ НАИМЕНОВАНИЯ КЛЮЧЕЙ СПИСКА
        # вся статистика
        if names not in stat_all:
            stat_all[names] = 1
        else:
            stat_all[names] += 1
        # статистика успешных прогнозов
        if use == True:
            if names not in stat_like:
                stat_like[names] = 1
            else:
                stat_like[names] += 1

    # считаем разнику и успешные проценты
    for k in stat_all:
        raznica[k] = stat_all[k] - stat_like[k]
        proc = float(k.split('_')[1])
        summa_procentov[k] = round(stat_like[k] * proc, 1)

    # print(stat_all)
    # print(stat_like)
    # print(raznica)
    # print(summa_procentov)

    # собираем в текст
    header = ''
    dolg = 0
    prc = 0
    for k in stat_all:
        header += f'{k}: {stat_like[k]}/{stat_all[k]} {raznica[k]} {summa_procentov[k]}%\n'
        dolg += raznica[k]
        prc += summa_procentov[k]

    # собираем крусы прогнозов, которые ожидаем
    dolg_kyrs = {}
    for s in statistics:
        bl = s[2]
        if bl == False:
            if s[1] not in dolg_kyrs:
                dolg_kyrs[s[1]] = str(s[3])
            else:
                dolg_kyrs[s[1]] += ', ' + str(s[3])

    # преобразовывеваем открытые прогнозы в строку(если они есть)
    dolg_kyrs_str = ''
    if dolg_kyrs:
        for d in dolg_kyrs:
            dolg_kyrs_str += d + ': ' + dolg_kyrs[d] + ' | '

    sms = (f'Статистика прогнозов\n\n'
           f'{header}\n'
           f'Доход: {prc}%\n\n'
           f'Прогнозы в работе: {dolg}\n'
           f'{dolg_kyrs_str}\n\n'
           f'💵 USDT: {coll_usdt} 💵'
           )

    # изменяем закрепленное сообщение со статистикой
    SendMessage.Refactor(sms)