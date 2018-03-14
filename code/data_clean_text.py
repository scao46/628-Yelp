# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:40:32 2018

@author: chenj
"""
import pandas as pd
#import nltk.corpus
import re
from nltk.stem import WordNetLemmatizer

train_data=pd.read_csv("../data/train_data.csv")
test_data=pd.read_csv("../data/testval_data.csv")

#combine the train data with the test data
#train_star=train_data["stars"]
train_text=train_data["text"]
test_text=test_data["text"]
frames=[train_text,test_text]
all_text=pd.concat(frames)

#####Do the data-cleaning step(text)
#step1:remove part punctuations and numbers
def process(text):
    temp = re.sub("[^a-zA-Z.?!', ]",'',text)
    temp = re.sub("([.?!,]+)"," \\1 ",temp)
    temp = temp.lower()
    temp = temp.split()
    #text_c.append(temp.split(" "))
    return temp
text_step1 = all_text.apply(process)

#step2:delete the useless word
lib_useless=['the','a','and','i','to','was','of','it','is','we','','that','this','my','you',
             'they','had','were','have','are','be','there','our','here',"it's","i'm","i've",
             'am','has','been','their','me',"it's",'an','would','which','will','your','got',
             'get','gets','he','she','them','his','her','him','us','our']
def delete(text):
    """
    delete the word in stopwords, save the Capital word
    """
    new = []
    for w in text:
        if w not in lib_useless:
            new.append(w)
    return new
text_remove = text_step1.apply(delete)

#step3: make the word Dictionary
WordList=[]
for i in text_remove:
    WordList.extend(i)
from collections import Counter
WordDict=dict(Counter(WordList))
dict_big_than_250 = dict((key, value) for key, value in WordDict.items() if value >250)
lib=set(list(dict_big_than_250.keys()))

#step4: remove some words that their frequency are less than 250
def get(text):
    new = []
    for w in text:
        if w in lib:
            new.append(w)
    return new
text_remove_2 = text_remove.apply(get)

#step5: lemmatizer
def word_tense(text):
    new=[];lemmatizer = WordNetLemmatizer()
    for i in text:
        new.append(lemmatizer.lemmatize(i, pos="v"))
    return new
text_after=text_remove_2.apply(word_tense)

#step6: combine the negation words with verbs and adjectives
word=list(dict_big_than_250.keys())
from textblob import TextBlob
use=' '.join(word)
blob = TextBlob(use)
word_tyep=blob.tags
adj=[]
for i in word_tyep:
    if i[1]=="JJ":
        adj.append(i[0])
adj.remove('i')
adj_sel=[]
for i in adj:
    if dict_big_than_250[i]>20000:
        adj_sel.append(i)
de=['lol','soup','dessert','table','want','hear','saturday','asked','bread','vegas','dish','opted','dishes','n','kick','sign','noodle','dip','oz','give','knew','bottle','th','mouth','etc','u','s','menus','arrive','friday']       
for i in de:
    adj_sel.remove(i)    
adj_lib=set(adj_sel) 

verb=['like','liked','likes''love','loved','loves','recommend','recommended','recommends','prefer','prefers','advocate']

deny=[]
for i in list(dict_big_than_250.keys()):
    if "n't" in i:
        deny.append(i)
deny.append('not')
deny.append('cannot')
deny.append('dont')
deny.append('wouldnt')
deny.append('cant')
deny.append('isnt')
deny.append('doesnt')
deny.append('werent')
deny.append('didnt')
deny.append('havent')
deny.append('wasnt')
deny.append('couldnt')
deny.append('shouldnt')
deny.append('wont')
deny.append('aint')
deny.append('arent')
deny.append('hadnt')
deny.append("never")#...
deny_lib=set(deny)  
      
punc_lib=set([".","?","!",","])

def combine_deny_adj(text):
    for i in range(len(text)):
        word=text[i]
        if word in deny_lib:
            for j in range(i,len(text)):
                word_2=text[j]
                if word_2[0] in punc_lib:
                    break
                elif word_2 in adj_lib or word_2 in set(verb):
                    text[i]="not"+word_2
                    text[j]=' '
                    break
                else:
                    next
    return text
text_combine=text_after.apply(combine_deny_adj)

def transfor(text):
    """
    change the pattern
    """
    r=" ".join(text)
    r = re.sub('\s+',' ',r)
    return r
text_combinefinal=text_combine.apply(transfor)
text_combinefinal.index=range(len(text_combinefinal))
value=text_combinefinal.iloc[text_combinefinal.values==''].index
text_combinefinal.iloc[value]="thisisanemptyline"

def remove_punc(text):
    temp = re.sub("'t",' ',text)
    temp = re.sub("'s",' ',temp)
    temp = re.sub("[!#$%&\()*+,-./:;<=>?@[\\]'^_`{|}~]"," ",temp)
    temp = re.sub('\s+',' ',temp)
    return temp
text_use_for_lasso=text_combinefinal.apply(remove_punc)
value_1=text_use_for_lasso.iloc[text_use_for_lasso.values==''].index
text_use_for_lasso.iloc[value]="thisisanemptyline"

import pandas as pd
train_data=pd.read_csv("../data/train_data.csv")
star=train_data['stars']
yelp=pd.DataFrame()    
yelp.insert(0,"text",text_use_for_lasso)
yelp.insert(1,"stars",star)
all_t=pd.read_csv('data_for_punc.csv')
all_t.columns
yelp.insert(2,'categories',all_t['categories'])
#yelp.insert(3,'len',all_t['len'])
yelp.insert(3,"dot",all_t['dot'])
yelp.insert(4,'exclamation',all_t['exclamation'])
yelp.insert(5,'questionmark',all_t['questionmark'])
yelp.insert(6,'smile',all_t['smile'])
yelp.insert(7,'cry',all_t['cry'])

yelp.to_csv("../data/data_clean.csv",header=None,index=False,encoding='utf-8')