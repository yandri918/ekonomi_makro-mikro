import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Economic Indices", page_icon="🔢", layout="wide")

st.title("🔢 Economic Indices: CPI & Inflation")
st.markdown("Calculate **Consumer Price Index (CPI)** and **Inflation Rate** by constructing a representative basket of goods.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🛒 Market Basket")
    
    # Default Basket
    default_data = pd.DataFrame({
        'Item': ['Food', 'Housing', 'Transport', 'Healthcare', 'Education'],
        'Quantity': [10, 1, 5, 2, 1],
        'Price_Base': [50, 500, 20, 100, 200],
        'Price_Current': [60, 550, 25, 120, 210]
    })
    
    edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

with col2:
    st.subheader("📊 Calculation Results")
    
    if not edited_df.empty:
        # Calculate Costs
        item = edited_df
        cost_base = (item['Quantity'] * item['Price_Base']).sum()
        cost_current = (item['Quantity'] * item['Price_Current']).sum()
        
        cpi = (cost_current / cost_base) * 100 if cost_base > 0 else 0
        inflation = ((cpi - 100) / 100) * 100 # Assuming Base CPI is 100
        
        st.metric("Cost of Basket (Base Year)", f"${cost_base:,.2f}")
        st.metric("Cost of Basket (Current Year)", f"${cost_current:,.2f}")
        
        st.divider()
        
        m1, m2 = st.columns(2)
        m1.metric("CPI (Index)", f"{cpi:.2f}")
        m2.metric("Inflation Rate", f"{inflation:.2f}%", delta=f"{inflation:.2f}%", delta_color="inverse")
        
        st.info(f"""
        **Formula:**
        $$ \\text{{CPI}} = \\frac{{\\text{{Cost of Basket}}_{{\\text{{Current}}}}}}{{\\text{{Cost of Basket}}_{{\\text{{Base}}}}}} \\times 100 $$
        
        This means prices have risen by **{inflation:.1f}%** compared to the base year.
        """)


st.divider()

st.subheader("🌍 Purchasing Power Parity (PPP) Demo")
pp_col1, pp_col2 = st.columns(2)

with pp_col1:
    st.markdown("**Big Mac Index Concept**")
    price_local = st.number_input("Price of Big Mac in Local Currency (IDR)", value=35000)
    price_us = st.number_input("Price of Big Mac in USA (USD)", value=5.50)
    
with pp_col2:
    implied_exchange_rate = price_local / price_us
    actual_exchange_rate = st.number_input("Actual Exchange Rate (USD/IDR)", value=15500)
    
    valuation = ((implied_exchange_rate - actual_exchange_rate) / actual_exchange_rate) * 100
    
    st.metric("Implied PPP Exchange Rate", f"1 USD = {implied_exchange_rate:,.0f} IDR")
    
    if valuation > 0:
        st.error(f"Currrency is **Overvalued** by {valuation:.1f}%")
    else:
        st.success(f"Currency is **Undervalued** by {abs(valuation):.1f}% (Good for exports!)")

