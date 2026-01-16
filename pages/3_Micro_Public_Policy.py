import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Public Policy", page_icon="🏛️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🏛️ Public Policy Simulation",
        'intro': "Simulate the impact of government interventions on market equilibrium and welfare.",
        'select_policy': "Select Policy Type",
        'none': "None",
        'tax': "Tax (Per Unit)",
        'subsidy': "Subsidy (Per Unit)",
        'floor': "Price Floor (Minimum Wage)",
        'ceiling': "Price Ceiling",
        'params': "⚙️ Market Parameters",
        'demand_int': "Demand Intercept",
        'demand_slope': "Demand Slope",
        'supply_int': "Supply Intercept",
        'supply_slope': "Supply Slope",
        'policy_params': "⚙️ Policy Parameters",
        'tax_amt': "Tax Amount (Rp)",
        'sub_amt': "Subsidy Amount (Rp)",
        'floor_price': "Price Floor (Rp)",
        'ceiling_price': "Price Ceiling (Rp)",
        'eq_res': "**Initial Equilibrium (No Policy):**",
        'eq_p': "Price (Rp):",
        'eq_q': "Quantity ($Q^*$):",
        'policy_impact': "**Policy Impact Analysis:**",
        'cons_price': "Consumer Price (Rp):",
        'prod_price': "Producer Price (Rp):",
        'new_q': "New Quantity ($Q_{new}$):",
        'dwl': "Deadweight Loss (Rp)",
        'gov_rev': "Govt Revenue (Rp)",
        'gov_cost': "Govt Cost (Rp)",
        'surplus': "Surplus (Excess Supply):",
        'shortage': "Shortage (Excess Demand):",
        'qty_traded': "Quantity Traded:",
        'eff_floor': "Binding Price Floor",
        'ineff_floor': "Non-binding Price Floor (No Effect)",
        'eff_ceiling': "Binding Price Ceiling",
        'ineff_ceiling': "Non-binding Price Ceiling (No Effect)"
    },
    'ID': {
        'title': "🏛️ Simulasi Kebijakan Publik",
        'intro': "Simulasikan dampak intervensi pemerintah terhadap keseimbangan pasar dan kesejahteraan.",
        'select_policy': "Pilih Jenis Kebijakan",
        'none': "Tidak Ada",
        'tax': "Pajak (Per Unit)",
        'subsidy': "Subsidi (Per Unit)",
        'floor': "Harga Dasar (Upah Minimum)",
        'ceiling': "Harga Tertinggi (HET)",
        'params': "⚙️ Parameter Pasar",
        'demand_int': "Intersep Permintaan",
        'demand_slope': "Kemiringan Permintaan",
        'supply_int': "Intersep Penawaran",
        'supply_slope': "Kemiringan Penawaran",
        'policy_params': "⚙️ Parameter Kebijakan",
        'tax_amt': "Besaran Pajak (Rp)",
        'sub_amt': "Besaran Subsidi (Rp)",
        'floor_price': "Harga Dasar (Rp)",
        'ceiling_price': "Harga Tertinggi (Rp)",
        'eq_res': "**Keseimbangan Awal (Tanpa Kebijakan):**",
        'eq_p': "Harga (Rp):",
        'eq_q': "Kuantitas ($Q^*$):",
        'policy_impact': "**Analisis Dampak Kebijakan:**",
        'cons_price': "Harga Konsumen (Rp):",
        'prod_price': "Harga Produsen (Rp):",
        'new_q': "Kuantitas Baru ($Q_{new}$):",
        'dwl': "Deadweight Loss (Rp)",
        'gov_rev': "Pendapatan Pemerintah (Rp)",
        'gov_cost': "Biaya Pemerintah (Rp)",
        'surplus': "Surplus (Kelebihan Penawaran):",
        'shortage': "Kelangkaan (Kelebihan Permintaan):",
        'qty_traded': "Kuantitas Diperdagangkan:",
        'eff_floor': "Harga Dasar Efektif",
        'ineff_floor': "Harga Dasar Tidak Efektif (Tidak Ada Efek)",
        'eff_ceiling': "Harga Tertinggi Efektif",
        'ineff_ceiling': "Harga Tertinggi Tidak Efektif (Tidak Ada Efek)"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['intro'])

