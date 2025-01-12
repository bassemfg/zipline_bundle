#%%
import csv
import numpy as np
import pandas as pd
import os


#%%
# Get the Trading Calendar, run from a zip35 code environment
with open('trading_calendar.csv') as f:
    reader = csv.reader(f)
    data = list(reader)

arr = np.array(data)
trading_days = arr.ravel()

#%%
# Function to format the csv files for the csvdir.py Zipline Bundle Ingest process
def format_bundle(indir, outdir):
       
    count = 0
    for f in os.listdir(indir): # For Production
    # for f in ['AAPL.csv']:  # For Testing
        
        df = pd.read_csv('{}/{}'.format(indir, f))
        df.rename(columns={'time':'date',
                           #'high_adj': 'high',
                           #'low_adj': 'low',
                           #'close_adj': 'close',
                           #'volume_adj': 'volume'
                           }, inplace=True)
        
        df.index = pd.DatetimeIndex(df['date'])
        print(df)
        # I need to add some logic here to force the number of rows to equal the number of expected trading days
        #df = df.reindex(trading_days)

        # Export it in the csvdir format needed for the ziplien bundle ingestion process
        #df.reset_index(inplace=True)
        
        aggregation = {'open'  :'first',
               'high'  :'max',
               'low'   :'min',
               'close' :'last',
               'volume':'sum'}
        period = '1Min'
        df = df.resample(period).agg(aggregation).dropna()

        # Check if there is there is any divident, if not make it zero
        if not 'dividend' in df.columns:
            df['dividend'] = 0.0
        
        df = df[[ 'open', 'high', 'low', 'close', 'volume','dividend']]
        df['dividend'].fillna(0.00, inplace=True)
        df['ratio'] = 1  # Since I alread did all the adjusting
        
        
        # Round the numbers in the dataframe
        df = df.round({'open':2,
                  'high':2,
                  'low':2,
                  'close':2,
                  'volume':1,
                  'dividend':2})
        print(df)


        df.to_csv('{}/{}'.format(outdir, f), index=True)

        count += 1
        
    return ('{} files was adjusted'.format(count))


#%%  Execute the function to format the files
format_bundle('data/5sec_bars', 'data/csvs/minute')
# %%
