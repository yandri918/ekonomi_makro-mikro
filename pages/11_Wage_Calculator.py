import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Regional Wage Calculator", page_icon="👷", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "👷 Regional Wage (UMR) Calculator",
        'subtitle': "Calculate **Minimum Wage Increase** (PP 51/2023) vs **Real Living Cost** (KHL).",
        'tab1': "📜 Official Regulation (PP 51/2023)",
        'tab2': "🛒 Decent Living Cost (KHL)",
        'current_umr': "Current Minimum Wage (Rp)",
        'inflation': "Yearly Inflation (%)",
        'growth': "Economic Growth (%)",
        'alpha': "Alpha (Labor Contribution Index)",
        'alpha_help': "Regulatory range: 0.10 - 0.30. Higher value = Workers get a bigger share of growth.",
        'calc_btn': "💰 Calculate New Wage",
        'result_title': "Calculation Result",
        'new_wage': "New Minimum Wage:",
        'increase': "Increase Amount:",
        'formula_exp': "Formula Explanation",
        'formula_desc': "**New Wage = Old Wage + (Old Wage x (Inflation + (Growth x Alpha)))**",
        'insight_official': """
        **What does this mean?**
        - Because Inflation is **{inf:.2f}%**, wages must go up to keep up with prices.
        - The Economy grew by **{gro:.2f}%**, and workers get a share of **{alp}** (Alpha).
        - Total Increase: **{pct:.2f}%**.
        """,
        'khl_title': "Estimate Real Living Needs",
        'food': "Food Cost (Monthly)",
        'housing': "Housing/Rent (Monthly)",
        'transport': "Transport (Monthly)",
        'health': "Health & Education",
        'clothing': "Clothing & Others",
        'total_khl': "Total Decent Living Cost (KHL)",
        'gap_title': "Gap: Wage vs Needs",
        'gap_surplus': "Surplus (Savings)",
        'gap_deficit': "Deficit (Need Side Hustle)",
        'purchasing_power': "🍔 Purchasing Power (Big Mac Equivalent)",
        'rice_equiv': "🍚 Rice Equivalent (kg)",
        'egg_equiv': "🥚 Egg Equivalent (kg)",
    },
    'ID': {
        'title': "👷 Kalkulator UMR & Upah Layak",
        'subtitle': "Hitung Kenaikan **UMR/UMP** (PP 51/2023) vs **Kebutuhan Hidup Layak** (KHL).",
        'tab1': "📜 Rumus Resmi (PP 51/2023)",
        'tab2': "🛒 Kebutuhan Hidup Layak (KHL)",
        'current_umr': "UMR Saat Ini (Rp)",
        'inflation': "Inflasi Tahunan (%)",
        'growth': "Pertumbuhan Ekonomi Daerah (%)",
        'alpha': "Alpha (Indeks Kontribusi Tenaga Kerja)",
        'alpha_help': "Rentang aturan: 0.10 - 0.30. Nilai makin tinggi = Buruh dapat porsi lebih besar dari pertumbuhan ekonomi.",
        'calc_btn': "💰 Hitung Upah Baru",
        'result_title': "Hasil Perhitungan",
        'new_wage': "UMR Baru:",
        'increase': "Besar Kenaikan:",
        'formula_exp': "Penjelasan Rumus",
        'formula_desc': "**UMR Baru = UMR Lama + (UMR Lama x (Inflasi + (Pertumbuhan x Alpha)))**",
        'insight_official': """
        **Penjelasan Mudah:**
        - Karena harga barang naik (**Inflasi {inf:.2f}%**), upah harus naik agar daya beli tetap.
        - Ekonomi daerah tumbuh **{gro:.2f}%**, dan aturan menetapkan buruh "menikmati" **{alp}** (nilai Alpha) dari pertumbuhan itu.
        - **Kesimpulan:** Upah naik total sebesar **{pct:.2f}%**.
        """,
        'khl_title': "Estimasi Kebutuhan Riil",
        'food': "Biaya Makan (Sebulan)",
        'housing': "Sewa Kost/Rumah (Sebulan)",
        'transport': "Transportasi (Sebulan)",
        'health': "Kesehatan & Pendidikan",
        'clothing': "Sandang & Lainnya",
        'total_khl': "Total Kebutuhan Hidup Layak (KHL)",
        'gap_title': "Selisih: UMR vs Kebutuhan",
        'gap_surplus': "Surplus (Bisa Nabung)",
        'gap_deficit': "Defisit (Perlu Cari Tambahan)",
        'purchasing_power': "🍔 Daya Beli (Indeks Makan)",
        'rice_equiv': "🍚 Setara Beras (kg)",
        'egg_equiv': "🥚 Setara Telur (kg)",
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- TABS ---
tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])

