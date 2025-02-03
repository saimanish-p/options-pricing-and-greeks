import numpy as np
from scipy.stats import norm
from utils.user_input import UserInput

def black_scholes(option_type, S, K, T, r, sigma, q=0):
    """
    Calculate the Black-Scholes option price.
    
    Parameters:
    - option_type: 'Call' or 'Put'
    - S: Underlying asset price
    - K: Strike price
    - T: Time to expiration (in years)
    - r: Risk-free interest rate (as a decimal)
    - sigma: Volatility (as a decimal)
    - q: Dividend yield (as a decimal, default is 0)
    
    Returns:
    - Option price
    """
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
    user_input.gather_input()
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

    # Display results
    print(f"{option_type} Option Price: {option_price}")