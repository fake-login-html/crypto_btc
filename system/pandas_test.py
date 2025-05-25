import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.dialects.postgresql import plainto_tsquery

from database.db_ton import DataBase
import psycopg2
import sqlalchemy as sa

my_series = pd.Series([5, 6, 7, 8, 9, 10])
indx = my_series.index
vall = my_series.values

# print(indx)
# print(vall)


my_series2 = pd.Series([5, 6, 7, 8, 9, 10], index=['a', 'b', 'c', 'd', 'e', 'f'])
my_series2[['a', 'b', 'f']] = 0
# print(my_series2[my_series2 > 0] * 2)
# print(my_series2)

my_series3 = pd.Series({'a': 5, 'b': 6, 'c': 7, 'd': 8})
# print(my_series3)
# print(5 in my_series3.values)

my_series3.name = 'numbers'
my_series3.index = ['A', 'B', 'C', 'D']
my_series3.index.name = 'letters'

# print(my_series3)

df = pd.DataFrame({
  'country': ['Kazakhstan', 'Russia', 'Belarus', 'Ukraine'],
  'population': [17.04, 143.5, 9.5, 45.5],
  'square': [2724902, 17125191, 207600, 603628]
})

df['density'] = df['population'] / df['square'] * 1000000
# df = df.rename(columns={'country': 'country_'})
# del df['square']

# print(df)
# print(df['country'])
# print(df.columns)
# print(df.loc[0])
# print(df.loc[[0, 1], 'population'])
# print(df.loc['1':'3', :])
# print(df[df.population > 10][['country', 'square']])
# print(df[df['population'] > 10])

# print(df)

pl = pd.read_csv('apple.csv', index_col='Date', parse_dates=True)
pl.sort_index()
# pl.resample('W')['Close'].mean()
# new_sample_df = pl.loc['2017-Feb', ['Close']]

# new_sample_df = pl.loc['2012-Feb':'2017-Feb', ['Close']]
# print(new_sample_df)
# new_sample_df.plot()
# plt.show()

# DATABASE
# dbs = DataBase().statistics()
# conn = psycopg2.connect(dbname='Crypto', user='satoshi', password='satoshi', host='localhost')

your_username = 'satoshi'
your_password = 'satoshi'
your_database = 'Crypto'
localhost = 'localhost'
your_port = 5432

conn = sa.create_engine(f'postgresql://{your_username}:{your_password}@{localhost}:{your_port}/{your_database}')

# график сигналов
my_series4 = pd.read_sql("SELECT date, procent, Null as price,price as price_s, moneta, use, prognoz FROM public.signal where moneta = 'TON'  order by date asc;", conn)
# my_series4 = pd.read_sql("SELECT date, procent, moneta, use, prognoz FROM public.signal where moneta = 'BTC' order by date asc;", conn)
# my_series4.plot(x='date', y='prognoz')

# график цены
my_series5 = pd.read_sql("SELECT date, price FROM public.price where moneta = 'TON' order by date asc;", conn)
# my_series5.plot(x='date', y='price')
# my_series4.plot(x='date')

my_series4 = my_series4[['date', 'price', 'price_s']]#, 'prognoz']]

test = pd.concat([my_series4, my_series5], sort=False, axis=0)
test.plot(x='date')
plt.show()

#
# my_series4.merge(my_series5, left_on='date', right_on='date', how='right')

test1 = test.mean()
print(my_series4)
# print(my_series4['prognoz'].agg(['mean']))

