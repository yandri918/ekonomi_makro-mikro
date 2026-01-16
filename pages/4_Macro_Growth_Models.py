import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Growth Models", page_icon="🌏", layout="wide")

st.title("🌏 Solow-Swan Growth Model")
st.markdown("Simulate how **Capital Accumulation**, **Savings Rate**, and **Population Growth** drive long-term economic prosperity.")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ Model Parameters")
    s = st.slider("Savings Rate (s)", 0.0, 0.5, 0.25, step=0.01)
    alpha = st.slider("Capital Share (α)", 0.1, 0.5, 0.33, step=0.01)
    delta = st.slider("Depreciation Rate (δ)", 0.0, 0.2, 0.05, step=0.01)
    n = st.slider("Population Growth (n)", 0.0, 0.1, 0.02, step=0.005)
    g = st.slider("Tech Growth (g)", 0.0, 0.1, 0.02, step=0.005)
    
    st.markdown("### 🎬 Simulation")
    k0 = st.number_input("Initial Capital per Worker (k0)", value=1.0)
    periods = st.slider("Time Periods", 20, 100, 50)

with col2:
    # Logic: Cobb-Douglas Production Function y = k^alpha
    # Capital Accumulation: Delta k = s*y - (delta + n + g)*k
    # k_next = s*k^alpha + (1 - delta - n - g)*k
    
    k_history = [k0]
    y_history = [k0**alpha]
    c_history = [(1-s) * y_history[0]]
    i_history = [s * y_history[0]]
    
    for t in range(1, periods + 1):
        k_prev = k_history[-1]
        y_prev = k_prev**alpha
        
        investment = s * y_prev
        break_even = (delta + n + g) * k_prev
        
        k_next = k_prev + investment - break_even
        
        k_history.append(k_next)
        y_history.append(k_next**alpha)
        c_history.append((1-s) * k_next**alpha)
        i_history.append(investment)
        
    # Steady State Calculation
    # s* k_ss^alpha = (delta + n + g) * k_ss
    # k_ss^(alpha-1) = (delta + n + g) / s
    # k_ss = (s / (delta + n + g)) ^ (1 / (1 - alpha))
    effective_depreciation = delta + n + g
    if effective_depreciation == 0:
        k_ss = 0
    else:
        k_ss = (s / effective_depreciation) ** (1 / (1 - alpha))
        
    y_ss = k_ss**alpha
    
    # Create Dataframe
    df = pd.DataFrame({
        'Period': range(periods + 1),
        'Capital (k)': k_history,
        'Output (y)': y_history,
        'Consumption (c)': c_history,
        'Investment (i)': i_history
    })
    
    df_melted = df.melt('Period', var_name='Variable', value_name='Value')
    
    # Plot
    chart = alt.Chart(df_melted).mark_line().encode(
        x='Period',
        y='Value',
        color='Variable',
        tooltip=['Period', 'Variable', alt.Tooltip('Value', format='.2f')]
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Steady State Metals
    st.markdown("### 🏁 Steady State Analysis (Long Run)")
    
    ss_col1, ss_col2 = st.columns(2)
    ss_col1.metric("Steady State Capital (k*)", f"{k_ss:.2f}")
    ss_col2.metric("Steady State Output (y*)", f"{y_ss:.2f}")
    
    st.info("""
    **Theory:**
    The economy grows until investment equals depreciation (break-even investment).
    At steady state: $sf(k^*) = (\delta + n + g)k^*$
    """)

