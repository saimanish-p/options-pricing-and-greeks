import numpy as np
from src.models.black_scholes import black_scholes
from src.models.monte_carlo import monte_carlo_simulation

def calculate_greeks_black_scholes(option_type, S, K, T, r, sigma, q=0):
    
    # Calculate option price for the current price
    price_current = black_scholes(option_type, S, K, T, r, sigma, q)

    # First-order Greeks
    price_up = black_scholes(option_type, S + 0.01, K, T, r, sigma, q)
    price_down = black_scholes(option_type, S - 0.01, K, T, r, sigma, q)
    delta = (price_up - price_down) / 0.02

    gamma = (price_up - 2 * price_current + price_down) / (0.01 ** 2)

    price_t_plus = black_scholes(option_type, S, K, T + 1/365, r, sigma, q)
    theta = (price_t_plus - price_current) * 365  # Annualize

    price_vol_up = black_scholes(option_type, S, K, T, r, sigma + 0.01, q)
    price_vol_down = black_scholes(option_type, S, K, T, r, sigma - 0.01, q)
    vega = (price_vol_up - price_vol_down) / 0.02

    price_r_up = black_scholes(option_type, S, K, T, r + 0.01, sigma, q)
    price_r_down = black_scholes(option_type, S, K, T, r - 0.01, sigma, q)
    rho = (price_r_up - price_r_down) / 0.02

    # Second-order Greeks
    charm = (black_scholes(option_type, S, K, T - 1/365, r, sigma, q) - price_current) / (1/365)
    speed = (black_scholes(option_type, S + 0.01, K, T, r, sigma, q) - 2 * price_current + black_scholes(option_type, S - 0.01, K, T, r, sigma, q)) / (0.01 ** 2)
    color = (black_scholes(option_type, S, K, T - 1/365, r, sigma, q) - price_current) / (1/365)
    zomma = (price_vol_up - 2 * price_current + price_vol_down) / (0.01 ** 2)
    veta = (black_scholes(option_type, S, K, T + 1/365, r, sigma, q) - price_current) / (1/365)
    volga = (price_vol_up - 2 * price_current + price_vol_down) / (0.01 ** 2)

    # Return the Greeks as separate dictionaries
    first_order_greeks = {
        'Delta': delta,
        'Gamma': gamma,
        'Theta': theta,
        'Vega': vega,
        'Rho': rho
    }

    second_order_greeks = {
        'Charm': charm,
        'Speed': speed,
        'Color': color,
        'Zomma': zomma,
        'Veta': veta,
        'Volga': volga
    }

    return first_order_greeks, second_order_greeks

