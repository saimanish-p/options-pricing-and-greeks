# Technical Notes

This file is divided into five sections and breaks down all assumptions, limitations, development challenges/solutions,
interpretation of certain visual plots, and lastly the implementation of the Black-Scholes and Monte Carlo models. 

Relevant code blocks are included for additional context and clarity. 

## Model Assumptions

1. **Geometric Brownian Motion for Asset Prices**

```bash
# Simulate the price path using geometric Brownian motion
price_path = S * np.exp(np.cumsum(
    (r - q - 0.5 * sigma ** 2) * dt + 
    sigma * np.sqrt(dt) * random_numbers[i]
))
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Assumption: The underlying asset price follows geometric Brownian motion with constant drift and volatility.

Implications:

- Returns are assumed to be log-normally distributed
- Volatility is constant across all price levels and time periods
- No sudden jumps in asset prices are possible
- The model cannot capture volatility clustering or fat-tailed distributions observed in real markets

2. **Risk-Neutral Valuation Framework**

```bash
# Discount payoffs back to present value
option_price = np.exp(-r * T) * np.mean(payoffs)
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

```bash
price = (S * np.exp(-q * T) * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
```
[Source: black_scholes.py](src/models/black_scholes.py)

Assumption: Markets are complete and arbitrage-free, allowing risk-neutral valuation.

Implications:

- All assets can be perfectly hedged
- Risk preferences don't affect option prices
- The risk-free rate is constant over the option's life
- Continuous hedging is possible without transaction costs

3. **Constant Interest Rates and Dividend Yields**

```bash
d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
```
[Source: black_scholes.py](src/models/black_scholes.py)

Assumption: Interest rates and dividend yields remain constant throughout the option's life.

Implications:

- Cannot model options on assets with time-varying dividend schedules
- Does not account for term structure of interest rates
- Unsuitable for long-term options where rates are likely to change

4. **European Exercise Style Only**

```bash
# Calculate option payoffs
if option_type == "Call":
    payoffs = np.maximum(prices - K, 0)
else:  # Put
    payoffs = np.maximum(K - prices, 0)
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Assumption: Options can only be exercised at expiration (European style)

Implications:

- Cannot price American options that allow early exercise
- May undervalue options on high-dividend stocks where early exercise might be optimal
- Not applicable to Bermudan options with specific exercise dates

5. **Perfect Liquidity and No Transaction Costs**

Assumption: Markets are perfectly liquid with no transaction costs, taxes, or bid-ask spreads.

Implications:

- No modeling of liquidity risk premiums
- Cannot account for the impact of transaction costs on hedging strategies
- May overvalue options in illiquid markets

6. **Normally Distributed Random Variables for Simulation**

```bash
# Generate or use provided random numbers
if random_numbers is None:
    random_numbers = np.random.normal(size=(num_simulations, 365))
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Assumption: Stock price movements can be accurately modeled using normally distributed random variables.

Implications:

- Cannot capture fat-tailed distributions observed in real market returns
- May underestimate the probability of extreme market movements
- Doesn't account for skewness in return distributions

7. **Continuous Differentiability for Greeks Calculation**

```bash
# Delta calculation
price_up = monte_carlo_simulation(option_type, S + h_s, K, T, r, sigma, q, num_simulations, random_numbers)
price_down = monte_carlo_simulation(option_type, S - h_s, K, T, r, sigma, q, num_simulations, random_numbers)
delta = (price_up - price_down) / (2 * h_s)
```
[Source: calculate_greeks.py](src/greeks/calculate_greeks.py)

Assumption: The option price function is smooth and continuously differentiable with respect to all parameters.

Implications:

- Greeks calculations may be inaccurate near discontinuities (e.g., at the strike price for digital options)
- Second-order Greeks especially may be unstable for certain parameter combinations
- Finite difference approximations assume local linearity that may not hold in practice

8. **No Counterparty Risk**

