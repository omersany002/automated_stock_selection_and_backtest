""""
This file uses Modern Portfolio Theory to 
return optimal investment weight in stocks.
"""
from scipy.optimize import minimize
import pandas as pd
import numpy as np

def get_data(tickers, price_df, end):
    """Calculates mean return and covariance matrix of tickers"""
    begin = end - pd.DateOffset(years=3)
    df = price_df[price_df['TICKER'].isin(tickers)].copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df[(df['date'] <= end) & (df['date'] >= begin)]
    pivoted_df = df.pivot_table(index='date', columns='TICKER', values='PRC')
    # Drop tickers that do not have price data
    pivoted_df.dropna(axis=1, how='all', inplace=True)
    returns = pivoted_df.bfill().ffill().pct_change().dropna()
    returns = returns.replace([np.inf, -np.inf, np.nan],0)
    mean_return = returns.mean()
    cov_matrix = returns.cov()
    return mean_return, cov_matrix

def optimize_portfolio_variance(mean_return, cov_matrix):
    """Returns a series of tickers and their optimal weights using mean variance"""
    num_stocks = len(mean_return)
    init_guess = np.repeat(1/num_stocks, num_stocks)
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0, 1) for _ in range(num_stocks))

    # The optimization function (portfolio variance)
    def portfolio_variance(weights, cov_matrix):
        return weights.T @ cov_matrix @ weights

    # Minimize the portfolio variance
    optimal_weights = minimize(portfolio_variance, init_guess,
                               args=(cov_matrix,), method='SLSQP',
                               bounds=bounds, constraints=constraints)

    # Return the optimal weights as a series
    return optimal_weights

def optimize_portfolio_sharpe(mean_ret, cov):
    """Optimal sharpe ratio portfolio weights."""
    const = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for x in range(len(mean_ret)))
    init_guess = np.array(len(mean_ret) * [1. / len(mean_ret)])

    def sharpe_ratio(weights, mean_ret, cov):
        """Sharpe Ratio Calculation Function"""
        return -np.dot(weights, mean_ret) / np.sqrt(np.dot(weights.T, np.dot(cov * 252, weights)))

    result = minimize(sharpe_ratio, init_guess, args=(mean_ret, cov),\
                        method='SLSQP', bounds=bounds, constraints=const)
    return result

def get_optimal_weights(tickers, price_df, time, port_type):
    """Executes the data function and the optimization function to return
    the optimal weights in the form of a dataframe.
    """
    mean_return, cov_matrix = get_data(tickers, price_df, time)
    if port_type == 'var':
        result = optimize_portfolio_variance(mean_return, cov_matrix)
        return pd.Series(result.x, index = tickers)
    result = optimize_portfolio_sharpe(mean_return, cov_matrix)
    return pd.Series(result.x, index = tickers)
