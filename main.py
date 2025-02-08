import streamlit as st
import sys
from pathlib import Path

file_path = Path(__file__).parent.resolve()
sys.path.append(str(file_path))

from src.visualisations.general_plots import (
    plot_price_comparison,
    plot_volatility_sensitivity,
    plot_time_to_expiration_sensitivity,
    plot_strike_price_sensitivity,
    animate_monte_carlo_simulation,
    plot_histogram_of_simulated_prices
)
from src.greeks.greeks_analysis import get_user_parameters, analyze_greeks
from src.visualisations.greeks_plots import (
    plot_first_order_greek,
    plot_second_order_greek,
    create_volatility_surface
)
from src.visualisations.styling import render_header

def main():
    # Set page config
    st.set_page_config(
        page_icon="🚀",
        layout='centered'
    )

    render_header()
    
    parameters = get_user_parameters()

    S = parameters['underlying_price']
    K = parameters['strike_price']
    T = parameters['time_to_expiration']
    r = parameters['risk_free_rate']
    sigma = parameters['volatility']
    q = parameters['dividend_yield']
    option_type = parameters['option_type']
    num_simulations = parameters['num_simulations']

    st.header("Option Pricing Model Comparison")
    
    plot_price_comparison(S, K, T, r, sigma, option_type)
    plot_volatility_sensitivity(S, K, T, r, option_type)
    plot_time_to_expiration_sensitivity(S, K, r, sigma, option_type)
    plot_strike_price_sensitivity(S, T, r, sigma, option_type)
    animate_monte_carlo_simulation(option_type, S, K, T, r, sigma, q=q)
    plot_histogram_of_simulated_prices(option_type, S, K, T, r, sigma, q=q, num_simulations=num_simulations)

    st.header("Greeks Analysis")
    analyze_greeks(parameters)  

    st.header("First Order Greeks Plots")
    
    first_order_greeks = ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']
    for greek in first_order_greeks:
        plot_first_order_greek(greek, S, K, T, r, sigma, option_type, q=q, num_simulations=num_simulations)

    st.header("Second Order Greeks Plots")

    second_order_greeks = ['Charm', 'Speed', 'Color', 'Zomma', 'Veta', 'Volga']
    for greek in second_order_greeks:
        plot_second_order_greek(greek, S, K, T, r, sigma, option_type, q=q, num_simulations=num_simulations)
    
    st.subheader(f"Black-Scholes {option_type} Option Greeks: Multi-Dimensional Sensitivity Plots")

    BS_volatility_surface_fig = create_volatility_surface(option_type, S, K, T, r, sigma, q)
    st.plotly_chart(BS_volatility_surface_fig)

if __name__ == "__main__":
    main()