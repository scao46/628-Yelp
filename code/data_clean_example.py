# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 18:09:40 2018

@author: chenj
"""

import pandas as pd 
train=pd.read_csv('data/raw data/train_data.csv')
yelp=pd.read_csv('data/clean data/data_clean.csv',header=None)
yelp.columns=['text','star','cate','len','dot','exclamation','questionmark','smile','cry']
print('Before:',' ', train['text'].iloc[2056][47:])
print('After:',' ',yelp['text'].iloc[2056][36:]) 