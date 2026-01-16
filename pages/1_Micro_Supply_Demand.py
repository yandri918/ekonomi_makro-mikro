import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Supply & Demand", page_icon="⚖️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "⚖️ Microeconomics: Supply, Demand & Elasticity",
        'tab1': "📉 Supply & Demand Simulation",
        'tab2': "🧮 Elasticity Calculator",
        'sd_title': "1. Market Equilibrium Simulator",
        'sd_intro': "Adjust the slopes and intercepts to see how **Supply** and **Demand** shifts affect the equilibrium price ($P^*$) and quantity ($Q^*$).",
        'params': "⚙️ Parameters",
        'dem_func': "**Demand Function:** $Q_d = a - bP$",
        'a_help': "Changes consumer willingness to buy (Income, Tastes)",
        'b_help': "Responsiveness of consumers to price changes",
        'sup_func': "**Supply Function:** $Q_s = c + dP$",
        'c_help': "Changes production costs/technology",
        'd_help': "Responsiveness of producers to price changes",
        'a_label': "Demand Intercept (a) - Shift Demand",
        'b_label': "Demand Slope (b) - Elasticity",
        'c_label': "Supply Intercept (c) - Shift Supply",
        'd_label': "Supply Slope (d) - Elasticity",
        'error_intercept': "Supply Intercept must be lower than Demand Intercept for a valid market!",
        'eq_result': "**Market Equilibrium:**",
        'qty': "Quantity (Q)",
        'price': "Price (P)",
        'el_title': "2. Elasticity Calculator",
        'el_intro': "Calculate **Price Elasticity of Demand (PED)** using the Midpoint Method.",
        'p1': "Initial Price (P1)",
        'p2': "New Price (P2)",
        'q1': "Initial Quantity (Q1)",
        'q2': "New Quantity (Q2)",
        'calc_btn': "Calculate Elasticity",
        'zero_err': "Price change cannot be zero.",
        'elastic': "Result: **ELASTIC** (Consumers are sensitive to price changes)",
        'inelastic': "Result: **INELASTIC** (Consumers are not very sensitive)",
        'unitary': "Result: **UNITARY ELASTIC**"
    },
    'ID': {
        'title': "⚖️ Ekonomi Mikro: Permintaan, Penawaran & Elastisitas",
        'tab1': "📉 Simulasi Permintaan & Penawaran",
        'tab2': "🧮 Kalkulator Elastisitas",
        'sd_title': "1. Simulator Keseimbangan Pasar",
        'sd_intro': "Atur kemiringan dan intersep untuk melihat bagaimana pergeseran **Permintaan** dan **Penawaran** mempengaruhi harga ($P^*$) dan kuantitas ($Q^*$) keseimbangan.",
        'params': "⚙️ Parameter",
        'dem_func': "**Fungsi Permintaan:** $Q_d = a - bP$",
        'a_help': "Mengubah keinginan beli konsumen (Pendapatan, Selera)",
        'b_help': "Responsivitas konsumen terhadap perubahan harga",
        'sup_func': "**Fungsi Penawaran:** $Q_s = c + dP$",
        'c_help': "Mengubah biaya produksi/teknologi",
        'd_help': "Responsivitas produsen terhadap perubahan harga",
        'a_label': "Intersep Permintaan (a) - Geser Permintaan",
        'b_label': "Kemiringan Permintaan (b) - Elastisitas",
        'c_label': "Intersep Penawaran (c) - Geser Penawaran",
        'd_label': "Kemiringan Penawaran (d) - Elastisitas",
        'error_intercept': "Intersep Penawaran harus lebih rendah dari Intersep Permintaan!",
        'eq_result': "**Keseimbangan Pasar:**",
        'qty': "Kuantitas (Q)",
        'price': "Harga (P)",
        'el_title': "2. Kalkulator Elastisitas",
        'el_intro': "Hitung **Elastisitas Harga Permintaan (PED)** menggunakan Metode Titik Tengah.",
        'p1': "Harga Awal (P1)",
        'p2': "Harga Baru (P2)",
        'q1': "Kuantitas Awal (Q1)",
        'q2': "Kuantitas Baru (Q2)",
        'calc_btn': "Hitung Elastisitas",
        'zero_err': "Perubahan harga tidak boleh nol.",
        'elastic': "Hasil: **ELASTIS** (Konsumen peka terhadap perubahan harga)",
        'inelastic': "Hasil: **INELASTIS** (Konsumen tidak terlalu peka)",
        'unitary': "Hasil: **ELASTIS UNITER**"
    }
}

