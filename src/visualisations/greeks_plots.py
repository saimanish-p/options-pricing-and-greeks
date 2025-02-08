import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from src.greeks.calculate_greeks import calculate_greeks_black_scholes, calculate_greeks_monte_carlo

def plot_first_order_greek(greek, S, K, T, r, sigma, option_type="Call", q=0, num_simulations=10000):

    # Calculate Greeks
    first_order_bs, _ = calculate_greeks_black_scholes(option_type, S, K, T, r, sigma, q)
    first_order_mc, _ = calculate_greeks_monte_carlo(option_type, S, K, T, r, sigma, q, num_simulations)
    
    # Prepare data for plotting
    bs_value = first_order_bs[greek]
    mc_value = first_order_mc[greek]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot bars
    width = 0.35
    ax.bar(['Black-Scholes', 'Monte Carlo'], [bs_value, mc_value], width, 
           color=['lightblue', 'orange'])
    
    # Add value labels on top of bars
    for i, v in enumerate([bs_value, mc_value]):
        ax.text(i, v, f'{v:.4f}', ha='center', va='bottom', fontweight='bold')
    
    # Customize plot
    ax.set_title(f'{greek} Comparison ({option_type})')
    ax.set_ylabel(f'{greek} Value')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add percentage difference
    pct_diff = abs(bs_value - mc_value) / abs(bs_value) * 100 if bs_value != 0 else 0
    plt.figtext(0.49, 0.01, f'Difference: {pct_diff:.2f}%', 
                ha='center', va='bottom', fontsize = 12, fontweight= 'bold', style='italic', color='red')
    
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

def plot_second_order_greek(greek, S, K, T, r, sigma, option_type="Call", q=0, num_simulations=10000):

    # Calculate Greeks
    _, second_order_bs = calculate_greeks_black_scholes(option_type, S, K, T, r, sigma, q)
    _, second_order_mc = calculate_greeks_monte_carlo(option_type, S, K, T, r, sigma, q, num_simulations)
    
    # Prepare data for plotting
    bs_value = second_order_bs[greek]
    mc_value = second_order_mc[greek]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot bars
    width = 0.35
    ax.bar(['Black-Scholes', 'Monte Carlo'], [bs_value, mc_value], width,
           color=['lightblue', 'orange'])
    
    # Add value labels on top of bars
    for i, v in enumerate([bs_value, mc_value]):
        ax.text(i, v, f'{v:.4f}', ha='center', va='bottom', fontweight='bold')
    
    # Customize plot
    ax.set_title(f'{greek} Comparison ({option_type})')
    ax.set_ylabel(f'{greek} Value')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add percentage difference
    pct_diff = abs(bs_value - mc_value) / abs(bs_value) * 100 if bs_value != 0 else 0
    plt.figtext(0.49, 0.01, f'Difference: {pct_diff:.2f}%', 
                ha='center', va='bottom', fontsize = 12, fontweight= 'bold', style='italic', color='red')
    
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

def create_volatility_surface(option_type, S, K, T, r, sigma, q):

    # Define Greek types
    greeks = ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']
    
    # Prepare containers for Greeks
    greek_surfaces = {}
    
    # Compute surfaces for each Greek
    for greek in greeks:
        # Dynamically determine parameter ranges
        if greek in ['Delta', 'Gamma', 'Vega']:
            x_param = np.linspace(S * 0.5, S * 1.5, 50)  # Stock prices
            y_param = np.linspace(max(0.01, sigma * 0.5), sigma * 1.5, 50)  # Volatilities
            x_title = 'Stock Price'
            y_title = 'Volatility'
            
            # Calculation function
            def calc_func(x_val, y_val):
                return calculate_greeks_black_scholes(
                    option_type, x_val, K, T, r, y_val, q
                )[0][greek]
        
        elif greek == 'Theta':
            x_param = np.linspace(0.1, T * 2, 50)  # Time to expiration
            y_param = np.linspace(S * 0.5, S * 1.5, 50)  # Stock prices
            x_title = 'Time to Expiration'
            y_title = 'Stock Price'
            
            # Calculation function
            def calc_func(x_val, y_val):
                return calculate_greeks_black_scholes(
                    option_type, y_val, K, x_val, r, sigma, q
                )[0][greek]
        
        elif greek == 'Rho':
            x_param = np.linspace(max(0.01, r * 0.5), r * 1.5, 50)  # Risk-free rates
            y_param = np.linspace(S * 0.5, S * 1.5, 50)  # Stock prices
            x_title = 'Risk-Free Rate'
            y_title = 'Stock Price'
            
            # Calculation function
            def calc_func(x_val, y_val):
                return calculate_greeks_black_scholes(
                    option_type, y_val, K, T, x_val, sigma, q
                )[0][greek]
        
        # Compute Greek values
        greek_values = []
        for y_val in y_param:
            row_values = []
            for x_val in x_param:
                row_values.append(calc_func(x_val, y_val))
            greek_values.append(row_values)
        
        # Store the surface
        greek_surfaces[greek] = {
            'z': greek_values,
            'x': x_param,
            'y': y_param,
            'x_title': x_title,
            'y_title': y_title
        }
    
    # Create base figure
    fig = go.Figure()
    
    # Add initial surface for Delta
    fig.add_trace(
        go.Surface(
            z=greek_surfaces['Delta']['z'],
            x=greek_surfaces['Delta']['x'],
            y=greek_surfaces['Delta']['y'],
            colorscale='Viridis',
            name='Delta Surface'
        )
    )
    
    # Update layout with dropdown menu
    fig.update_layout(
        scene=dict(
            xaxis_title=greek_surfaces['Delta']['x_title'],
            yaxis_title=greek_surfaces['Delta']['y_title'],
            zaxis_title='Delta Value'
        ),
        updatemenus=[
            {
                'buttons': [
                    {'label': greek, 
                     'method': 'update', 
                     'args': [
                         {'z': [greek_surfaces[greek]['z']], 
                          'x': [greek_surfaces[greek]['x']], 
                          'y': [greek_surfaces[greek]['y']], 
                          'name': [f'{greek} Surface']},
                         {
                             'scene.xaxis.title': greek_surfaces[greek]['x_title'],
                             'scene.yaxis.title': greek_surfaces[greek]['y_title'],
                             'scene.zaxis.title': f'{greek} Value'
                         }
                     ]} 
                    for greek in greeks
                ],
                'direction': 'down',
                'showactive': True,
                'x': 0.0,
                'xanchor': 'left',
                'y': 1.1,
                'yanchor': 'top'
            }
        ],
        width=700,
        height=800
    )
    
    return fig

