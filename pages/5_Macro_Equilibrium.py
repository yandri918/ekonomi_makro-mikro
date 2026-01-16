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
        'tab3': "📊 Policy & Growth",
        'islm_title': "1. IS-LM Model (Short Run)",
        'islm_intro': "Interaction between the **Goods Market (IS)** and **Money Market (LM)**.",
        'fiscal_policy': "🏛️ Fiscal Policy (IS Curve)",
        'G': "Govt Spending (G - Rp Trillion)",
        'T': "Taxes (T - Rp Trillion)",
        'MPC': "Marginal Propensity to Consume (MPC)",
        'monetary_policy': "🏦 Monetary Policy (LM Curve)",
        'Ms': "Money Supply (Ms - Rp Trillion)",
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
        'full_emp': "Full Employment",
        'tab3': "📊 Policy & Growth",
        'growth_title': "3. Economic Growth & Policy Multipliers",
        'growth_intro': "Calculate the impact of Fiscal and Monetary Policy on **GDP Growth**.",
        'current_state': "Current Economic State",
        'current_gdp': "Current Nominal GDP (Rp Trillion)",
        'fiscal_stimulus': "🏛️ Fiscal Stimulus / Contraction",
        'delta_G': "Change in Govt Spending ($\Delta G$)",
        'delta_T': "Change in Taxes ($\Delta T$)",
        'monetary_stimulus': "🏦 Monetary Stimulus",
        'delta_Ms': "Change in Money Supply ($\Delta Ms$)",
        'growth_res': "Growth Projection Results"
    },
    'ID': {
        'title': "⚖️ Keseimbangan Makroekonomi: IS-LM & AD-AS",
        'tab1': "📉 Model IS-LM",
        'tab2': "📈 Model AD-AS",
        'tab3': "📊 Pertumbuhan & Kebijakan",
        'islm_title': "1. Model IS-LM (Jangka Pendek)",
        'islm_intro': "Interaksi antara **Pasar Barang (IS)** dan **Pasar Uang (LM)**.",
        'fiscal_policy': "🏛️ Kebijakan Fiskal (Kurva IS)",
        'G': "Belanja Pemerintah (G - Rp Triliun)",
        'T': "Pajak (T - Rp Triliun)",
        'MPC': "Kecenderungan Mengkonsumsi (MPC)",
        'monetary_policy': "🏦 Kebijakan Moneter (Kurva LM)",
        'Ms': "Jumlah Uang Beredar (Ms - Rp Triliun)",
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
        'full_emp': "Kesempatan Kerja Penuh",
        'growth_title': "3. Pertumbuhan Ekonomi & Multiplier Kebijakan",
        'growth_intro': "Hitung dampak Kebijakan Fiskal dan Moneter terhadap **Pertumbuhan PDB**.",
        'current_state': "Kondisi Ekonomi Saat Ini",
        'current_gdp': "PDB Nominal Saat Ini (Rp Triliun)",
        'fiscal_stimulus': "🏛️ Stimulus / Kontraksi Fiskal",
        'delta_G': "Perubahan Belanja Pemerintah ($\Delta G$)",
        'delta_T': "Perubahan Pajak ($\Delta T$)",
        'monetary_stimulus': "🏦 Stimulus Moneter",
        'delta_Ms': "Perubahan Jml Uang Beredar ($\Delta Ms$)",
        'growth_res': "Hasil Proyeksi Pertumbuhan"
    }
}

txt = T[lang]

st.title(txt['title'])

tab1, tab2, tab3 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3']])

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
        st.altair_chart((chart_adas + chart_lras + eq_p).interactive(), use_container_width=True)
        
        gap = Y_eq - Y_pot
        status = txt['full_emp']
        if gap < 0: status = txt['recession']
        elif gap > 0: status = txt['inflation']
        
        st.info(f"""
        {txt['eq_res_adas']}
        - **output (Y*):** {Y_eq:.2f}
        - **{txt['p_lvl']}** {P_eq:.2f}
        - **{txt['gap']}** {gap:.2f} ({status})
        """)

