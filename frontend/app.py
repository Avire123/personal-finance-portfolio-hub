import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="Personal Finance Hub",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Personal Finance & Investment Portfolio Hub")

# --- TAB NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Portfolio Overview", "➕ Add Asset", "💸 Expense Tracker"])

# --- TAB 1: PORTFOLIO OVERVIEW ---
with tab1:
    st.header("Portfolio Breakdown & Performance")
    try:
        res = requests.get(f"{API_BASE_URL}/assets/summary/")
        if res.status_code == 200:
            summary = res.json()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Invested", f"${summary['total_invested']:,.2f}")
            col2.metric("Current Value", f"${summary['current_value']:,.2f}")
            col3.metric("Total Gain/Loss", f"${summary['total_gain_loss']:,.2f}", 
                        delta_color="normal")

            if summary['holdings']:
                df = pd.DataFrame(summary['holdings'])
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.subheader("Asset Allocation by Type")
                    fig_pie = px.pie(df, values='current_value', names='asset_type', title="Allocation Breakdown", hole=0.4)
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col_chart2:
                    st.subheader("Holdings Comparison")
                    fig_bar = px.bar(df, x='name', y=['purchase_price', 'live_price'], barmode='group', title="Purchase vs Current Live Price")
                    st.plotly_chart(fig_bar, use_container_width=True)

                st.subheader("Holdings Detail Table")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No assets added yet. Use the 'Add Asset' tab to get started!")
        else:
            st.error("Failed to connect to FastAPI backend.")
    except Exception as e:
        st.warning(f"Could not reach API server at {API_BASE_URL}. Ensure uvicorn is running.")

# --- TAB 2: ADD ASSET ---
with tab2:
    st.header("Add New Holding")
    with st.form("add_asset_form"):
        name = st.text_input("Asset Name (e.g., Apple Inc, Bitcoin)", value="")
        ticker = st.text_input("Ticker Symbol (e.g., AAPL, BTC-USD)", value="")
        asset_type = st.selectbox("Asset Class", ["stock", "crypto", "savings", "debt"])
        quantity = st.number_input("Quantity Owned", min_value=0.0001, step=1.0, value=1.0)
        purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, step=10.0, value=100.0)

        submitted = st.form_submit_button("Add Asset")
        if submitted:
            payload = {
                "name": name,
                "ticker": ticker if ticker else None,
                "asset_type": asset_type,
                "quantity": quantity,
                "purchase_price": purchase_price
            }
            res = requests.post(f"{API_BASE_URL}/assets/", json=payload)
            if res.status_code == 201:
                st.success(f"Successfully added {name}!")
                st.rerun()
            else:
                st.error(f"Error adding asset: {res.text}")

# --- TAB 3: EXPENSE TRACKER ---
with tab3:
    st.header("Log Expenses & Budget Tracking")
    with st.form("add_expense_form"):
        category = st.text_input("Category (e.g., Housing, Food, Entertainment)")
        amount = st.number_input("Amount ($)", min_value=0.01, step=5.0)
        monthly_limit = st.number_input("Monthly Target Cap ($)", min_value=0.0, step=50.0)
        description = st.text_input("Description / Notes")

        submit_exp = st.form_submit_button("Log Expense")
        if submit_exp:
            exp_payload = {
                "category": category,
                "amount": amount,
                "monthly_limit": monthly_limit if monthly_limit > 0 else None,
                "description": description
            }
            res = requests.post(f"{API_BASE_URL}/expenses/", json=exp_payload)
            if res.status_code == 201:
                st.success("Expense logged successfully!")
                st.rerun()

    # Display Existing Expenses
    try:
        exp_res = requests.get(f"{API_BASE_URL}/expenses/")
        if exp_res.status_code == 200 and exp_res.json():
            exp_df = pd.DataFrame(exp_res.json())
            st.subheader("Recorded Expenses")
            st.dataframe(exp_df, use_container_width=True)
    except Exception:
        pass
