import pandas as pd
import numpy as np
import sys
from datetime import datetime
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

data = {}

#Plots all assets included in the list in the corresponding color
def plot_assets(assets, colors):

    yearOnly = mdates.DateFormatter('%Y')
    
    for x in range(0, len(assets)):
        plt.plot_date(data[assets[x]].Date, data[assets[x]].Close, '-' + colors[x])

    ax = plt.gca()
    ax.legend(assets)
    ax.xaxis.set_major_formatter(yearOnly)

    plt.ylabel('Value (USD)')
    plt.title('Historical Prices of Crypto Currencies')
    plt.show()


#Reads in the data produced by DataCompressor.py
#Running both this file and DataCompressor.py from the same directory
# will ensure all the files and directories are correctly formatted
def read(assets):
    for name in assets:
        df = pd.read_csv('data/clean_' + name + '.csv', index_col=0)
        data[name] = df


#Crypto prices are reported everyday while traditional stock prices
# are reported only on trading days.
#
# This function gets the first n entries of the two assets with
#  matching dates.
def get_first_matching(n, asset1, asset2):
    matches = [[], []]
    j = 0
    i = 0
    match_count = 0

    len1 = len(asset1.Date)
    len2 = len(asset2.Date)

    while ( match_count < n and i < len1 and j < len2):
        if asset1.Date[i] == asset2.Date[j]:
            matches[0].append(asset1.Close[i])
            matches[1].append(asset2.Close[j])
            i += 1
            j += 1
            match_count += 1
        elif asset1.Date[i] > asset2.Date[j]:
            i += 1
        elif asset1.Date[i] < asset2.Date[j]:
            j += 1

    #if match_count < n:
    #   print('Warning: You have requested more matching dates that are available.' +
    #                  '\n\tReturning ' + str(match_count) + ' matches.')

    return matches
            

#pearsonr returns 2 values:
#   The first is the correlation coefficient
#   The second is the probability that this data would
#       have arisen if they were uncorrelated
#
# Given value n is the number of days to compare
def correlation(n, asset0, asset1):
    closing_prices = get_first_matching(n, asset0, asset1)
    
    print(pearsonr(closing_prices[0], closing_prices[1]))
    
    plt.plot(closing_prices[0], closing_prices[1], '.')
    plt.title('Historical Prices of Litecoin vs. VOO')
    plt.ylabel('Price of Litecoin (USD)')
    plt.xlabel('Price of VOO (USD)')
    plt.show()

#Returns a DataFrame with columns named Date and Close.
#The returned DataFrame only holds prices for dates
# within start_date and end_date. 
def get_time_set(asset, start_date, end_date):

    time_set = []

    for i in range(0, len(asset.Date) - 1):
        curr_date = datetime.strptime(asset.Date[i], '%Y-%m-%d')

        if(curr_date >= start_date and curr_date <= end_date):
            time_set.append([asset.Date[i], asset.Close[i]])
            
    return pd.DataFrame(time_set, columns=['Date', 'Close'])


# Returns a DataFrame with columns named Date and Close.
# The returned DataFrame only holds price info for dates which
#  are present in both asset0 and asset1 and fall within
#  start_date and end_date
# start_date and end_date should be of the form: YYYY-MM-DD
def compare_time_sets(asset0, asset1, start_date, end_date):
    time_set0 = get_time_set(asset0,
                             datetime.strptime(start_date, '%Y-%m-%d'),
                             datetime.strptime(end_date,   '%Y-%m-%d'))
    
    time_set1 = get_time_set(asset1,
                             datetime.strptime(start_date, '%Y-%m-%d'),
                             datetime.strptime(end_date,   '%Y-%m-%d'))

    return get_first_matching(sys.maxsize, time_set0, time_set1)


#Example usage of compare_time_sets to find correlation over a given
# time frame.
def time_set_correlation(asset0, asset1, start_date, end_date):
    time_matches = compare_time_sets(asset0, asset1, start_date, end_date)
    print(pearsonr(time_matches[0], time_matches[1]))

#uncomment one line below to see example usage of the code
if __name__ == "__main__":

    interest_stocks = ['Bitcoin', 'Litecoin', 'Ethereum', 'VGT', 'VOO', 'VTI']
    
    read(interest_stocks)
    print("Bitcoin to VGT 2016")
    time_set_correlation(data['Bitcoin'], data['VGT'], '2016-01-01', '2017-01-01')
    print("Bitcoin to VGT 2015")
    time_set_correlation(data['Bitcoin'], data['VGT'], '2015-01-01', '2016-01-01')
    print("Bitcoin to VGT 2014")
    time_set_correlation(data['Bitcoin'], data['VGT'], '2014-01-01', '2015-01-01')

    print("Ethereum to VGT 2016")
    time_set_correlation(data['Ethereum'], data['VGT'], '2016-01-01', '2017-01-01')
    print("Ethereum to VGT 2015")
    time_set_correlation(data['Ethereum'], data['VGT'], '2015-01-01', '2016-01-01')
    print("Ethereum to VGT 2014")
    #time_set_correlation(data['Ethereum'], data['VGT'], '2014-01-01', '2015-01-01')
    correlation(10000, data['Ethereum'], data['VGT'])

    print("Litecoin to VGT 2016")
    time_set_correlation(data['Litecoin'], data['VGT'], '2016-01-01', '2017-01-01')
    print("Litecoin to VGT 2015")
    time_set_correlation(data['Litecoin'], data['VGT'], '2015-01-01', '2016-01-01')
    print("Litecoin to VGT 2014")
    time_set_correlation(data['Litecoin'], data['VGT'], '2014-01-01', '2015-01-01')
    #correlation(1000, data['VOO'], data['Litecoin'])
    #plot_assets(interest_stocks[:3],  ['r', 'b', 'g'])
    print("Complete")
