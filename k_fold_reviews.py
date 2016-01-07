# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 15:30:38 2015

@author: USER
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
destination_prefix = "../dataset/yelp_review_"

folds = 10
limit = 1000
cursor = 0

destination_dirs = []
for i in range(folds):
    if not os.path.exists(destination_prefix + str(i)):
        os.mkdir(destination_prefix + str(i))
        destination_dirs.append(destination_prefix + str(i) + "/")

# make fold user/business id list
user_ids = {}
business_ids = {}
for i in range(folds):
    user_ids[i] = []
    business_ids[i] = []

dest_reviews = []
for dirname in destination_dirs:
    dest_reviews.append(open(dirname + "reviews.json", "w"))

with open(review_path) as review_file:
    for line in review_file:
        k = random.randint(0, (folds - 1))
        dest_reviews[k].write(line)
        single_review = json.loads(line.strip())
        if not single_review["user_id"] in user_ids[k]:
            user_ids[k].append(single_review["user_id"])
        if not single_review["business_id"] in business_ids[k]:
            business_ids[k].append(single_review["business_id"])
        cursor += 1
        if limit is not None and cursor >= limit:
            print("break @ " + str(cursor))
            break

for review_file in dest_reviews:
    review_file.close()

# make fold user according to reviews' fold
dest_users = []
for dirname in destination_dirs:
    dest_users.append(open(dirname + "users.json", "w"))

with open(user_path, "r") as user_file:
    for line in user_file:
        single_user = json.loads(line.strip())
        for k in range(folds):
            if single_user["user_id"] in user_ids[k]:
                dest_users[k].write(line)

for user_file in dest_users:
    user_file.close()

# make fold business according to reviews' fold
dest_business = []
for dirname in destination_dirs:
    dest_business.append(open(dirname + "business.json", "w"))

with open(business_path, "r") as business_file:
    for line in business_file:
        single_business = json.loads(line.strip())
        for k in range(folds):
            if single_business["business_id"] in business_ids[k]:
                dest_business[k].write(line)

for business_file in dest_business:
    business_file.close()
