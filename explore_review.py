# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:19:12 2015

@author: Ophidian Wang
"""

import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from od_misc.FileIter import FieldIter
import pickle


def main():
    dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
    business_path = dataset_path + "yelp_academic_dataset_business.json"
    review_path = dataset_path + "yelp_academic_dataset_review.json"
    user_path = dataset_path + "yelp_academic_dataset_user.json"
    checkin_path = dataset_path + "yelp_academic_dataset_checkin.json"
    tip_path = dataset_path + "yelp_academic_dataset_tip.json"
    destination_path = "../dataset/yelp_review_sampled/"

    doc_limit = None  # limit int for reviews, set to None if wants to load all reviews
    idf = False
    vectorizor_type = "count"

    # test_counter = Counter(destination_path+"sampled_user.json")
    # review_itr = ReviewTextItr(destination_path+"sampled_review.json", doc_limit)
    review_itr = FieldIter(review_path, "json", "text", doc_limit)

    vectorizer = None
    if vectorizor_type == "tfidf":
        vectorizer = TfidfVectorizer(max_df=0.5, min_df=10, \
                                     stop_words='english', use_idf=idf, \
                                     strip_accents="unicode"
                                     )
    elif vectorizor_type == "count":
        vectorizer = CountVectorizer(max_df=0.5, min_df=10, stop_words='english', \
                                     strip_accents="unicode")
    else:
        raise Exception("vectorizer_type error")

    start_time = datetime.datetime.now();
    X = vectorizer.fit_transform(review_itr)
    tfidf_done_time = datetime.datetime.now();
    print("spend " + str(
        tfidf_done_time.timestamp() - start_time.timestamp()) + " sec. on " + vectorizor_type + " vectorize.\n")

    # print(type(X))
    # print(vectorizer.get_feature_names())
    with open("yelp_ch6/" + vectorizor_type + "_vector_" + str(doc_limit) + ".pickle", "wb") as f:
        save_var = {"feature": vectorizer.get_feature_names(),
                    "vectors": X
                    }
        pickle.dump(save_var, f)

    with open("yelp_ch6/" + vectorizor_type + "_vector_" + str(doc_limit) + ".pickle", "rb") as f:
        load_var = pickle.load(f)
        print(load_var.keys())


if __name__ == "__main__":
    main()