# Global var for comparison
final_wage_calc = 0

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        current_wage = st.number_input(txt['current_umr'], value=5000000.0, step=100000.0)
        inflation = st.number_input(txt['inflation'], value=3.0, step=0.1)
        growth = st.number_input(txt['growth'], value=5.2, step=0.1)
        # Alpha Constraint
        alpha = st.slider(txt['alpha'], 0.10, 0.30, 0.20, step=0.01, help=txt['alpha_help'])
    
    with col2:
        # PP 51/2023 Formula
        # Adjustment Value = Inflation + (Growth * Alpha)
        # Note: In some specific cases (if growth < consumption), formula differs, but we verify standard case.
        adj_percent = inflation + (growth * alpha)
        increase_amount = current_wage * (adj_percent / 100)
        new_wage = current_wage + increase_amount
        final_wage_calc = new_wage
        
        st.subheader(txt['result_title'])
        st.metric(txt['new_wage'], f"Rp {new_wage:,.0f}", delta=f"+ Rp {increase_amount:,.0f} (+{adj_percent:.2f}%)")
        
        st.info(txt['insight_official'].format(inf=inflation, gro=growth, alp=alpha, pct=adj_percent))
        
        st.markdown(txt['formula_exp'])
        st.markdown(txt['formula_desc'])

with tab2:
    st.markdown("Simulasikan apakah UMR tersebut cukup untuk hidup layak?")
    
    c_food = st.number_input(txt['food'], value=1500000.0, step=50000.0)
    c_house = st.number_input(txt['housing'], value=800000.0, step=50000.0)
    c_trans = st.number_input(txt['transport'], value=400000.0, step=10000.0)
    c_health = st.number_input(txt['health'], value=300000.0, step=10000.0)
    c_cloth = st.number_input(txt['clothing'], value=500000.0, step=10000.0)
    
    total_khl = c_food + c_house + c_trans + c_health + c_cloth
    
    st.divider()
    
    k_col1, k_col2 = st.columns(2)
    
    with k_col1:
        st.metric(txt['total_khl'], f"Rp {total_khl:,.0f}")
        
        gap = final_wage_calc - total_khl
        if gap > 0:
            st.success(f"**{txt['gap_surplus']}: Rp {gap:,.0f}**")
        else:
            st.error(f"**{txt['gap_deficit']}: -Rp {abs(gap):,.0f}**")

    with k_col2:
        st.subheader(txt['purchasing_power'])
        # Simplified prices
        price_rice = 14000 # per kg
        price_egg = 28000 # per kg
        
        rice_qty = final_wage_calc / price_rice
        egg_qty = final_wage_calc / price_egg
        
        st.write(f"**{txt['rice_equiv']}**: {rice_qty:,.1f} kg")
        st.write(f"**{txt['egg_equiv']}**: {egg_qty:,.1f} kg")
        
        # Simple Bar Chart Comparison
        df_comp = pd.DataFrame({
            'Category': ['UMR Baru (New Wage)', 'KHL (Needs)'],
            'Value': [final_wage_calc, total_khl]
        })
        
        chart = alt.Chart(df_comp).mark_bar().encode(
            x='Category',
            y='Value',
            color=alt.Color('Category', scale=alt.Scale(domain=['UMR Baru (New Wage)', 'KHL (Needs)'], range=['green', 'red']))
        )
        st.altair_chart(chart, use_container_width=True)
