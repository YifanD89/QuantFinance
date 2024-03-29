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
	def __init__(self,strategy,startDate,endDate,beginCash,step_position):
		self.strategy = strategy
		self.startDate = startDate
		self.endDate = endDate
		self.beginCash = beginCash
		self.step_position = step_position
		print(strategy,startDate,endDate,step_position)

### load signal factors from funcDefinition
dfs = []
results = []
backtests = []

for i in config.index:
	configi = config.loc[i,:].values.tolist()
	strategyConfig(configi[0], configi[1], configi[2], configi[3],configi[4])
	signal = getattr(funcDefinition, configi[0]) # source signal from definition
	signal = signal()
	signal.index = pd.to_datetime(signal.index)
	signal['Datelogic'] = np.logical_and(signal.index >= pd.Timestamp(configi[1]), signal.index<=pd.Timestamp(configi[2])).astype(int)
	signal.loc[signal['buy']>=signal['Adj Close'],'combine'] = configi[4] #buy and sell for fixed % of total position
	signal.loc[signal['sell']<=signal['Adj Close'],'combine'] = -configi[4]

	## factor logic
	signal['combine'] = signal['combine'] * signal['Datelogic'].round(2)
	signal = ulti.LO(signal, 'combine').round(2)
	signal['Trade'] = (signal['LO'] - (signal['LO'].shift(1).replace(np.nan,0))).round(2)
	signal['TradeQut'] = 0
	signal['TotalQut'] = 0
	signal['Cash'] = configi[3]
	signal['TotalExp'] = 0
	signal['returns'] = 0
	signal = signal.reset_index()

	## trade logic
	for i in signal.index:

		#first day 
		signal.loc[(signal['Date']==configi[1]) & (signal['Trade']>0),'TradeQut'] =\
		(configi[3]*configi[4]/(1-0)/signal['Adj Close']).apply(np.floor).replace(np.nan,0)

		#any day after
		signal.loc[(signal['Date']>configi[1]) & (signal['Trade']>0),'TradeQut'] =\
		(signal['Cash'].shift(1)*configi[4]/(1-signal['LO'].shift(1))/signal['Adj Close']).apply(np.floor).replace(np.nan,0)

		signal.loc[(signal['Date']>configi[1]) & (signal['Trade']<0),'TradeQut'] =\
		(-signal['TotalQut'].shift(1)*configi[4]/(signal['LO'].shift(1))).apply(np.ceil).replace(np.nan,0)

		signal.loc[signal['Trade']==0,'TradeQut'] = 0
		
		signal['TotalQut'] = signal['TradeQut'].cumsum()
		signal['Cash'] = configi[3] - (signal['TradeQut']*signal['Adj Close']).cumsum()
		signal['TotalExp'] = signal['Cash'] + signal['TotalQut']*signal['Adj Close']

	signal = signal.set_index('Date')
	signal['returns'] = (signal['TotalExp']/signal['TotalExp'].shift(1)).replace(np.nan,1) -1
			
	backtest = qs.reports.metrics(signal[['returns']], mode="basic",display=False).T
	backtest = backtest[['Sharpe', 'Max Drawdown','Longest DD Days']] ## DD includes weekend
	# signal = signal.drop(['Datelogic','combine','LO','Trade','TradeQut','TotalQut','Cash','returns'],axis ='columns')

	signal = signal.rename(columns={'buy':configi[0]+'_buy','sell':configi[0]+'_sell','TotalExp':configi[0]+'_exp'},inplace=False)
	result = (signal.loc[pd.Timestamp(configi[2]),configi[0]+'_exp'] / signal.loc[pd.Timestamp(configi[1]),configi[0]+'_exp']) -1

	dfs.append(signal)
	results.append(result)
	backtests.append(backtest)
	# print(signal)

signal= pd.concat(dfs,axis=1)
backtests = pd.concat(backtests,axis = 0).reset_index(drop=True)
signal.to_csv('signal.csv')
print()

### build result file
res = config
res['result'] = results
res = pd.concat([res, backtests], axis=1)
res.to_csv('result.csv')






