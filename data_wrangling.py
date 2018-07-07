'''
Functions: Cleaning data, Fill nan values, Create training, observation and test sets, etc.
Tiansh Wang, University of Delaware
'''


import pandas as pd
import math
from datetime import datetime, timedelta

def data_wrangling(csvfile, clustering_start, obs_start, test_start, test_end):


    sp505_full_features_df = pd.read_csv(csvfile)
    sp505_df = sp505_full_features_df.pivot(index='Name', columns='date', values='close')
    sp505_df.columns = pd.to_datetime(sp505_df.columns)
    sp505_df = sp505_df.loc[:, clustering_start:]


    sp_df = pd.DataFrame()
    for index, row in sp505_df.iterrows():
        if row.isnull().sum().sum() < 10:
            while row.isnull().sum().sum()>0:
                row = row.fillna(method='ffill')
                row = row.fillna(method='bfill')
                #print("filling row"+str(index))
            sp_df = sp_df.append(row)
    print('Shape of dataframe is' + str(sp_df.shape) + ' after removing stocks missing 10-day or more data.')


    sp_init_price = sp_df.iloc[:,0].copy(deep=True)
    for column in sp_df:
        sp_df[[column]] = sp_df[[column]].divide(sp_init_price, axis=0)


    sp_clustering = sp_df.loc[:, :obs_start]
    print('Shape of the clustering set is:'+ str(sp_clustering.shape) )

    sp_obs = sp_df.loc[:, obs_start:test_start]
    sp_test = sp_df.loc[:, test_start:test_end]
    print('Shape of the observation set is:'+ str(sp_obs.shape) )
    print('Shape of the test set is:'+ str(sp_test.shape) )
    sp_all_sets = sp_df.loc[:, clustering_start:test_end]
    return sp_clustering, sp_obs, sp_test, sp_all_sets

