import numpy as np
from scipy.stats import norm
from src.utils.user_input import UserInput

def black_scholes(option_type, S, K, T, r, sigma, q=0):
    
    # Input validation
    if S <= 0 or K <= 0 or T <= 0:
        raise ValueError("S, K, and T must be greater than zero.")
    if sigma < 0:
        raise ValueError("Volatility (sigma) must be non-negative.")

    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "Call":
        price = (S * np.exp(-q * T) * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    elif option_type == "Put":
        price = (K * np.exp(-r * T) * norm.cdf(-d2)) - (S * np.exp(-q * T) * norm.cdf(-d1))
    else:
        raise ValueError("Invalid option type. Use 'Call' or 'Put'.")

    return price

def calculate_black_scholes():
    
    # Create an instance of UserInput to gather parameters
    user_input = UserInput()
    user_input.gather_input(prefix="black_scholes_")
    parameters = user_input.get_parameters()

    # Extract parameters
    underlying_price = parameters['underlying_price']
    strike_price = parameters['strike_price']
    time_to_expiration = parameters['time_to_expiration']  # Already in years
    risk_free_rate = parameters['risk_free_rate']  # As a decimal
    volatility = parameters['volatility']  # As a decimal
    dividend_yield = parameters['dividend_yield']  # As a decimal
    option_type = parameters['option_type']

    # Calculate option price using the Black-Scholes formula
    option_price = black_scholes(option_type, underlying_price, strike_price, time_to_expiration, risk_free_rate, volatility, dividend_yield)
    return option_price