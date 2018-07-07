import matplotlib.pyplot as plt
import pandas as pd

'''
Input: dataframe, index is stock name, columns are dates (not time series)
'''

def plot_stocks(stocks_df,title,lines=None):
    stocks_df = stocks_df.T
    stocks_df.index = pd.to_datetime(stocks_df.index)
    stocks_df.plot()
    plt.ylabel('Price/price_at_the_fist_day')
    plt.title(title)
    plt.xlabel('Date')
    if lines!=None:
        for val in lines:
            plt.axvline(val,linestyle='dashed', color='black')
    plt.show()

