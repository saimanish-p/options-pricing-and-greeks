import numpy as np
from utils.user_input import UserInput

def monte_carlo_simulation(option_type, S, K, T, r, sigma, q=0, num_simulations=10000):
    """
    Perform a Monte Carlo simulation to estimate the option price.
    
    Parameters:
    - option_type: 'Call' or 'Put'
    - S: Underlying asset price
    - K: Strike price
    - T: Time to expiration (in years)
    - r: Risk-free interest rate (as a decimal)
    - sigma: Volatility (as a decimal)
    - q: Dividend yield (as a decimal, default is 0)
    - num_simulations: Number of simulated paths
    
    Returns:
    - Estimated option price
    """
    # Simulate price paths
    dt = T / 365  # Daily time steps
    prices = np.zeros(num_simulations)

    for i in range(num_simulations):
        # Simulate the price path using geometric Brownian motion
        price_path = S * np.exp(np.cumsum((r - q - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.normal(size=365)))
        prices[i] = price_path[-1]  # Final price at expiration

    # Calculate option payoffs
    if option_type == "Call":
        payoffs = np.maximum(prices - K, 0)
    elif option_type == "Put":
        payoffs = np.maximum(K - prices, 0)
    else:
        raise ValueError("Invalid option type. Use 'Call' or 'Put'.")

    # Discount payoffs back to present value
    option_price = np.exp(-r * T) * np.mean(payoffs)
    return option_price

def calculate_monte_carlo():
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

    # Perform Monte Carlo simulation
    option_price = monte_carlo_simulation(option_type, underlying_price, strike_price, time_to_expiration, risk_free_rate, volatility, dividend_yield)

    # Display results
    print(f"{option_type} Option Price (Monte Carlo): {option_price}")