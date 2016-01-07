# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 09:25:55 2015
This script is for sampling yelp dataset based on reviews.
@author: Ophidian Wang
"""

import os
import json
import random

dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
business_path = dataset_path + "yelp_academic_dataset_business.json"
review_path = dataset_path + "yelp_academic_dataset_review.json"
user_path = dataset_path + "yelp_academic_dataset_user.json"
checkin_path = dataset_path + "yelp_academic_dataset_checkin.json"
tip_path = dataset_path + "yelp_academic_dataset_tip.json"
destination_path = "../dataset/yelp_review_sampled/"

if not os.path.exists(destination_path):
    os.mkdir(destination_path)

sampling_rate = 100  # 1/sampling_rate
cursor = 0
user_ids = []
business_ids = []

with open(destination_path + "sampled_review.json", "w") as sampled_review, \
        open(review_path) as review_file:
    for line in review_file:
        cursor += 1
        if not random.randint(1, sampling_rate) == 1:
            continue
        print("sample review #" + str(cursor))
        sampled_review.write(line)
        single_review = json.loads(line.strip())
        if not single_review["user_id"] in user_ids:
            user_ids.append(single_review["user_id"])
        if not single_review["business_id"] in business_ids:
            business_ids.append(single_review["business_id"])

with open(destination_path + "sampled_business.json", "w") as sampled_business, \
        open(business_path) as business_file:
    for line in business_file:
        single_business = json.loads(line.strip())
        if single_business["business_id"] in business_ids:
            sampled_business.write(line)

with open(destination_path + "sampled_user.json", "w") as sampled_user, \
        open(user_path) as user_file:
    for line in user_file:
        single_user = json.loads(line.strip())
        if single_user["user_id"] in user_ids:
            sampled_user.write(line)
