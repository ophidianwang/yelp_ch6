# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:52:39 2015

@author: USER
"""

from od_misc.FileIter import FieldIter
import re
import pandas as pd

categories_set = set()
food_categories_set = set()
food_categories_accumulate = {}
business_iter = FieldIter(
    "../dataset/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json",
    "json", "categories")
for val in business_iter:
    categories_set = categories_set.union(set(val))
    #find business about food (for specific field mining)
    if "Food" in val:
        food_categories_set = food_categories_set.union(set(val))
        for phrase in val:
            if phrase in food_categories_accumulate:
                food_categories_accumulate[phrase] +=1
            else:
                food_categories_accumulate[phrase] =1
    else:
        for phrase in val:
            if re.match(".*Food.*", phrase) or re.match(".*food.*", phrase):
                food_categories_set = food_categories_set.union(set(val))
                break
        else:
            continue
        #if break, add all phrases' accumulator
        for phrase in val:
            if phrase in food_categories_accumulate:
                food_categories_accumulate[phrase] +=1
            else:
                food_categories_accumulate[phrase] =1

with open("./yelp_ch6/categories.txt","w") as f:
    for category in categories_set:
        f.write( category + "\n" )

with open("./yelp_ch6/food_categories.txt","w") as f:
    for category in food_categories_accumulate:
        f.write( category + "\t" + str(food_categories_accumulate[category]) + "\n" )

categories_items = list( map(lambda x:(x,[food_categories_accumulate[x]]) , food_categories_accumulate) )
categories_df = pd.DataFrame.from_items(items=categories_items, columns=["count"], orient="index")
categories_df = categories_df.sort_values("count", ascending=False)   #sort by count desc

frequent_categories_df = categories_df.query("count>5")
print(frequent_categories_df)
frequent_categories_df.plot(kind="bar")