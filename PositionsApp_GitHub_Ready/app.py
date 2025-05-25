import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Position Size Calculator", layout="centered")
st.title("📊 Position Size Calculator (Stocks)")

# Debugging: Show current files in directory
st.subheader("🔍 Debugging Info (for deployment)")
st.write("Files in current directory:")
st.write(os.listdir())

# File path
file_path = "PositionsCalcStocks_Final.xlsx"

# Try loading the Excel file
try:
    excel_file = pd.ExcelFile(file_path)
    st.success("✅ Excel file loaded successfully!")
    st.write("Sheets found:", excel_file.sheet_names)

    # Allow user to pick a sheet
    sheet_name = st.selectbox("Select sheet:", excel_file.sheet_names)
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Display data
    st.subheader("📈 Data Preview")
    st.dataframe(df)

    # Position calculator section
    st.subheader("💰 Position Size Calculator")

    capital = st.number_input("Enter total capital ($)", value=10000.0, min_value=0.0)
    risk_pct = st.slider("Risk per trade (%)", min_value=0.5, max_value=10.0, value=2.0, step=0.5)
    entry_price = st.number_input("Entry price ($)", value=50.0, min_value=0.01)
    stop_loss = st.number_input("Stop loss price ($)", value=45.0, min_value=0.01)

    if entry_price > stop_loss:
        risk_per_share = entry_price - stop_loss
        dollars_at_risk = capital * (risk_pct / 100)
        position_size = dollars_at_risk / risk_per_share
        shares = int(position_size)
        st.markdown(f"### 🧮 You can buy: **{shares} shares**")
    else:
        st.warning("⚠️ Entry price must be greater than stop loss.")

except FileNotFoundError:
    st.error("❌ Excel file not found. Please make sure 'PositionsCalcStocks_Final.xlsx' is in the root directory of your GitHub repo.")

except Exception as e:
    st.error(f"❌ Error loading Excel file: {e}")
