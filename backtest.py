"""This file backtests the tickers we received from the Stock Selection Strategy file"""

# importing packages
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#importing local file
from stock_selection import SelectionStrategies

def process_iteration(args):
    """Iterates backtesting Process"""
    start, rebalance, port = args
    ret = SelectionStrategies(start, rebalance, port)
    return ret.performance_measure()

def backtest_portfolio_parallel(start, rebalance, years, port):
    """Backtesting strategies"""
    interval = int(12 / rebalance)
    start = datetime.strptime(start, "%Y-%m-%d")
    iterations = years * interval

    # Use multiprocessing for parallel execution
    returns = []
    args_list = [(start + pd.DateOffset(months=i * rebalance), \
                  rebalance, port) for i in range(iterations)]
    with ProcessPoolExecutor() as executor:
        returns = list(executor.map(process_iteration, args_list))

    # DataFrame of the output
    df = pd.DataFrame(returns, columns=[
        'Date',
        'SP 500',
        'Value Portfolio',
        'Growth Portfolio',
        'Dividend Portfolio',
        'Quality Portfolio']).set_index('Date')

    avg_ret = df.mean() * interval
    #rf = yf.Ticker('^IRX').history('5d').Close.values[0] / 100
    sharpe_ratio = (avg_ret) / df.std()

    # Plotting the result
    plt.figure(figsize=(12, 6))
    for column in df.columns:
        plt.plot(df.index, df[column], label=column)    #pylint: disable=unsubscriptable-object
    # Plot styling
    plt.title('Portfolio Returns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Returns')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Visualizing cumulative return
    cum_df = (1+df).cumprod() -1
    plt.figure(figsize=(12, 6))
    for column in cum_df.columns:
        plt.plot(cum_df.index, cum_df[column], label=column)    #pylint: disable=unsubscriptable-object
    # Plot styling
    plt.title('Portfolio Cumulative Returns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    # Display average half-yearly return of the strategies
    print(f"Average yearly return of the strategies:\n{avg_ret}")
    print(f"Sharpe Ratio:\n{sharpe_ratio}")
    cum_df.to_excel(f'{port}output.xlsx')

# Variables for backtesting function
# Set 'var' if you want minimum variance portfolio else 'sharp'
START_DATE = '2008-01-01'
YEARS = 10
REBALANCE = 1
PORT_TYPE = 'var'

if __name__ == '__main__':
    # Running the backtest
    backtest_portfolio_parallel(START_DATE, REBALANCE, YEARS, PORT_TYPE)
