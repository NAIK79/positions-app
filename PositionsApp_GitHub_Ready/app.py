import streamlit as st
import pandas as pd

# Load Excel file
file_path = "PositionsCalcStocks_Final.xlsx"
excel_file = pd.ExcelFile(file_path)

# Load sheets
df_portfolio = excel_file.parse("Portfolio")
df_positions = excel_file.parse("My Positions")
df_focus = excel_file.parse("Position Size Focus List")
df_risk = excel_file.parse("Risk Reduce")

st.title("📊 Stock Position & Risk Calculator")

# --- Portfolio Overview ---
st.header("1. Portfolio Overview")
try:
    portfolio_value = float(df_portfolio.iloc[0, 1])
    st.metric("Total Portfolio Value", f"${portfolio_value:,.2f}")
except:
    st.warning("Could not read Total Portfolio Value")

# --- My Positions ---
st.header("2. Position Summary (My Positions)")
st.dataframe(df_positions, use_container_width=True)

# --- Position Size Focus List ---
st.header("3. Position Size Calculator")
st.markdown("Input a stock price to calculate position sizes based on preset risk levels.")

with st.form("position_size_form"):
    price = st.number_input("Stock Price", min_value=0.01, step=0.01)
    submit = st.form_submit_button("Calculate Position Sizes")

if submit:
    risk_levels = {
        "6.25%": 0.0625,
        "12.5%": 0.125,
        "15%": 0.15,
        "20%": 0.20,
        "25%": 0.25
    }
    calc_data = [(label, round(portfolio_value * risk / price)) for label, risk in risk_levels.items()]
    df_calc = pd.DataFrame(calc_data, columns=["Risk %", "Shares"])
    st.table(df_calc)

# --- Risk Reduce ---
st.header("4. Risk Reduction Planner")
try:
    buy_price = float(df_risk.loc[df_risk["Unnamed: 0"] == "Avg buy price"].iloc[0, 1])
    stop_price = float(df_risk.loc[df_risk["Unnamed: 0"] == "Stop price"].iloc[0, 1])
    shares = float(df_risk.loc[df_risk["Unnamed: 0"] == "Number of shares"].iloc[0, 1])
    dollar_risk = (buy_price - stop_price) * shares
    percent_risk = ((buy_price - stop_price) / buy_price) * 100

    st.write(f"**Buy Price:** ${buy_price:.2f}")
    st.write(f"**Stop Price:** ${stop_price:.2f}")
    st.write(f"**Shares:** {shares}")
    st.success(f"Dollar Risk: ${dollar_risk:.2f} ({percent_risk:.2f}%)")
except:
    st.warning("Could not calculate risk reduction due to missing or malformed data.")
