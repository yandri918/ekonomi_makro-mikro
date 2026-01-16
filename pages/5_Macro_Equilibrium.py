import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Macro Equilibrium", page_icon="⚖️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "⚖️ Macroeconomic Equilibrium: IS-LM & AD-AS",
        'tab1': "📉 IS-LM Model",
        'tab2': "📈 AD-AS Model",
        'islm_title': "1. IS-LM Model (Short Run)",
        'islm_intro': "Interaction between the **Goods Market (IS)** and **Money Market (LM)**.",
        'fiscal_policy': "🏛️ Fiscal Policy (IS Curve)",
        'G': "Govt Spending (G)",
        'T': "Taxes (T)",
        'MPC': "Marginal Propensity to Consume (MPC)",
        'monetary_policy': "🏦 Monetary Policy (LM Curve)",
        'Ms': "Money Supply (Ms)",
        'P': "Price Level (P)",
        'k': "Money Demand Sensitivity to Y (k)",
        'h': "Money Demand Sensitivity to r (h)",
        'eq_res': "**IS-LM Equilibrium:**",
        'eq_y': "Output (Y*):",
        'eq_r': "Interest Rate (r*):",
        'adas_title': "2. AD-AS Model (Fluctuations)",
        'adas_intro': "Simulate shocks to **Aggregate Demand (AD)** and **Short-Run Aggregate Supply (SRAS)**.",
        'shock_params': "⚡ Shock Parameters",
        'ad_shock': "AD Shock (Demand Side)",
        'sras_shock': "SRAS Shock (Supply Side)",
        'pos_shock': "Positive Shock",
        'neg_shock': "Negative Shock",
        'eq_res_adas': "**AD-AS Equilibrium:**",
        'p_lvl': "Price Level (P*):",
        'gap': "Output Gap (Y* - Y_potential):",
        'recession': "Recessionary Gap",
        'inflation': "Inflationary Gap",
        'full_emp': "Full Employment"
    },
    'ID': {
        'title': "⚖️ Keseimbangan Makroekonomi: IS-LM & AD-AS",
        'tab1': "📉 Model IS-LM",
        'tab2': "📈 Model AD-AS",
        'islm_title': "1. Model IS-LM (Jangka Pendek)",
        'islm_intro': "Interaksi antara **Pasar Barang (IS)** dan **Pasar Uang (LM)**.",
        'fiscal_policy': "🏛️ Kebijakan Fiskal (Kurva IS)",
        'G': "Belanja Pemerintah (G)",
        'T': "Pajak (T)",
        'MPC': "Kecenderungan Mengkonsumsi (MPC)",
        'monetary_policy': "🏦 Kebijakan Moneter (Kurva LM)",
        'Ms': "Jumlah Uang Beredar (Ms)",
        'P': "Tingkat Harga (P)",
        'k': "Sensitivitas Permintaan Uang thd Y (k)",
        'h': "Sensitivitas Permintaan Uang thd r (h)",
        'eq_res': "**Keseimbangan IS-LM:**",
        'eq_y': "Output (Y*):",
        'eq_r': "Suku Bunga (r*):",
        'adas_title': "2. Model AD-AS (Fluktuasi)",
        'adas_intro': "Simulasikan guncangan pada **Permintaan Agregat (AD)** dan **Penawaran Agregat Jangka Pendek (SRAS)**.",
        'shock_params': "⚡ Parameter Guncangan",
        'ad_shock': "Guncangan AD (Sisi Permintaan)",
        'sras_shock': "Guncangan SRAS (Sisi Penawaran)",
        'pos_shock': "Guncangan Positif",
        'neg_shock': "Guncangan Negatif",
        'eq_res_adas': "**Keseimbangan AD-AS:**",
        'p_lvl': "Tingkat Harga (P*):",
        'gap': "Celah Output (Y* - Y_potensial):",
        'recession': "Celah Resesi",
        'inflation': "Celah Inflasi",
        'full_emp': "Kesempatan Kerja Penuh"
    }
}

txt = T[lang]

st.title(txt['title'])

tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])