Assumption: There is no risk of default by any counterparty.

Implications:

- Cannot model credit value adjustments (CVA)
- May overvalue options in markets with significant counterparty risk
- Not suitable for credit-sensitive derivatives

9. **Market Parameters Are Known with Certainty**

```bash
def black_scholes(option_type, S, K, T, r, sigma, q=0):
```
[Source: black_scholes.py](src/models/black_scholes.py)

Assumption: All input parameters (especially volatility) are known with certainty.

Implications:

- Does not account for parameter uncertainty
- annot model volatility risk premium
- Assumes perfect calibration to market data

10. **Daily Time Steps Are Sufficient for Accuracy**

```bash
# Simulate price paths
dt = T / 365  # Daily time steps
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Assumption: Daily time steps provide sufficient granularity for accurate simulation.

Implications:

- May not capture intraday price movements that could be relevant for short-term options
- Fixed time step approach may be inefficient for certain option types
- Could miss critical price paths in path-dependent options

## Technical Limitations

1. **Fixed Daily Time Steps in Monte Carlo Simulation**

```bash
# Simulate price paths
dt = T / 365  # Daily time steps
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Reasoning: The Monte Carlo simulation uses a fixed 365 daily time steps regardless of the option's time to expiration. This approach:

- May be inefficient for very short-term options (using too many steps)
- Could be insufficient for accurately capturing price dynamics of long-term options
- Doesn't allow users to adjust time step granularity based on their specific needs
- A more flexible approach would allow variable time steps based on the option's characteristics.

2. **European Options Only**

```bash
# Calculate option payoffs
if option_type == "Call":
    payoffs = np.maximum(prices - K, 0)
else:  # Put
    payoffs = np.maximum(K - prices, 0)

# Discount payoffs back to present value
option_price = np.exp(-r * T) * np.mean(payoffs)
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Reasoning: Both the Monte Carlo and Black-Scholes implementations only consider the final price at expiration, making them suitable only for European options. The code doesn't support:

- American options (early exercise)
- Exotic options (barrier, Asian, lookback, etc.)
- Path-dependent options

This is a fundamental limitation of the current implementation.

3. **Geometric Brownian Motion Assumption**

```bash
# Simulate the price path using geometric Brownian motion
price_path = S * np.exp(np.cumsum(
    (r - q - 0.5 * sigma ** 2) * dt + 
    sigma * np.sqrt(dt) * random_numbers[i]
))
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Reasoning: The model assumes that asset prices follow geometric Brownian motion with constant volatility. This doesn't account for:

- Volatility smiles/skews observed in real markets
- Jump processes in asset prices
- Mean-reverting behavior
- Stochastic volatility

This limitation affects both the pricing accuracy and the Greeks calculations for real-world options.

4. **Numerical Stability in Second-Order Greeks**

```bash
# Veta (rate of change of vega with respect to time)
price_vol_up_dt = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma + h_v, q, num_simulations, random_numbers)
price_vol_down_dt = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma - h_v, q, num_simulations, random_numbers)
vega_dt = (price_vol_up_dt - price_vol_down_dt) / (2 * h_v)
veta = (vega_dt - vega) / h_t
```
[Source: calculate_greeks.py](src/greeks/calculate_greeks.py)

Reasoning: While the implementation uses improved finite difference methods, second-order Greeks still face numerical stability issues, especially for:

- Deep in-the-money or out-of-the-money options
- Very short-term options
- Options with very low volatility

The code uses simple finite differences which can amplify numerical errors when calculating higher-order derivatives.

5. **Fixed Random Number Generation Method**

