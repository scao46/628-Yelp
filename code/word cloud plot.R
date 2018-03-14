############### word cloud #################

library(data.table); library(tidyverse); library(tidytext); library(Matrix)
library("tm"); library("SnowballC"); library("wordcloud"); library("RColorBrewer")
catagory = fread("category.csv")
datacleaned = fread("data_clean_for_wordcloud.csv", sep = ",", header = TRUE)
datacleaned = datacleaned[1:1546379, 2:4] 
colnames(datacleaned) = c("index", "text", "star")


## fast food
fast_food_index = catagory$restu[which(catagory$word == "fast food")]
fast_food = datacleaned[fast_food_index,]
d = data_frame(restu = 1:nrow(fast_food), text = as.character(fast_food$text), star = fast_food$star) ##then go to common part

## deserts
dessert_index = catagory$restu[which(catagory$word == "desserts")]
dessert = datacleaned[dessert_index,]
d = data_frame(restu = 1:nrow(dessert), text = as.character(dessert$text), star = dessert$star) ##then go to common part

## coffee & tea
coffeetea_index = catagory$restu[which(catagory$word == "coffee & tea")]
coffeeteadessert = datacleaned[coffeetea_index,]
d = data_frame(restu = 1:nrow(coffeetea), text = as.character(coffeetea$text), star = coffeeteadessert$star)##then go to common part

## cafes
cafes_index = catagory$restu[which(catagory$word == "cafes")]
cafes = datacleaned[cafes_index,]
d = data_frame(restu = 1:nrow(cafes), text = as.character(cafes$text), star = cafes$star)##then go to common part

## coffeeteaa & cafes & deserts & bakeries
dctb_index = catagory$restu[which(catagory$word == "cafes" | catagory$word == "coffee & tea" |
                                  catagory$word == "desserts" | catagory$word == "bakeries" )]
dctb = datacleaned[dctb_index,]
d = data_frame(restu = 1:nrow(dctb), text = as.character(dctb$text), star = dtcb$star)##then go to common part

## french
french_index = catagory$restu[which(catagory$word == "french")]
french = datacleaned[french_index,]
d = data_frame(restu = 1:nrow(french), text = as.character(french$text), star = french$star)##then go to common part

## sports bars
sportsbars_index = catagory$restu[which(catagory$word == "sports bars")]##then go to common part
sportsbars = datacleaned[sportsbars_index,]
d = data_frame(restu = 1:nrow(sportsbars), text = as.character(sportsbars$text), star = sportsbars$star)##then go to common part

## vegetarian and vegan
vv_index = catagory$restu[which(catagory$word == "vegetarian" | catagory$word == "vegan")]
vv= datacleaned[vv_index,]
d = data_frame(restu = 1:nrow(vv), text = as.character(vv$text), star = vv$star)##then go to common part


## common part
d = d %>% unnest_tokens(word, text)

## remove some too common words which appears in each categories
d = d[-which(d$word %in% c("take", "took", "came","come", "one", "two","say", "said", "told", "go", 
                           "going", "would","get", "got", "give", "gave", "i'm", "i'll", "i'd", 
                           "could", "n", "put", "see", "put", "coming", "thru","made", "make",
                           "though","in", "that's", "i've","out", "five", "bit", "eat", "maybe", 
                           "inside", "us", "around", "ever", "restaurant","restaurants", "thing",
                           "things","think", "went", "know", "und", "ordered", "good", "food", 
                           "place", "menu", "order","lot", "le","de", "la","great","service",
                           "also", "back", "first", "really", "like", "time", "little", 
                           "et", "try", "ask", "asked", "want", "wanted", "tried")),]



d$frequency = NA
d$frequency[which(d$star == 1)] = 559993/164676
d$frequency[which(d$star == 2)] = 559993/152401
d$frequency[which(d$star == 3)] = 559993/225710
d$frequency[which(d$star == 4)] = 559993/443599
d$frequency[which(d$star == 5)] = 1


d_table = data.frame(table(d$word))
d_table = d_table[order(-d_table$Freq),]
colnames(d_table) = c("word", "freq")

head(d_table, 10)
set.seed(1234)
wordcloud(words = d_table$word, freq = d_table$freq, min.freq = 1,
          max.words=110, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))






