📊 MULTI-ASSET RISK MATRIX ENGINE

An interactive portfolio risk and return simulation engine built with Python, NumPy, Pandas, Plotly, and Streamlit to model correlated asset movements, portfolio variance, and Value-at-Risk (VaR).

🌐 System Overview

The Multi-Asset Risk Matrix Engine simulates multi-asset financial behavior across Equities, Bonds, and Gold over a selectable trading horizon. Using covariance matrix math and Cholesky decomposition, it generates correlated daily return series, tracks cumulative portfolio wealth starting from a base index of 100, computes key risk-return metrics, and displays interactive charts alongside a detailed daily data table.

🛠️ Architecture & Tech Stack

1. Core Engine: Python (Portfolio allocation normalization, return simulation, and risk metric calculations)
2. Matrix & Risk Math: NumPy (Covariance matrix construction, Cholesky decomposition, annualized volatility, and percentile VaR)
3. Tabular & Time-Series Processing: Pandas (Daily return DataFrames, cumulative wealth tracking, and formatted output tables)
4. Interactive Visualization: Plotly (plotly.graph_objects multi-line wealth trajectory chart with unified hover inspection)
5. Web Dashboard & Controls: Streamlit (Sidebar allocation/simulation sliders, confidence level selector, 4 KPI metric cards, and expandable data table)

🎛️ Interactive Controls & Metrics

Sidebar Controls:

1. Equity Weight (%) (0 to 100)
2. Fixed Income / Bonds Weight (%) (0 to 100)
3. Commodities / Gold Weight (%) (0 to 100)
4. Simulation Days (60 to 500 trading days)
5. Confidence Level (0.90, 0.95, or 0.99)

Top KPI Cards:

1. Annualized Return (with active asset weight ratio)
2. Annualized Volatility
3. Return-to-Risk Ratio
4. Daily VaR (at the selected confidence level)

📁 Project Structure

1. portfolio_risk_engine.py — Main Streamlit application containing the simulation math, KPI cards, Plotly chart, and expandable table
2. requirements.txt — Python dependencies (streamlit, numpy, pandas, plotly)
3. README.md — Project documentation and setup guide

🚀 Quick Start & Local Setup

Run the project locally in your terminal:

1. Clone the repository:
   git clone https://github.com/techrabiya/Multi-Asset-Risk-Matrix-Engine

2. Enter the project folder:
   cd Multi-Asset-Risk-Matrix-Engine

3. Install dependencies:
   pip install -r requirements.txt

4. Launch the app:
  https://multi-asset-risk-matrix-engine-3mkddbxdqhhcbz4nx9ctnb.streamlit.app/

👑 Built By
  Rabia Razzaq Khan — Self-Taught Developer & Data/AI Builder
