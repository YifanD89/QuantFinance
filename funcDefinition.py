import pandas as pd
import numpy as np
import yfinance as yf

# Ticker = ['SPY','AAPL','^VIX']
Ticker = ['SPY']
price = pd.DataFrame()

for i in Ticker:
	pricei = yf.download(i,start='2022-01-01',end='2023-12-31')
	pricei['Ticker'] = i 
	pricei = pricei[['Ticker','Adj Close']]
	price = pd.concat([price,pricei])
price.to_csv('price.csv')

date = pd.read_csv('price.csv', index_col=0)
# print(date)

def Target_480():
	df = date
	df['buy'] = 480 # close lower than buy then buy, 0 never buy
	df['sell'] = 480 # close higher than sell then sell, 10000 never sell
	return(df)

def Target_470():
	df = date
	df['buy'] = 470 
	df['sell'] = 470 
	return(df)

def Target_460():
	df = date
	df['buy'] = 460 
	df['sell'] = 460 
	return(df)

def Target_450():
	df = date
	df['buy'] = 450 
	df['sell'] = 450 
	return(df)
	
def Target_440():
	df = date
	df['buy'] = 440 
	df['sell'] = 440 
	return(df)

def Target_430():
	df = date
	df['buy'] = 430 
	df['sell'] = 430 
	return(df)

def Target_420():
	df = date
	df['buy'] = 420 
	df['sell'] = 420 
	return(df)

def Target_410():
	df = date
	df['buy'] = 410 
	df['sell'] = 410 
	return(df)

def Target_400():
	df = date
	df['buy'] = 400 
	df['sell'] = 400 
	return(df)

def Target_390():
	df = date
	df['buy'] = 390 
	df['sell'] = 390 
	return(df)

def Target_380():
	df = date
	df['buy'] = 380 
	df['sell'] = 380 
	return(df)

def Target_370():
	df = date
	df['buy'] = 370 
	df['sell'] = 370 
	return(df)

def Target_360():
	df = date
	df['buy'] = 360 
	df['sell'] = 360 
	return(df)

def Target_300():
	df = date
	df['buy'] = 300 
	df['sell'] = 300 
	return(df)

def Target_100():
	df = date
	df['buy'] = 100 
	df['sell'] = 100 
	return(df)

def Avg_Prev30():
	df = date
	df['buy'] = df['Close'].rolling(21).mean().replace(np.nan,0)
	df['sell'] = df['Close'].rolling(21).mean().replace(np.nan,10000)
	return(df)

def Avg_Prev90():
	df = date
	df['buy'] = df['Close'].rolling(63).mean().replace(np.nan,0)
	df['sell'] = df['Close'].rolling(63).mean().replace(np.nan,10000)
	return(df)

def Avg_Prev180():
	df = date
	df['buy'] = df['Close'].rolling(126).mean().replace(np.nan,0)
	df['sell'] = df['Close'].rolling(126).mean().replace(np.nan,10000)
	return(df)

def B380_S420():
	df = date
	df['buy'] = 380
	df['sell'] = 420
	return(df)

def Target_25():
	df = date
	df['buy'] = 25
	df['sell'] = 25
	return(df)

def Target_20():
	df = date
	df['buy'] = 20
	df['sell'] = 20
	return(df)