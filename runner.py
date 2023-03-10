import pandas as pd
import numpy as np
import yfinance as yf
import funcDefinition
import ulti
import datetime
import quantstats as qs
import warnings
warnings.filterwarnings('ignore')

### load config factors from config
# config = pd.read_csv('config.csv', nrows=2)
config = pd.read_csv('config.csv')
print()

class strategyConfig():
	def __init__(self,strategy,startDate,endDate,beginCash):
		self.strategy = strategy
		self.startDate = startDate
		self.endDate = endDate
		self.beginCash = beginCash
		print(strategy,startDate,endDate)

### load signal factors from funcDefinition
dfs = []
results = []
backtests = []

for i in config.index:
	configi = config.loc[i,:].values.tolist()
	strategyConfig(configi[0], configi[1], configi[2], configi[3])
	signal = getattr(funcDefinition, configi[0]) # source signal from definition
	signal = signal()
	signal.index = pd.to_datetime(signal.index)
	signal['Datelogic'] = np.logical_and(signal.index >= pd.Timestamp(configi[1]), signal.index<=pd.Timestamp(configi[2])).astype(int)
	signal.loc[signal['buy']>=signal['Close'],'combine'] = 0.1 #buy and sell for 10% of beginCash only
	signal.loc[signal['sell']<=signal['Close'],'combine'] = -0.1
	signal['combine'] = signal['combine'] * signal['Datelogic']
	signal = ulti.LO(signal, 'combine')
	signal['Trade'] = signal['LO'] - (signal['LO'].shift(1).replace(np.nan,0))
	signal['TradeQut'] = (signal['Trade']*configi[3]/signal['Close']).apply(np.floor)
	signal['TotalQut'] = signal['TradeQut'].cumsum()
	signal['Cash'] = configi[3] - (signal['TradeQut']*signal['Close']).cumsum()
	signal['TotalExp'] = signal['Cash'] + signal['TotalQut']*signal['Close']
	signal['returns'] = (signal['TotalExp']/signal['TotalExp'].shift(1)).replace(np.nan,1) -1
	backtest = qs.reports.metrics(signal[['returns']], mode="basic",display=False).T
	backtest = backtest[['Sharpe', 'Max Drawdown','Longest DD Days']]
	signal = signal.drop(['Datelogic','combine','LO','Trade','TradeQut','TotalQut','Cash','returns'],axis ='columns')
	signal = signal.rename(columns={'buy':configi[0]+'_buy','sell':configi[0]+'_sell','TotalExp':configi[0]+'_exp'},inplace=False)

	result = (signal.loc[pd.Timestamp(configi[2]),configi[0]+'_exp'] / signal.loc[pd.Timestamp(configi[1]),configi[0]+'_exp']) -1

	dfs.append(signal)
	results.append(result)
	backtests.append(backtest)
	#print(signal)

signal= pd.concat(dfs,axis=1)
backtests = pd.concat(backtests,axis = 0).reset_index(drop=True)
signal.to_csv('signal.csv')
print()

### build result file
res = config
res['result'] = results
res = pd.concat([res, backtests], axis=1)
res.to_csv('result.csv')






