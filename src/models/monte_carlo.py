import numpy as np
from src.utils.user_input import UserInput

def monte_carlo_simulation(option_type, S, K, T, r, sigma, q=0, num_simulations=10000, random_numbers=None):

    # Input validation
    if S <= 0:
        raise ValueError("Underlying asset price (S) must be greater than zero.")
    if K <= 0:
        raise ValueError("Strike price (K) must be greater than zero.")
    if T <= 0:
        raise ValueError("Time to expiration (T) must be greater than zero.")
    if sigma < 0:
        raise ValueError("Volatility (sigma) must be non-negative.")
    if num_simulations <= 0:
        raise ValueError("Number of simulations must be a positive integer.")
    if option_type not in ["Call", "Put"]:
        raise ValueError("Invalid option type. Use 'Call' or 'Put'.")

    # Simulate price paths
    dt = T / 365  # Daily time steps
    prices = np.zeros(num_simulations)

    # Generate or use provided random numbers
    if random_numbers is None:
        random_numbers = np.random.normal(size=(num_simulations, 365))
    
    # Ensure random_numbers has correct shape
    if random_numbers.shape != (num_simulations, 365):
        raise ValueError(f"random_numbers must have shape ({num_simulations}, 365)")

    for i in range(num_simulations):
        # Simulate the price path using geometric Brownian motion
        # Using provided random numbers for consistency
        price_path = S * np.exp(np.cumsum(
            (r - q - 0.5 * sigma ** 2) * dt + 
            sigma * np.sqrt(dt) * random_numbers[i]
        ))
        prices[i] = price_path[-1]  # Final price at expiration

    # Calculate option payoffs
    if option_type == "Call":
        payoffs = np.maximum(prices - K, 0)
    else:  # Put
        payoffs = np.maximum(K - prices, 0)

    # Discount payoffs back to present value
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    return option_price

def calculate_monte_carlo():
    
    # Create an instance of UserInput to gather parameters
    user_input = UserInput()
    user_input.gather_input(prefix="monte_carlo_")
    parameters = user_input.get_parameters()

    # Extract parameters
    underlying_price = parameters['underlying_price']
    strike_price = parameters['strike_price']
    time_to_expiration = parameters['time_to_expiration']  # Already in years
    risk_free_rate = parameters['risk_free_rate']  # As a decimal
    volatility = parameters['volatility']  # As a decimal
    dividend_yield = parameters['dividend_yield']  # As a decimal
    option_type = parameters['option_type']
    num_simulations = parameters['num_simulations']  # Accessing num_simulations from user input

    # Perform Monte Carlo simulation
    option_price = monte_carlo_simulation(option_type, underlying_price, strike_price, time_to_expiration, risk_free_rate, volatility, dividend_yield, num_simulations)
    return option_price 