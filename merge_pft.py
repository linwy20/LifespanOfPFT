#-*- coding : utf-8-*-
"""
Created on Fri 2023-06-09 21:39:52 

@author: Wanyi

"""


import numpy as np
import pandas as pd



data0 = pd.read_csv('merge_wright.csv',sep=',',header=0)
# ['ObservationID', 'lifespan', 'UnitName', 'ErrorRisk', 'Dataset',
#        'SpeciesName', 'AccSpeciesName', 'pft_wright_SpsMatch', 'lon', 'lat',
#        'Altitude', 'ValueKindName', 'OrigUncertaintyStr', 'UncertaintyName',
#        'Replicates', 'RelUncertaintyPercent', 'Location_Site_Name',
#        'Location_Site_ID', 'Location_Country', 'Location_Region',
#        'Location Name', 'Vegetation-type/Biome', 'Vegetation-type/Biome2',
#        'Treatment_Exposition', 'CZofProvenace',
#        'Ecosystem_Description_Of_Provenance_Litter',
#        'Habitat_site_description', 'Habitat_at_provenance_of_litter',
#        'LAI_of_Site', 'Mean_sum_of_annual_precipitation',
#        'Mean_annual_temperature_(MAT)', 'Maximum_Green_Vegetation_Fraction',
#        'LastName', 'Comments_notes_methods', 'Comment', 'Reference']


# ============================================================================================================
# 读取PFT数据
data = pd.read_csv('pft_unprocessed.csv', sep=',', header=0, usecols=[7,8,10,11,12,13,15,21,26],low_memory=False)
# 所有column: ['Unnamed: 0', 'LastName', 'FirstName', 'DatasetID', 'Dataset',
#        'SpeciesName', 'AccSpeciesID', 'AccSpeciesName', 'ObservationID',
#        'ObsDataID', 'TraitID', 'TraitName', 'DataID', 'DataName', 'OriglName',
#        'OrigValueStr', 'OrigUnitStr', 'ValueKindName', 'OrigUncertaintyStr',
#        'UncertaintyName', 'Replicates', 'StdValue', 'UnitName',
#        'RelUncertaintyPercent', 'OrigObsDataID', 'ErrorRisk', 'Reference',
#        'Comment', 'StdValueStr', 'V29']

# ============================================================================================================
# 根据 data0的 ObsID来裁剪 pft数据
data ['ObservationID'] = data ['ObservationID'].astype('str')
data0['ObservationID'] = data0['ObservationID'].astype('str')
data1  = data[data['ObservationID'].isin(data0['ObservationID'])]


# 制作 ['ObservationID','Pft_{scheme}] 数据框
def makedframe(datain, scheme, scheme_short):
	df = datain[(datain['TraitID'] == 197) & (datain['DataName'] == scheme)]
	df = df[['ObservationID','OrigValueStr']]
	df = df.rename(columns={'OrigValueStr': 'pft_%s'%scheme_short})
	# 去掉nan值
	df.replace('na',np.nan,inplace=True)
	df = df[~(pd.isna(df['pft_%s'%scheme_short]))]
	print('\nlen of %s:'%scheme_short, len(df), len(np.unique(df['ObservationID'])))
	return(df)

dfsdgvm1 = makedframe(data1, 'Plant functional type PFT (Sheffield DGVM 1)', 'SDGVM1')
dfsdgvm2 = makedframe(data1, 'Plant functional type PFT (Sheffield DGVM 2)', 'SDGVM2')
dfsdgvm3 = makedframe(data1, 'Plant functional type PFT (Sheffield DGVM 3)', 'SDGVM3')
dfbbgc1  = makedframe(data1, 'Plant functional type PFT (Biome-BGC 1)', 'BBGC1')
dfbbgc2  = makedframe(data1, 'Plant functional type PFT (Biome-BGC 2)', 'BBGC2')
dflpj1   = makedframe(data1, 'Plant functional type PFT (LPJ DGVM 1)', 'LPJ1')
dflpj2   = makedframe(data1, 'Plant functional type PFT (LPJ DGVM 2)', 'LPJ2')

# 把数据框与 lifespan数据合并
dfmer = data0
dfmer = pd.merge(dfmer, dfsdgvm3,how='outer',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfbbgc2, how='outer',on=['ObservationID'])
dfmer = pd.merge(dfmer, dflpj2,  how='outer',on=['ObservationID'])



# ============================================================================================================
# 根据 data0的 'AccSpeciesName' 来裁剪 pft数据。 如果某个观测没有pft信息, 但存在相同的物种有pft, 则把pft共享, 输出到新的列
data2  = data[data['AccSpeciesName'].isin(data0['AccSpeciesName'])]
data2 = data2.replace('na',np.nan)  # 把na设为缺省值

# 制作 ['ObservationID','Pft_{scheme}_SpsMatch] 数据框
def makedframev2(datain, scheme, scheme_short):
	df = datain[(datain['TraitID'] == 197) & (datain['DataName'] == scheme)]
	df = df[['ObservationID','AccSpeciesName','OrigValueStr']]
	df = df.rename(columns={'OrigValueStr': 'pft_%s'%scheme_short})
	# print('\nReference:',np.unique(df['Reference']))
	
	# 去掉nan值后统计
	df = df[~(pd.isna(df['pft_%s'%scheme_short]))]
	print('\nlen of %s:'%scheme_short, len(df), len(np.unique(df['AccSpeciesName'])))
	return(df)

