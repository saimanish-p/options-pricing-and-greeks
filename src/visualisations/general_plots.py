import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from src.models.black_scholes import black_scholes
from src.models.monte_carlo import monte_carlo_simulation
import time 

def plot_price_comparison(S, K, T, r, sigma, option_type="Call", q=0, num_simulations=10000):
    bs_price = black_scholes(option_type, S, K, T, r, sigma, q)
    mc_price = monte_carlo_simulation(option_type, S, K, T, r, sigma, q, num_simulations)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(['Black-Scholes', 'Monte Carlo'], [bs_price, mc_price], 
                 color=['lightblue', 'orange'])
    
    # Add data labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_title(f'Option Price Comparison ({option_type})')
    ax.set_ylabel('Option Price')
    
    # Add percentage difference
    pct_diff = abs(bs_price - mc_price) / bs_price * 100
    plt.figtext(0.57, 0.01, f'Difference: {pct_diff:.2f}%', ha='right', va='bottom', style='italic', fontweight='bold', color='red')
    
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

def plot_volatility_sensitivity(S, K, T, r, option_type="Call", q=0, num_simulations=10000):
    volatilities = np.linspace(0.1, 1.0, 10)  # Volatility range from 10% to 100%
    bs_prices = [black_scholes(option_type, S, K, T, r, sigma, q) for sigma in volatilities]
    mc_prices = [monte_carlo_simulation(option_type, S, K, T, r, sigma, q, num_simulations) for sigma in volatilities]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(volatilities, bs_prices, label='Black-Scholes', marker='o')
    ax.plot(volatilities, mc_prices, label='Monte Carlo', marker='x')
    ax.set_title(f'Volatility Sensitivity ({option_type})')
    ax.set_xlabel('Volatility (σ)')
    ax.set_ylabel('Option Price')
    ax.legend()
    ax.grid()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

def plot_time_to_expiration_sensitivity(S, K, r, sigma, option_type="Call", q=0, num_simulations=10000):
    times = np.linspace(0.01, 1.0, 10)  # Time to expiration from 1 day to 1 year
    bs_prices = [black_scholes(option_type, S, K, T, r, sigma, q) for T in times]
    mc_prices = [monte_carlo_simulation(option_type, S, K, T, r, sigma, q, num_simulations) for T in times]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(times, bs_prices, label='Black-Scholes', marker='o')
    ax.plot(times, mc_prices, label='Monte Carlo', marker='x')
    ax.set_title(f'Time to Expiration Sensitivity ({option_type})')
    ax.set_xlabel('Time to Expiration (Years)')
    ax.set_ylabel('Option Price')
    ax.legend()
    ax.grid()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

def plot_strike_price_sensitivity(S, T, r, sigma, option_type="Call", q=0, num_simulations=10000):
    strike_prices = np.linspace(S * 0.5, S * 1.5, 10)  # Strike prices from 50% to 150% of S
    bs_prices = [black_scholes(option_type, S, K, T, r, sigma, q) for K in strike_prices]
    mc_prices = [monte_carlo_simulation(option_type, S, K, T, r, sigma, q, num_simulations) for K in strike_prices]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(strike_prices, bs_prices, label='Black-Scholes', marker='o')
    ax.plot(strike_prices, mc_prices, label='Monte Carlo', marker='x')
    ax.set_title(f'Strike Price Sensitivity ({option_type})')
    ax.set_xlabel('Strike Price (K)')
    ax.set_ylabel('Option Price')
    ax.legend()
    ax.grid()
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")

