#Evaluate the performance of stocks in stock_names using test_set data. The average_performance is AVG(last_day_price)/ AVG(first_day_price). 
def evaluate_performance(stock_names, sp_test):
    sp_slice_all_dates = sp_test.loc[stock_names, :]
    sp_slice =sp_slice_all_dates.iloc[:,[0,-1]].copy() #Get prices on the first (0) and last (-1) days.
    sp_slice.loc[:,'changes'] = sp_slice.iloc[:,1]/sp_slice.iloc[:,0]  #Add 'change' column (-1) to DF.
    #print(sp_slice)
    average_performance = sp_slice.iloc[:,-1].mean() #Mean of 'change'
    #print(sp_slice.iloc[0:5,[0,-1]])
    return average_performance
