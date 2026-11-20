import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Multi-Asset Risk Matrix Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E8F1F5 0%, #D4E6F1 100%);
        border-right: 2px solid #AED6F1;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #184F72 !important;
        font-weight: 600;
    }
    div[data-testid="metric-container"] {
        background-color: #F8F9F9;
        border: 1px solid #D5DBDB;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Multi-Asset Risk Matrix Engine")
st.subheader("Portfolio Covariance, Return Simulation & Value-at-Risk (VaR)")
st.markdown("---")

st.sidebar.header("🎛️ Allocation & Risk Controls")
w_equity = st.sidebar.slider("Equity Weight (%)", 0, 100, 50, 5)
w_bonds = st.sidebar.slider("Fixed Income / Bonds Weight (%)", 0, 100, 30, 5)
w_gold = st.sidebar.slider("Commodities / Gold Weight (%)", 0, 100, 20, 5)
trading_days = st.sidebar.slider("Simulation Days", 60, 500, 252, 20)
confidence_level = st.sidebar.selectbox("Confidence Level", [0.90, 0.95, 0.99], index=1)

try:
    total_weight = w_equity + w_bonds + w_gold
    if total_weight == 0:
        weights = np.array([1 / 3, 1 / 3, 1 / 3])
    else:
        weights = np.array([w_equity, w_bonds, w_gold], dtype=float) / total_weight

    np.random.seed(13)
    assets = ["Equities", "Bonds", "Gold"]

    mean_returns = np.array([0.00045, 0.00018, 0.00025])
    volatilities = np.array([0.0140, 0.0045, 0.0095])

    corr_matrix = np.array([
        [1.00, -0.15, 0.05],
        [-0.15, 1.00, 0.10],
        [0.05, 0.10, 1.00]
    ])

    cov_matrix = np.outer(volatilities, volatilities) * corr_matrix

    cholesky_matrix = np.linalg.cholesky(cov_matrix)
    standard_normals = np.random.normal(0.0, 1.0, size=(trading_days, 3))
    correlated_returns = mean_returns + (standard_normals @ cholesky_matrix.T)

    returns_df = pd.DataFrame(correlated_returns, columns=assets)
    returns_df["Day"] = np.arange(1, trading_days + 1)

    portfolio_daily_ret = correlated_returns @ weights
    returns_df["Portfolio_Return"] = portfolio_daily_ret

    returns_df["Portfolio_Index"] = 100.0 * np.cumprod(1.0 + portfolio_daily_ret)
    returns_df["Equity_Index"] = 100.0 * np.cumprod(1.0 + returns_df["Equities"])
    returns_df["Bonds_Index"] = 100.0 * np.cumprod(1.0 + returns_df["Bonds"])
    returns_df["Gold_Index"] = 100.0 * np.cumprod(1.0 + returns_df["Gold"])

    annualized_return = np.mean(portfolio_daily_ret) * 252 * 100
    annualized_vol = np.std(portfolio_daily_ret, ddof=1) * np.sqrt(252) * 100
    sharpe_like = (annualized_return / annualized_vol) if annualized_vol > 0 else 0.0
    var_threshold = np.percentile(portfolio_daily_ret, (1.0 - confidence_level) * 100) * 100

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="📈 Annualized Return",
            value=f"{annualized_return:.2f}%",
            delta=f"Weights: {int(weights[0]*100)}/{int(weights[1]*100)}/{int(weights[2]*100)}"
        )
    with col2:
        st.metric(
            label="🌊 Annualized Volatility",
            value=f"{annualized_vol:.2f}%"
        )
    with col3:
        st.metric(
            label="⚖️ Return-to-Risk Ratio",
            value=f"{sharpe_like:.2f}"
        )
    with col4:
        st.metric(
            label=f"🛡️ Daily VaR ({int(confidence_level*100)}%)",
            value=f"{var_threshold:.2f}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=returns_df["Day"],
        y=returns_df["Portfolio_Index"],
        mode="lines",
        name="Portfolio Index",
        line=dict(color="#1F618D", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=returns_df["Day"],
        y=returns_df["Equity_Index"],
        mode="lines",
        name="Equities Index",
        line=dict(color="#E74C3C", width=1.8, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=returns_df["Day"],
        y=returns_df["Bonds_Index"],
        mode="lines",
        name="Bonds Index",
        line=dict(color="#27AE60", width=1.8, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=returns_df["Day"],
        y=returns_df["Gold_Index"],
        mode="lines",
        name="Gold Index",
        line=dict(color="#D4AC0D", width=1.8, dash="dashdot")
    ))

    fig.update_layout(
        title="Simulated Wealth Trajectory (Base = 100)",
        xaxis_title="Trading Day",
        yaxis_title="Index Value",
        template="plotly_white",
        hovermode="x unified",
        height=440,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 View Simulated Daily Returns & Index Data"):
        display_df = returns_df[[
            "Day",
            "Portfolio_Index",
            "Portfolio_Return",
            "Equities",
            "Bonds",
            "Gold"
        ]].copy()
        display_df["Portfolio_Index"] = np.round(display_df["Portfolio_Index"], 2)
        display_df["Portfolio_Return"] = np.round(display_df["Portfolio_Return"] * 100, 3)
        display_df["Equities"] = np.round(display_df["Equities"] * 100, 3)
        display_df["Bonds"] = np.round(display_df["Bonds"] * 100, 3)
        display_df["Gold"] = np.round(display_df["Gold"] * 100, 3)
        st.dataframe(display_df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Risk Engine Error: {e}")
    st.info("Adjust allocation weights or simulation days and try again.")
