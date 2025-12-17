#-*- coding : utf-8-*-
"""
Created on Fri 2023-09-15 21:18:52 

@author: Wanyi

"""


import numpy as np
import pandas as pd


data0 = pd.read_csv('merge_LUT.csv',sep=',',header=0)

data1 = pd.read_csv('growthform_unprocessed.csv',sep=',',header=0,low_memory=False)


data2  = data1[data1['AccSpeciesName'].isin(data0['AccSpeciesName']) | data1['AccSpeciesName'].isin(data0['SpeciesName'])]

output='./growthform_cutrow.csv'
data2.to_csv(output,sep=',',index=False)#,header=False)
