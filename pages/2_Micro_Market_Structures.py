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
        'subtitle': "Compare how firms maximize profit under different market conditions.",
        'select_struct': "Select Market Structure:",
        'perf_comp': "Perfect Competition",
        'monopoly': "Monopoly",
        'mono_comp': "Monopolistic Competition",
        'oligopoly': "Oligopoly (Kinked Demand)",
        'cost_params': "⚙️ Cost Parameters",
        'fc': "Fixed Cost (FC)",
        'vc': "Variable Cost Linear (VC)",
        'dem_params': "💰 Demand Parameters",
        'mkt_price': "Market Price (P)",
        'perf_comp_info': "In Perfect Competition, Price is determined by the market. The firm is a price taker ($P = MR = AR$).",
        'dem_int': "Demand Intercept",
        'dem_slope': "Demand Slope",
        'monopoly_info': "A Monopolist faces the entire market demand. Marginal Revenue (MR) falls twice as fast as Price.",
        'mono_comp_info': "**Monopolistic Competition**: Many firms sell differentiated products (e.g., Restaurants). Demand is flatter (more elastic) than Monopoly because customers can switch to competitors.",
        'oligopoly_info': "**Oligopoly (Kinked Demand)**: Few giant firms (e.g., Airlines). If you raise price, rivals won't follow (you lose share). If you cut price, rivals follow (Price War). Strategy: Stick to rigid price.",
        'profit_max': "**Profit Maximization Analysis:**",
        'opt_q': "- Optimal Quantity ($Q^*$):",
        'opt_p': "- Optimal Price (Rp):",
        'atc_q': "- Average Total Cost at $Q^*$ (Rp):",
        'super_profit': "📈 Supernormal Profit:",
        'loss': "📉 Loss:",
        'normal_profit': "⚖️ Normal Profit (Break-even)",
        'where_mr_mc': "(where $MR = MC$)",
        'kink_price': "Kink Price ($P_0$)",
        'kink_qty': "Kink Quantity ($Q_0$)"
    },
    'ID': {
        'title': "🏭 Struktur Pasar & Teori Produksi",
        'subtitle': "Bandingkan bagaimana perusahaan memaksimalkan keuntungan dalam berbagai kondisi pasar.",
        'select_struct': "Pilih Struktur Pasar:",
        'perf_comp': "Persaingan Sempurna",
        'monopoly': "Monopoli",
        'mono_comp': "Persaingan Monopolistik",
        'oligopoly': "Oligopoli (Kurva Patah)",
        'cost_params': "⚙️ Parameter Biaya",
        'fc': "Biaya Tetap (FC)",
        'vc': "Biaya Variabel Linear (VC)",
        'dem_params': "💰 Parameter Permintaan",
        'mkt_price': "Harga Pasar (P)",
        'perf_comp_info': "Dalam Persaingan Sempurna, Harga ditentukan oleh pasar. Perusahaan adalah penerima harga ($P = MR = AR$).",
        'dem_int': "Intersep Permintaan",
        'dem_slope': "Kemiringan Permintaan",
        'monopoly_info': "Monopolis menghadapi seluruh permintaan pasar. Pendapatan Marginal (MR) turun dua kali lebih cepat dari Harga.",
        'mono_comp_info': "**Persaingan Monopolistik**: Banyak penjual produk beda tipis (contoh: Restoran, Cafe). Kurva lebih landai (elastis) dibanding Monopoli karena pelanggan bisa pindah ke pesaing.",
        'oligopoly_info': "**Oligopoli (Kurva Patah)**: Dikuasai segelintir raksasa (contoh: Operator Seluler). Jika harga naik, pesaing tidak ikut (pelanggan lari). Jika harga turun, pesaing ikut (Perang Harga). Strategi: Harga cenderung kaku.",
        'profit_max': "**Analisis Maksimisasi Laba:**",
        'opt_q': "- Kuantitas Optimal ($Q^*$):",
        'opt_p': "- Harga Optimal (Rp):",
        'atc_q': "- Rata-rata Total Biaya pada $Q^*$ (Rp):",
        'super_profit': "📈 Laba Supernormal:",
        'loss': "📉 Rugi:",
        'normal_profit': "⚖️ Laba Normal (Impas)",
        'where_mr_mc': "(dimana $MR = MC$)",
        'kink_price': "Harga Kaku ($P_0$)",
        'kink_qty': "Kuantitas Kaku ($Q_0$)"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

structure_type = st.radio(txt['select_struct'], 
                          [txt['perf_comp'], txt['monopoly'], txt['mono_comp'], txt['oligopoly']], 
                          horizontal=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### {txt['cost_params']}")
    # Total Cost = FC + VC*Q + alpha*Q^2 + beta*Q^3 (Cubic Cost Function for U-shaped MC/AC)
    fc = st.slider(txt['fc'], 10, 100, 50)
    vc_linear = st.slider(txt['vc'], 1, 10, 2)
    # alpha = 0.5 # Quadratic term implicitly handled in formulas below
    
    st.markdown("---")
    st.markdown(f"### {txt['dem_params']}")
    
    # Initialize defaults
    quantity_max = 50
    p_star, q_star, atc_at_qstar = 0, 0, 0
    
    if structure_type == txt['perf_comp']:
        market_price = st.slider(txt['mkt_price'], 10, 50, 20)
        st.info(txt['perf_comp_info'])
        quantity_max = 50
        
    elif structure_type == txt['monopoly']:
        intercept = st.slider(txt['dem_int'], 30, 100, 60)
        slope = st.slider(txt['dem_slope'], 0.5, 2.0, 1.0)
        st.info(txt['monopoly_info'])
        quantity_max = int(intercept / slope) if slope > 0 else 50
        
    elif structure_type == txt['mono_comp']:
        # Similar to Monopoly but high elasticity (low slope)
        intercept = st.slider(txt['dem_int'], 30, 80, 40)
        slope = st.slider(txt['dem_slope'], 0.1, 0.8, 0.4, help="Low slope = Elastic Demand")
        st.info(txt['mono_comp_info'])
        quantity_max = int(intercept / slope) if slope > 0 else 50
        
    elif structure_type == txt['oligopoly']:
        # Kink parameters
        kink_P = st.slider(txt['kink_price'], 20, 50, 30)
        kink_Q = st.slider(txt['kink_qty'], 10, 40, 20)
        st.info(txt['oligopoly_info'])
        quantity_max = kink_Q * 2

with col2:
    # Generate Data
    Q_range = np.linspace(0.1, quantity_max, 200)
    
    # Cost Functions (Quadratic TC -> Linear MC)
    # TC = FC + VC*Q + 0.1*Q^2
    tc = fc + vc_linear * Q_range + 0.1 * (Q_range**2)
    mc = vc_linear + 0.2 * Q_range
    atc = tc / Q_range
    
    # Revenue Logic
    price = np.zeros_like(Q_range)
    mr = np.zeros_like(Q_range)
    
    if structure_type == txt['perf_comp']:
        price = np.full_like(Q_range, market_price)
        mr = price
        
        # Equilibrium MC = P
        # vc + 0.2Q = P -> Q = (P - vc) / 0.2
        if market_price > vc_linear:
            q_star = (market_price - vc_linear) / 0.2
            p_star = market_price
        
    elif structure_type in [txt['monopoly'], txt['mono_comp']]:
        price = intercept - slope * Q_range
        mr = intercept - 2 * slope * Q_range
        
        # Equilibrium MC = MR
        # vc + 0.2Q = int - 2*slope*Q
        # Q(0.2 + 2*slope) = int - vc
        num = intercept - vc_linear
        den = 0.2 + 2 * slope
        q_star = num / den if den != 0 else 0
        p_star = intercept - slope * q_star
        
    elif structure_type == txt['oligopoly']:
        # Kinked Demand logic
        # Segment 1 (Q < Kink): Elastic (Flat)
        # Segment 2 (Q > Kink): Inelastic (Steep)
        
        slope1 = 0.5  # Elastic
        slope2 = 2.0  # Inelastic
        
        # Calculate intercepts so lines meet at (kink_Q, kink_P)
        # P = A - bQ -> A = P + bQ
        A1 = kink_P + slope1 * kink_Q
        A2 = kink_P + slope2 * kink_Q
        
        # Vectorized Price Calculation
        price = np.where(Q_range <= kink_Q, A1 - slope1 * Q_range, A2 - slope2 * Q_range)
        
        # Vectorized MR Calculation
        # MR1 = A1 - 2*slope1*Q
        # MR2 = A2 - 2*slope2*Q
        mr = np.where(Q_range <= kink_Q, A1 - 2 * slope1 * Q_range, A2 - 2 * slope2 * Q_range)
        
        # Determine Equilibrium
        # Check MC at Kink
        mc_at_kink = vc_linear + 0.2 * kink_Q
        mr_left_at_kink = A1 - 2 * slope1 * kink_Q
        mr_right_at_kink = A2 - 2 * slope2 * kink_Q
        
        # Does MC pass through the gap?
        # Gap is between mr_right (lower) and mr_left (upper)
        if mr_right_at_kink <= mc_at_kink <= mr_left_at_kink:
            # Sticky Price Equilibrium
            q_star = kink_Q
            p_star = kink_P
            st.success("🔒 **Sticky Price Logic**: MC passes through the MR Gap. Price stays rigid at Kink.")
        elif mc_at_kink < mr_right_at_kink:
            # Intersect on the right (very low MC)
            # 0.2Q + vc = A2 - 2*slope2*Q
            q_star = (A2 - vc_linear) / (0.2 + 2 * slope2)
            p_star = A2 - slope2 * q_star
            st.warning("📉 Low Cost Structure: Equilibrium shifts right of Kink.")
        else:
             # Intersect on the left (very high MC)
            q_star = (A1 - vc_linear) / (0.2 + 2 * slope1)
            p_star = A1 - slope1 * q_star
            st.warning("📈 High Cost Structure: Equilibrium shifts left of Kink.")
            
    # DataFrame for plotting
    df = pd.DataFrame({
        'Quantity': Q_range,
        'MC': mc,
        'ATC': atc,
        'MR': mr,
        'AR (Demand)': price
    })
    
    # Filter negatives
    df = df[df['Quantity'] <= quantity_max]
    df = df[df['AR (Demand)'] >= 0] 
    
    # Check bounds for q_star
    q_star = max(0, q_star)
    
    # Melt
    df_melt_cost = df.melt('Quantity', value_vars=['MC', 'ATC'], var_name='Type', value_name='Price')
    df_melt_rev = df.melt('Quantity', value_vars=['MR', 'AR (Demand)'], var_name='Type', value_name='Price')
    
    # Base Charts
    c_cost = alt.Chart(df_melt_cost).mark_line().encode(
        x='Quantity', y='Price', color=alt.Color('Type', scale=alt.Scale(range=['red', 'orange']))
    )
    c_rev = alt.Chart(df_melt_rev).mark_line(strokeDash=[5,5]).encode(
        x='Quantity', y='Price', color=alt.Color('Type', scale=alt.Scale(range=['blue', 'green']))
    )
    
    # Equilibrium Point
    point_df = pd.DataFrame({'Q': [q_star], 'P': [p_star]})
    c_pt = alt.Chart(point_df).mark_point(size=200, color='black', fill='black').encode(x='Q', y='P')
    c_txt = c_pt.mark_text(dy=-15, text=f"Eq: ({q_star:.1f}, {p_star:.1f})").encode()
    
    final_chart = (c_cost + c_rev + c_pt + c_txt).interactive()
    st.altair_chart(final_chart, use_container_width=True)
    
    # Metrics
    atc_val = (fc + vc_linear * q_star + 0.1 * q_star**2) / q_star if q_star > 0 else 0
    profit = (p_star - atc_val) * q_star
    
    st.markdown(txt['profit_max'])
    m1, m2, m3 = st.columns(3)
    m1.metric(txt['opt_q'].split(':')[0], f"{q_star:.2f}")
    m2.metric(txt['opt_p'].split(':')[0], f"Rp {p_star:,.2f}")
    m3.metric(txt['atc_q'].split(':')[0], f"Rp {atc_val:,.2f}")
    
    if profit > 1:
        st.success(f"**{txt['super_profit']} Rp {profit:,.2f}**")
    elif profit < -1:
        st.error(f"**{txt['loss']} Rp {profit:,.2f}**")
    else:
        st.info(f"**{txt['normal_profit']}**")


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
        'opt_p': "- Optimal Price (Rp):",
        'atc_q': "- Average Total Cost at $Q^*$ (Rp):",
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
        'opt_p': "- Harga Optimal (Rp):",
        'atc_q': "- Rata-rata Total Biaya pada $Q^*$ (Rp):",
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
        st.success(f"{txt['super_profit']} **Rp {profit:,.2f}**")
    elif profit < 0:
        st.error(f"{txt['loss']} **Rp {profit:,.2f}**")
    else:
        st.info(txt['normal_profit'])


