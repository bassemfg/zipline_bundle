#%%
from zipline.api import order, record, symbol
from zipline.finance import commission, slippage
from zipline import run_algorithm
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt


def initialize(context):
    context.asset = symbol("TQQQ")

    # Explicitly set the commission/slippage to the "old" value until we can
    # rebuild example data.
    # github.com/quantopian/zipline/blob/master/tests/resources/
    # rebuild_example_data#L105
    context.set_commission(commission.PerShare(cost=0.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    order(context.asset, 10)
    record(TQQQ=data.current(context.asset, "price"))


# Note: this function can be removed if running
# this algorithm on quantopian.com
def analyze(context=None, results=None):
    import matplotlib.pyplot as plt

    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel("Portfolio value (USD)")
    ax2 = plt.subplot(212, sharex=ax1)
    results.TQQQ.plot(ax=ax2)
    ax2.set_ylabel("TQQQ price (USD)")

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()


start = pd.Timestamp("2018-7-2", tz='utc')
end = pd.Timestamp("2021-7-23", tz='utc')

sp500 = web.DataReader("SP500", "fred", start, end).SP500
benchmark_returns = sp500.pct_change()
print(benchmark_returns.head())

result = run_algorithm(
    start=start,
    end=end,
    initialize=initialize,
    handle_data=handle_data,
    capital_base=100000,
    benchmark_returns=benchmark_returns,
    bundle="intraday-tqqq",
    data_frequency="minute",
)

print(result.info())
print(result)
result.to_csv("buy_tqqq.csv")

# %%
result.portfolio_value.plot()
plt.show()
#%%
import  pyfolio as pf
returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(result)
pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions, benchmark_rets=benchmark_returns)
pf.create_returns_tear_sheet(returns, benchmark_rets=benchmark_returns)
# %%
