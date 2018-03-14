"""
Created on Sat Feb 17

@author:scao46@wisc.edu
"""
# -*- coding: utf-8 -*-
import pandas as pd
from gensim import models
text = pd.read_csv("./data/clean data/data_clean.csv",header=None)[0]
#model = models.Word2Vec(text, size=100, window=5, min_count=250, workers=4)
fname='word2vec.model'
#model.save(fname)
model = models.Word2Vec.load("./data/"+fname)
wv = model.wv
#word_vectors.most_similar(positive=['awesome'])
#word_vectors.most_similar(positive=['disgusting'])
#word_vectors.most_similar(positive=['waiter','woman'], negative=['man'])
#word_vectors.most_similar_cosmul(positive=['waiter','woman'], negative=['man'])
#word_vectors.most_similar(positive=['tokyo','usa'], negative=['asia'])
#word_vectors.doesnt_match("I like this gentle hotdog".split())
#word_vectors.doesnt_match("He is a very gentle hotdog".split())
#word_vectors['seriously']
#del model
