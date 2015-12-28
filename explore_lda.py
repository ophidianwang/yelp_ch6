# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:57:11 2015

@author: USER
"""

import pickle
from time import time
from sklearn.decomposition import LatentDirichletAllocation as LDA

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

n_topics = 100

lda = LDA(  n_topics=n_topics, max_iter=10,
            learning_method='online', learning_offset=50.,
            random_state=0, n_jobs=-1)

tfidf_feature_names = []
with open("yelp_ch6/tfidf_feature.pickle","rb") as f:
    tfidf_feature_names = pickle.load(f)
print("feature numbers: " + str(len(tfidf_feature_names)))

tfidf_vectors = None
with open("yelp_ch6/tfidf_vector_None.pickle","rb") as f:
    load_var = pickle.load(f)
    tfidf_vectors = load_var["vectors"][:10000]    #extract part of csr_matrix for dev
print(tfidf_vectors.shape)

t0 = time()
lda.fit(tfidf_vectors)
print("done in %0.3fs." % (time() - t0))

print_top_words(lda, tfidf_feature_names, 20)