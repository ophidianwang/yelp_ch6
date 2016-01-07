# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 12:28:46 2015

@author: Ophidian Wang
"""

import pickle
from sklearn.cluster.bicluster import SpectralBiclustering


def main():
    # n_clusters = (5,10)
    n_clusters = 200
    feature_path = "yelp_ch6/tfidf_feature.pickle"
    tfidf_vector_path = "yelp_ch6/tfidf_vector_None.pickle"
    document_limit = None

    vectors = None
    with open(tfidf_vector_path, "rb") as f:
        load_var = pickle.load(f)
        vectors = load_var["vectors"]
        if type(document_limit) is int:
            print("document_limit is int")
            vectors = vectors[:document_limit]  # extract part of csr_matrix for dev
    print(vectors.shape)

    SB = SpectralBiclustering(n_clusters=n_clusters, n_jobs=-1)
    SB.fit(vectors)

    with open("review_word_SpectralBiclustering.pickle", "wb") as f:
        pickle.dump(SB, f)


if __name__ == "__main__":
    main()
