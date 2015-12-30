# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 12:22:44 2015
cluster business by geo. distance (each cluster represent a living area)
first try in one city?
use hiretical or k-method?
find k-nearest-neighbor in same cluster?
try find if there are categories pattern between clusters? (which means a living area usually contain what business)

@author: Ophidian Wang
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from sklearn.cluster import hierarchical
from sklearn.cluster import DBSCAN
from od_misc.FileIter import FieldsIter
#from pyspark.mlib.fpm import FPGrowth

def drawScatterHist(x, y):
    """
    scatter plot with hist
    """
    
    nullfmt = NullFormatter()         # no labels
    
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    
    # start with a rectangular Figure
    plt.figure(1, figsize=(8, 8))
    
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    
    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    
    # the scatter plot:
    axScatter.scatter(x, y)
    
    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
    lim = (int(xymax/binwidth) + 1) * binwidth
    
    axScatter.set_xlim((-lim, lim))
    axScatter.set_ylim((-lim, lim))
    
    bins = np.arange(-lim, lim + binwidth, binwidth)
    axHistx.hist(x, bins=bins)
    axHisty.hist(y, bins=bins, orientation='horizontal')
    
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())
    
    plt.show()

def businessFromCluster():
    """
    find common business category in geometrical clusters
    use pyspark.mlib.fpm.FPGrowth ?
    """
    print("businessFromCluster")
    # 2-D clustering (latitude, longitude)
    
    # for each cluster, get cluster-categories(business)
    
    # observe the frequent category set, if if make sense
        
   
def livingAreaFromPattern():
    """
    find living area(business-cluster)/user_group(user_cluster) from user-[review]-business pattern
    use pyspark.mlib.fpm.FPGrowth ?
    """
    print("livingAreaFromUser")
    # get review by business
    
    # get user by business-review
    
    # reform user-categories(business) association
    
    # fp-growth on user-categories set
        
    # observe the frequent category set, if it can form business cluster

def explore():
    target_state = "AZ"
    target_city = "Phoenix"
    
    dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
    business_path = dataset_path + "yelp_academic_dataset_business.json"
    target_fields = ["business_id", "name", "state", "city", "categories", "latitude", "longitude"]
    business_iter = FieldsIter(business_path, "json", target_fields, 10)
    x = []
    y = []
    for row in business_iter:
        if row["state"] != target_state:
            continue
        print(row)
        x.append(row["latitude"])
        y.append(row["longitude"])
    
    drawScatterHist(x, y)


if __name__=="__main__":
    #explore()
    # the random data
    x = np.random.randn(1000)
    y = np.random.randn(1000)
    drawScatterHist(x, y)