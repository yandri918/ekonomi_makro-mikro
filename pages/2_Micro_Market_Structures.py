import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Market Structures", page_icon="🏭", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🏭 Market Structures & Production Theory",
        'subtitle': "Compare how firms maximize profit under **Perfect Competition** vs **Monopoly**.",
        'select_struct': "Select Market Structure:",
        'perf_comp': "Perfect Competition",
        'monopoly': "Monopoly",
        'cost_params': "⚙️ Cost Parameters",
        'fc': "Fixed Cost (FC)",
        'vc': "Variable Cost Linear (VC)",
        'dem_params': "💰 Demand Parameters",
        'mkt_price': "Market Price (P)",
        'perf_comp_info': "In Perfect Competition, Price is determined by the market. The firm is a price taker ($P = MR = AR$).",
        'dem_int': "Demand Intercept",
        'dem_slope': "Demand Slope",
        'monopoly_info': "A Monopolist faces the entire market demand. Marginal Revenue (MR) falls twice as fast as Price.",
        'profit_max': "**Profit Maximization Analysis:**",
        'opt_q': "- Optimal Quantity ($Q^*$):",
        'opt_p': "- Optimal Price ($P^*$):",
        'atc_q': "- Average Total Cost at $Q^*$:",
        'super_profit': "📈 Supernormal Profit:",
        'loss': "📉 Loss:",
        'normal_profit': "⚖️ Normal Profit (Break-even)",
        'where_mr_mc': "(where $MR = MC$)"
    },
    'ID': {
        'title': "🏭 Struktur Pasar & Teori Produksi",
        'subtitle': "Bandingkan bagaimana perusahaan memaksimalkan keuntungan dalam **Persaingan Sempurna** vs **Monopoli**.",
        'select_struct': "Pilih Struktur Pasar:",
        'perf_comp': "Persaingan Sempurna",
        'monopoly': "Monopoli",
        'cost_params': "⚙️ Parameter Biaya",
        'fc': "Biaya Tetap (FC)",
        'vc': "Biaya Variabel Linear (VC)",
        'dem_params': "💰 Parameter Permintaan",
        'mkt_price': "Harga Pasar (P)",
        'perf_comp_info': "Dalam Persaingan Sempurna, Harga ditentukan oleh pasar. Perusahaan adalah penerima harga ($P = MR = AR$).",
        'dem_int': "Intersep Permintaan",
        'dem_slope': "Kemiringan Permintaan",
        'monopoly_info': "Monopolis menghadapi seluruh permintaan pasar. Pendapatan Marginal (MR) turun dua kali lebih cepat dari Harga.",
        'profit_max': "**Analisis Maksimisasi Laba:**",
        'opt_q': "- Kuantitas Optimal ($Q^*$):",
        'opt_p': "- Harga Optimal ($P^*$):",
        'atc_q': "- Rata-rata Total Biaya pada $Q^*$:",
        'super_profit': "📈 Laba Supernormal:",
        'loss': "📉 Rugi:",
        'normal_profit': "⚖️ Laba Normal (Impas)",
        'where_mr_mc': "(dimana $MR = MC$)"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

structure_type = st.radio(txt['select_struct'], [txt['perf_comp'], txt['monopoly']], horizontal=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### {txt['cost_params']}")
    # Total Cost = FC + VC*Q + alpha*Q^2 + beta*Q^3 (Cubic Cost Function for U-shaped MC/AC)
    fc = st.slider(txt['fc'], 10, 100, 50)
    vc_linear = st.slider(txt['vc'], 1, 10, 2)
    alpha = 0.5 # Quadratic term
    
    st.markdown("---")
    st.markdown(f"### {txt['dem_params']}")
    
    if structure_type == txt['perf_comp']:
        market_price = st.slider(txt['mkt_price'], 10, 50, 20)
        st.info(txt['perf_comp_info'])
        quantity_max = 50
    else: # Monopoly
        intercept = st.slider(txt['dem_int'], 30, 100, 60)
        slope = st.slider(txt['dem_slope'], 0.5, 2.0, 1.0)
        st.info(txt['monopoly_info'])
        quantity_max = int(intercept / slope) if slope > 0 else 50
    
with col2:
    # Generate Data
    Q_range = np.linspace(0.1, quantity_max, 100) # Start from 0.1 to avoid division by zero for AC
    
    tc = fc + vc_linear * Q_range + 0.1 * (Q_range**2)
    mc = vc_linear + 0.2 * Q_range
    atc = tc / Q_range
    
    # Revenue Functions
    if structure_type == txt['perf_comp']:
        price = np.full_like(Q_range, market_price)
        tr = market_price * Q_range
        mr = price # MR = P
        ar = price # AR = P
        
        # Find Equilibrium: MC = MR => vc + 0.2Q = P => 0.2Q = P - vc => Q = (P - vc) / 0.2
        if market_price > vc_linear:
            q_star = (market_price - vc_linear) / 0.2
            p_star = market_price
        else:
            q_star = 0
            p_star = market_price
            
    else: # Monopoly
        # P = Intercept - Slope*Q
        price = intercept - slope * Q_range
        tr = price * Q_range
        # MR = Intercept - 2*Slope*Q
        mr = intercept - 2 * slope * Q_range
        ar = price
        
        # Find Equilibrium: MC = MR
        # vc + 0.2Q = int - 2*slope*Q
        # (0.2 + 2*slope)Q = int - vc
        if intercept > vc_linear:
            q_star = (intercept - vc_linear) / (0.2 + 2 * slope)
            p_star = intercept - slope * q_star
        else:
            q_star = 0
            p_star = 0

    # DataFrame
    df = pd.DataFrame({
        'Quantity': Q_range,
        'MC': mc,
        'ATC': atc,
        'MR': mr,
        'Average Revenue (Demand)': ar
    })
    
    # Filter for plotting range
    df = df[df['Quantity'] <= quantity_max]
    
    # Melt
    df_melted_costs = df.melt('Quantity', value_vars=['MC', 'ATC'], var_name='Cost Curves', value_name='Price')
    df_melted_revenue = df.melt('Quantity', value_vars=['MR', 'Average Revenue (Demand)'], var_name='Revenue Curves', value_name='Price')
    
    # Combine
    chart_costs = alt.Chart(df_melted_costs).mark_line().encode(
        x='Quantity', 
        y=alt.Y('Price', scale=alt.Scale(domain=[0, max(p_star*2, 100)])),
        color=alt.Color('Cost Curves', scale=alt.Scale(domain=['MC', 'ATC'], range=['red', 'orange']))
    )
    
    chart_rev = alt.Chart(df_melted_revenue).mark_line(strokeDash=[5,5]).encode(
        x='Quantity',
        y='Price',
        color=alt.Color('Revenue Curves', scale=alt.Scale(domain=['MR', 'Average Revenue (Demand)'], range=['green', 'blue']))
    )
    
    # Equilibrium Point
    eq_df = pd.DataFrame({'Quantity': [q_star], 'Price': [p_star]})
    point = alt.Chart(eq_df).mark_point(size=200, color='black').encode(x='Quantity', y='Price')
    text = point.mark_text(dx=10, dy=-10, text=f"Q*={q_star:.1f}, P*={p_star:.1f}").encode()
    
    st.altair_chart((chart_costs + chart_rev + point + text).interactive(), use_container_width=True)
    
    # Profit Calculation
    atc_at_qstar = (fc + vc_linear * q_star + 0.1 * (q_star**2)) / q_star if q_star > 0 else 0
    profit = (p_star - atc_at_qstar) * q_star
    
    st.markdown(txt['profit_max'])
    st.write(f"{txt['opt_q']} **{q_star:.2f}** {txt['where_mr_mc']}")
    st.write(f"{txt['opt_p']} **{p_star:.2f}**")
    st.write(f"{txt['atc_q']} **{atc_at_qstar:.2f}**")
    
    if profit > 0:
        st.success(f"{txt['super_profit']} **${profit:.2f}**")
    elif profit < 0:
        st.error(f"{txt['loss']} **${profit:.2f}**")
    else:
        st.info(txt['normal_profit'])