```bash
# Generate or use provided random numbers
if random_numbers is None:
    random_numbers = np.random.normal(size=(num_simulations, 365))
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

Reasoning: The Monte Carlo simulation uses standard normal random numbers without options for:

- Quasi-random sequences (Sobol, Halton) which can improve convergence
- Antithetic variates for variance reduction
- Control variates or other variance reduction techniques
- Importance sampling for rare events

These advanced sampling techniques could improve accuracy and efficiency.

6. **Limited Handling of Extreme Parameter Values**

```bash
# Step sizes for finite differences
h_s = S * 0.001      # 0.1% of spot price
h_v = sigma * 0.01   # 1% of volatility
h_r = max(0.001, r * 0.001)  # 0.1% of rate
h_t = 1/12           # One month instead of one day
```
[Source: calculate_greeks.py](src/greeks/calculate_greeks.py)

Reasoning: While the code scales step sizes with parameter values, it may still encounter issues with:

- Near-zero interest rates (despite the minimum floor)
- Very high volatility scenarios
- Deep in/out-of-the-money options where delta approaches 0 or 1

These edge cases might require more sophisticated adaptive step sizing.

7. **No Support for Multi-Asset Options**

The entire codebase is designed for single-asset options without support for:

- Spread options
- Basket options
- Rainbow options

This limits the application to more complex derivatives that depend on multiple underlying assets.

## Development Challenges / Implemented Solutions

1. **Monte Carlo Random Number Issue**

In the original implementation, each Greek calculation generated new random paths:

```bash
# Before the fix - each calculation would use different random numbers
price_up = monte_carlo_simulation(option_type, S + h_s, K, T, r, sigma, q, num_simulations)
price_down = monte_carlo_simulation(option_type, S - h_s, K, T, r, sigma, q, num_simulations)
```

This approach introduced significant noise in the calculations, where:

- Greeks showed large deviations from Black-Scholes even though prices matched
- Gamma values were unrealistic (661.46 vs 0.02)
- Delta calculations varied by ±0.3 between runs

```bash
# Generate random numbers once to use across all simulations
random_numbers = np.random.normal(size=(num_simulations, 365))
# Calculate option price for the current price
price_current = monte_carlo_simulation(option_type, S, K, T, r, sigma, q, num_simulations, random_numbers)

# First-order Greeks
# Delta calculation
price_up = monte_carlo_simulation(option_type, S + h_s, K, T, r, sigma, q, num_simulations, random_numbers)
price_down = monte_carlo_simulation(option_type, S - h_s, K, T, r, sigma, q, num_simulations, random_numbers)
```
[Source: calculate_greeks.py](src/greeks/calculate_greeks.py)

The solution ensures that the same random paths are used for all calculations, isolating the effect of changing parameters. 
This is analogous to measuring a slope under identical conditions rather than in changing weather.

The monte_carlo_simulation function was designed to accept external random numbers:

```bash
# Generate or use provided random numbers
if random_numbers is None:
    random_numbers = np.random.normal(size=(num_simulations, 365))
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

2. **Second-Order Greeks Calculation**

The original code used simple finite differences for second-order Greeks:

```bash
# Black-Scholes implementation (problematic)
veta = (black_scholes(option_type, S, K, T + 1/365, r, sigma, q) - price_current) / (1/365)
volga = (price_vol_up - 2 * price_current + price_vol_down) / (0.01 ** 2)
```

This approach led to significant errors:

- Veta showing 14,098.56 vs Black-Scholes 5.33
- Color and Charm completely mismatched

Solution Implementation (for Veta example):
```bash
# Monte Carlo implementation (improved)
# Veta (rate of change of vega with respect to time)
price_vol_up_dt = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma + h_v, q, num_simulations, random_numbers)
price_vol_down_dt = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma - h_v, q, num_simulations, random_numbers)
vega_dt = (price_vol_up_dt - price_vol_down_dt) / (2 * h_v)
veta = (vega_dt - vega) / h_t
```
[Source: calculate_greeks.py](src/greeks/calculate_greeks.py)

The improved implementation correctly calculates mixed derivatives by:
- Computing vega at time $$T$$
- Computing vega at time $$T+h_t$$
- Finding the difference and dividing by the time step

