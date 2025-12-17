#-*- coding : utf-8-*-
"""
Created on Fri 2023-06-09 21:39:52 

@author: Wanyi

"""


import numpy as np
import pandas as pd


data = pd.read_csv('./lifespan_unprocessed.csv',sep=',',header=0,low_memory=False,usecols=[1,4,5,7,8,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]) # 仅读取部分列


# 根据['OrigObsDataID']删掉duplicate的观测=======================================
dupid = data[data['OrigObsDataID'] > 0]  # 提取 ['OrigObsDataID']>0 时的['ObservationID']
# 把重复的观测删掉
data = data[~data['ObservationID'].isin(dupid['ObservationID'])]
# 根据['OrigObsDataID']删掉duplicate的观测=======================================


# 删掉lifespan=0、缺测的观测===========================================================
zeroid = data[(data['TraitID'] == 12) & (data['StdValue'] == 0)]  # 提取 ['TraitID']=12 且 ['StdValue']=0 时的['ObservationID']
data = data[~data['ObservationID'].isin(zeroid['ObservationID'])]

nanid  = data[(data['TraitID'] == 12) & (pd.isna(data['StdValue']))]
data   = data[~data['ObservationID'].isin(nanid['ObservationID'])]    # 去掉缺测值
# 删掉lifespan=0、缺测的观测===========================================================


del dupid, zeroid, nanid



# 制作新的dataframe, 使经纬度、物种、观测ID、lifespan等变成列名=========================
# | ObservationID | lat | lon |zone | loc | species  | lifespan | unit |
# ---------------------------------------------------------------------
# |               |     |     |     |     |          |          |      |
# |               |     |     |     |     |          |          |      |
# |               |     |     |     |     |          |          |      |

dflat = data[['ObservationID','StdValue']][data['DataID'] == 59]   
dflat = dflat.rename(columns={'StdValue': 'lat'})       
dftest = dflat.dropna(subset=['lat'])  # 看看有没有缺测值        

dflon = data[['ObservationID','StdValue']][data['DataID'] == 60]
dflon = dflon.rename(columns={'StdValue': 'lon'})
dftest = dflon.dropna(subset=['lon'])  # 看看有没有缺测值


# ==========获取其他的DataID for 更多信息=============
# 加上海拔高度数据(m)
dfaltt = data[['ObservationID','StdValue']][data['DataID'] == 61]
dfaltt = dfaltt.rename(columns={'StdValue': 'Altitude'})

# 加上源地气候区数据, 很可能是实验数据, 所以才给源地的情况. 'Climate zone of provenance of litter'
dfczpl = data[['ObservationID','OrigValueStr']][data['DataID'] == 509]
dfczpl = dfczpl.rename(columns={'OrigValueStr': 'CZofProvenace'})

# 加上 'Comments, notes, methods'
dfcnms = data[['ObservationID','OrigValueStr']][data['DataID'] == 235]
dfcnms = dfcnms.rename(columns={'OrigValueStr': 'Comments_notes_methods'})

# 加上 'Ecosystem description of provenance of litter', 可以帮助确定PFT！ 也很可能是实验数据。
dfedpl = data[['ObservationID','OrigValueStr']][data['DataID'] == 511]
dfedpl = dfedpl.rename(columns={'OrigValueStr': 'Ecosystem_Description_Of_Provenance_Litter'})

# 加上 'Habitat / site description', 可能可以帮助确定PFT, 好像大部分是forest
dfhabi = data[['ObservationID','OrigValueStr']][data['DataID'] == 1863]
dfhabi = dfhabi.rename(columns={'OrigValueStr': 'Habitat_site_description'})

# 加上 'Habitat / site description', 可能可以帮助确定PFT, 好像大部分是forest
dfhabi2 = data[['ObservationID','OrigValueStr']][data['DataID'] == 510]
dfhabi2 = dfhabi2.rename(columns={'OrigValueStr': 'Habitat_at_provenance_of_litter'})

# 加上 'Leaf area index of the site (LAI) (m2/m2)'; 还有GPP, ET, FPAR, NDVI, NPP, 生长季节长度(LGP), VPD, PET... 后面需要再来加上
dflai = data[['ObservationID','OrigValueStr']][data['DataID'] == 201]
dflai = dflai.rename(columns={'OrigValueStr': 'LAI_of_Site'})

# 加上 'Location / Site Name'
dfsite = data[['ObservationID','OrigValueStr']][data['DataID'] == 114]
dfsite = dfsite.rename(columns={'OrigValueStr': 'Location_Site_Name'})

# 加上 'Location Country'
dfcnty = data[['ObservationID','OrigValueStr']][data['DataID'] == 1412]
dfcnty = dfcnty.rename(columns={'OrigValueStr': 'Location_Country'})

# 加上 'Location Name'
dflcnm = data[['ObservationID','OrigValueStr']][data['DataID'] == 1736]
dflcnm = dflcnm.rename(columns={'OrigValueStr': 'Location Name'})

# 加上 'Location Region'
dflcrg = data[['ObservationID','OrigValueStr']][data['DataID'] == 449]
dflcrg = dflcrg.rename(columns={'OrigValueStr': 'Location_Region'})

# 加上 'Location Site ID'
dfsiid = data[['ObservationID','OrigValueStr']][data['DataID'] == 112]
dfsiid = dfsiid.rename(columns={'OrigValueStr': 'Location_Site_ID'})

