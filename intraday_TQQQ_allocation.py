#%%
import pandas as pd
import numpy as np
import zipline

from zipline.api import order_target, record, symbol#, history, add_history
import matplotlib.pyplot as plt
import pytz
from datetime import datetime


def initialize(context):
    context.i = 0
    context.sym = symbol('TQQQ')
    print(context)
    #add_history(10, '1m', 'price')
    #add_history(30, '1m', 'price')

def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 30:
        return
    print(context)
    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.asset, 'price', bar_count=10, frequency="1m").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=30, frequency="1m").mean()
    print(long_mavg,short_mavg)

    # Trading logic
    if short_mavg > long_mavg:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.asset, 100)
    elif short_mavg < long_mavg:
        order_target(context.asset, 0)

    # Save values for later inspection
    record(TQQQ=data.current(context.asset, 'price'),
           short_mavg=short_mavg,
           long_mavg=long_mavg)


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')
    print(perf)
    ax2 = fig.add_subplot(212)
    perf['TQQQ'].plot(ax=ax2)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax2)
    print(perf)
    perf_trans = perf.loc[[t != [] for t in perf.transactions]]
    buys = perf_trans.loc[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    print(perf_trans)
    sells = perf_trans.loc[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.short_mavg.loc[buys.index],
             '^', markersize=10, color='m')
    ax2.plot(sells.index, perf.short_mavg.loc[sells.index],
             'v', markersize=10, color='k')
    ax2.set_ylabel('price in $')
    plt.legend(loc=0)
    plt.show()



#%%
start =  pd.Timestamp('2018-7-2', tz='utc')
end =  pd.Timestamp('2021-6-23', tz='utc')


# Fire off backtest
result = zipline.run_algorithm(
    start=start, # Set start
    end=end,  # Set end
    initialize=initialize, # Define startup function
    capital_base=100000, # Set initial capital
    data_frequency = 'minute',  # Set data frequency
    bundle='intraday-tqqq' ) # Select bundle


print("Ready to analyze result.")
#%%

print(result)
#analyze(result, bench_series)

# Dump out the results to a csv
result.to_csv('result.csv')

#%%
'''def initialize(context):
    # ETFs and target weights for a balanced and hedged portfolio
    context.securities = {
        'TQQQ': 1 

    }
    
    # Schedule rebalance for once a month
    schedule_function(rebalance, date_rules.month_start(), time_rules.market_open())
    
    # Set up a benchmark to measure against
    context.set_benchmark(symbol('TQQQ'))


def rebalance(context, data):
    # Loop through the securities
    for sec, weight in context.securities.items():
        sym = symbol(sec)
        
        # Check if we can trade
        if data.can_trade(sym):
            # Reset the weight
            order_target_percent(sym, weight) 


#%%
start =  pd.Timestamp('2018-7-2', tz='utc')
end =  pd.Timestamp('2021-6-23', tz='utc')


# Fire off backtest
result = zipline.run_algorithm(
    start=start, # Set start
    end=end,  # Set end
    initialize=initialize, # Define startup function
    capital_base=100000, # Set initial capital
    data_frequency = 'minute',  # Set data frequency
    bundle='intraday-tqqq' ) # Select bundle

print("Ready to analyze result.")


#%% Create a benchmark file for Pyfolio
bench_df = pd.read_csv('data/5sec_bars/TQQQ21725.csv')
bench_df['return'] = bench_df.close_adj.pct_change()
bench_df.to_csv('TQQQ.csv', columns=['date','return'], index=False)

#%%
# Create a benchmark dataframe
bench_series = create_benchmark('TQQQ')
#%%
# Filter for the dates in returns to line up the graphs - normalize cleans up the dates
result.index = result.index.normalize() # to set the time to 00:00:00
bench_series = bench_series[bench_series.index.isin(result.index)]
bench_series

#%%
# Run the tear sheet analysis
print(result)
#analyze(result, bench_series)


#%%
# Dump out the results to a csv
result.to_csv('result.csv')
'''