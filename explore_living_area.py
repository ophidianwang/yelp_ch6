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
from time import time
import datetime
from itertools import cycle
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import NullFormatter
from sklearn.cluster import Birch
from sklearn.cluster import AgglomerativeClustering
from od_misc.FileIter import FieldsIter
#from pyspark.mlib.fpm import FPGrowth

def maskedList(mask, data):
    result = []
    for index,val in enumerate(mask):
        if val:
            result.append(data[index])
    return result

def drawScatterHist(x, y):
    """
    scatter plot with hist
    """
    # get x,y range    
    xmax = np.max(x)
    xmin = np.min(x)
    ymax = np.max(y)
    ymin = np.min(y)
    xlen = np.max(x)-np.min(x)
    ylen = np.max(y)-np.min(y)
    print([xmin, xmax])
    print([ymin, ymax])
    print((xlen,ylen))
        
    size_tuple = (0, 0)
    if xlen>ylen:
        size_tuple = (8*xlen/ylen, 8)
    else:
        size_tuple = (8, 8*ylen/xlen)
    
    nullfmt = NullFormatter()         # no labels
    
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    
    # start with a rectangular Figure
    plt.figure(1, figsize=size_tuple)
    
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    
    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    
    # the scatter plot:
    axScatter.scatter(x, y)
    
    # now determine nice limits by hand:
    binwidth = 0.01
    xlim_max = (int(xmax/binwidth) + 1) * binwidth
    xlim_min = (int(xmin/binwidth) - 1) * binwidth
    ylim_max = (int(ymax/binwidth) + 1) * binwidth
    ylim_min = (int(ymin/binwidth) - 1) * binwidth
    
    #print((xlim_min, xlim_max))
    #print((ylim_min, ylim_max))

    axScatter.set_xlim((xmin, xmax))
    axScatter.set_ylim((ymin, ymax))
    
    xbins = np.arange(xlim_min, xlim_max + binwidth, binwidth)
    ybins = np.arange(ylim_min, ylim_max + binwidth, binwidth)
    axHistx.hist(x, bins=xbins)
    axHisty.hist(y, bins=ybins, orientation='horizontal')
    
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())
    
    plt.show()

def patternFromCluster(model, business_list, X_dots, sc=None):
    """
    find common business categories/users in geometrical clusters
    use pyspark.mlib.fpm.FPGrowth ?
    """
    print("patternFromCluster")
    # 2-D clustering (latitude, longitude)
    
    # for each cluster, get cluster-categories(business)
    labels = model.labels_
    centroids = model.subcluster_centers_
    n_clusters = np.unique(labels).size
    
    #extract categories from cluster-businesses
    cluster_categories = []
    for this_centroid, k in zip(centroids, range(n_clusters)):
        current_categories = set()
        mask = labels == k
        targets = maskedList(mask, business_list)
        print("cluster #" + str(k) + " has " + str(len(targets)) + " business.")
        for row in targets:
            # each row is a business
            for category in row[4]:
                current_categories.add(category)
        print("cluster #" + str(k) + " has " + str(len(current_categories)) + " kinds of business categories.")
        print(current_categories)
        cluster_categories.append(current_categories)

    # pyspark PFP, observe the frequent category set, if if make sense
    """
    sc.parallelize(cluster_categories)
    model = FPGrowth.train(transactions, minSupport=0.1, numPartitions=4)
    
    result = model.freqItemsets().collect()
    for fi in result:
        print(fi)
    """
   
def livingAreaFromPattern(business_list):
    """
    find living area(business-cluster)/user_group(user_cluster) from user-[review]-business pattern
    use pyspark.mlib.fpm.FPGrowth ?
    """
    print("livingAreaFromUser")
    dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
    review_path = dataset_path + "yelp_academic_dataset_review.json"
    
    # make empty user list for each business
    business_user_list = {} # mine user set from business
    user_business_list = {} # mine business set from user
    for row in business_list:
        business_user_list[row[0]] = [] #business_id

    # get review by business
    # get user by business-review
    user_iter = FieldsIter(review_path, "json", ["user_id", "business_id"])
    for row in user_iter:
        user_id = row[0]
        business_id = row[1]
        if business_id in business_user_list:
            business_user_list[business_id].append(user_id)
        if user_id not in user_business_list:
            user_business_list[user_id] = [business_id]
        else:
            user_business_list[user_id].append(business_id)
    
    for business_id in business_user_list:
        print("business_id: " + business_id + " has " + str(len(business_user_list[business_id])) + " users' reviews")
        #print(business_user_list[business_id])

    return business_user_list, user_business_list
    
    # reform user-categories(or business) association
    
    # fp-growth on user-categories(or business) set
        
    # observe the frequent category set, if it can form business cluster