def animate_monte_carlo_simulation(option_type, S, K, T, r, sigma, q=0):

    st.subheader("Monte Carlo Option Price Path Simulation")
    col1, col2 = st.columns(2)
    
    with col1:
        num_paths = st.slider("Number of paths", 1, 50, 10)
    with col2:
        if st.button("Generate New Paths"):
            np.random.seed(int(time.time()))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Calculate time steps backwards (from T to 0)
    dt = T / 365
    days_to_expiry = np.arange(365, -1, -1)  # From 365 to 0
    time_to_expiry = days_to_expiry * dt  # Convert to years
    
    # Plot option price paths
    for _ in range(num_paths):
        # Generate stock price path
        random_walks = np.random.normal(size=365)
        stock_prices = np.zeros(366)
        stock_prices[0] = S
        
        # Generate full stock price path
        for t in range(365):
            stock_prices[t + 1] = stock_prices[t] * np.exp(
                (r - q - 0.5 * sigma**2) * dt + 
                sigma * np.sqrt(dt) * random_walks[t]
            )
        
        # Calculate option prices along the path
        option_prices = np.zeros(366)
        for t in range(366):
            if t == 365:  # At expiration
                if option_type == "Call":
                    option_prices[t] = max(stock_prices[t] - K, 0)
                else:
                    option_prices[t] = max(K - stock_prices[t], 0)
            else:
                # Use Black-Scholes for option price at each point
                option_prices[t] = black_scholes(
                    option_type, stock_prices[t], K, time_to_expiry[t], 
                    r, sigma, q
                )
        
        # Plot option price path
        ax.plot(days_to_expiry, option_prices, alpha=0.4)
    
    # Add reference lines
    initial_price = black_scholes(option_type, S, K, T, r, sigma, q)
    ax.plot(365, initial_price, 'go', label='Starting Option Price')
    
    # Customize plot
    ax.set_title(f'Monte Carlo Option Price Paths ({option_type})')
    ax.set_xlabel('Days Until Expiration')
    ax.set_ylabel('Option Price')
    
    # Set axis limits
    ax.set_xlim(365, 0)  
    ax.set_ylim(bottom=0)  
    
    # Add grid and legend
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add statistics
    stats_text = (
        f'Parameters:\n'
        f'S₀: ${S:.2f}\n'
        f'K: ${K:.2f}\n'
        f'σ: {sigma*100:.1f}%\n'
        f'T: {T:.2f}yr\n'
        f'r: {r*100:.1f}%\n'
        f'Initial Price: ${initial_price:.2f}'
    )
    plt.text(0.98, 0.98, stats_text,
             transform=ax.transAxes,
             fontsize=10,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    st.pyplot(fig)
    plt.close(fig)
    
    st.markdown("---")

def plot_histogram_of_simulated_prices(option_type, S, K, T, r, sigma, q=0, num_simulations=10000):

    dt = T / 365
    option_prices = np.zeros(num_simulations)

    for i in range(num_simulations):
        random_walks = np.random.normal(0, 1, size=365)
        price_path = S * np.exp(np.cumsum((r - q - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * random_walks))        
        final_stock_price = price_path[-1]
        
        if option_type == "Call":
            payoff = max(final_stock_price - K, 0)
        else:  # Put
            payoff = max(K - final_stock_price, 0)
        
        option_prices[i] = np.exp(-r * T) * payoff

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Calculate statistics for setting x-axis limits
    mean_price = np.mean(option_prices)
    std_price = np.std(option_prices)

    # Plot histogram with focused range
    ax.hist(option_prices, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    
    # Add vertical lines
    ax.axvline(x=mean_price, color='red', linestyle='--', label=f'Mean Price: {mean_price:.2f}')
    bs_price = black_scholes(option_type, S, K, T, r, sigma, q)
    ax.axvline(x=bs_price, color='green', linestyle='--', label=f'Black-Scholes Price: {bs_price:.2f}')

    # Set x-axis limits to show the full distribution
    ax.set_xlim(0, np.percentile(option_prices, 99))  
        
    # Labels and title
    ax.set_title(f'Monte Carlo Simulated {option_type} Option Price Distribution ({num_simulations:,} paths)')
    ax.set_xlabel('Option Price')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add summary statistics
    stats_text = (f'Statistics:\n'
                 f'Mean: {mean_price:.4f}\n'
                 f'Std Dev: {std_price:.4f}\n'
                 f'Min: {np.min(option_prices):.4f}\n'
                 f'Max: {np.max(option_prices):.4f}')
    plt.figtext(0.71, 0.62, stats_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("---")
