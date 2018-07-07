
def evaluate_performance(stock_names, sp_test):

    sp_slice_all_dates = sp_test.loc[stock_names, :]
    sp_slice =sp_slice_all_dates.iloc[:,[0,-1]].copy()
    sp_slice.loc[:,'changes'] = sp_slice.iloc[:,1]/sp_slice.iloc[:,0]
    #print(sp_slice)
    average_performance = sp_slice.iloc[:,-1].mean()
    #print(sp_slice.iloc[0:5,[0,-1]])
    return average_performance