This properly captures how vega changes over time, rather than incorrectly assuming veta is the same as theta.

3. **Step Size Selection**

The original code used fixed step sizes for finite differences:
```bash
# Black-Scholes implementation
price_up = black_scholes(option_type, S + 0.01, K, T, r, sigma, q)
price_down = black_scholes(option_type, S - 0.01, K, T, r, sigma, q)
```

Fixed step sizes (0.01) don't scale with parameter values, leading to:

- Potential numerical instability for very small or large parameter values
- Inconsistent precision across different parameter scales

```bash
# Monte Carlo implementation
# Step sizes for finite differences
h_s = S * 0.001      # 0.1% of spot price
h_v = sigma * 0.01   # 1% of volatility
h_r = max(0.001, r * 0.001)  # 0.1% of rate
h_t = 1/12           # One month instead of one day
```
[Source: calculate_greeks.py](src/greeks/calculate_greeks.py)

The improved implementation scales step sizes with parameter values:

- For stock price: 0.1% of the current price
- For volatility: 1% of current volatility
- For interest rate: 0.1% with a minimum floor
- For time: using a month instead of a day for better numerical stability

This is analogous to using an appropriately sized measuring tool for different objects (millimeter ruler for a pencil, meter stick for a football field).

4. **Time Step Direction**

The Black-Scholes implementation used forward difference for theta:

```bash
price_t_plus = black_scholes(option_type, S, K, T + 1/365, r, sigma, q)
theta = (price_t_plus - price_current) * 365  # Annualize
```

This approach:

- Doesn't match the conventional definition of theta (rate of price decay)
- Could lead to sign confusion in interpretation

```bash
# Monte Carlo implementation
# Theta calculation (forward difference to avoid negative time)
price_t_plus = monte_carlo_simulation(option_type, S, K, T + h_t, r, sigma, q, num_simulations, random_numbers)
theta = (price_t_plus - price_current) / h_t
```
[Source: calculate_greeks.py](src/greeks/calculate_greeks.py)

The implementation explicitly notes it's using forward difference to avoid negative time issues. 
While this doesn't match the conventional negative theta definition, it avoids numerical issues with negative time values in the simulation.

## Visualisation Interpretation

**Monte Carlo Option Price Path Simulation Guide**

  X-Axis: Days until option expiration (decreasing from left to right)
  Y-Axis: Option price trajectories

  Key Observations:
    - Each colored line represents a potential price path
    - Early paths (far from expiration) are clustered
    - Paths spread out as expiration approaches
    - Widening illustrates increasing price uncertainty
    - Visualization limited to 50 paths (vs. 10,000 used in computational analysis)
    - Reduced paths due to visualization resource constraints

  Why Paths Spread:
    - Reflects market's increasing uncertainty
    - Small price changes have larger option value impacts
    - Demonstrates potential range of option outcomes

  Interpretation:
    - Central paths show most likely scenarios
    - Extreme paths represent high-risk/high-reward possibilities
    - Visualizes option's potential value evolution

**Monte Carlo Price Distribution Histogram**

  The histogram of simulated option prices can dramatically change based on 
  input parameters, particularly the relationship between underlying asset 
  price (S) and strike price (K).

  Critical Observation:
    - Small parameter changes can cause SIGNIFICANT shifts in the option 
    price distribution
    - The histogram may range from concentrated near zero to widely spread 
    across a large value range

  Example Scenarios:
    - S = 100, K = 105: Mostly zero-value paths
    - S = 160, K = 100: Widespread, meaningful option values

  This is NOT a simulation error, but a fundamental representation of 
  the probabilistic nature of option pricing. 
  
  The drastic changes reflect real-world pricing dynamics and demonstrate how market 
  conditions profoundly impact option valuations.

  Recommended Exploration:
    - Experiment with various input combinations
    - Observe how different parameters influence the price distribution
    - Understand that the wide variation is a feature, not a bug