col1, col2 = st.columns([1, 2])

with col1:
    policy = st.selectbox(txt['select_policy'], [txt['none'], txt['tax'], txt['subsidy'], txt['floor'], txt['ceiling']])
    
    st.markdown("---")
    st.markdown(f"### {txt['params']}")
    a = st.slider(txt['demand_int'], 50, 200, 100)
    b = st.slider(txt['demand_slope'], 0.5, 2.0, 1.0)
    c = st.slider(txt['supply_int'], 0, 50, 20)
    d = st.slider(txt['supply_slope'], 0.5, 2.0, 1.0)
    
    st.markdown("---")
    magnitude = 0
    if policy == txt['tax']:
        st.markdown(f"### {txt['policy_params']}")
        magnitude = st.slider(txt['tax_amt'], 0, 50, 10)
    elif policy == txt['subsidy']:
        st.markdown(f"### {txt['policy_params']}")
        magnitude = st.slider(txt['sub_amt'], 0, 50, 10)
    elif policy == txt['floor']:
        st.markdown(f"### {txt['policy_params']}")
        # Set default near equilibrium
        magnitude = st.slider(txt['floor_price'], 0, 100, 50)
    elif policy == txt['ceiling']:
        st.markdown(f"### {txt['policy_params']}")
        magnitude = st.slider(txt['ceiling_price'], 0, 100, 30)