def clusterPlot(model, X_dots, x, y, title):
    
    # get x,y range    
    xmax = np.max(x)
    xmin = np.min(x)
    ymax = np.max(y)
    ymin = np.min(y)
    xlen = np.max(x)-np.min(x)
    ylen = np.max(y)-np.min(y)

    size_tuple = (0, 0)
    if xlen>ylen:
        size_tuple = (8*xlen/ylen, 8)
    else:
        size_tuple = (8, 8*ylen/xlen)
    
    # Use all colors that matplotlib provides by default.
    colors_ = cycle(colors.cnames.keys())

    # start with a rectangular Figure
    my_dpi = 120
    plt.figure(1, figsize=size_tuple, dpi=my_dpi)

    # Plot result
    labels = model.labels_
    centroids = model.subcluster_centers_
    n_clusters = np.unique(labels).size

    print("n_clusters : %d" % n_clusters)
    
    ax = plt.axes()
    for this_centroid, k, col in zip(centroids, range(n_clusters), colors_):
        #print((this_centroid, k, col))
        mask = labels == k
        ax.plot(X_dots[mask, 0], X_dots[mask, 1], 'w',
                markerfacecolor=col, marker='.')
        if birch_model.n_clusters is None:
            ax.plot(this_centroid[0], this_centroid[1], '+', markerfacecolor=col,
                    markeredgecolor='k', markersize=5) 
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))
    ax.set_autoscaley_on(False)
    ax.set_title(title)
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    
    plt.savefig(title + "_" + \
        datetime.datetime.now().strftime("%Y%m%d%H%M%S") + \
        ".png",format="png", dpi=my_dpi)

def explore(sc=None):

    dataset_path = "../dataset/yelp_dataset_challenge_academic_dataset/"
    business_path = dataset_path + "yelp_academic_dataset_business.json"
    target_fields = ["business_id", "name", "state", "city", "categories", "latitude", "longitude"]
    #explore_match = {"state":"AZ"}
    #explore_match = {"state":"AZ","city":"Phoenix"}
    explore_match = {"city":"Phoenix"}
    index_list = list( map(lambda x:target_fields.index(x), explore_match.keys()) )
    index_match= dict(zip(index_list, explore_match.values()))
    
    business_iter = FieldsIter(business_path, "json", target_fields)
    match_business = []
    x = []
    y = []
    dots = []
    for row in business_iter:
        #check condition
        for index in index_match:
            if row[index]!= index_match[index]:
                break
        else:   #all cond. matched
            #print(row)
            x.append(row[6])    #longitude
            y.append(row[5])    #latitude
            dots.append([row[6],row[5]])
            match_business.append(row)

    print( "business number: " + str(len(x)))
    #drawScatterHist(x, y)
    
    return livingAreaFromPattern(match_business)
    
    
    dots = np.array(dots)
    
    birch_model = Birch(threshold=0.02, n_clusters=None)
    t = time()
    birch_model.fit(dots)
    print("Birch without global clustering took %0.2f seconds" % (time() - t))
    
    clusterPlot(birch_model, dots, x, y, "Phoenix_Business_Birch")
    patternFromCluster(birch_model, match_business, dots, sc=sc)
    
    return birch_model

if __name__=="__main__":
    #sc = SparkContext(appName="explore_living_area")
    business_user_list, user_business_list = explore()
    """
    # the random data
    x = np.random.randn(1000)
    y = np.random.randn(1000)
    drawScatterHist(x, y)
    """