# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 23:34:19 2018

@author: Think
"""
import pandas as pd
import re
import math
'''
yelp=pd.read_csv("edition1.0_train_test_use_for_neural.csv",header=None)
yelp.columns=['text','stars']

s_train=yelp.iloc[:100000]
s_valid=yelp.iloc[100000:200000]
def remove_punc(text):
    temp = re.sub("[!#$%&\()*+,-./:;<=>?@[\\]^_`{|}~]"," ",text)
    temp = re.sub('\s+',' ',temp)
    return temp
def add_label(text):
    return ("__label__"+str(text))
yelp['text'] = yelp['text'].apply(remove_punc)
yelp['stars'] = yelp['stars'].apply(add_label)
yelp.iloc[:1546379].to_csv('edition2.0_train_fasttext.txt',sep=" ", index=False,header=None)
test = yelp['text'][1546379:].reset_index(drop=True)
test.to_csv('edition2.0_test_fasttext.txt',sep=" ", index=False,header=None)
s_train['text'] = s_train['text'].apply(remove_punc)
s_train['stars'] = s_train['stars'].apply(add_label)
s_train.to_csv('train_small.txt',sep=" ",index=False,header=None)
s_valid['text'] = s_valid['text'].apply(remove_punc)
s_valid['stars'] = s_valid['stars'].apply(add_label)
s_valid.to_csv('valid_small.txt',sep=" ",index=False,header=None)
'''

'''
valid = pd.read_csv('valid_small.txt',sep=" ",header=None)
valid[1] = [int(re.sub('[^1-5]','',r)) for r in valid[1]]
nn = pd.read_csv('nn.txt',header=None)
nn['Id'] = range(1,len(nn)+1)
nn['Prediction1'] = [int(re.sub('[^1-5]','',r)) for r in nn[0]]
nn=nn.drop(0,1)
#nn.to_csv('tt.csv',index=False)
'''
nn_prob = pd.read_csv('nn_prob.txt',sep=' +',header=None,engine='python')
nn_prob[0] = [int(re.sub('[^1-5]','',r)) if (r is not None) else 0 for r in nn_prob[0]]
nn_prob[2] = [int(re.sub('[^1-5]','',r)) if (r is not None) else 0 for r in nn_prob[2]]
nn_prob[4] = [int(re.sub('[^1-5]','',r)) if (r is not None) else 0 for r in nn_prob[4]]
nn_prob[6] = [int(re.sub('[^1-5]','',r)) if (r is not None) else 0 for r in nn_prob[6]]
nn_prob[8] = [int(re.sub('[^1-5]','',r)) if (r is not None) else 0 for r in nn_prob[8]]
nn_prob[1] = [0 if math .isnan(r) else r for r in nn_prob[1]]
nn_prob[3] = [0 if math.isnan(r) else r for r in nn_prob[3]]
nn_prob[5] = [0 if math.isnan(r) else r for r in nn_prob[5]]
nn_prob[7] = [0 if math.isnan(r) else r for r in nn_prob[7]]
nn_prob[9] = [0 if math.isnan(r) else r for r in nn_prob[9]]
output = pd.DataFrame(columns=['Id','Prediction1'])
output['Id'] = range(1,len(nn_prob)+1)
output['Prediction1'] = nn_prob[0]*nn_prob[1]+nn_prob[2]*nn_prob[3]+nn_prob[4]*nn_prob[5]+nn_prob[6]*nn_prob[7]+nn_prob[8]*nn_prob[9]
output['Prediction1'] = [min(star,5) for star in output['Prediction1']]
output['Prediction1'] = [max(star,1) for star in output['Prediction1']]
output.to_csv('tt_prob.csv',index=False)
#mse = np.mean([(nn[1][i]-valid[1][i])^2 for i in range(nn.shape[0])])
