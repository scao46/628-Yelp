# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 14:00:31 2018

@author: chenj
"""
import pandas as pd
import nltk.corpus
import re
from nltk.stem import WordNetLemmatizer

train_data=pd.read_csv("../data/train_data.csv")
test_data=pd.read_csv("../data/testval_data.csv")

frames=[train_data,test_data]
all_data=pd.concat(frames)

###combine the train data with the test data
all_text=all_data['text']
all_cate=all_data["categories"]

###for categories
def transfor_c(text):
    text=re.sub('\s+','',text)
    return eval(text)
cate_step1=all_cate.apply(transfor_c)

def transfor_c_1(text):
    """
    change the pattern
    """
    r=" ".join(text)
    return r
cate_clean=cate_step1.apply(transfor_c_1)
yelp=pd.DataFrame()
yelp.insert(0,'categories',cate_clean)

#step1: just save the punctuations
def process_punc(text):
    """
    save all the characters and ' 
    """
    new=[]
    temp = re.sub('[a-zA-Z0123456789]', ' ', text)#????????number?数字也去掉吧？
    temp = re.sub('\s+',' ',temp)
    for w in temp.split(" "):
        if len(w)>1:
            new.append(w)
    return new
text_punc=all_text.apply(process_punc)

#step2: make the dictionary for punc
punc=[]
for i in text_punc:
    punc.extend(i)
from collections import Counter
PUNC=dict(Counter(punc))
sort_punc=sorted(PUNC.items(), key=lambda d:d[1], reverse = True) 

#step3: we divided the punc into five group('..','!!','??',':) and :-)',':( and :-(')
def count_punc(text,punc):
    n=0
    for i in text:
        if punc in i:
            n=n+1
    return n

length_doubdot=text_punc.apply(count_punc,'..')
yelp.insert(1,"dot",length_doubdot)
length_douexc=text_punc.apply(count_punc,'!!')
yelp.insert(2,"exclamation",length_douexc)
length_doubque=text_punc.apply(count_punc,'??')
yelp.insert(3,"questionmark",length_doubque)
length_smile_1=text_punc.apply(count_punc,':)')
length_smile_2=text_punc.apply(count_punc,':-)')    
yelp.insert(4,"smile",length_smile_1+length_smile_2)
length_cry_1=text_punc.apply(count_punc,':(')
length_cry_2=text_punc.apply(count_punc,":-(")
yelp.insert(5,"cry",length_cry_1+length_cry_2)
yelp.to_csv('../data/data_for_punc.csv',index=False,encoding='utf-8')




