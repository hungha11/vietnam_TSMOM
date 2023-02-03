## take data from TCBS API
import json
from locale import D_FMT
from requests import get
import pandas as pd
import datetime
import time
import numpy as np
import matplotlib.pyplot as plot

class DataLoader:
    '''
    Web scraping from TCBS


    INPUT
    -----------------
    ticker :: stock or index symbol
    type :: if symbol is a stock, type is stock; if symbol is index, type is index
    resolution :: timeframe of data (1m, 5m, 30m, Daily, etc)
    startDate :: starting date of the api
    endDate :: ending date of the api
    data ::


    OUTPUT
    -------------
    dataframe :: OHCLV dataframe
    API_LOAD :: api link
    '''
    
    def __init__(self, ticker, type, resolution, startDate, endDate, data):
        self.ticker = ticker 
        self.type = type 
        self.resolution = resolution 
        self.startDate = startDate 
        self.endDate = endDate 
        self.data = data

    def getData(ticker, type, resolution, startDate, endDate):
        timeFormat = '%Y-%m-%d'
        startDate = str(int(time.mktime(time.strptime(startDate, timeFormat))))
        endDate = str(int(time.mktime(time.strptime(endDate, timeFormat))))
        API_LOAD = "https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/bars-long-term?ticker=" + ticker +"&type=" + type + "&resolution=" \
                    + resolution + "&from=" + startDate + "&to=" + endDate
        data = json.loads(
            get(API_LOAD).text
        )
        
        return data, API_LOAD

#load stock and index data
def load_stock_data(symbol,start,end):
    '''
    stock data loading fundtion

    INPUT
    ---------
    symbol :: stock symbol
    start  :: starting date
    end    :: end date


    OUTPUT
    ---------
    dataframe :: stock price OHCLV data frame and percentage return, logrithm return
    '''


    data, API = DataLoader.getData(ticker = symbol, type ='stock', resolution ="D", 
                                   startDate = start, endDate = end)
    
    df = pd.DataFrame.from_dict(data['data'])
    df.set_index('tradingDate', inplace=True)
    df['pct_return'] = df.close.pct_change()
    df['log_return'] = np.log(df.close) - np.log(df.close.shift(1))
    df.index = pd.to_datetime(df.index)
    df.index=df.index.strftime('%Y-%m-%d')
    if df.index[-1]==df.index[-2]:
        df = df[:-1]
    return df[1:]

def load_index_data(symbol,start,end):
    '''
    index data loading fundtion

    INPUT
    ---------
    symbol :: index symbol
    start  :: starting date
    end    :: end date


    OUTPUT
    ---------
    dataframe :: index price OHCLV data frame and percentage return, logrithm return
    '''
    data, API = DataLoader.getData(ticker = symbol, type ='index', resolution ="D", 
                                   startDate = start, endDate = end)
    
    df = pd.DataFrame.from_dict(data['data'])
    df.set_index('tradingDate', inplace=True)
    df['pct_return'] = df.close.pct_change()
    df['log_return'] = np.log(df.close) - np.log(df.close.shift(1))
    df.index = pd.to_datetime(df.index)
    df.index=df.index.strftime('%Y-%m-%d')
    df = df[:end]
    return df[1:]

def load_macro_data(symbol,start,end):
#     symbol = 'VNgovbond10y'
#     symbol ='USDVND'
    if symbol == 'VNgovbond10y':
        URL = 'https://markets.tradingeconomics.com/chart?s=vnmgovbon10y:gov&span=5y&securify=new&url=/vietnam/government-bond-yield&AUTH=YRSYnbh3Baw6lci66b%2F1cDvnXWG4aGg2EDEvMmg%2FL%2B9GZI8zrNUxjxD7ZWzTS9h1&ohlc=0'
    if symbol == 'USDVND':
        URL = ' https://markets.tradingeconomics.com/chart?s=usdvnd:cur&span=5y&securify=new&url=/vietnam/currency&AUTH=YRSYnbh3Baw6lci66b%2F1cGYi0i5YijET80qrMpuaZJnyBxceZvjxbtkitI%2FYUjUK&ohlc=0'
    
    
    data = json.loads(get(URL).text)
    df = pd.DataFrame(data['series'][0]['data'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(df.date,inplace=True)
    df.drop(['date','x'],axis=1,inplace=True)
    df.index=df.index.strftime('%Y-%m-%d')
    df.rename(columns={'y':symbol},inplace=True)
    return df.loc[start:end]