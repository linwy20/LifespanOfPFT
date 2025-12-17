#-*- coding : utf-8-*-
"""
Created on Fri 2023-09-12 21:18:52 

@author: Wanyi

"""


import numpy as np
import pandas as pd



df = pd.read_csv('merge_growthform.csv',sep=',',header=0)

df.loc[(df['Location_Region']=='North West  Mediterranean Basin'), 'Location_Region' ] = 'Tmp'
df.loc[(df['Vegetation-type/Biome']=='Warmtemp'), 'Location_Region' ] = 'Tmp'
df.loc[(df['Vegetation-type/Biome']=='ArcBor'), 'Location_Region' ] = 'Bor'
df.loc[(df['Vegetation-type/Biome']=='TEMP'), 'Location_Region' ] = 'Tmp'
df.loc[(df['Vegetation-type/Biome']=='TR'), 'Location_Region' ] = 'Trp'
df.loc[(df['Vegetation-type/Biome']=='TEMP_FOR'), 'Location_Region' ] = 'Tmp'
df.loc[(df['Vegetation-type/Biome']=='ALPINE'), 'Location_Region' ] = 'Bor'
df.loc[(df['Vegetation-type/Biome']=='TUNDRA'), 'Location_Region' ] = 'Bor'
df.loc[(df['Vegetation-type/Biome']=='BOREAL'), 'Location_Region' ] = 'Bor'
df.loc[(df['Vegetation-type/Biome']=='TROP_FOR'), 'Location_Region' ] = 'Trp'
df.loc[(df['Vegetation-type/Biome']=='TROP_RF'), 'Location_Region' ] = 'Trp'


df['pftout'] = ''

df.loc[(df['pft_LPJ2']=='BorDcBl') & (df['SumForm']=='S'), 'pftout' ] = 'BorDcBlSh'
df.loc[(df['pft_LPJ2']=='BorDcBl') & (df['SumForm']=='T'), 'pftout' ] = 'BorDcBlTr'

df.loc[(df['pft_LPJ2']=='BorDcNl') & (df['SumForm']=='T'), 'pftout' ] = 'BorDcNlTr'

df.loc[(df['pft_LPJ2']=='BorEvBl') & (df['SumForm']=='S'), 'pftout' ] = 'BorEvBlSh'

df.loc[(df['pft_LPJ2']=='BorEvNl') & (df['SumForm']=='T'), 'pftout' ] = 'BorEvNlTr'

df.loc[(df['pft_LPJ2']=='GC3') & (df['SumForm']=='G'), 'pftout' ] = 'C3GRA'

df.loc[(df['pft_LPJ2']=='GC4') & (df['SumForm']=='G'), 'pftout' ] = 'C4GRA'

df.loc[(df['pft_LPJ2']=='TmpDcBl') & (df['SumForm']=='S'), 'pftout' ] = 'TmpDcBlSh'
df.loc[(df['pft_LPJ2']=='TmpDcBl') & (df['SumForm']=='T'), 'pftout' ] = 'TmpDcBlTr'

df.loc[(df['pft_LPJ2']=='TmpEvBl') & (df['SumForm']=='S'), 'pftout' ] = 'TmpEvBlSh'
df.loc[(df['pft_LPJ2']=='TmpEvBl') & (df['SumForm']=='T'), 'pftout' ] = 'TmpEvBlTr'

df.loc[(df['pft_LPJ2']=='TmpEvNl') & (df['SumForm']=='S'), 'pftout' ] = 'TmpEvBlSh'
df.loc[(df['pft_LPJ2']=='TmpEvNl') & (df['SumForm']=='T'), 'pftout' ] = 'TmpEvBlTr'

df.loc[(df['pft_LPJ2']=='TrpDcBl') & (df['SumForm']=='T'), 'pftout' ] = 'TrpDcBlTr'

df.loc[(df['pft_LPJ2']=='TrpEvBl') & (df['SumForm']=='S'), 'pftout' ] = 'TrpEvBlSh'
df.loc[(df['pft_LPJ2']=='TrpEvBl') & (df['SumForm']=='T'), 'pftout' ] = 'TrpEvBlTr'



df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='G') & (df['PhotosyntheticPathway']=='C3'), 'pftout' ] = 'C3GRA' 
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='G') & (df['PhotosyntheticPathway']=='C4'), 'pftout' ] = 'C4GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='G') & (df['PhotosyntheticPathway']=='C3/C4'), 'pftout' ] = 'GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='G') & (pd.isna(df['PhotosyntheticPathway'])) & (df['pft_BBGC2_SpsMatch']=='GC3'), 'pftout' ] = 'C3GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='G') & (pd.isna(df['PhotosyntheticPathway'])) & (pd.isna(df['pft_BBGC2_SpsMatch'])), 'pftout' ] = 'GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm_SpsMatch']=='G') & (df['PhotosyntheticPathway']=='C3'), 'pftout' ] = 'C3GRA' 
 


