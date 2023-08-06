"""
This module provides functions for calculating the expected cost and variance of the cost of trading in the
Almgren-Chriss model.

Functions
----------
cost_expectation
    Calculate the expected cost of trading.
cost_variance
    Calculate the variance of the cost of trading.
"""
import math

import numpy as np
from scipy.stats import norm

from .decay_rate import kappa, tilde_tau


__all__ = ['cost_expectation', 'cost_variance', 'value_at_risk']


def cost_expectation(lambda_: float, tau: float, sigma: float, gamma: float, eta: float, epsilon: float,
                     X: float, T: float) -> np.ndarray:
    r"""
    Compute the expected cost of trading in the Almgren-Chriss model.

    .. math:: E(X) = \frac{1}{2}\gamma X^2+\epsilon X+\tilde{\eta}X^2\frac{\tanh(\frac{1}{2}\kappa\tau)\big(\tau\sinh(2\kappa T) + 2T\sinh(\kappa\tau) \big)}{2\tau^2\sinh^2(\kappa T)}

    Parameters
    ----------
    lambda_ : float
        Risk tolerance
    tau : float
        Interval between trades
    sigma : float
        Volatility
    gamma : float
        Permanent impact slope
    eta : float
        Temporary impact slope
    epsilon: float
        Temporary impact intercept
    X : float
        Total number of shares
    T : float
        Trading duration

    Returns
    -------
    float
        The expected cost of trading
    """
    kappa_ = kappa(lambda_, tau, sigma, gamma, eta)
    a = math.tanh(kappa_ * tau / 2) * (tau * math.sinh(2 * kappa_ * T) + 2 * T * math.sinh(kappa_ * tau))
    b = 2 * tau ** 2 * math.sinh(kappa_ * T) ** 2
    return ((gamma * X ** 2) / 2
            + epsilon * X
            + tilde_tau(lambda_, tau, sigma, gamma, eta) * X ** 2 * (a / b))


def cost_variance(lambda_: float, tau: float, sigma: float, gamma: float, eta: float,
                  X: float, T: float) -> np.ndarray:
    r"""
    Compute the variance of the cost of trading in the Almgren-Chriss model.

    .. math:: V(X) = \frac{1}{2}\sigma^2X^2\frac{\tau\sinh(\kappa T) \cosh(\kappa(T-\tau))-T\sinh(\kappa\tau)}{\sinh^2(\kappa T)\sinh(\kappa\tau)}

    Parameters
    ----------
    lambda_ : float
        Risk tolerance
    tau : float
        Interval between trades
    sigma : float
        Volatility
    gamma : float
        Permanent impact slope
    eta : float
        Temporary impact slope
    X : float
        Total number of shares
    T : float
        Trading duration

    Returns
    -------
    float
        The variance of the cost of trading
    """
    kappa_ = kappa(lambda_, tau, sigma, gamma, eta)
    a = tau * math.sinh(kappa_ * T) * math.cosh(kappa_ * (T - tau)) - T * math.sinh(kappa_ * tau)
    b = math.sinh(kappa_ * T) ** 2 * math.sinh(kappa_ * tau)
    return (sigma ** 2 * X ** 2 / 2) * (a / b)


def value_at_risk(lambda_: float, tau: float, sigma: float, gamma: float, eta: float, epsilon: float,
                  X: float, T: float,
                  probability: float = .95) -> np.ndarray:
    r"""
    Compute the value-at-risk of the cost of trading in the Almgren-Chriss model.

    .. math:: Var_p(x) = E(x) + \lambda_v \sqrt{V(x)}

    Parameters
    ----------
    lambda_ : float
        Risk tolerance
    tau : float
        Interval between trades
    sigma : float
        Volatility
    gamma : float
        Permanent impact slope
    eta : float
        Temporary impact slope
    epsilon: float
        Temporary impact intercept
    X : float
        Total number of shares
    T : float
        Trading duration
    probability : float
        Probability that the cost won't exceed the value-at-risk.

    Returns
    -------
    float
        The value-at-risk of the cost of trading
    """
    E_x = cost_expectation(lambda_, tau, sigma, gamma, eta, epsilon, X, T)
    V_x = cost_variance(lambda_, tau, sigma, gamma, eta, X, T)
    return E_x + norm.ppf(probability) * math.sqrt(V_x)