# --- TAB 3: POLICY & GROWTH ---
with tab3:
    st.markdown(f"### {txt['growth_title']}")
    st.markdown(txt['growth_intro'])
    
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        st.subheader(txt['current_state'])
        current_gdp = st.number_input(txt['current_gdp'], value=20000.0, step=100.0)
        
        st.markdown("---")
        st.subheader(txt['fiscal_stimulus'])
        delta_G = st.number_input(txt['delta_G'], value=0.0, step=10.0, help="Change in Govt Spending")
        delta_T = st.number_input(txt['delta_T'], value=0.0, step=10.0, help="Change in Taxes (increase = contractionary)")
        
        st.markdown("---")
        st.subheader(txt['monetary_stimulus'])
        delta_Ms = st.number_input(txt['delta_Ms'], value=0.0, step=10.0)
        
    with col_g2:
        # Multipliers
        # MPC is from Tab 1 (shared state or re-declared? Better to re-declare or use session state if we want persistence, 
        # but for simplicity let's use a local MPC slider or assume a standard one)
        # To avoid confusion, let's add specific parameters for this calc
        
        st.subheader("⚙️ Analysis Parameters")
        mpc_grow = st.slider("MPC (Marginal Propensity to Consume)", 0.1, 0.9, 0.75, key="mpc_grow")
        tax_rate = st.slider("Tax Rate (t)", 0.0, 0.5, 0.2, key="tax_grow")
        
        # Calculations
        # 1. Fiscal Multiplier (Government Spending)
        # k_g = 1 / (1 - MPC*(1-t))
        k_g = 1 / (1 - mpc_grow * (1 - tax_rate))
        
        # 2. Tax Multiplier
        # k_t = -MPC / (1 - MPC*(1-t))
        k_t = -mpc_grow / (1 - mpc_grow * (1 - tax_rate))
        
        # 3. Monetary Impact (Simplified)
        # Assuming Delta Ms affects Interest Rate -> Investment -> GDP
        # We'll use a simplified 'Money Multiplier' or 'Transmission Coefficient'
        # Let's assume Delta Y_monetary = Delta Ms * Velocity (V is constant-ish) or similar proxy
        # For this edu simulation, let's say 1T Ms adds 0.8 * k_g to GDP (liquidity effect)
        monetary_coefficient = 0.8 * k_g
        
        # Total Changes
        impact_G = delta_G * k_g
        impact_T = delta_T * k_t # Note: delta_T positive means Tax HIKE -> Negative Impact
        impact_Ms = delta_Ms * monetary_coefficient
        
        total_change = impact_G + impact_T + impact_Ms
        new_gdp = current_gdp + total_change
        growth_rate = (total_change / current_gdp) * 100
        
        # Display Results
        st.markdown(f"### {txt['growth_res']}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Fiscal Multiplier (Gov)", f"{k_g:.2f}x")
        m2.metric("Tax Multiplier", f"{k_t:.2f}x")
        m3.metric("Projected Growth", f"{growth_rate:.2f}%", delta=f"{total_change:,.1f}", delta_color="normal")
        
        st.info(f"""
        **Projected GDP:** Rp {new_gdp:,.2f} Triliun
        - Impact from Gov Spending ($\Delta G$): Rp {impact_G:,.2f}
        - Impact from Taxes ($\Delta T$): Rp {impact_T:,.2f}
        - Impact from Monetary ($\Delta Ms$): Rp {impact_Ms:,.2f}
        """)
        
        # Visualization: Waterfall or Bar Chart
        data = pd.DataFrame({
            'Component': ['Initial GDP', 'Gov Spending Effect', 'Tax Effect', 'Monetary Effect'],
            'Value': [current_gdp, impact_G, impact_T, impact_Ms]
        })
        
        # Waterfall logic simulation in bar chart
        # Cumulative sum for waterfall? Or just a breakdown.
        # Let's do a simple component bar chart
        
        chart_growth = alt.Chart(data).mark_bar().encode(
            x=alt.X('Component', sort=None),
            y=alt.Y('Value', title='Rp Trilliun'),
            color=alt.condition(
                alt.datum.Value >= 0,
                alt.value("green"),
                alt.value("red")
            ),
            tooltip=['Component', alt.Tooltip('Value', format=',.2f')]
        ).properties(title="GDP Impact Analysis")
        
        st.altair_chart(chart_growth, use_container_width=True)
