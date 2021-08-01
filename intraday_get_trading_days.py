
#%%
#!pip install pandas
#!conda install pandas=0.22.0 
#!conda  install -c quantopian zipline
#%%
import pandas as pd
import csv
import numpy as np
from trading_calendars import get_calendar
from zipline.utils.calendars import TradingCalendar
from zipline.utils.tradingcalendar import get_trading_days
from pandas import Timestamp

#Jul 02 2018 08:00:00 1530518400000000000 TQQQ21725 1627084795000000000 Jul 23 2021 23:59:55 
#%%
#This is the process to get the correct trading days, which will then be use in the Bundle Ingest process to index the days
trading_days = get_trading_days(start=Timestamp('2018-07-02 08:00:00+0000', tz='UTC'), 
                                end=Timestamp('2021-07-23 23:59:55+0000') #, tz='UTC'
                                ).date.astype(str)

# %%
# US Markets Closed December 5, 2018: National Day of Mourning for George H.W. Bush
trading_days = np.delete(trading_days, np.where(trading_days == '2018-12-05'))
trading_days[trading_days == '2018-12-05']


#%%
# Create a CSV file to set the Zipline Bundle Ingest process against
with open('intraday_trading_calendar.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(trading_days)
# %%

# %%
