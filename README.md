# Options Pricing and Greeks Analysis

## Contact info

Email: saimanishprabhakar2020@gmail.com

[Linkedin](https://www.linkedin.com/in/saimanish-prabhakar-3074351a0/)

## Project Overview

### Key Features

#### Customizable Option Parameters
Users can dynamically input and adjust:
- Option Type (Call/Put)
- Underlying Asset Price
- Strike Price
- Time to Expiration
- Risk-Free Interest Rate
- Volatility
- Dividend Yield
- Monte Carlo Simulation Count

#### Visualization and Analysis
1. **Options Pricing Insights**
   - Detailed visual analysis of option prices
   - Sensitivity visualizations for:
     - Volatility
     - Time to Expiration
     - Strike Price

2. **Monte Carlo Simulation**
   - **Visual Path Simulation**: 
     - Configurable display of 1-50 sample price paths (limited for visualisation purposes)
     - Interactive graph showing possible price evolution scenarios
   - **Pricing Calculation**:
     - Utilises 10,000 simulation paths by default for accurate price estimation
     - Configurable simulation count parameter for balancing precision and performance
   - **Price Distribution Analysis**:
     - Histogram showing distribution of final prices across all simulation paths
     - Statistical summary of simulation results

3. **Comprehensive Greeks Analysis**
   - First-Order Greeks:
     - Delta
     - Gamma
     - Theta
     - Vega
     - Rho

   - Second-Order Greeks:
     - Charm
     - Speed
     - Color
     - Zomma
     - Veta
     - Volga

#### Comparative Visualization
- Bar charts include a 'Difference %' metric
- Compares Black-Scholes and Monte Carlo method results
- Provides insight into model accuracy and deviation

#### Multi-Dimensional Sensitivity Plots
Based on Black-Scholes Greeks:
- Delta Surface: (Greek, Volatility, Stock Price)
- Gamma Surface: (Greek, Volatility, Stock Price)
- Vega Surface: (Greek, Volatility, Stock Price)
- Theta Surface: (Greek, Time to Expiration, Stock Price)
- Rho Surface: (Greek, Risk-Free Rate, Stock Price)

## Built with

- <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">

- <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">

- <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white" alt="Matplotlib">

- <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">

- <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">

- <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" alt="SciPy">

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your_username/options-pricing-and-greeks.git
cd options-pricing-and-greeks
```
### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required libraries
pip install -r requirements.txt

# When done working on the project
deactivate
```
### Alternative: Direct Installation
```bash
# If you prefer not to use a virtual environment, you can directly install dependencies
pip install -r requirements.txt
```
### 3. Change git remote url to avoid accidental pushes to base project
```bash
git remote set-url origin github_username/options-pricing-and-greeks
git remote -v # confirm the changes
```

## Usage

### Video walkthrough of project

Here is a video explaining everything about the concept of the project, its features, and how to get the most 
out of it. Alternatively, you can read the written step-by-step walkthrough of the project alongside some images 
below if you can't stand my voice!

*** Video Tutorial - Coming soon ***

### Step-by-Step image walkthorugh of project

