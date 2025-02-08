# Importing functions from general_plots
from src.visualisations.general_plots import (
    plot_price_comparison,
    plot_volatility_sensitivity,
    plot_time_to_expiration_sensitivity,
    plot_strike_price_sensitivity,
    animate_monte_carlo_simulation,
    plot_histogram_of_simulated_prices
)

# Importing functions from greeks_plots
from src.visualisations.greeks_plots import (
    plot_first_order_greek,
    plot_second_order_greek,
    create_volatility_surface,
)

# Importing styling functions
from .styling import render_header

# Optionally, you can define the __all__ variable to specify what is exported
__all__ = [
    'plot_price_comparison',
    'plot_volatility_sensitivity',
    'plot_time_to_expiration_sensitivity',
    'plot_strike_price_sensitivity',
    'animate_monte_carlo_simulation',
    'plot_histogram_of_simulated_prices',
    'plot_first_order_greek',
    'plot_second_order_greek',
    'create_volatility_surface',
    'render_header'
]