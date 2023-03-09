import pandas as pd
import numpy as np

# data = {
# 	'A':[0.5,0.5,0.5,-0.5-0.5-0.5],
# 	'B':[0.5,0.5,0.5,-0.5-0.5-0.5],
# }

# df = pd.DataFrame(data)

def LO(df,col):
	df['LO'] = np.where(df.index==df.index[0],df[col],df[col].cumsum()-df[col])
	df['LO'] = np.where(df['LO']>=1,1,np.where(df['LO']<=0,0,df['LO']))
	for i in range(1,len(df.index)):
		df['LO'][i] = df['LO'][i-1] + df[col][i]
		df['LO'][i] = np.where(df['LO'][i] >=1,1,np.where(df['LO'][i]<0,0,df['LO'][i]))
	return df

# print(LO(df,'A'))