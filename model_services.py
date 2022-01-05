import nltk
import pickle
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import pandas as pd
from textblob import TextBlob
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import wordnet
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, svm
from sklearn.metrics import accuracy_score

def sentiment_(sentences):
    if type(sentences) == list:
        sentiment = []
        for sentence in sentences:
            pol = TextBlob(sentence).sentiment.polarity
            if pol <= 0.3 and pol >= -0.3:
                sentiment.append('Neutral')
            elif pol > 0.3:
                sentiment.append('Positive')
            elif pol < -0.3:
                sentiment.append('Negative')
        return sentiment
    else:
        temp = [sentences]
        return sentiment_(temp)

def travel_related_classification(tweet):
  with open("model/tfidf.txt",'rb') as f:
        Tfidf_vect = pickle.load(f) 
  word_Lemmatized = WordNetLemmatizer()
  tweet = tokenizer.tokenize(tweet.lower())
  new_tweet = []
  for word in tweet:
    if word not in stop_words and word.isalpha() :
      word = word_Lemmatized.lemmatize(word)
      new_tweet.append(word)
  new_tweet = pd.Series(str(new_tweet))
  return Tfidf_vect.transform(new_tweet)

def classify_tweets(final_tweets):
    with open("model/model_new.txt",'rb') as f:
        SVM_Travel = pickle.load(f)

    for single_tweet in final_tweets:
      single_tweet.travel_related = (list(SVM_Travel.predict(travel_related_classification(single_tweet.tweet)))[0])
      
    # TODO
    travel_related_tweet_list = []
    for tweets in final_tweets:
        if tweets.travel_related == 1:
            travel_related_tweet_list.append(tweets)
    # print(travel_related_tweet_list)
    del final_tweets
    #TODO: change finaltweets to travel_related_tweet_list

    return category_classification(travel_related_tweet_list)

def category_classification(travel_related_tweet_list):
    with open("model/category_model.txt",'rb') as f:
        SVM_category = pickle.load(f)
    zoo = []
    restaurant = []
    museum = []
    for tweet in travel_related_tweet_list:
        tweet.travel_category = (SVM_category.predict([tweet.tweet])[0])
        # print("=========================================")
        # print(SVM_category.predict_proba([tweet.tweet]))
        tweet.sentiment = sentiment_([tweet.tweet])

    # for tweet in travel_related_tweet_list:
    #     print("====================================================================================")
    #     print('\033[1m' + 'Tweet Text')
    #     print('\033[0m' +tweet.tweet)
    #     print("--------------------------------------------------------------------------------")
    #     print('\033[1m' + 'Tweet Score :\t \033[0m' + str(tweet.sentiment))
    #     print("--------------------------------------------------------------------------------")
    #     print('\033[1m' + 'Travel Realted :\t \033[0m' + str(tweet.screen_name))
    #     print("--------------------------------------------------------------------------------")
    #     print('\033[1m' + 'Category :\t \033[0m' + str(tweet.travel_category))
    #     print("====================================================================================")

    for tweet in travel_related_tweet_list:
        if tweet.travel_category == "zoo":
            zoo.append(tweet)
        elif tweet.travel_category == "restaurant":
            restaurant.append(tweet)
        elif tweet.travel_category == "museum":
            museum.append(tweet)
    return zoo, restaurant, museum
if __name__ == "__main__":
    classify_tweets("@TagAlongDeb A fantastic book! Hope you get home soon!")