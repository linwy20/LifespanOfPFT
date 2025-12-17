#-*- coding : utf-8-*-
"""
Created on Fri 2023-09-12 21:18:52 

@author: Wanyi

"""

import numpy as np
import pandas as pd



data0 = pd.read_csv('merge_pft.csv',sep=',',header=0)


data1 = pd.read_excel('./trait_lookup_table/TRY_Categorical_Traits_Lookup_Table_2012_03_17_TestRelease.xlsx')
# 根据 data0 的 AccSpeciesName 来裁剪 LUT 数据
data1 = data1[ (data1['AccSpeciesName'].isin(data0['AccSpeciesName'])) ]
# 创建新的一列, 合并PFT特征
data1['SumChar'] = data1['PlantGrowthForm'] +' '+ data1['LeafType'] +' '+data1['LeafPhenology']
data1 = data1[['AccSpeciesName','SumChar', 'PhotosyntheticPathway']]
dftmp1 = pd.merge(data0, data1, how='left', on=['AccSpeciesName'])


data2 = pd.read_excel('./trait_lookup_table/TRY_Categorical_Traits_Lookup_Table_2012_03_17_TestRelease.xlsx')
# 根据 data0 的 SpeciesName 来裁剪 LUT 数据
data2 = data2[ (data2['AccSpeciesName'].isin(data0['SpeciesName'])) ]
# 创建新的一列, 合并PFT特征
data2['SumChar'] = data2['PlantGrowthForm'] +' '+ data2['LeafType'] +' '+data2['LeafPhenology']
data2 = data2[['AccSpeciesName','SumChar', 'PhotosyntheticPathway']]
data2 = data2.rename(columns={'AccSpeciesName': 'SpeciesName'})
dftmp2 = pd.merge(data0, data2, how='left', on=['SpeciesName'])


dfmer = pd.concat([dftmp1, dftmp2])
dfmer = dfmer.drop_duplicates(subset=['ObservationID']) 


# 输出文件
output='merge_LUT.csv'
dfmer.to_csv(output,sep=',',index=False)#,header=False)
