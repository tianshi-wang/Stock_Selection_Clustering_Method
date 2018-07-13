Cluster stocks and find temporarily under-evaluated ones from S&P500

This algorithm assumes stocks which performed similarly in the past will probably continue doing so in the near future. Therefore, it is regarded as a buy single when a stock performed worse than others in a cluster.  

Clustered S&P500 stocks from their daily performance from 201401 to 201801 using KMeans method. Selected ~50 underperformed (to-buy) and outperformed (to-sell) stocks from their performance during 201802-201805. The selected to-buy stocks return 2.2% in 201806 (or 26% annually) compared to 0.5% for market and -0.6% for to-sell stocks. More details can be found at https://tswang.wixsite.com/home/machine-learning

Planned futher work are as follows:
1. Improve clustering algorithm e.g. setting stock price at the last day the same;
2. Find the length of period for stock selection and holding from historic data;
3. Optimize the selection threshold for clusters according to their size.

Tianshi Wang
University of Delaware
tswang@udel.edu
https://tswang.wixsite.com/home

