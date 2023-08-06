"""
This package provides functions for implementing the Almgren-Chriss model for optimal execution of portfolio
transactions.

Modules
-------
cost
    Provides functions for calculating the expectation, variance and value-at-risk of the cost of trading.
decay_rate
    Provides functions for calculating the trade decay rate.
trade
    Provides functions for calculating the trading trajectory and the list of trades.

Functions
---------
cost_expectation
    Calculate the expected cost of trading.
cost_variance
    Calculate the variance of the cost of trading.
value_at_risk
    Calculate the value-at-risk of the cost of trading.
decay_rate
    Calculate the trade decay rate.
trade_trajectory
    Calculate the trading trajectory.
trade_list
    Calculate the list of trades.
"""
from .cost import cost_expectation, cost_variance, value_at_risk
from .decay_rate import kappa as decay_rate
from .trade import trade_trajectory, trade_list
