'''
Assumption: stocks which performed similarly in the past(a cluster) will probably continue doing so in the near future.
This code can:
    1. Collect and wrangle daily stock price for SP500
    2. Cluster S&P500 stocks into a number of clusters. The number can be determined using elbow method.
    3. Find the under-evaluated stocks in three months and evaluate their performance in the next month.
Tianshi Wang, University of Delaware
https://tswang.wixtsite.com/home
'''

import stock_selection
from data_wrangling import data_wrangling
from plot_stocks import plot_stocks
from stock_selection import *
from evaluate_performance import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import random
'''
Tianshi Wang, University of Delaware

'''

#The csv file is downloaded using the getData.py.
#Data wrangling; split the dataset to three sets.
sp_clustering, sp_obs, sp_test,sp_all_sets = data_wrangling("./data/sp500_all_data.csv", clustering_start='2015-01-01',
                                           obs_start='2018-03-01', test_start='2018-06-01',
                                           test_end='2018-07-01')
names = list(sp_clustering.index)

#Plot six random stocks on training set.
plot_stocks(sp_clustering.sample(10),title='Price Chart of Eight Random Stocks in S&P500')

#Train for clustering using k-means.
print("Calculating the Sum of squared distances of stock to their closest cluster center for cluster numbers from 5 to 200.")
elbow_data = np.array([])
print("Number_of_Clusters: Sum of squared distances of stock to their closest cluster center ")
for k in range(5,200,10):
    kmeans_train = KMeans(n_clusters=k, random_state=0, max_iter=300).fit(sp_clustering)
    elbow_data=np.append(elbow_data, [k, kmeans_train.inertia_ ])
    print(str(k)+": " + str(int(kmeans_train.inertia_)))
elbow_data = np.reshape(elbow_data, (-1,2))

plt.plot(elbow_data[:,0], elbow_data[:,1])
plt.xlabel('Number of Clusters')
plt.ylabel('Sum of squared distances of stock to their closest cluster center')
plt.show()

print("Choose number_of_clusters=150")
kmeans_train = KMeans(n_clusters=150, random_state=0, max_iter=300).fit(sp_clustering)
labels_train = kmeans_train.labels_   #lables_train is the
name_cluster_dict = {names[i]:labels_train[i] for i in range(0,len(names))}

#Summarize how many stocks in each cluster, single-stock-cluster is neglected.
unique, counts = np.unique(labels_train, return_counts=True)
clusters_dict = {key:val for key, val in dict(zip(unique, counts)).items() if val >2}
for key, val in clusters_dict.items():
    print("Cluster "+str(key)+" has "+str(val)+" stocks.")
clusters_stockName_dict={}
for cluster_index in clusters_dict.keys():
    cluster_stocks = [index for index, val in enumerate(labels_train) if val==cluster_index]
    cluster_stocks_names = [names[i] for i in cluster_stocks]
    clusters_stockName_dict[cluster_index] = cluster_stocks_names

#Plot stock Price Chart for four random cluster.
cluster_to_plot = random.choices(list(clusters_stockName_dict.keys()),k=4)
for cluster_index in cluster_to_plot:
    plot_stocks(sp_clustering.loc[clusters_stockName_dict[cluster_index],:],
    str('Price Chart of Stocks in Trained Cluster '+str(cluster_index)+' (Randomly Selected)'))


#Find underperformed and outperformed stocks within each cluster based on obs_set
threshold = 0.05    #Select stocks underperforming or outperforming the rest stocks in a cluster by the threshold.
to_buy, to_sell = stock_selection (clusters_stockName_dict, sp_obs, threshold)
print("Using the data from "+str(sp_obs.columns[0].date())+" to "+str(sp_obs.columns[-1].date())+" to select stocks.")
print("The stocks underperformed others in same clusters in this period (which are expected to outperform later) are"+
      str(to_buy))
print("The stocks outperformed others in same clusters in this period (which are expected to underperform later) are"+
      str(to_sell))

#Evaluate the selected stocks on the test set.
performance_to_buy = evaluate_performance(to_buy, sp_test)
performance_to_sell = evaluate_performance(to_sell, sp_test)
performance_sp_average = evaluate_performance(list(sp_test.index), sp_test)

print("\nChecking whether the underperformed can perform better than the market from "+str(sp_test.columns[0].date())+" to "
      +str(sp_test.columns[-1].date())+".")
print("Performance of selected-underperformed stocks: "+str(performance_to_buy))
print("Performance of selected-outperformed stocks: "+str(performance_to_sell))
print("Performance of avaraged S&P500 stocks: "+str(performance_sp_average))

stock_input = input("Key in a stock name to view its price chart in clustering, observation, and test sets (q to exit): ")
while stock_input!="q":
    try:
        names.index(stock_input)
    except ValueError:
        if stock_input!="q":
            print("Wrong input. Must be in the form 'AAL'")
    else:
        plot_stocks(sp_all_sets.loc[clusters_stockName_dict[name_cluster_dict[stock_input]],:],
                    title=str(stock_input+' Stock Price Chart'),
                    lines=[sp_obs.columns[0], sp_test.columns[0], sp_test.columns[-1]] )
    stock_input = input("Another one? Type q to exit: ")
