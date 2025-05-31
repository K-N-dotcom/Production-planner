Python 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Production Planning App", layout="centered")
st.title("📦 Optimized Production Planning")

st.sidebar.header("Enter Product Details")

# User Inputs
customer = st.sidebar.text_input("Customer Name")
product_code = st.sidebar.text_input("Product Code")
order_qty = st.sidebar.number_input("Order Quantity", min_value=1, value=100)
stock_at_customer = st.sidebar.number_input("Stock at Customer", min_value=0, value=50)
depletion_days = st.sidebar.number_input("Depletion Days (how long current stock will last)", min_value=1, value=2)
transit_hrs = st.sidebar.number_input("Transit Time (hrs)", min_value=1, value=2)
cycle_time_min = st.sidebar.number_input("Cycle Time (min/unit)", min_value=1.0, value=1.0)

if st.sidebar.button("Generate Plan"):
    today = datetime.today()
    shift_hours = 9

    required_delivery_date = today + timedelta(days=depletion_days)
    transit_days = transit_hrs / shift_hours
    total_production_time_hrs = (order_qty * cycle_time_min) / 60
    shifts_needed = total_production_time_hrs / shift_hours
    production_end_date = required_delivery_date - timedelta(days=transit_days)
    production_start_date = production_end_date - timedelta(days=shifts_needed)

    # Display Output
    st.subheader("📋 Production Schedule")
    plan = {
        "Customer": customer,
        "Product Code": product_code,
        "Order Quantity": order_qty,
        "Stock at Customer": stock_at_customer,
        "Depletion Days": depletion_days,
        "Transit Time (hrs)": transit_hrs,
        "Cycle Time (min/unit)": cycle_time_min,
        "Required Delivery Date": required_delivery_date.date(),
        "Production Start Date": production_start_date.date(),
        "Production End Date": production_end_date.date(),
        "Total Production Time (hrs)": round(total_production_time_hrs, 2),
        "Shifts Needed": round(shifts_needed, 2)
    }

    df_plan = pd.DataFrame([plan])
    st.dataframe(df_plan)

    # Download option
    csv = df_plan.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Plan as CSV",
        data=csv,
        file_name="production_plan.csv",
        mime="text/csv"
    )