**Surface Plot Interpretations**

  Delta Surface:
  - Shows option's price sensitivity to underlying price and volatility
  - Delta approaches 1 for deep ITM calls, 0 for deep OTM calls
  - Surface demonstrates how delta's behavior changes with volatility
  - Higher volatility creates more gradual transition between 0 and 1
  - BS limitation: Assumes constant volatility, while real markets show volatility smile/skew
  
  Gamma Surface:
  - Peak at ATM shows maximum convexity/hedging needs
  - Surface demonstrates how gamma concentrates near strike price
  - Higher volatility spreads out gamma effect across wider price range
  - BS limitation: Constant vol assumption means symmetric gamma distribution
  - More sophisticated models like SABR better capture market skew effects
  
  Theta Surface:
  - Maximum time decay near strike price, especially close to expiry
  - Surface shows theta increases as option approaches expiration
  - Higher volatility reduces theta effect by increasing time value
  - BS limitation: Time decay pattern assumes constant volatility regime
  - Models like Heston better capture term structure of volatility
  
  Vega Surface:
  - Peak vega for ATM options shows maximum volatility sensitivity
  - Surface demonstrates how vega decays for deep ITM/OTM options
  - BS limitation: Cannot capture volatility smile/skew patterns
  - Advanced models needed for more realistic vega profiles
  
  Rho Surface:
  - Shows interest rate sensitivity across strikes and rates
  - Greater effect for longer-dated options
  - BS limitation: Assumes constant interest rates

**Surface Plot Interpretations - Understanding the 'Why'**

  Delta Surface:
  - Becomes 1 for deep ITM calls because option behaves exactly like stock
     * Deep ITM: Almost certain to be exercised, moves one-to-one with stock
     * Deep OTM: Very unlikely to be exercised, minimal price movement
  - Higher volatility smooths Delta transition because:
     * More uncertainty means less binary outcomes
     * Greater chance OTM options become ITM and vice versa
  
  Gamma Surface:
  - Peaks at ATM because:
     * Maximum uncertainty about whether option will expire ITM or OTM
     * Small price changes can significantly affect probability of exercise
     * Delta changes most rapidly here (maximum convexity)
  - Higher volatility spreads gamma because:
     * Increases uncertainty range around strike price
     * Makes options further from strike more sensitive to price changes
  
  Theta Surface:
  - Most negative ATM because:
     * ATM options have maximum time value to lose
     * ITM/OTM options have more intrinsic value or less total value to decay
  - Peak increases near expiry because:
     * Less time for favorable movement
     * Time value decays non-linearly (accelerates near expiry)
     * Uncertainty diminishes rapidly
  
  Vega Surface:
  - Highest for ATM options because:
     * Maximum uncertainty about expiry outcome
     * Most time value affected by volatility changes
     * Deep ITM/OTM have more certainty, less affected by volatility
  - Decreases with time because:
     * Less time for volatility to affect outcome
     * More certainty about final payoff
  
  Rho Surface:
  - Greater for ITM calls because:
       * Higher probability of exercising
       * More affected by discounting of strike price
  - Increases with time because:
       * Interest rate effects compound over time
       * Present value calculations more sensitive to rate changes

**Note on the Monte Carlo options price value in the sensitivity plots (vol, time to expiry, strike price)**

For those who might be asking, "why does the MC model provide a different options price everytime I use the same parameters?"

  Inherent Characteristics:
    - Stochastic (random) pricing model
    - Uses pseudo-random number generation
    - Approximation method, not an exact calculation
    - Pricing is statistical estimate, not deterministic value

  Why Variations Occur:
    - Random walk simulations
    - Probabilistic nature of financial modeling
    - Finite number of price path simulations
    - Computational approximation of complex financial dynamics

  Key Insight:
    - Small price differences are expected and normal
    - Reflects the probabilistic nature of financial markets
    - Demonstrates model's ability to capture market uncertainty

## Bonus: What factors contributed towards the accuracy of options pricing for MC models in this project?

