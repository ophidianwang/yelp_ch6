# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:57:11 2015
RAM!!!

@author: Ophidian Wang
"""

import pickle
from time import time
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import NMF

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
def main():
    n_topics = 200
    feature_path = "yelp_ch6/tfidf_feature.pickle"
    count_vector_path = "yelp_ch6/count_vector_None.pickle"
    tfidf_vector_path = "yelp_ch6/tfidf_vector_None.pickle"
    document_limit = None
    
    feature_names = []
    with open(feature_path,"rb") as f:
        feature_names = pickle.load(f)
    print("feature numbers: " + str(len(feature_names)))
    
    """
    count Vectorize + LDA
    """
    lda = LDA(  n_topics=n_topics, max_iter=10,
                learning_method='online', learning_offset=50.,
                random_state=0, n_jobs=-1)  #use all cpu
    vectors = None
    with open(count_vector_path,"rb") as f:
        load_var = pickle.load(f)
        vectors = load_var["vectors"]
        if document_limit is int:
            vectors = vectors[:document_limit]    #extract part of csr_matrix for dev
    print(vectors.shape)
    t0 = time()
    lda.fit(vectors)
    print("lda done in %0.3fs." % (time() - t0))
    print_top_words(lda, feature_names, 20)
    
    #save model
    with open("tf_lda_model.pickle", "wb") as f:
        pickle.dump(lda, f)
    
    """
    Tfidf vectorize + NMF
    """
    vectors = None
    with open(tfidf_vector_path,"rb") as f:
        load_var = pickle.load(f)
        vectors = load_var["vectors"]
        if document_limit is int:
            vectors = vectors[:document_limit]    #extract part of csr_matrix for dev
    print(vectors.shape)
    nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5)
    t0 = time()
    nmf.fit(vectors)
    print("nmf done in %0.3fs." % (time() - t0))
    print_top_words(nmf, feature_names, 20)
    
    #save model
    with open("tfidf_nmf_model.pickle", "wb") as f:
        pickle.dump(lda, f)

if __name__=="__main__":
    main()