import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Economic Indices", page_icon="🔢", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🔢 Economic Indices: CPI & PPP",
        'tab1': "🛒 CPI & Inflation Calculator",
        'tab2': "🍔 PPP & Big Mac Index",
        'cpi_title': "1. Consumer Price Index (CPI) Calculator",
        'cpi_intro': "Build a **Market Basket** of goods to calculate CPI and Inflation Rate.",
        'basket_editor': "Edit Market Basket:",
        'item': "Item",
        'qty': "Quantity",
        'base_price': "Base Year Price ($)",
        'curr_price': "Current Year Price ($)",
        'res': "Results:",
        'cost_base': "- Cost of Basket (Base Year):",
        'cpi_base': "- CPI (Base Year):",
        'cost_curr': "- Cost of Basket (Current):",
        'cpi_curr': "- CPI (Current):",
        'inflation': "- Inflation Rate:",
        'ppp_title': "2. Purchasing Power Parity (PPP)",
        'ppp_intro': "Understand PPP using the famous **Big Mac Index** concept.",
        'compare_to': "Compare Currency to USD ($)",
        'local_curr': "Local Currency Name",
        'bm_price_local': "Price of Big Mac in Local Currency",
        'bm_price_us': "Price of Big Mac in USD ($)",
        'ex_rate': "Actual Exchange Rate (Local/USD)",
        'ppp_calc': "PPP Calculations:",
        'implied_rate': "- Implied PPP Exchange Rate:",
        'valuation': "- Valuation vs USD:",
        'over': "OVERVALUED",
        'under': "UNDERVALUED",
        'fair': "FAIR VALUE"
    },
    'ID': {
        'title': "🔢 Indeks Ekonomi: IHK & PPP",
        'tab1': "🛒 Kalkulator IHK & Inflasi",
        'tab2': "🍔 PPP & Indeks Big Mac",
        'cpi_title': "1. Kalkulator Indeks Harga Konsumen (IHK)",
        'cpi_intro': "Buat **Keranjang Belanja** barang untuk menghitung IHK dan Tingkat Inflasi.",
        'basket_editor': "Edit Keranjang Belanja:",
        'item': "Barang",
        'qty': "Kuantitas",
        'base_price': "Harga Tahun Dasar ($)",
        'curr_price': "Harga Tahun Berjalan ($)",
        'res': "Hasil:",
        'cost_base': "- Biaya Keranjang (Thn Dasar):",
        'cpi_base': "- IHK (Thn Dasar):",
        'cost_curr': "- Biaya Keranjang (Sekarang):",
        'cpi_curr': "- IHK (Sekarang):",
        'inflation': "- Tingkat Inflasi:",
        'ppp_title': "2. Paritas Daya Beli (PPP)",
        'ppp_intro': "Pahami PPP menggunakan konsep **Indeks Big Mac** yang terkenal.",
        'compare_to': "Bandingkan Mata Uang thd USD ($)",
        'local_curr': "Nama Mata Uang Lokal",
        'bm_price_local': "Harga Big Mac (Mata Uang Lokal)",
        'bm_price_us': "Harga Big Mac di USD ($)",
        'ex_rate': "Nilai Tukar Aktual (Lokal/USD)",
        'ppp_calc': "Perhitungan PPP:",
        'implied_rate': "- Nilai Tukar PPP Implisit:",
        'valuation': "- Valuasi thd USD:",
        'over': "DINILAI TERLALU TINGGI (Overvalued)",
        'under': "DINILAI TERLALU RENDAH (Undervalued)",
        'fair': "NILAI WAJAR"
    }
}

txt = T[lang]

st.title(txt['title'])

tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])

with tab1:
    st.markdown(f"### {txt['cpi_title']}")
    st.markdown(txt['cpi_intro'])
    
    # Initial Data
    default_data = pd.DataFrame([
        {txt['item']: "Apples", txt['qty']: 10, txt['base_price']: 1.00, txt['curr_price']: 1.50},
        {txt['item']: "Bread", txt['qty']: 5, txt['base_price']: 2.00, txt['curr_price']: 2.20},
        {txt['item']: "Gasoline", txt['qty']: 20, txt['base_price']: 3.00, txt['curr_price']: 3.50},
        {txt['item']: "Rent", txt['qty']: 1, txt['base_price']: 500.00, txt['curr_price']: 550.00},
    ])
    
    st.subheader(txt['basket_editor'])
    edited_df = st.data_editor(default_data, num_rows="dynamic")
    
    # Calculations
    # Cost Base = Sum(Qty * BasePrice)
    cost_base = (edited_df[txt['qty']] * edited_df[txt['base_price']]).sum()
    cost_curr = (edited_df[txt['qty']] * edited_df[txt['curr_price']]).sum()
    
    cpi_base = 100.0 # By definition
    cpi_curr = (cost_curr / cost_base) * 100 if cost_base > 0 else 0
    inflation_rate = ((cpi_curr - cpi_base) / cpi_base) * 100
    
    st.markdown(f"### {txt['res']}")
    col_c1, col_c2 = st.columns(2)
    col_c1.metric(txt['cost_base'], f"${cost_base:,.2f}")
    col_c1.metric(txt['cpi_base'], f"{cpi_base:.1f}")
    
    col_c2.metric(txt['cost_curr'], f"${cost_curr:,.2f}")
    col_c2.metric(txt['cpi_curr'], f"{cpi_curr:.1f}")
    
    st.success(f"{txt['inflation']} **{inflation_rate:.2f}%**")
    
    st.latex(r"CPI = \frac{\text{Cost of Basket}_{current}}{\text{Cost of Basket}_{base}} \times 100")

with tab2:
    st.markdown(f"### {txt['ppp_title']}")
    st.markdown(txt['ppp_intro'])
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader(txt['compare_to'])
        currency = st.text_input(txt['local_curr'], "IDR (Rupiah)")
        p_local = st.number_input(txt['bm_price_local'], value=50000.0, format="%.2f")
        p_us = st.number_input(txt['bm_price_us'], value=5.50)
        e_actual = st.number_input(txt['ex_rate'], value=15500.0)
        
    with col_p2:
        st.subheader(txt['ppp_calc'])
        
        # implied rate = P_local / P_us
        implied_rate = p_local / p_us
        
        # Valuation = (Implied - Actual) / Actual
        valuation_pct = ((implied_rate - e_actual) / e_actual) * 100
        
        st.metric(txt['implied_rate'], f"{implied_rate:,.2f} {currency}/USD")
        
        status = txt['fair']
        color = "off"
        if valuation_pct > 10: 
            status = txt['over']
            color = "inverse" # red usually
        elif valuation_pct < -10: 
            status = txt['under']
            color = "normal" # green usually
        
        st.metric(txt['valuation'], f"{valuation_pct:.2f}%", delta=valuation_pct, delta_color="inverse")
        st.info(f"The {currency} is **{status}** against the USD based on the Big Mac Index.")