df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='tree scale-shaped evergreen'),   'pftout' ] = 'EvNlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='tree needleleaved evergreen'),   'pftout' ] = 'EvNlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='tree needleleaved deciduous'),   'pftout' ] = 'DcNlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='tree broadleaved evergreen'),    'pftout' ] = 'EvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='tree broadleaved deciduous/evergreen') & (df['lifespan'] >= 12),'pftout' ] = 'EvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='tree broadleaved deciduous/evergreen') & (df['lifespan'] < 12), 'pftout' ] = 'DcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='tree broadleaved deciduous'),    'pftout' ] = 'DcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='shrub/tree scale-shaped evergreen') & (df['pft_LPJ2_SpsMatch']=='TmpEvNl'),    'pftout' ] = 'EvNlTr' 
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='shrub/tree broadleaved evergreen'),    'pftout' ] = 'EvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='shrub/tree broadleaved deciduous'),    'pftout' ] = 'DcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='shrub broadleaved evergreen'),    'pftout' ] = 'EvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='shrub broadleaved deciduous'),    'pftout' ] = 'DcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['SumChar']=='fern broadleaved evergreen'),    'pftout' ] = 'EvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (df['pft_LPJ2_SpsMatch']=='TmpEvBl'),    'pftout' ] = 'TmpEvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (pd.isna(df['SumChar'])) & (df['pft_LPJ2_SpsMatch']=='TmpEvBl'), 'pftout' ] = 'TmpEvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (pd.isna(df['SumChar'])) & (df['pft_LPJ2_SpsMatch']=='TmpDcBl'), 'pftout' ] = 'TmpDcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (pd.isna(df['SumChar'])) & (df['pft_LPJ2_SpsMatch']=='TrpDcBl'), 'pftout' ] = 'TrpDcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (pd.isna(df['SumChar'])) & (df['pft_LPJ2_SpsMatch']=='TrpEvBl'), 'pftout' ] = 'TrpEvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (pd.isna(df['SumChar'])) & (pd.isna(df['pft_LPJ2_SpsMatch'])) & (df['pft_LPJ1_SpsMatch']=='TrpEvBl'), 'pftout' ] = 'TrpEvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='T') & (pd.isna(df['SumChar'])) & (pd.isna(df['pft_LPJ2_SpsMatch'])) & (pd.isna(df['pft_LPJ1_SpsMatch'])) & (df['pft_wright_SpsMatch']=='EB_T'), 'pftout' ] = 'EvBlTr'


df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='tree broadleaved evergreen'),             'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='tree broadleaved deciduous/evergreen'),   'pftout' ] = 'DcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='tree broadleaved deciduous'),             'pftout' ] = 'DcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub/tree needleleaved evergreen'),      'pftout' ] = 'EvNlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub/tree needleleaved evergreen'),      'pftout' ] = 'EvNlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub/tree broadleaved deciduous/evergreen') & (df['pft_LPJ2_SpsMatch']=='TmpEvBl'),   'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub/tree broadleaved deciduous'),       'pftout' ] = 'DcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub needleleaved evergreen'),           'pftout' ] = 'EvNlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub broadleaved evergreen'),            'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub/tree broadleaved evergreen'),       'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='shrub broadleaved deciduous'),            'pftout' ] = 'DcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='herb/shrub broadleaved evergreen'),   'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='herb/shrub broadleaved deciduous'),   'pftout' ] = 'DcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='herb broadleaved evergreen'),         'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['SumChar']=='herb broadleaved deciduous'),         'pftout' ] = 'DcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (df['pft_LPJ2_SpsMatch']=='TmpEvBl'),    'pftout' ] = 'TmpEvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (pd.isna(df['SumChar']) & (df['pft_LPJ2_SpsMatch']=='BorDcBl')), 'pftout' ] = 'BorDcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (pd.isna(df['SumChar']) & (df['pft_LPJ2_SpsMatch']=='TmpDcBl')), 'pftout' ] = 'TmpDcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (pd.isna(df['SumChar']) & (df['pft_LPJ2_SpsMatch']=='TmpEvBl')), 'pftout' ] = 'TmpEvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']=='S') & (pd.isna(df['SumChar']) & (df['pft_SDGVM2_SpsMatch']=='TEB')),   'pftout' ] = 'EvBlSh'


df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='herb broadleaved deciduous'), 'pftout' ] = 'C3GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='herb broadleaved evergreen'), 'pftout' ] = 'C3GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='shrub broadleaved deciduous'), 'pftout' ] = 'DcBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='shrub broadleaved evergreen'), 'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='shrub needleleaved evergreen'), 'pftout' ] = 'EvNlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='tree broadleaved deciduous'), 'pftout' ] = 'DcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='tree broadleaved evergreen'), 'pftout' ] = 'EvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='tree needleleaved deciduous'), 'pftout' ] = 'DcNlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['SumChar']=='tree needleleaved evergreen'), 'pftout' ] = 'EvNlTr'