txt = T[lang]

st.title(txt['title'])

tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])

# --- TAB 1: SUPPLY & DEMAND ---
with tab1:
    st.markdown(f"### {txt['sd_title']}")
    st.markdown(txt['sd_intro'])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader(txt['params'])
        
        st.markdown(txt['dem_func'])
        a = st.slider(txt['a_label'], 50, 200, 100, help=txt['a_help'])
        b = st.slider(txt['b_label'], 0.5, 5.0, 1.0, step=0.1, help=txt['b_help'])
        
        st.markdown("---")
        
        st.markdown(txt['sup_func'])
        c = st.slider(txt['c_label'], 0, 100, 20, help=txt['c_help'])
        d = st.slider(txt['d_label'], 0.5, 5.0, 1.0, step=0.1, help=txt['d_help'])

    with col2:
        # 1. Calculate Equilibrium
        if c >= a:
            st.error(txt['error_intercept'])
            P_eq = 0
            Q_eq = 0
        else:
            P_eq = (a - c) / (b + d)
            Q_eq = a - b * P_eq

        # 2. Generate Data for Plotting
        # Create a price range around the equilibrium
        P_max = (a / b) if b > 0 else 100
        prices = np.linspace(0, max(P_max, P_eq * 1.5), 100)
        
        df = pd.DataFrame({'Price': prices})
        df['Demand'] = a - b * df['Price']
        df['Supply'] = c + d * df['Price']
        
        # Filter negative quantities
        df = df[(df['Demand'] >= 0) & (df['Supply'] >= 0)]
        
        # Melt for Altair
        df_melted = df.melt('Price', var_name='Type', value_name='Quantity')

        # 3. Plotting
        base = alt.Chart(df_melted).encode(
            x=alt.X('Quantity', title=txt['qty']),
            y=alt.Y('Price', title=txt['price'])
        )
        
        lines = base.mark_line(size=3).encode(
            color=alt.Color('Type', scale=alt.Scale(domain=['Demand', 'Supply'], range=['#FF4B4B', '#1C83E1']))
        )
        
        # Equilibrium Point
        eq_point = alt.Chart(pd.DataFrame({'Price': [P_eq], 'Quantity': [Q_eq]})).mark_point(
            size=200, fill='black', color='black'
        ).encode(
            x='Quantity', y='Price',
            tooltip=[alt.Tooltip('Price', format=',.2f'), alt.Tooltip('Quantity', format=',.2f')]
        )
        
        # Text labels for Equilibrium
        eq_text = eq_point.mark_text(
            align='left', baseline='bottom', dx=7, dy=-7, fontSize=14
        ).encode(
            text=alt.value(f"E ({Q_eq:.1f}, {P_eq:.1f})")
        )

        st.altair_chart((lines + eq_point + eq_text).interactive(), use_container_width=True)

        st.info(f"""
        {txt['eq_result']}
        - **{txt['price']} ($P^*$):** {P_eq:.2f}
        - **{txt['qty']} ($Q^*$):** {Q_eq:.2f}
        """)

# --- TAB 2: ELASTICITY ---
with tab2:
    st.markdown(f"### {txt['el_title']}")
    st.markdown(txt['el_intro'])
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        P1 = st.number_input(txt['p1'], value=10.0)
        P2 = st.number_input(txt['p2'], value=12.0)
        
    with col_e2:
        Q1 = st.number_input(txt['q1'], value=100.0)
        Q2 = st.number_input(txt['q2'], value=80.0)
        
    if st.button(txt['calc_btn']):
        # Midpoint Formula
        delta_Q = Q2 - Q1
        avg_Q = (Q2 + Q1) / 2
        pct_change_Q = delta_Q / avg_Q
        
        delta_P = P2 - P1
        avg_P = (P2 + P1) / 2
        pct_change_P = delta_P / avg_P
        
        if pct_change_P == 0:
            st.error(txt['zero_err'])
        else:
            PED = abs(pct_change_Q / pct_change_P)
            
            st.metric("Price Elasticity of Demand (|Ed|)", f"{PED:.2f}")
            
            if PED > 1:
                st.success(txt['elastic'])
            elif PED < 1:
                st.warning(txt['inelastic'])
            else:
                st.info(txt['unitary'])
            
            st.latex(r"E_d = \left| \frac{\% \Delta Q}{\% \Delta P} \right| = \left| \frac{(Q_2 - Q_1) / [(Q_2 + Q_1)/2]}{(P_2 - P_1) / [(P_2 + P_1)/2]} \right|")


