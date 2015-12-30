# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 09:48:30 2015

@author: USER
"""

import pickle
from od_misc.FileIter import FieldIter
from od_misc.FileIter import FieldsIter

def main():
    dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
    business_path = dataset_path + "yelp_academic_dataset_business.json"
    review_path = dataset_path + "yelp_academic_dataset_review.json"
    business_limit = None
    vector_path = "yelp_ch6/count_vector_None.pickle" #tfidf_vector_None.pickle
    result_path = "yelp_ch6/category_count_vector.pickle"
    
    # load business categories
    business_cat_dict = {}
    business_iter = FieldsIter(business_path, "json", ["business_id", "categories"], business_limit)
    for row in business_iter:
        business_cat_dict[row[0]] = row[1]
    print("load business done")
        
    # load vectors
    with open(vector_path,"rb") as f:
        load_var = pickle.load(f)
        vectors = load_var["vectors"]
    print("load vectors done")
    
    # load reviews and start mapping categories
    cursor = 0
    categories_tf = {}
    review_iter = FieldIter(review_path, "json", "business_id")
    for review_business_id in review_iter:
        if (cursor%10000)==0:
            print("working on review @ " + str(cursor))
        #print( business_cat_dict[review_business_id] )
        for category in business_cat_dict[review_business_id]:
            if category not in categories_tf:
                categories_tf[category] = vectors[cursor]
            else:
                #print(categories_tf[category].shape)
                categories_tf[category] += vectors[cursor]
                #print(categories_tf[category].shape)
                #return
        cursor += 1
    print("load vectors done")
    
    # save category to count vector
    with open(result_path, "wb") as f:
        pickle.dump(categories_tf, f)
    print("save categories_tf done")
    
if __name__=="__main__":
    main()