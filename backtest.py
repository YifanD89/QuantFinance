import datetime as dt
import pandas as pd
import numpy as np
# from openbb_terminal.sdk import openbb
import quantstats as qs
# import backtrader as bt

df = pd.read_csv('signal.csv',index_col=0)
df = df[['Target_400_exp']]
df['returns'] = (df['Target_400_exp'] / df['Target_400_exp'].shift(1)).replace(np.nan,1) -1
df = df.drop('Target_400_exp',axis = 'columns')
df.index = pd.to_datetime(df.index)
print(df)
print()

# qs.reports.metrics(df, mode="basic")

a = qs.reports.metrics(df, mode="basic",display=False).T
a = a[['Sharpe', 'Max Drawdown','Longest DD Days']]

print(a)