with col2:
    # 1. Base Equilibrium
    if b+d == 0: # Avoid division by zero if slopes are 0
        P_eq, Q_eq = 0, 0
    else:
        P_eq = (a - c) / (b + d)
        Q_eq = a - b * P_eq
    
    st.markdown(txt['eq_res'])
    c1, c2 = st.columns(2)
    c1.metric(txt['eq_p'], f"{P_eq:.2f}")
    c2.metric(txt['eq_q'], f"{Q_eq:.2f}")
    
    # 2. Policy Impact
    DWL = 0
    Gov_Rev = 0
    Gov_Cost = 0
    Q_new = Q_eq
    P_cons = P_eq
    P_prod = P_eq
    
    # Variables for DWL calculation in price controls
    Pd_at_Qnew = P_eq
    Ps_at_Qnew = P_eq

    # Logic
    if policy == txt['none']:
        Q_new = Q_eq
        P_cons = P_eq
        P_prod = P_eq
        
    elif policy == txt['tax']:
        # Supply shifts up by tax: P_s = (c + tax) + d*Q_s (Inverted Supply P = (Q-c)/d + tax)
        # easier: Q_d = a - b*P_c, Q_s = c + d*P_p, P_c - P_p = Tax
        # a - b(P_p + Tax) = c + d*P_p
        # a - b*Tax - c = (b+d)P_p
        P_prod = (a - c - b * magnitude) / (b + d)
        Q_new = c + d * P_prod
        P_cons = P_prod + magnitude
        
        DWL = 0.5 * (Q_eq - Q_new) * magnitude
        Gov_Rev = magnitude * Q_new
        
    elif policy == txt['subsidy']:
        # P_p - P_c = Subsidy
        # Q = a - b*P_c = c + d*P_p
        # a - b*P_c = c + d(P_c + Subsidy)
        # a - c - d*Subsidy = (b+d)P_c
        P_cons = (a - c - d * magnitude) / (b + d)
        Q_new = a - b * P_cons
        P_prod = P_cons + magnitude
        
        DWL = 0.5 * (Q_new - Q_eq) * magnitude
        Gov_Cost = magnitude * Q_new

    elif policy == txt['floor']:
        P_floor = magnitude
        if P_floor > P_eq: # Binding
            Q_d = a - b * P_floor
            Q_s = c + d * P_floor
            Q_traded = min(Q_d, Q_s) # Market Limiting Principle
            Surplus = Q_s - Q_d
            
            Q_new = Q_traded
            P_cons = P_floor # Consumers pay floor
            P_prod = P_floor # Producers get floor
            
            # DWL is area between Supply and Demand from Q_traded to Q_eq
            # Height at Q_traded: P_d = (a-Q)/b, P_s = (Q-c)/d
            Pd_at_Qnew = (a - Q_new) / b
            Ps_at_Qnew = (Q_new - c) / d 
            
            DWL = 0.5 * (Q_eq - Q_new) * (Pd_at_Qnew - Ps_at_Qnew)
            
            st.warning(f"⚠️ {txt['eff_floor']} ({txt['surplus']} {Surplus:.2f})")
        else:
            st.info(txt['ineff_floor'])
            
    elif policy == txt['ceiling']:
        P_ceiling = magnitude
        if P_ceiling < P_eq: # Binding
            Q_d = a - b * P_ceiling
            Q_s = c + d * P_ceiling
            Q_traded = min(Q_d, Q_s)
            Shortage = Q_d - Q_s
            
            Q_new = Q_traded
            P_cons = P_ceiling
            P_prod = P_ceiling
            
            # DWL
            Pd_at_Qnew = (a - Q_new) / b
            Ps_at_Qnew = (Q_new - c) / d
            DWL = 0.5 * (Q_eq - Q_new) * (Pd_at_Qnew - Ps_at_Qnew)
            
            st.warning(f"⚠️ {txt['eff_ceiling']} ({txt['shortage']} {Shortage:.2f})")
        else:
            st.info(txt['ineff_ceiling'])

    # Visualization
    P_max = (a / b) if b > 0 else 100
    prices = np.linspace(0, max(P_max * 1.2, P_cons*1.2, P_prod*1.2, P_eq*1.2, magnitude*1.2), 100)
    df = pd.DataFrame({'Price': prices})
    df['Demand'] = a - b * df['Price']
    df['Supply'] = c + d * df['Price']
    
    # New Supply curve for Tax (Visual only)
    if policy == txt['tax']:
         # S_tax: P = (Q-c)/d + tax -> Q = c + d(P - tax)
         df['Supply + Tax'] = c + d * (df['Price'] - magnitude)
    elif policy == txt['subsidy']:
        df['Supply + Subsidy'] = c + d * (df['Price'] + magnitude)
         
    df_melted = df.melt('Price', var_name='Type', value_name='Quantity')
    # Filter negative Q
    df_melted = df_melted[df_melted['Quantity'] >= 0]
    
    base_chart = alt.Chart(df_melted).mark_line().encode(
        x=alt.X('Quantity', title='Quantity'),
        y='Price',
        color='Type'
    )
    
    # Shade DWL if applicable
    if DWL > 0 and policy in [txt['tax'], txt['subsidy']]:
        dwl_df = pd.DataFrame([
            {'Quantity': Q_new, 'Price': P_cons},
            {'Quantity': Q_new, 'Price': P_prod},
            {'Quantity': Q_eq, 'Price': P_eq}
        ])
        dwl_area = alt.Chart(dwl_df).mark_area(opacity=0.3, color='gray').encode(
            x='Quantity', y='Price'
        )
        base_chart += dwl_area
    elif DWL > 0 and policy in [txt['floor'], txt['ceiling']]:
         dwl_df = pd.DataFrame([
            {'Quantity': Q_new, 'Price': Pd_at_Qnew},
            {'Quantity': Q_new, 'Price': Ps_at_Qnew},
            {'Quantity': Q_eq, 'Price': P_eq}
        ])
         dwl_area = alt.Chart(dwl_df).mark_area(opacity=0.3, color='gray').encode(
            x='Quantity', y='Price'
        )
         base_chart += dwl_area

    st.altair_chart(base_chart.interactive(), use_container_width=True)
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("New Quantity", f"{Q_new:.2f}", delta=f"{Q_new - Q_eq:.2f}")
    m2.metric("Deadweight Loss", f"{DWL:.2f}", delta_color="inverse")
    if policy == "Tax (Per Unit)":
        m3.metric("Gov Revenue", f"{Gov_Rev_Cost:.2f}")
    elif policy == "Subsidy (Per Unit)":
        m3.metric("Gov Cost", f"{abs(Gov_Rev_Cost):.2f}", delta_color="inverse")
        
    st.info("The Gray shaded area represents the **Deadweight Loss (DWL)**: the loss of economic efficiency when the equilibrium outcome is not achievable or not achieved.")