# 制作 ['ObservationID','pft_{scheme}_SpsMatch'] 数据框
dfpft      = makedframev2(data2, 'Plant functional Type' , 'PFT_SpsMatch')
dfwright   = makedframev2(data2, 'Plant functional type (Ian Wright)', 'Ian Wright_SpsMatch')
dfjules_ev = makedframev2(data2, 'Plant functional type (JULES plus ev/dec)', 'JULES plus ev/dec_SpsMatch')
dfjules    = makedframev2(data2, 'Plant functional type (JULES)' , 'JULES _SpsMatch')
dfpft_pft  = makedframev2(data2, 'Plant functional type (PFT)', 'PFT(PFT)_SpsMatch')
dfstich    = makedframev2(data2, 'Plant functional type (Sitch, Harper, Mercado)', 'Sitch, Harper, Mercado_SpsMatch')
dfbbgc1    = makedframev2(data2, 'Plant functional type PFT (Biome-BGC 1)', 'BBGC1_SpsMatch')
dfbbgc2    = makedframev2(data2, 'Plant functional type PFT (Biome-BGC 2)', 'BBGC2_SpsMatch')
dflpj1     = makedframev2(data2, 'Plant functional type PFT (LPJ DGVM 1)', 'LPJ1_SpsMatch')
dflpj2     = makedframev2(data2, 'Plant functional type PFT (LPJ DGVM 2)', 'LPJ2_SpsMatch')
dfsdgvm1   = makedframev2(data2, 'Plant functional type PFT (Sheffield DGVM 1)', 'SDGVM1_SpsMatch')
dfsdgvm2   = makedframev2(data2, 'Plant functional type PFT (Sheffield DGVM 2)', 'SDGVM2_SpsMatch')
dfsdgvm3   = makedframev2(data2, 'Plant functional type PFT (Sheffield DGVM 3)', 'SDGVM3_SpsMatch')


# 把所有数据框合并
dfmer2 = dfpft
list1 = ['dfpft','dfwright','dfjules_ev','dfjules','dfpft_pft','dfstich','dfbbgc1','dfbbgc2','dflpj1','dflpj2','dfsdgvm1','dfsdgvm2','dfsdgvm3']  
for i in list1[1:]:
    exec('dfmer2 = pd.merge(dfmer2, {}, how=\'outer\',on=[\'ObservationID\',\'AccSpeciesName\'])'.format(i))

# ============================================================================================================
# 新建列, 如果物种存在, 给它赋值
pftlist = ['pft_PFT_SpsMatch', 'pft_Ian Wright_SpsMatch','pft_JULES plus ev/dec_SpsMatch', 'pft_JULES _SpsMatch','pft_PFT(PFT)_SpsMatch', 'pft_Sitch, Harper, Mercado_SpsMatch','pft_BBGC1_SpsMatch', 'pft_BBGC2_SpsMatch', 'pft_LPJ1_SpsMatch','pft_LPJ2_SpsMatch', 'pft_SDGVM1_SpsMatch', 'pft_SDGVM2_SpsMatch','pft_SDGVM3_SpsMatch']
maxnum = 1
strr = '/'
for p in range(len(pftlist)):
	# print('\n==============%s=============='%pftlist[p])
	dfmer[pftlist[p]] = ''
	for i in range(len(dfmer)):
		tmp0 = dfmer2[pftlist[p]][dfmer2['AccSpeciesName']==dfmer.loc[i,'AccSpeciesName']]
		pfts  = tmp0.dropna().astype(str)
		if len(np.unique(pfts)) == 1:
			dfmer.loc[i,pftlist[p]] = np.unique(pfts)[0]
		elif len(np.unique(pfts)) > 1:
			# print(dfmer.loc[i,'AccSpeciesName'],np.unique(pfts))
			dfmer.loc[i,pftlist[p]] = strr.join(np.unique(pfts))
			
			if len(np.unique(pfts)) > maxnum:
				maxnum = len(np.unique(pfts))

			if len(np.unique(pfts)) == 5:
				print(dfmer.loc[i,'AccSpeciesName'],np.unique(pfts))



# 可能可以补充缺失的经纬度的数据 ———— 没有新的可以补充======================
tmpp = dfmer['ObservationID'][~pd.isna(dfmer['lat'])]
tmp2 = dfmer['ObservationID'][~pd.isna(dfmer['lat'])]
print('\nlen(tmp2)',len(tmp2))  # 2706
list = [59,60,193,449,505,506,509,1412,1413,202,114,1736,2525,112]
for i in range(len(list)):
	dftmp = data1[['ObservationID','OrigValueStr','DataName']][data['DataID'] == list[i]]        
	print('\n\n','DataID=', list[i],'\nlen of dftmp', len(dftmp)) 
	dftmp  = dftmp.reset_index(drop=True)
	if (len(dftmp)>0): print('\nDataName=', dftmp.loc[0,'DataName'])   
	tmp1 = dftmp[ ~dftmp['ObservationID'].isin(tmpp) ]
	if i==0:
		tmp2 = tmp1['ObservationID']
		print('\nlen new:', len(tmp2))
	else:
		tmp0 = tmp1[ ~tmp1['ObservationID'].isin(tmp2) ]
		if (list[i]==1736): print(tmp0['OrigValueStr'])
		tmp2 = pd.concat([tmp2,tmp0['ObservationID']])
		print('\nlen new:', len(tmp0))
# len new 全都是0
# 可能可以补充缺失的经纬度的数据 ———— 没有新的可以补充======================


# 输出文件
output='merge_pft.csv'
dfmer.to_csv(output,sep=',',index=False)#,header=False)