# 加上 'Maximum Green Vegetation Fraction (%)'
dfmgvf = data[['ObservationID','OrigValueStr']][data['DataID'] == 7044]
dfmgvf = dfmgvf.rename(columns={'OrigValueStr': 'Maximum_Green_Vegetation_Fraction'})

# 加上 'Mean annual temperature (MAT) (C)'
dfmat = data[['ObservationID','OrigValueStr']][data['DataID'] == 62]
dfmat = dfmat.rename(columns={'OrigValueStr': 'Mean_annual_temperature_(MAT)'})

# 加上  'Mean sum of annual precipitation (PPT / MAP / TAP) (mm)'
dfmap = data[['ObservationID','OrigValueStr']][data['DataID'] == 80]
dfmap = dfmap.rename(columns={'OrigValueStr': 'Mean_sum_of_annual_precipitation'})

# 加上'Vegetation type / Biome'
dfbiom = data[['ObservationID','OrigValueStr']][data['DataID'] == 193]
dfbiom = dfbiom.rename(columns={'OrigValueStr': 'Vegetation-type/Biome'})

# 加上'Vegetation type / Biome2'
dfbiom2 = data[['ObservationID','OrigValueStr']][data['DataID'] == 202]
dfbiom2 = dfbiom2.rename(columns={'OrigValueStr': 'Vegetation-type/Biome2'})

# 加上'Treatment: Exposition'. If plants were reported to have grown under experimental conditions this is reported as a covariate entry.
dftrea = data[['ObservationID','OrigValueStr']][data['DataID'] == 327]
dftrea = dftrea.rename(columns={'OrigValueStr': 'Treatment_Exposition'})
# ==========获取其他的DataID for 更多信息=============


# ==========可能可以补充缺失的经纬度的数据=============
print(np.unique(data['DataName']))
tmp2 = dflat['ObservationID'] #[pd.isna(dflat['lat'])]
list = [193,449,505,506,509,1412,1413,202,114,1736,2525,112]
for i in range(len(list)):
	# 看这些变量对应的ObsID是否为缺少经纬度的ObsID
	dftmp = data[['ObservationID','OrigValueStr','DataName']][data['DataID'] == list[i]]        
	print('\n','DataID=', list[i],'\nlen of dftmp', len(dftmp)) 
	dftmp  = dftmp.reset_index(drop=True)
	print('DataName=', dftmp.loc[0,'DataName'])   
	tmp1 = dftmp[ ~dftmp['ObservationID'].isin(dflat['ObservationID']) ]
	if i==0:
		tmp2 = tmp1['ObservationID']
		print('len new:', len(tmp2))
	else:
		tmp0 = tmp1[ ~tmp1['ObservationID'].isin(tmp2) ]
		if (list[i]==1736): print(tmp0['OrigValueStr'])
		tmp2 = pd.concat([tmp2,tmp0['ObservationID']])
		print('len new:', len(tmp0))

# ==========可能可以补充缺失的经纬度的数据=============



dflife = data[['LastName', 'Dataset', 'SpeciesName', 'AccSpeciesName', 'ObservationID', 'ValueKindName', 'OrigUncertaintyStr', 'UncertaintyName', 'Replicates', 'StdValue', 'UnitName', 'RelUncertaintyPercent', 'ErrorRisk', 'Reference', 'Comment']][data['TraitID'] == 12]
dflife = dflife.rename(columns={'StdValue': 'lifespan'})



# ==========制作新的dataframe, 使经纬度、物种、观测ID、lifespan等变成列名=========
dfmer = pd.merge(dflon, dflat, how='outer',on=['ObservationID'])  #对两个dataframes的ObsID列取并集,进行连接
dfmer = pd.merge(dflife, dfmer, how='left',on=['ObservationID'] ) # 以lifespan为基准去抓取经纬度

dfmer = pd.merge(dfmer, dfaltt ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfbiom ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfbiom2,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfcnms ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfcnty ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfczpl ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfedpl ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfhabi ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfhabi2,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dflai  ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dflcnm ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dflcrg ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfmap  ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfmat  ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfmgvf ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfsiid ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dfsite ,  how='left',on=['ObservationID'])
dfmer = pd.merge(dfmer, dftrea ,  how='left',on=['ObservationID'])

dfmer = dfmer[['ObservationID', 'lifespan', 'UnitName', 'ErrorRisk', 'Dataset', 'SpeciesName', 'AccSpeciesName', 'lon', 'lat', 'Altitude', 'ValueKindName', 'OrigUncertaintyStr', 'UncertaintyName', 'Replicates', 'RelUncertaintyPercent', 'Location_Site_Name', 'Location_Site_ID', 'Location_Country', 'Location_Region', 'Location Name', 'Vegetation-type/Biome', 'Vegetation-type/Biome2', 'Treatment_Exposition', 'CZofProvenace', 'Ecosystem_Description_Of_Provenance_Litter', 'Habitat_site_description', 'Habitat_at_provenance_of_litter', 'LAI_of_Site', 'Mean_sum_of_annual_precipitation', 'Mean_annual_temperature_(MAT)', 'Maximum_Green_Vegetation_Fraction', 'LastName', 'Comments_notes_methods', 'Comment', 'Reference']]
# ==========制作新的dataframe, 使经纬度、物种、观测ID、lifespan等变成列名=========



output='./lifespan_processed.csv'
dfmer.to_csv(output,sep=',',index=False)#,header=False)
