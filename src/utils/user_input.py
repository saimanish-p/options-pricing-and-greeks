import streamlit as st

class UserInput:
    def __init__(self):
        self.parameters = {}

    def gather_input(self):
        """
        Gather user inputs for options pricing models using Streamlit.
        """
        st.title("Options Pricing Model Input")

        # Select option type (Call or Put)
        option_type = st.selectbox("Select the option type:", ("Call", "Put"))
        self.parameters['option_type'] = option_type

        # Get underlying asset price
        self.parameters['underlying_price'] = st.number_input("Enter the underlying asset price:", value=0.0, step=0.01)

        # Get strike price
        self.parameters['strike_price'] = st.number_input("Enter the strike price:", value=0.0, step=0.01)

        # Get time to expiration in years
        self.parameters['time_to_expiration'] = st.number_input("Enter the time to expiration (in years):", value=0.0, step=0.01)

        # Get risk-free interest rate (as a percentage)
        self.parameters['risk_free_rate'] = st.number_input("Enter the risk-free interest rate (as a percentage):", value=0.0, step=0.01) / 100

        # Get volatility (as a percentage)
        self.parameters['volatility'] = st.number_input("Enter the volatility (as a percentage):", value=0.0, step=0.01) / 100

        # Get dividend yield (optional, for models that require it)
        self.parameters['dividend_yield'] = st.number_input("Enter the dividend yield (as a percentage, enter 0 if none):", value=0.0, step=0.01) / 100

        if st.button("Submit"):
            st.success("Parameters submitted successfully!")
            st.json(self.parameters)  # Display the parameters for confirmation

    def get_parameters(self):
        """Return the gathered parameters."""
        return self.parameters