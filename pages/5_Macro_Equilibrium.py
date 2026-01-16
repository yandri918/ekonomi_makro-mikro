import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Macro Equilibrium", page_icon="⚖️", layout="wide")

st.title("⚖️ General Equilibrium: IS-LM & AD-AS")

tab1, tab2 = st.tabs(["📉 IS-LM Model", "📈 AD-AS Model"])

# --- TAB 1: IS-LM ---
with tab1:
    st.markdown("### 1. IS-LM Model (Goods & Money Market)")
    st.markdown("Analyze how Fiscal Policy (G, T) and Monetary Policy (M) affect Interest Rates ($r$) and Output ($Y$).")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🏛️ Fiscal Policy (IS)")
        G = st.slider("Gov Spending (G)", 100, 500, 200)
        T = st.slider("Taxes (T)", 100, 500, 150)
        MPC = st.slider("MPC (b)", 0.5, 0.9, 0.75)
        
        st.markdown("---")
        st.subheader("🏦 Monetary Policy (LM)")
        Ms = st.slider("Money Supply (Ms)", 100, 1000, 500)
        P = st.slider("Price Level (P)", 1.0, 5.0, 2.0)
        k = st.slider("Money Demand Sensitivity to Y (k)", 0.1, 1.0, 0.5)
        h = st.slider("Money Demand Sensitivity to r (h)", 10, 100, 50)

    with col2:
        # Simulations
        # IS Curve: Y = C + I + G
        # C = a + b(Y-T)
        # I = e - dr
        # Y = a + bY - bT + e - dr + G
        # Y(1-b) = a - bT + e + G - dr
        # r = (a - bT + e + G)/d - (1-b)/d * Y
        a = 100 # Autonomous Consumption
        e = 200 # Autonomous Investment
        d_param = 20 # Interest sensitivity of investment
        
        Y_range = np.linspace(0, 3000, 100)
        
        # IS Equation for r
        IS_intercept = (a - MPC*T + e + G) / d_param
        IS_slope = (1 - MPC) / d_param
        r_IS = IS_intercept - IS_slope * Y_range
        
        # LM Curve: Ms/P = kY - hr
        # hr = kY - Ms/P
        # r = (k/h)*Y - (1/h)*(Ms/P)
        LM_intercept = -(1/h) * (Ms/P)
        LM_slope = k/h
        r_LM = LM_intercept + LM_slope * Y_range
        
        # Create DF
        df_is = pd.DataFrame({'Y': Y_range, 'r': r_IS, 'Type': 'IS Curve'})
        df_lm = pd.DataFrame({'Y': Y_range, 'r': r_LM, 'Type': 'LM Curve'})
        df = pd.concat([df_is, df_lm])
        
        # Filter negative r
        df = df[df['r'] >= 0]
        
        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('Y', title='Income / Output (Y)'),
            y=alt.Y('r', title='Interest Rate (r)'),
            color=alt.Color('Type', scale=alt.Scale(domain=['IS Curve', 'LM Curve'], range=['red', 'blue']))
        ).interactive()
        
        # Equilibrium Calculation
        # IS: r = A - B*Y
        # LM: r = C + D*Y
        # A - BY = C + DY => Y(B+D) = A - C => Y = (A-C)/(B+D)
        Y_eq = (IS_intercept - LM_intercept) / (IS_slope + LM_slope)
        r_eq = LM_intercept + LM_slope * Y_eq
        
        eq_point = alt.Chart(pd.DataFrame({'Y': [Y_eq], 'r': [r_eq]})).mark_point(
            size=200, color='black', fill='black'
        ).encode(x='Y', y='r')
        
        st.altair_chart((chart + eq_point), use_container_width=True)
        
        st.info(f"""
        **Equilibrium:**
        - **Output ($Y^*$):** {Y_eq:.2f}
        - **Interest Rate ($r^*$):** {r_eq:.2f}%
        """)

# --- TAB 2: AD-AS ---
with tab2:
    st.markdown("### 2. AD-AS Model (Aggregate Demand & Supply)")
    st.markdown("Visualize the impact of shocks on Inflation ($\pi$) and Output Gap.")
    
    col_ad1, col_ad2 = st.columns([1, 2])
    
    with col_ad1:
        st.subheader("⚡ Shocks")
        ad_shock = st.slider("Aggregate Demand Shock", -50, 50, 0, help="Shift AD (e.g. Consumer Confidence)")
        sras_shock = st.slider("Supply Shock (SRAS)", -50, 50, 0, help="Shift SRAS (e.g. Oil Prices)")
        
    with col_ad2:
        # Simple Linear Model
        # AD: P = 10 - 0.5Y + Shock
        # SRAS: P = 2 + 0.5Y + Shock
        # LRAS: Y = 8 (Potential Output)
        
        Y_vals = np.linspace(4, 12, 100)
        
        # Equations
        AD_P = (14 + ad_shock/10) - 1.0 * Y_vals
        SRAS_P = (2 + sras_shock/10) + 0.5 * Y_vals
        
        df_ad = pd.DataFrame({'Y': Y_vals, 'P': AD_P, 'Type': 'AD'})
        df_sras = pd.DataFrame({'Y': Y_vals, 'P': SRAS_P, 'Type': 'SRAS'})
        df_lras = pd.DataFrame({'Y': [8, 8], 'P': [0, 15], 'Type': 'LRAS'})
        
        df_macro = pd.concat([df_ad, df_sras])
        
        base_macro = alt.Chart(df_macro).mark_line().encode(
            x=alt.X('Y', title='Real GDP (Y)', scale=alt.Scale(domain=[4, 12])),
            y=alt.Y('P', title='Price Level (P)', scale=alt.Scale(domain=[2, 10])),
            color=alt.Color('Type', scale=alt.Scale(domain=['AD', 'SRAS', 'LRAS'], range=['red', 'blue', 'green']))
        )
        
        lras_line = alt.Chart(df_lras).mark_line(strokeDash=[5,5], color='green').encode(
            x='Y', y='P'
        )
        
        # Equilibrium
        # 14 + shock_ad - Y = 2 + shock_as + 0.5Y
        # 1.5Y = 12 + shock_ad - shock_as
        Y_macro_eq = (12 + ad_shock/10 - sras_shock/10) / 1.5
        P_macro_eq = (2 + sras_shock/10) + 0.5 * Y_macro_eq
        
        eq_macro = alt.Chart(pd.DataFrame({'Y': [Y_macro_eq], 'P': [P_macro_eq]})).mark_point(
            size=200, color='black', fill='black'
        ).encode(x='Y', y='P')
        
        st.altair_chart((base_macro + lras_line + eq_macro).interactive(), use_container_width=True)
        
        gap = Y_macro_eq - 8
        st.metric("Output Gap (Y - Y*)", f"{gap:.2f}")
        if gap > 0:
            st.warning("⚠️ Inflationary Gap (Overheating)")
        elif gap < 0:
            st.error("⚠️ Recessionary Gap")