df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_BBGC2_SpsMatch']=='EvNl'), 'pftout' ] = 'EvNlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_BBGC2_SpsMatch']=='GC3'), 'pftout' ] = 'C3GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_SDGVM3_SpsMatch']=='SEB'), 'pftout' ] = 'EvBlSh'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_BBGC2_SpsMatch']=='DcBl'), 'pftout' ] = 'DcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_BBGC2_SpsMatch']=='EvBl'), 'pftout' ] = 'EvBlTr'

df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_LPJ1_SpsMatch']=='TmpH'), 'pftout' ] = 'C3GRA'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_LPJ1_SpsMatch']=='TrpEvBl'), 'pftout' ] = 'TrpEvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_LPJ1_SpsMatch']=='TrpDcBl'), 'pftout' ] = 'TrpDcBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_LPJ1_SpsMatch']=='TmpEvBl'), 'pftout' ] = 'TmpEvBlTr'
df.loc[(pd.isna(df['pft_LPJ2'])) & (df['SumForm']!='G')  & (df['SumForm']!='T') & (df['SumForm']!='S') & (df['pft_LPJ1_SpsMatch']=='TmpEvBl') & (df['pft_JULES _SpsMatch']=='S'), 'pftout' ] = 'TmpEvBlSh'

df.loc[(df['pftout']=='') & (df['SumChar']=='tree broadleaved deciduous/evergreen')  & (df['lifespan'] >= 12) , 'pftout' ] = 'EvBlTr'
df.loc[(df['pftout']=='') & (df['SumChar']=='tree broadleaved deciduous/evergreen')  & (df['lifespan'] < 12) , 'pftout' ] = 'DcBlTr'
df.loc[(df['pftout']=='') & (df['SumChar']=='shrub broadleaved deciduous/evergreen') & (df['lifespan'] < 12) , 'pftout' ] = 'DcBlSh'
df.loc[(df['pftout']=='') & (df['SumChar']=='graminoid broadleaved evergreen') & (df['PhotosyntheticPathway']=='C3'), 'pftout' ] = 'C3GRA'
df.loc[(df['pftout']=='') & (df['SumChar']=='tree scale-shaped evergreen') , 'pftout' ] = 'EvNlTr'
df.loc[(df['pftout']=='') & (df['SumChar']=='shrub/tree broadleaved evergreen') & (df['Vegetation-type/Biome']=='lowland tropical moist semi-evergreen forest') , 'pftout' ] = 'EvBlTr'
df.loc[(df['pftout']=='') & (df['SumChar']=='shrub/tree broadleaved evergreen') & (df['Vegetation-type/Biome']=='lowland tropical moist semi-evergreen forest') , 'pftout' ] = 'EvBlTr'
df.loc[(df['pftout']=='') & (df['SumChar']=='shrub/tree broadleaved evergreen') & (df['Vegetation-type/Biome']=='lowland tropical dry deciduous forest') , 'pftout' ] = 'DcBlTr'
df.loc[(df['pftout']=='') & (df['SumChar']=='shrub/tree broadleaved deciduous') & (df['Vegetation-type/Biome']=='lowland tropical dry deciduous forest') , 'pftout' ] = 'DcBlTr'


df.loc[(df['pftout']=='') & (df['SumForm']=='G') , 'pftout' ] = 'GRA'
df.loc[(df['pftout']=='') & (df['SumForm_SpsMatch']=='G') , 'pftout' ] = 'GRA'


df.loc[(df['pftout']=='DcBlTr') & (df['pft_LPJ2_SpsMatch']=='TmpDcBl') , 'pftout' ] = 'TmpDcBlTr'
df.loc[(df['pftout']=='DcBlTr') & (df['pft_LPJ2_SpsMatch']=='BorDcBl') , 'pftout' ] = 'BorDcBlTr'
df.loc[(df['pftout']=='DcBlTr') & (df['pft_LPJ1_SpsMatch']=='BorDcBl') , 'pftout' ] = 'BorDcBlTr'
df.loc[(df['pftout']=='EvNlTr') & (df['pft_LPJ2_SpsMatch']=='TmpEvNl') , 'pftout' ] = 'TmpEvNlTr'
df.loc[(df['pftout']=='EvNlTr') & (df['pft_LPJ1_SpsMatch']=='TmpEvNl') , 'pftout' ] = 'TmpEvNlTr'
df.loc[(df['pftout']=='EvNlTr') & (df['pft_PFT_SpsMatch']=='boreal conifer') , 'pftout' ] = 'BorEvNlTr'
df.loc[(df['pftout']=='EvNlTr') & (df['pft_PFT_SpsMatch']=='Boreal conifer') , 'pftout' ] = 'BorEvNlTr'


output='pft_out.csv' 
df.to_csv(output,sep=',',index=False)#,header=False)

