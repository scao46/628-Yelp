# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 23:27:05 2018

@author: chenj
"""

import pandas as pd
yelp=pd.read_csv("./data/clean data/data_clean.csv",header=None)
yelp.columns=['text','star','cate','len','dot','exclamation','questionmark','smile','cry']

#step1: get the sparse matrix for text
from sklearn.feature_extraction.text import CountVectorizer  
vectorizer = CountVectorizer()  
matrix = vectorizer.fit_transform(yelp['text']) 
#print(matrix.shape)

#step2: combine the feature dot,exclamation,questionmark,smile,cry
import numpy as np
import scipy
matrix_step2=scipy.sparse.hstack((matrix,np.array(yelp['dot'])[:,None]))
matrix_step2=scipy.sparse.hstack((matrix_step2,np.array(yelp['exclamation'])[:,None]))
matrix_step2=scipy.sparse.hstack((matrix_step2,np.array(yelp['questionmark'])[:,None]))
matrix_step2=scipy.sparse.hstack((matrix_step2,np.array(yelp['smile'])[:,None]))
matrix_step2=scipy.sparse.hstack((matrix_step2,np.array(yelp['cry'])[:,None]))

#step3: tranfor the value to tfidf
from sklearn.feature_extraction.text import TfidfTransformer  
transformer = TfidfTransformer()  
tfidf = transformer.fit_transform(matrix_step2)  
#print(tfidf.shape)

#step4: get the sparse matrix for category
from sklearn.feature_extraction.text import CountVectorizer  
vectorizer = CountVectorizer()  
import re
def remove_punc(text):
    temp = re.sub('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]',"",text)
    return temp
cate_use=yelp['cate'].apply(remove_punc)
matrix_cate = vectorizer.fit_transform(cate_use) 
#print(matrix_cate.shape)

transformer = TfidfTransformer()  
tfidf_cate = transformer.fit_transform(matrix_cate)  
#print(tfidf_cate.shape)

matrix_cccccc=scipy.sparse.hstack([tfidf,tfidf_cate])
matrix_final_cccccccc=scipy.sparse.csr.csr_matrix(matrix_cccccc)

train=matrix_final_cccccccc[:1546379];test=matrix_final_cccccccc[1546379:]
from sklearn.linear_model import LogisticRegression   
classifier = LogisticRegression(C=2.2,penalty="l2",multi_class="multinomial",solver="saga")
import datetime as dt  
times1 = dt.datetime.now()
p_log=classifier.fit(train,yelp['star'].iloc[:1546379])
times2 = dt.datetime.now()
print('Time spent on training model: '+ str(times2-times1))
y_log=p_log.predict_proba(test)
pre = [sum(np.array([1,2,3,4,5])*i) for i in y_log]
#coef positive 5-star, 1-5, delicious 11.86; amazing 11.27; great9.57; excellent 9.3; awesome 8.92
#coef positive 1-star, 1-5, worst 10.88; poisoning 9.16; horrible 9.04; horrible 9.04; terrible 8.89

tt = pd.DataFrame(columns=['Id','Prediction1'])
tt['Id'] = range(1,len(pre)+1)
tt['Prediction1'] = pre
#tt.to_csv('tt_5.csv',index=False)
