# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:19:12 2015

@author: USER
"""

import os
import json
import math
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class Counter:
    def __init__(self, file_path):
        self.file = open(file_path,"r")

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def __iter__(self):
        return self

    def __next__(self): # Python 2: def next(self)
        return self.file.readline()
        
class ReviewTextItr:
    def __init__(self, file_path, limit=None):
        self.limit = limit
        self.file = open(file_path,"r")

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None:
            if self.limit==0:
                raise StopIteration
            self.limit-=1
        try:
            review = json.loads(self.file.readline())    
            return review["text"]
        except:
            raise StopIteration 

dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
business_path = dataset_path + "yelp_academic_dataset_business.json"
review_path = dataset_path + "yelp_academic_dataset_review.json"
user_path = dataset_path + "yelp_academic_dataset_user.json"
checkin_path = dataset_path + "yelp_academic_dataset_checkin.json"
tip_path = dataset_path + "yelp_academic_dataset_tip.json"
destination_path = "../dataset/yelp_review_sampled/"

doc_limit = None   #limit int for reviews, set to None if wants to load all reviews

#test_counter = Counter(destination_path+"sampled_user.json")
#review_itr = ReviewTextItr(destination_path+"sampled_review.json", doc_limit)
review_itr = ReviewTextItr(review_path, doc_limit)

"""
cursor = 0
for review_text in review_itr:    
    print(review_text)
    print( str(cursor) )
    cursor+=1
else:
    print("done")
"""
"""
vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000, \
                             min_df=5, stop_words='english', use_idf=True)
"""
vectorizer = TfidfVectorizer(max_df=0.5, min_df=10, \
                            stop_words='english', use_idf=True)

start_time = datetime.datetime.now();
X = vectorizer.fit_transform(review_itr)
tfidf_done_time = datetime.datetime.now();
print( "spend " + str( tfidf_done_time.timestamp() - start_time.timestamp() ) + " sec. on tfidf vectorize.\n" )

#print(type(X))
#print(vectorizer.get_feature_names())
with open("yelp_ch6/tfidf_vector_" + str(doc_limit) + ".pickle","wb") as f:
    save_var = {"feature":vectorizer.get_feature_names(),
                "vectors":X
                }
    pickle.dump(save_var, f)

with open("yelp_ch6/tfidf_vector_" + str(doc_limit) + ".pickle","rb") as f:
    load_var = pickle.load(f)
    print(load_var.keys())