def calculate_greeks_monte_carlo(option_type, S, K, T, r, sigma, q=0, num_simulations=10000):

    # Generate random numbers once to use across all simulations
    random_numbers = np.random.normal(size=(num_simulations, 365))
    # Calculate option price for the current price
    price_current = monte_carlo_simulation(option_type, S, K, T, r, sigma, q, num_simulations, random_numbers)
    
    # Step sizes for finite differences
    h_s = S * 0.001      # 0.1% of spot price
    h_v = sigma * 0.01  # 1% of volatility
    h_r = max(0.001, r * 0.001)  # 0.1% of rate
    h_t = 1/12          # One month instead of one day

    # First-order Greeks
    # Delta calculation
    price_up = monte_carlo_simulation(option_type, S + h_s, K, T, r, sigma, q, num_simulations, random_numbers)
    price_down = monte_carlo_simulation(option_type, S - h_s, K, T, r, sigma, q, num_simulations, random_numbers)
    delta = (price_up - price_down) / (2 * h_s)

    # Gamma calculation
    gamma = (price_up - 2 * price_current + price_down) / (h_s ** 2)

    # Theta calculation (forward difference to avoid negative time)
    price_t_plus = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma, q, num_simulations, random_numbers)
    theta = (price_t_plus - price_current) / h_t

    # Vega calculation
    price_vol_up = monte_carlo_simulation(option_type, S, K, T, r, sigma + h_v, q, num_simulations, random_numbers)
    price_vol_down = monte_carlo_simulation(option_type, S, K, T, r, sigma - h_v, q, num_simulations, random_numbers)
    vega = (price_vol_up - price_vol_down) / (2 * h_v)

    # Rho calculation
    price_r_up = monte_carlo_simulation(option_type, S, K, T, r + h_r, sigma, q, num_simulations, random_numbers)
    price_r_down = monte_carlo_simulation(option_type, S, K, T, r - h_r, sigma, q, num_simulations, random_numbers)
    rho = (price_r_up - price_r_down) / (2 * h_r)

    # Second-order Greeks using same random numbers
    
    # Charm (rate of change of delta with respect to time)
    price_up_dt = monte_carlo_simulation(option_type, S + h_s, K, T + h_t, r, sigma, q, num_simulations, random_numbers)
    price_down_dt = monte_carlo_simulation(option_type, S - h_s, K, T + h_t, r, sigma, q, num_simulations, random_numbers)
    delta_dt = (price_up_dt - price_down_dt) / (2 * h_s)
    charm = (delta_dt - delta) / h_t

    # Speed (rate of change of gamma with respect to stock price)
    price_up_2h = monte_carlo_simulation(option_type, S + 2*h_s, K, T, r, sigma, q, num_simulations, random_numbers)
    price_down_2h = monte_carlo_simulation(option_type, S - 2*h_s, K, T, r, sigma, q, num_simulations, random_numbers)
    gamma_up = (price_up_2h - 2*price_up + price_current) / (h_s ** 2)
    gamma_down = (price_current - 2*price_down + price_down_2h) / (h_s ** 2)
    speed = (gamma_up - gamma_down) / (2 * h_s)

    # Color (rate of change of gamma with respect to time)
    price_up_dt = monte_carlo_simulation(option_type, S + h_s, K, T + h_t, r, sigma, q, num_simulations, random_numbers)
    price_down_dt = monte_carlo_simulation(option_type, S - h_s, K, T + h_t, r, sigma, q, num_simulations, random_numbers)
    price_dt = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma, q, num_simulations, random_numbers)
    gamma_dt = (price_up_dt - 2*price_dt + price_down_dt) / (h_s ** 2)
    color = (gamma_dt - gamma) / h_t

    # Zomma (rate of change of gamma with respect to volatility)
    price_up_vol = monte_carlo_simulation(option_type, S + h_s, K, T, r, sigma + h_v, q, num_simulations, random_numbers)
    price_down_vol = monte_carlo_simulation(option_type, S - h_s, K, T, r, sigma + h_v, q, num_simulations, random_numbers)
    gamma_up_vol = (price_up_vol - 2*price_vol_up + price_down_vol) / (h_s ** 2)
    gamma_down_vol = (price_up - 2*price_current + price_down) / (h_s ** 2)
    zomma = (gamma_up_vol - gamma_down_vol) / (2 * h_v)

    # Veta (rate of change of vega with respect to time)
    price_vol_up_dt = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma + h_v, q, num_simulations, random_numbers)
    price_vol_down_dt = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma - h_v, q, num_simulations, random_numbers)
    vega_dt = (price_vol_up_dt - price_vol_down_dt) / (2 * h_v)
    veta = (vega_dt - vega) / h_t

    # Volga (rate of change of vega with respect to volatility)
    price_2vol_up = monte_carlo_simulation(option_type, S, K, T, r, sigma + 2*h_v, q, num_simulations, random_numbers)
    price_2vol_down = monte_carlo_simulation(option_type, S, K, T, r, sigma - 2*h_v, q, num_simulations, random_numbers)
    vega_up = (price_2vol_up - price_vol_up) / h_v
    vega_down = (price_vol_down - price_2vol_down) / h_v
    volga = (vega_up - vega_down) / (2 * h_v)

    # Return the Greeks as separate dictionaries
    first_order_greeks = {
        'Delta': delta,
        'Gamma': gamma,
        'Theta': theta,
        'Vega': vega,
        'Rho': rho
    }
    second_order_greeks = {
        'Charm': charm,
        'Speed': speed,
        'Color': color,
        'Zomma': zomma,
        'Veta': veta,
        'Volga': volga
    }
    return first_order_greeks, second_order_greeks