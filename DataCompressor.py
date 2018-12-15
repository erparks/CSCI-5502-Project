import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


#convert given format into datetime objects
crypto_date_converter = lambda date: datetime.strptime(date, '%b %d, %Y')
stock_date_converter  = lambda date: datetime.strptime(date, '%Y-%m-%d')


def clean_crypto(path):
    df = pd.read_csv(path)
    df.Date = list(map(crypto_date_converter, df.Date))
    calc_percent_change(df)
    return df

def clean_stock(path):
    df = pd.read_csv(path)
    df.Date = list(map(stock_date_converter, df.Date))
    df.sort_index(axis=1 ,ascending=True)
    df = df.iloc[::-1]
    df.index = range(len(df.index))
    calc_percent_change(df)
    return df

def calc_percent_change(df):
    change = []
    for i  in range(1, len(df.Close)):
        change.append(daily_change(df.Close[i], df.Close[i-1]))

    change.insert(0, 0)

    df['daily_change'] = change

def daily_change(old, new):
    return (old - new)/old;



#This assumes data files are located in a file named 'data' in the same directory
# as this python script
def combine():

    #Read in crypto prices
    Bitcoin  = clean_crypto('data/bitcoin_price.csv')
    Litecoin = clean_crypto('data/litecoin_price.csv')
    Ethereum = clean_crypto('data/Ethereum_price.csv')
    
    Bitcoin.to_csv('data/clean_Bitcoin.csv')
    Litecoin.to_csv('data/clean_Litecoin.csv')
    Ethereum.to_csv('data/clean_Ethereum.csv')
    
    #Read in stock prices
    VGT = clean_stock('data/VGT.csv')
    VOO = clean_stock('data/VOO.csv')
    VTI = clean_stock('data/VTI.csv')

    VGT.to_csv('data/clean_VGT.csv')
    VOO.to_csv('data/clean_VOO.csv')
    VTI.to_csv('data/clean_VTI.csv')

    print('complete')
    print(VGT)

if __name__ == "__main__":
    combine()