# --- TAB 1: IS-LM ---
with tab1:
    st.markdown(f"### {txt['islm_title']}")
    st.markdown(txt['islm_intro'])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader(txt['fiscal_policy'])
        G = st.slider(txt['G'], 50, 200, 100)
        T_val = st.slider(txt['T'], 20, 100, 50)
        MPC = st.slider(txt['MPC'], 0.1, 0.9, 0.75)
        
        st.subheader(txt['monetary_policy'])
        Ms = st.slider(txt['Ms'], 100, 500, 200)
        P_val = st.slider(txt['P'], 1.0, 5.0, 2.0)
        k = st.slider(txt['k'], 0.1, 1.0, 0.5)
        h = st.slider(txt['h'], 10, 100, 50)

    with col2:
        # IS Curve: Y = C + I + G
        # C = a + MPC(Y-T)
        # I = I_bar - b*r
        # Mathematical derivation for r as function of Y:
        # Y = a + MPC(Y-T) + I_bar - b*r + G
        # Y(1-MPC) = a - MPC*T + I_bar + G - b*r
        # b*r = (a - MPC*T + I_bar + G) - (1-MPC)Y
        # r = (Autonomous_Expenditure)/b - ((1-MPC)/b)*Y
        
        # Simplified IS: r = IS_intercept - IS_slope * Y
        # Let Auto_Exp = G - MPC*T + 300 (Consumption + Investment constant)
        auto_exp = G - MPC * T_val + 300
        IS_slope = (1 - MPC) / 50 # Assume sensitivity b=50
        IS_intercept = auto_exp / 50
        
        # LM Curve: Ms/P = L(Y, r) = kY - hr
        # hr = kY - Ms/P
        # r = (k/h)Y - (1/h)(Ms/P)
        real_money_supply = Ms / P_val
        LM_Slope = k / h
        LM_intercept = -real_money_supply / h
        
        # Calculate Equilibrium
        # IS_int - IS_slope*Y = LM_int + LM_slope*Y
        # IS_int - LM_int = (IS_slope + LM_slope)Y
        Y_eq = (IS_intercept - LM_intercept) / (IS_slope + LM_Slope)
        r_eq = IS_intercept - IS_slope * Y_eq
        
        # Plotting Data
        Y_vals = np.linspace(Y_eq * 0.5, Y_eq * 1.5, 100)
        
        r_is = IS_intercept - IS_slope * Y_vals
        r_lm = LM_intercept + LM_Slope * Y_vals
        
        df_is = pd.DataFrame({'Output (Y)': Y_vals, 'Interest Rate (r)': r_is, 'Curve': 'IS'})
        df_lm = pd.DataFrame({'Output (Y)': Y_vals, 'Interest Rate (r)': r_lm, 'Curve': 'LM'})
        
        df_chart = pd.concat([df_is, df_lm])
        
        # Filter negative r
        # df_chart = df_chart[df_chart['Interest Rate (r)'] >= 0]
        
        chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('Output (Y)', scale=alt.Scale(zero=False)),
            y=alt.Y('Interest Rate (r)', scale=alt.Scale(zero=False)),
            color=alt.Color('Curve', scale=alt.Scale(domain=['IS', 'LM'], range=['red', 'blue']))
        )
        
        eq_point = alt.Chart(pd.DataFrame({'Y': [Y_eq], 'r': [r_eq]})).mark_point(
            size=200, fill='black', color='black'
        ).encode(x='Y', y='r', tooltip=['Y', 'r'])
        
        st.altair_chart((chart + eq_point).interactive(), use_container_width=True)
        
        st.info(f"""
        {txt['eq_res']}
        - **{txt['eq_y']}** {Y_eq:.2f}
        - **{txt['eq_r']}** {r_eq:.2f}%
        """)

# --- TAB 2: AD-AS ---
with tab2:
    st.markdown(f"### {txt['adas_title']}")
    st.markdown(txt['adas_intro'])
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader(txt['shock_params'])
        ad_shock = st.slider(txt['ad_shock'], -10.0, 10.0, 0.0, help=f"{txt['pos_shock']} = Demand Pull, {txt['neg_shock']} = Demand Shock")
        sras_shock = st.slider(txt['sras_shock'], -10.0, 10.0, 0.0, help=f"{txt['neg_shock']} = Cost Push (Oil price spike)")
        
    with c2:
        # AD: P = 100 - Y + AD_shock
        # SRAS: P = 10 + Y + SRAS_shock
        # LRAS: Y = 45 (Potential Output)
        
        Y_pot = 45
        
        # Equilibrium
        # 100 - Y + ad = 10 + Y + sras
        # 90 + ad - sras = 2Y
        Y_eq = (90 + ad_shock - sras_shock) / 2
        P_eq = 100 - Y_eq + ad_shock
        
        # Visualization
        Y_range = np.linspace(20, 70, 100)
        P_ad = 100 - Y_range + ad_shock
        P_sras = 10 + Y_range + sras_shock
        
        df_ad = pd.DataFrame({'Output (Y)': Y_range, 'Price Level (P)': P_ad, 'Curve': 'AD'})
        df_sras = pd.DataFrame({'Output (Y)': Y_range, 'Price Level (P)': P_sras, 'Curve': 'SRAS'})
        df_lras = pd.DataFrame({'Output (Y)': [Y_pot, Y_pot], 'Price Level (P)': [0, 100], 'Curve': 'LRAS'})
        
        chart_adas = alt.Chart(pd.concat([df_ad, df_sras])).mark_line().encode(
            x='Output (Y)', y='Price Level (P)', color='Curve'
        )
        
        chart_lras = alt.Chart(df_lras).mark_line(strokeDash=[5,5], color='green').encode(
            x='Output (Y)', y='Price Level (P)'
        )
        
        eq_p = alt.Chart(pd.DataFrame({'Y': [Y_eq], 'P': [P_eq]})).mark_point(
            size=200, fill='black', color='black'
        ).encode(x='Y', y='P')
        st.altair_chart((base_macro + lras_line + eq_macro).interactive(), use_container_width=True)
        
        gap = Y_macro_eq - 8
        st.metric("Output Gap (Y - Y*)", f"{gap:.2f}")
        if gap > 0:
            st.warning("⚠️ Inflationary Gap (Overheating)")
        elif gap < 0:
            st.error("⚠️ Recessionary Gap")
