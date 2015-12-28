# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 09:25:55 2015

@author: USER
"""

import os
import json
import math
import pandas as pd
import matplotlib.pyplot as plt

dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
business_path = dataset_path + "yelp_academic_dataset_business.json"
review_path = dataset_path + "yelp_academic_dataset_review.json"
user_path = dataset_path + "yelp_academic_dataset_user.json"
checkin_path = dataset_path + "yelp_academic_dataset_checkin.json"
tip_path = dataset_path + "yelp_academic_dataset_tip.json"
destination_path = "../dataset/yelp_review_sampled/"

user_json = ""
with open(destination_path+"/sampled_user.json","r") as user_file:
    user_json = "[" + ",".join(user_file.readlines()) + "]"
user_df = pd.read_json(user_json)
round_stars = user_df["average_stars"].apply(lambda x:round(x,0))

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 14))

user_df = user_df.assign(round_stars=round_stars)
user_df.groupby("round_stars").size().plot(title="round avg. stars", kind="bar", ax=axes[0])

user_df= user_df.assign(review_range=user_df["review_count"].apply(lambda x:math.floor(x/100)))
user_df.groupby("review_range").size().plot(title="review range", kind="bar", ax=axes[1])