I can only assume that people may want to understand the reason for the pricing accuracy of the options 
for the Monte Carlo model relative to its Black-Scholes counterpart, the following section answers that:

1. **Identical Stochastic Process Assumption**

Both models use geometric Brownian motion to model stock price movements:

```bash
# Monte Carlo implementation
price_path = S * np.exp(np.cumsum(
    (r - q - 0.5 * sigma ** 2) * dt + 
    sigma * np.sqrt(dt) * random_numbers[i]
))
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

```bash
# Black-Scholes implementation (underlying math)
d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
```
[Source: black_scholes.py](src/models/black_scholes.py)

Both use the same drift term (r - q - 0.5 * sigma ** 2) and volatility term sigma * sqrt(dt), 
ensuring they're modeling the same stochastic process.

2. **Fine-Grained Time Steps**

The Monte Carlo simulation uses daily time steps, providing high resolution:

```bash
# Daily time steps for accurate path simulation
dt = T / 365  # Daily time steps
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

This fine granularity ensures the price paths closely follow the theoretical continuous process assumed by Black-Scholes.

3. **Sufficient Number of Simulations**

The default of 10,000 simulations provides strong statistical convergence:

```bash
def monte_carlo_simulation(option_type, S, K, T, r, sigma, q=0, num_simulations=10000, random_numbers=None):
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

The law of large numbers ensures that with enough simulations, the Monte Carlo estimate converges to the true expected value, which is what Black-Scholes calculates analytically.

4. **Proper Risk-Neutral Valuation**

```bash
# Risk-neutral valuation
option_price = np.exp(-r * T) * np.mean(payoffs)
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

```bash
# Risk-neutral valuation (embedded in the formula)
price = (S * np.exp(-q * T) * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
```
[Source: black_scholes.py](src/models/black_scholes.py)

5. **Efficient Vectorized Implementation**

The Monte Carlo implementation uses NumPy's vectorized operations for efficiency and numerical stability:

```bash
# Vectorized payoff calculation
if option_type == "Call":
    payoffs = np.maximum(prices - K, 0)
else:  # Put
    payoffs = np.maximum(K - prices, 0)
```
[Source: monte_carlo.py](src/models/monte_carlo.py)

This reduces numerical errors that might accumulate in loop-based implementations.

**Mathematical Equivalence**

The key insight is that Monte Carlo is numerically approximating the same mathematical expectation that Black-Scholes solves analytically:

1. Black-Scholes: Derives a closed-form solution to the option pricing PDE
2. Monte Carlo: Approximates the expected value through random sampling

For European options (which only depend on the final price), both approaches should converge to the same value as the number of simulations increases.

**Code Excerpt Showing Key Accuracy Contributors**

```bash
# 1. Identical stochastic process as Black-Scholes
price_path = S * np.exp(np.cumsum(
    (r - q - 0.5 * sigma ** 2) * dt + 
    sigma * np.sqrt(dt) * random_numbers[i]
))

# 2. Only using final price (European option characteristic)
prices[i] = price_path[-1]  # Final price at expiration

# 3. Risk-neutral valuation (same as Black-Scholes)
option_price = np.exp(-r * T) * np.mean(payoffs)
```

The Monte Carlo implementation achieves high accuracy because it:

- Uses the same underlying stochastic process assumptions as Black-Scholes
- Employs sufficient simulations (10,000) to ensure statistical convergence
- Implements daily time steps for precise path simulation
- Applies proper risk-neutral valuation
- Uses numerically stable vectorized operations

For European options, Monte Carlo should theoretically converge to the Black-Scholes price as the number of simulations approaches infinity. 
The <1% difference observed is due to the finite number of simulations, but 10,000 is typically sufficient for practical purposes.
The real advantage of Monte Carlo comes when pricing more complex options where Black-Scholes has no analytical solution, but for standard European options, 
it serves as an excellent validation that both methods are implemented correctly.
