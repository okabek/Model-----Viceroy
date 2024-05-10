# Viceroy
# - forecasting a currency's price change in the next hour after [x news] is released by using a knn algorithm
# - model 'trained' on ~40000 pieces of data ranging from 2007 - 2017
#
## u = mean average positive change | w = mean average negetive change | o = 1 stdev | x = forecasted change
### "strong buy signal": x >= u + 2o 
### "buy signal": x >= u + 1o 
### "sell signal": x <= w - 1o
### "strong sell signal": x <= w - 2o 
### else "no signal found"
