import pandas as pd
import numpy as np



def stock_selection(clusters_stockName_dict, sp_obs, threshold):
    # Create a df. Index: stock name, first colunm: price on first day, second column: price on te last day.
    underperformed=[]
    outperformed=[]

    for cluster_index, stock_names in clusters_stockName_dict.items():
        single_cluster_allDate = sp_obs.loc[stock_names, :]
        single_cluster =single_cluster_allDate.iloc[:,[0,-1]].copy()
        single_cluster.loc[:,'changes'] = single_cluster.iloc[:,1]/single_cluster.iloc[:,0]
        #print(single_cluster)
        average_performance = single_cluster.iloc[:,-1].mean()
        selection_window = threshold*np.sqrt(single_cluster.shape[0]-2)
        underperformed_in_this_cluster = list(single_cluster[single_cluster['changes']<average_performance*(1-selection_window)].index)
        outperformed_in_this_cluster = list(single_cluster[single_cluster['changes']>average_performance*(1+selection_window)].index)
        underperformed.extend(underperformed_in_this_cluster)
        outperformed.extend(outperformed_in_this_cluster)
    return underperformed, outperformed

