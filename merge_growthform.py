#-*- coding : utf-8-*-
"""
Created on Fri 2023-09-15 21:18:52 

@author: Wanyi

"""


import numpy as np
import pandas as pd


data1 = pd.read_csv('merge_LUT.csv',sep=',',header=0)

data2 = pd.read_csv('growthform_cutrow.csv',sep=',',header=0,low_memory=False)

# ====================================================
data1['ObservationID'] = data1['ObservationID'].astype('str')
data2['ObservationID'] = data2['ObservationID'].astype('str')

data3 = data2[ data2['ObservationID'].isin(data1['ObservationID']) ]

data3 = data3[['ObservationID','OrigValueStr','Comment','DataID','DataName']][data3['TraitID'] == 42]
data3 = data3.rename(columns={'OrigValueStr': 'growthform'})

dataids = [47,870,959,2390,2391,2392,2393,2394,2395,2396,2397,2398,2399,2400,2401,2402,2403,2404,2405,2407,2408,2409,2410,2411,2481,2503,7059]

datanames = ['']*len(dataids)
for x in range(len(dataids)):
	tmp = data3[data3['DataID']==dataids[x]]['DataName']
	tmp = tmp.reset_index(drop=True)
	datanames[x] = tmp[0]
	print(datanames[x])



def makedframe(data, dataid, dataname):
	df = data[data['DataID'] == dataid]
	df = df[['ObservationID','growthform']]
	print('======================')
	print('len of id=%d:'%dataid, len(df))
	print('len of observationID:',len(np.unique(df['ObservationID'])))
	df = df.rename(columns={'growthform': '%s'%dataname})
	return(df)

dfmer = data1
print('dfmer:\n',dfmer)
for i in range(len(dataids)):
	df = makedframe(data3,dataids[i],datanames[i])
	print(np.unique(df[datanames[i]]))
	print('df:\n',df)
	dfmer = pd.merge(dfmer, df,  how='outer',on=['ObservationID'])


print('columns:\n',dfmer.columns)
long = ['Plant growth form: tree', 'Plant growth form: small tree','Plant growth form: shrub', 'Plant growth form: erect dwarf shrub','Plant growth form: prostrate dwarf shrub', 'Plant growth form: liana','Plant growth form: climber', 'Plant growth form: forb','Plant growth form: geophyte', 'Plant growth form: graminoid','Plant growth form: succulent', 'Plant growth form: fern/fern ally','Plant growth form: epiphyte/parasite']#, 'Plant form: Non-distinctive','Plant form: vase', 'Plant form: open', 'Plant form: cushion','Plant form: caespitose', 'Plant form: tangled', 'Plant form: climbing','Plant form: prostrate', 'Leaf succulence', 'Stem succulent']
shor = ['T','T','S','S','S','liana','C','G','geophyte','G','succulent','fern','EP']#, 'Plant form: Non-distinctive','vase', 'open', 'cushion','caespitose', 'tangled', 'climbing','prostrate', 'Leaf succulence', 'Stem succulent']

dfmer['SumForm'] = ''
for i in range(len(long)):
	dfmer.loc[dfmer[long[i]]=='yes', 'SumForm' ] = shor[i]


print(np.unique(dfmer['Plant growth form'].astype('str')))
long = ['C', 'Climb  resp.  V', 'Climber', 'Epiphyte', 'F', 'G', 'G&S  resp.  G&S', 'H', 'Halfshrubs  resp.  S', 'Herb', 'Herb  resp.  H', 'L', 'Palm  resp.  Palm', 'S', 'S  resp.  S', 'ST', 'Shrub', 'T', 'T  resp.  S', 'T  resp.  T', 'Tree', 'V', 'W climb  resp.  V', 'carnivorous plant  resp.  carnivorous plant', 'gras', 'herb', 'herbaceous', 'nan', 'resp.  S', 'resp.  T', 'saplings', 'seedlings', 'shrub', 'tree', 'vine', 'woody shrub']
shor = ['C', 'C/V', 'C', 'EP', 'F', 'G', 'G/S', 'G', 'S', 'G', 'G', 'L', 'T', 'S', 'S', 'T/S', 'S', 'T', 'T/S', 'T', 'T', 'V', 'C/V', 'G', 'G', 'G', 'G', '', 'S', 'T', 'T', 'T', 'S', 'T', 'V', 'S']

print(len(long),len(shor))
for i in range(len(long)):
	dfmer.loc[dfmer['Plant growth form']==long[i], 'SumForm' ] = shor[i]


dfmer.drop(columns=['Plant growth form', 'Plant growth form: Succulence', 'Multi-stemness', 'Plant growth form: tree', 'Plant growth form: small tree', 'Plant growth form: shrub', 'Plant growth form: erect dwarf shrub', 'Plant growth form: prostrate dwarf shrub', 'Plant growth form: liana', 'Plant growth form: climber', 'Plant growth form: forb', 'Plant growth form: geophyte', 'Plant growth form: graminoid', 'Plant growth form: succulent', 'Plant growth form: fern/fern ally', 'Plant growth form: epiphyte/parasite', 'Plant form: Non-distinctive', 'Plant form: vase', 'Plant form: open', 'Plant form: cushion', 'Plant form: caespitose', 'Plant form: tangled', 'Plant form: climbing', 'Plant form: prostrate', 'Leaf succulence', 'Stem succulent', 'Plant growth form (genera)'],inplace=True)

# ======================================================================



dfmer['SumForm_SpsMatch'] = dfmer['SumForm']
dfmer['SumForm_SpsMatch'] = dfmer['SumForm_SpsMatch'].replace('',np.nan)
nanind = np.where( pd.isna(dfmer['SumForm_SpsMatch']) )[0]

maxnum = 1
strr   = '/'
for i in range(len(nanind)):
	tmp0 = dfmer['SumForm_SpsMatch'][ dfmer['AccSpeciesName']==dfmer['AccSpeciesName'][nanind[i]] ]
	form = tmp0.dropna().astype(str)
	if len(np.unique(form)) == 1:
		dfmer.loc[[nanind[i]],'SumForm_SpsMatch'] = np.unique(form)[0]
	elif len(np.unique(form)) > 1:
		dfmer.loc[[nanind[i]],'SumForm_SpsMatch'] = strr.join(np.unique(form))
		print(dfmer['AccSpeciesName'][nanind[i]], np.unique(form))
		
		if len(np.unique(form)) > maxnum:
			maxnum = len(np.unique(form))


output='merge_growthform.csv'
dfmer.to_csv(output,sep=',',index=False)#,header=False)
