# automated_stock_selection_and_backtest

## Project Overview:
The project consists of four Python scripts aimed at implementing and backtesting stock selection strategies using Modern Portfolio Theory (MPT). Each script focuses on specific aspects of the process.

1. Local CSV Optimizer (optimizer.py):
A script designed to optimize local CSV files by filtering out irrelevant tickers.
Reads the original price and financial ratios CSV files (price_data.csv and fin_ratios.csv).
Utilizes the SelectionStrategies class to select relevant tickers based on specific criteria (e.g., value, growth, dividend, quality).
Outputs smaller and optimized CSV files (opt_price.csv and opt_ratios.csv) containing data only for selected tickers.
The optimized files serve as input for subsequent steps in the stock selection and backtesting process.

2. Stock Selection Strategies (stock_selection.py):
Implements different stock selection strategies.
Strategies include Value Stocks, Growth Stocks, Dividend Stocks, and Quality Stocks.
Uses financial ratios and price data to select stocks based on specific criteria.
Outputs optimized CSV files for price and ratios.
3. Stock Selection Strategies with Local Data (stock_selection_local.py):
Extends stock selection strategies from stock_selection.py using local data.
Utilizes optimized CSV files for price and ratios.
Imports functions from mpt_optimizer.py for portfolio optimization.
Provides methods to get optimal weights, calculate portfolio returns, and measure strategy performance.

3. Portfolio Construction (portfolio_construction.py):
This script implements functions related to Modern Portfolio Theory (MPT) for portfolio construction.
It imports necessary packages such as numpy and scipy.optimize.
Provides functions to calculate the mean return and covariance matrix of selected stock tickers, which are crucial components for MPT.
Offers two main optimization functions:
    * optimize_portfolio_variance: Returns optimal weights to minimize the portfolio variance.
    * optimize_portfolio_sharpe: Returns optimal weights to maximize the Sharpe ratio.
The get_optimal_weights function combines the data and optimization functions to obtain optimal weights for a given set of tickers and time period.

4. Backtesting Tickers (backtest.py):
Backtests the stock tickers received from the Stock Selection Strategies file.
Utilizes parallel processing for efficient backtesting.
Displays average yearly returns, Sharpe ratios, and visualizations of portfolio returns over time.
Outputs cumulative returns to an Excel file.


## Usage:
### Install Dependencies:
Ensure that the required packages (pandas, numpy, yfinance, matplotlib) are installed.

### Run Scripts:
* Execute the optimizer.py file
* Run the backtest.py file

### Adjust Configuration:
Customize the variables in each script according to your preferences, such as start date, rebalance frequency, and portfolio type.

### Interpret Results:
Analyze the generated visualizations and printed performance metrics to evaluate the effectiveness of the implemented stock selection strategies.

## Conclusion:
The project provides a comprehensive framework for selecting and backtesting stocks based on different strategies, incorporating principles from Modern Portfolio Theory. Users can customize the configuration, analyze results, and potentially extend the project with additional strategies or improvements.
