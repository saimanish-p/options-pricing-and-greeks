import streamlit as st

class UserInput:
    def __init__(self):
        self.parameters = {}

    def gather_input(self, prefix=''):
        
        # Select option type (Call or Put) with a unique key
        option_type = st.sidebar.selectbox(
            "Select the option type:", 
            ("Call", "Put"), 
            key=f"{prefix}option_type",
            help="Call: right to buy at strike price; Put: right to sell at strike price"
        )
        self.parameters['option_type'] = option_type

        # Get underlying asset price with a default value and a unique key
        self.parameters['underlying_price'] = st.sidebar.number_input(
            "Enter the underlying asset price:", 
            value=105.0, 
            step=1.0, 
            key=f"{prefix}underlying_price",
            help="Current market price of the underlying asset (stock, index, etc.)"
        )

        # Get strike price with a default value and a unique key
        self.parameters['strike_price'] = st.sidebar.number_input(
            "Enter the strike price:", 
            value=100.0, 
            step=1.0, 
            key=f"{prefix}strike_price",
            help="Price at which the option can be exercised"
        )

        # Get time to expiration in years with a default value and a unique key
        self.parameters['time_to_expiration'] = st.sidebar.number_input(
            "Enter the time to expiration (in years):", 
            value=1.0, 
            step=0.50, 
            key=f"{prefix}time_to_expiration",
            help="Time until option expires (0.5 = 6 months, 1.0 = 1 year)"
        )

        # Get risk-free interest rate (as a percentage) with a default value and a unique key
        self.parameters['risk_free_rate'] = st.sidebar.number_input(
            "Enter the risk-free interest rate (as a percentage):", 
            value=5.0, 
            step=0.50, 
            key=f"{prefix}risk_free_rate",
            help="Annual rate for risk-free investments (enter 5 for 5% not 0.5); affects time value of options"
        ) / 100

        # Get volatility (as a percentage) with a default value and a unique key
        self.parameters['volatility'] = st.sidebar.number_input(
            "Enter the volatility (as a percentage):", 
            value=20.0, 
            step=1.0, 
            key=f"{prefix}volatility",
            help="Expected price fluctuation magnitude (enter 20 for 20%, not 0.20); higher values increase option premiums"
        ) / 100

        # Get dividend yield (optional, for models that require it) with a default value and a unique key
        self.parameters['dividend_yield'] = st.sidebar.number_input(
            "Enter the dividend yield (as a percentage, enter 0 if none):", 
            value=1.5, 
            step=0.50, 
            key=f"{prefix}dividend_yield",
            help="Annual dividend percentage (enter 1.5 for 1.5%, not 0.015); reduces call values, increases put values"
        ) / 100

        # Get number of simulations for Monte Carlo with a default value and a unique key
        self.parameters['num_simulations'] = int(st.sidebar.number_input(
            "Enter the number of simulations for Monte Carlo:", 
            value=10000, 
            step=500, 
            key=f"{prefix}num_simulations",
            help="Number of price paths to simulate; higher values improve accuracy but slow performance"
        ))

        # Add a unique key to the button
        if st.sidebar.button("Submit", key=f"{prefix}submit_button"):
            st.success("Parameters submitted successfully!")
            st.json(self.parameters)

    def get_parameters(self):
        return self.parameters