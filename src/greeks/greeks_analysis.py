import streamlit as st
import pandas as pd
from src.greeks.calculate_greeks import calculate_greeks_black_scholes, calculate_greeks_monte_carlo
from src.utils.user_input import UserInput

def get_user_parameters():
    user_input = UserInput()
    user_input.gather_input()
    return user_input.get_parameters()

def analyze_greeks(parameters):
    
    # Extract parameters
    S = parameters['underlying_price']
    K = parameters['strike_price']
    T = parameters['time_to_expiration']
    r = parameters['risk_free_rate']
    sigma = parameters['volatility']
    q = parameters['dividend_yield']
    option_type = parameters['option_type']
    num_simulations = parameters['num_simulations']

    # Calculate Greeks using Black-Scholes
    first_order_greeks_bs, second_order_greeks_bs = calculate_greeks_black_scholes(
        option_type, S, K, T, r, sigma, q)

    # Calculate Greeks using Monte Carlo
    first_order_greeks_mc, second_order_greeks_mc = calculate_greeks_monte_carlo(
        option_type, S, K, T, r, sigma, q, num_simulations)
    
    # Create a DataFrame to compare the first-order Greeks
    comparison_first_order_df = pd.DataFrame({
        'Greek': ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho'],
        'Black-Scholes': [first_order_greeks_bs['Delta'], first_order_greeks_bs['Gamma'], first_order_greeks_bs['Theta'], first_order_greeks_bs['Vega'], first_order_greeks_bs['Rho']],
        'Monte Carlo': [first_order_greeks_mc['Delta'], first_order_greeks_mc['Gamma'], first_order_greeks_mc['Theta'], first_order_greeks_mc['Vega'], first_order_greeks_mc['Rho']]
    })

    # Set the Greek column as the index for first-order Greeks
    comparison_first_order_df.set_index('Greek', inplace=True)

    # Round the values to 2 decimal places
    comparison_first_order_df = comparison_first_order_df.round(2)

    # Display the first-order Greeks DataFrame
    st.subheader("First-Order Greeks Comparison")
    st.dataframe(comparison_first_order_df) 
    st.markdown("---")

    # Create a DataFrame to compare the second-order Greeks
    comparison_second_order_df = pd.DataFrame({
        'Greek': ['Charm', 'Speed', 'Color', 'Zomma', 'Veta', 'Volga'],
        'Black-Scholes': [second_order_greeks_bs['Charm'], second_order_greeks_bs['Speed'], second_order_greeks_bs['Color'], second_order_greeks_bs['Zomma'], second_order_greeks_bs['Veta'], second_order_greeks_bs['Volga']],
        'Monte Carlo': [second_order_greeks_mc['Charm'], second_order_greeks_mc['Speed'], second_order_greeks_mc['Color'], second_order_greeks_mc['Zomma'], second_order_greeks_mc['Veta'], second_order_greeks_mc['Volga']]
    })

    # Set the Greek column as the index for second-order Greeks
    comparison_second_order_df.set_index('Greek', inplace=True)

    # Round the values to 2 decimal places
    comparison_second_order_df = comparison_second_order_df.round(2)

    # Display the second-order Greeks DataFrame
    st.subheader("Second-Order Greeks Comparison")
    st.dataframe(comparison_second_order_df)
    st.markdown("---")

    return parameters