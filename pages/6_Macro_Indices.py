import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(page_title="Economic Indices", page_icon="🔢", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🔢 Consumer Price Index & Inflation Analyzer",
        'subtitle': "Professional CPI calculation with detailed inflation analysis and basket composition insights.",
        'tab1': "🛒 CPI Calculator",
        'tab2': "📊 Inflation Analysis",
        'tab3': "📈 Time Series Tracker",
        'cpi_title': "Consumer Price Index (CPI) Calculator",
        'cpi_intro': "Build a realistic **Market Basket** to calculate CPI and analyze inflation patterns.",
        'basket_editor': "Market Basket (Editable)",
        'category': "Category",
        'item': "Item",
        'weight': "Weight (%)",
        'qty': "Quantity",
        'unit': "Unit",
        'base_price': "Base Year Price (Rp)",
        'curr_price': "Current Price (Rp)",
        'results': "CPI Results",
        'cost_base': "Basket Cost (Base Year)",
        'cost_curr': "Basket Cost (Current)",
        'cpi_value': "CPI (Base=100)",
        'inflation_rate': "Inflation Rate",
        'breakdown': "Inflation Breakdown by Category",
        'contribution': "Contribution to Inflation",
        'price_change': "Price Change (%)",
        'core_inflation': "Core Inflation (ex. Food & Energy)",
        'headline_inflation': "Headline Inflation",
        'analysis_title': "Detailed Inflation Analysis",
        'volatile_items': "Most Volatile Items",
        'stable_items': "Most Stable Items",
        'recommendations': "Policy Recommendations",
        'tracker_title': "CPI Time Series Tracker",
        'add_period': "Add New Period",
        'period_name': "Period Name",
        'view_trend': "View Inflation Trend",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nProfessional CPI calculator used by central banks and statistical agencies to measure inflation and cost of living changes.",
        'story_insight': "**Key Insight:**\nCPI measures how much more expensive (or cheaper) a basket of goods becomes over time. It's the foundation for monetary policy decisions.",
        'story_users': "**Who needs this?**",
        'use_central_bank': "🏦 **Central Banks:** Monitor inflation for interest rate decisions.",
        'use_govt': "🏛️ **Government:** Adjust minimum wages, pensions, and subsidies.",
        'use_business': "🏢 **Businesses:** Plan pricing strategies and wage adjustments."
    },
    'ID': {
        'title': "🔢 Analisis Indeks Harga Konsumen & Inflasi",
        'subtitle': "Perhitungan IHK profesional dengan analisis inflasi detail dan wawasan komposisi keranjang.",
        'tab1': "🛒 Kalkulator IHK",
        'tab2': "📊 Analisis Inflasi",
        'tab3': "📈 Pelacak Time Series",
        'cpi_title': "Kalkulator Indeks Harga Konsumen (IHK)",
        'cpi_intro': "Buat **Keranjang Belanja** realistis untuk menghitung IHK dan menganalisis pola inflasi.",
        'basket_editor': "Keranjang Belanja (Dapat Diedit)",
        'category': "Kategori",
        'item': "Barang",
        'weight': "Bobot (%)",
        'qty': "Kuantitas",
        'unit': "Satuan",
        'base_price': "Harga Tahun Dasar (Rp)",
        'curr_price': "Harga Sekarang (Rp)",
        'results': "Hasil IHK",
        'cost_base': "Biaya Keranjang (Tahun Dasar)",
        'cost_curr': "Biaya Keranjang (Sekarang)",
        'cpi_value': "IHK (Basis=100)",
        'inflation_rate': "Tingkat Inflasi",
        'breakdown': "Rincian Inflasi per Kategori",
        'contribution': "Kontribusi terhadap Inflasi",
        'price_change': "Perubahan Harga (%)",
        'core_inflation': "Inflasi Inti (tanpa Pangan & Energi)",
        'headline_inflation': "Inflasi Umum",
        'analysis_title': "Analisis Inflasi Detail",
        'volatile_items': "Barang Paling Volatil",
        'stable_items': "Barang Paling Stabil",
        'recommendations': "Rekomendasi Kebijakan",
        'tracker_title': "Pelacak Time Series IHK",
        'add_period': "Tambah Periode Baru",
        'period_name': "Nama Periode",
        'view_trend': "Lihat Tren Inflasi",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nKalkulator IHK profesional yang digunakan bank sentral dan badan statistik untuk mengukur inflasi dan perubahan biaya hidup.",
        'story_insight': "**Wawasan Utama:**\nIHK mengukur seberapa mahal (atau murah) keranjang barang menjadi seiring waktu. Ini adalah fondasi untuk keputusan kebijakan moneter.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_central_bank': "🏦 **Bank Sentral:** Memantau inflasi untuk keputusan suku bunga.",
        'use_govt': "🏛️ **Pemerintah:** Menyesuaikan UMR, pensiun, dan subsidi.",
        'use_business': "🏢 **Bisnis:** Merencanakan strategi harga dan penyesuaian upah."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Initialize session state for time series
if 'cpi_history' not in st.session_state:
    st.session_state['cpi_history'] = []

# TABS
tab1, tab2, tab3 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3']])

# ========== TAB 1: CPI CALCULATOR ==========
with tab1:
    st.markdown(f"### {txt['cpi_title']}")
    st.info(txt['cpi_intro'])
    
    # Realistic Indonesian Market Basket (BPS-style)
    default_data = pd.DataFrame([
        # Food & Beverages (33.5%)
        {txt['category']: "Pangan", txt['item']: "Beras", txt['weight']: 5.0, txt['qty']: 10, txt['unit']: "kg", txt['base_price']: 12000, txt['curr_price']: 13500},
        {txt['category']: "Pangan", txt['item']: "Daging Ayam", txt['weight']: 3.5, txt['qty']: 2, txt['unit']: "kg", txt['base_price']: 35000, txt['curr_price']: 38000},
        {txt['category']: "Pangan", txt['item']: "Telur", txt['weight']: 2.0, txt['qty']: 1, txt['unit']: "kg", txt['base_price']: 28000, txt['curr_price']: 30000},
        {txt['category']: "Pangan", txt['item']: "Minyak Goreng", txt['weight']: 2.5, txt['qty']: 2, txt['unit']: "liter", txt['base_price']: 14000, txt['curr_price']: 16000},
        {txt['category']: "Pangan", txt['item']: "Gula Pasir", txt['weight']: 1.5, txt['qty']: 2, txt['unit']: "kg", txt['base_price']: 13000, txt['curr_price']: 14000},
        
        # Housing (25.8%)
        {txt['category']: "Perumahan", txt['item']: "Sewa Rumah/Kost", txt['weight']: 15.0, txt['qty']: 1, txt['unit']: "bulan", txt['base_price']: 1500000, txt['curr_price']: 1600000},
        {txt['category']: "Perumahan", txt['item']: "Listrik", txt['weight']: 5.0, txt['qty']: 1, txt['unit']: "bulan", txt['base_price']: 300000, txt['curr_price']: 320000},
        {txt['category']: "Perumahan", txt['item']: "Air", txt['weight']: 2.0, txt['qty']: 1, txt['unit']: "bulan", txt['base_price']: 50000, txt['curr_price']: 55000},
        
        # Transportation (15.7%)
        {txt['category']: "Transportasi", txt['item']: "Bensin Pertalite", txt['weight']: 8.0, txt['qty']: 20, txt['unit']: "liter", txt['base_price']: 10000, txt['curr_price']: 10000},
        {txt['category']: "Transportasi", txt['item']: "Ojek Online", txt['weight']: 4.0, txt['qty']: 10, txt['unit']: "trip", txt['base_price']: 15000, txt['curr_price']: 16000},
        
        # Education (7.5%)
        {txt['category']: "Pendidikan", txt['item']: "SPP Sekolah", txt['weight']: 5.0, txt['qty']: 1, txt['unit']: "bulan", txt['base_price']: 500000, txt['curr_price']: 525000},
        
        # Health (3.5%)
        {txt['category']: "Kesehatan", txt['item']: "Obat-obatan", txt['weight']: 2.0, txt['qty']: 1, txt['unit']: "bulan", txt['base_price']: 100000, txt['curr_price']: 105000},
        
        # Communication (4.0%)
        {txt['category']: "Komunikasi", txt['item']: "Pulsa/Paket Data", txt['weight']: 3.0, txt['qty']: 1, txt['unit']: "bulan", txt['base_price']: 100000, txt['curr_price']: 100000},
    ])
    
    st.subheader(txt['basket_editor'])
    edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True, hide_index=True)
    
    # Calculations
    edited_df['Base Cost'] = edited_df[txt['qty']] * edited_df[txt['base_price']]
    edited_df['Current Cost'] = edited_df[txt['qty']] * edited_df[txt['curr_price']]
    edited_df['Price Change (%)'] = ((edited_df[txt['curr_price']] - edited_df[txt['base_price']]) / edited_df[txt['base_price']] * 100).round(2)
    
    # Weighted calculations
    total_weight = edited_df[txt['weight']].sum()
    edited_df['Weighted Base'] = edited_df['Base Cost'] * (edited_df[txt['weight']] / total_weight)
    edited_df['Weighted Current'] = edited_df['Current Cost'] * (edited_df[txt['weight']] / total_weight)
    
    cost_base = edited_df['Weighted Base'].sum()
    cost_curr = edited_df['Weighted Current'].sum()
    
    cpi_base = 100.0
    cpi_curr = (cost_curr / cost_base) * 100 if cost_base > 0 else 0
    inflation_rate = ((cpi_curr - cpi_base) / cpi_base) * 100
    
    # Core inflation (excluding Food & Energy)
    core_df = edited_df[~edited_df[txt['category']].isin(['Pangan', 'Transportasi'])]
    core_base = core_df['Weighted Base'].sum()
    core_curr = core_df['Weighted Current'].sum()
    core_inflation = ((core_curr - core_base) / core_base) * 100 if core_base > 0 else 0
    
    st.markdown(f"### {txt['results']}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(txt['cost_base'], f"Rp {cost_base:,.0f}")
    col2.metric(txt['cost_curr'], f"Rp {cost_curr:,.0f}", delta=f"{cost_curr-cost_base:,.0f}")
    col3.metric(txt['cpi_value'], f"{cpi_curr:.2f}", delta=f"{cpi_curr-cpi_base:.2f}")
    col4.metric(txt['headline_inflation'], f"{inflation_rate:.2f}%", delta_color="inverse")
    
    st.metric(txt['core_inflation'], f"{core_inflation:.2f}%", delta_color="inverse")
    
    # Formula
    st.latex(r"CPI = \frac{\sum (Q_i \times P_{current,i}) \times W_i}{\sum (Q_i \times P_{base,i}) \times W_i} \times 100")
    
    # Category breakdown
    st.markdown(f"### {txt['breakdown']}")
    
    category_summary = edited_df.groupby(txt['category']).agg({
        'Weighted Base': 'sum',
        'Weighted Current': 'sum',
        txt['weight']: 'sum'
    }).reset_index()
    
    category_summary['Inflation (%)'] = ((category_summary['Weighted Current'] - category_summary['Weighted Base']) / category_summary['Weighted Base'] * 100).round(2)
    category_summary['Contribution'] = (category_summary['Inflation (%)'] * category_summary[txt['weight']] / 100).round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=category_summary[txt['category']],
        y=category_summary['Inflation (%)'],
        marker_color=['red' if x > inflation_rate else 'blue' for x in category_summary['Inflation (%)']],
        text=category_summary['Inflation (%)'].apply(lambda x: f"{x:.1f}%"),
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Inflation Rate by Category",
        xaxis_title="Category",
        yaxis_title="Inflation (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(category_summary, use_container_width=True, hide_index=True)

# ========== TAB 2: INFLATION ANALYSIS ==========
with tab2:
    st.markdown(f"### {txt['analysis_title']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {txt['volatile_items']}")
        volatile = edited_df.nlargest(5, 'Price Change (%)')[[txt['item'], 'Price Change (%)']].rename(columns={'Price Change (%)': txt['price_change']})
        st.dataframe(volatile, use_container_width=True, hide_index=True)
        
        st.markdown(f"#### {txt['stable_items']}")
        stable = edited_df.nsmallest(5, 'Price Change (%)')[[txt['item'], 'Price Change (%)']].rename(columns={'Price Change (%)': txt['price_change']})
        st.dataframe(stable, use_container_width=True, hide_index=True)
    
    with col2:
        # Contribution to inflation
        st.markdown(f"#### {txt['contribution']}")
        
        contribution_df = category_summary.sort_values('Contribution', ascending=False)
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=contribution_df[txt['category']],
            values=contribution_df['Contribution'].abs(),
            hole=.3
        )])
        fig_pie.update_layout(title="Contribution to Inflation by Category", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Policy Recommendations
    st.markdown(f"### {txt['recommendations']}")
    
    if inflation_rate > 6:
        st.error("🔴 **High Inflation Alert** (>6%)")
        st.write("**Recommended Actions:**")
        st.write("- 🏦 Central Bank: Consider raising interest rates")
        st.write("- 🏛️ Government: Review subsidy programs for volatile items")
        st.write("- 📊 Monitor supply chain disruptions")
    elif inflation_rate > 3:
        st.warning("🟡 **Moderate Inflation** (3-6%)")
        st.write("**Recommended Actions:**")
        st.write("- 🏦 Central Bank: Maintain current monetary stance")
        st.write("- 🏛️ Government: Monitor food and energy prices closely")
        st.write("- 📊 Track core inflation trends")
    else:
        st.success("🟢 **Low Inflation** (<3%)")
        st.write("**Recommended Actions:**")
        st.write("- 🏦 Central Bank: Consider accommodative policy if needed")
        st.write("- 🏛️ Government: Focus on growth-oriented policies")
        st.write("- 📊 Monitor for deflationary risks")
    
    # Insights
    st.info(f"""
    **Key Insights:**
    - Headline Inflation: {inflation_rate:.2f}%
    - Core Inflation: {core_inflation:.2f}%
    - Main Driver: {category_summary.nlargest(1, 'Contribution').iloc[0][txt['category']]} ({category_summary.nlargest(1, 'Contribution').iloc[0]['Contribution']:.2f}% contribution)
    - Most Volatile: {edited_df.nlargest(1, 'Price Change (%)').iloc[0][txt['item']]} (+{edited_df.nlargest(1, 'Price Change (%)').iloc[0]['Price Change (%)']:.1f}%)
    """)

# ========== TAB 3: TIME SERIES TRACKER ==========
with tab3:
    st.markdown(f"### {txt['tracker_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['add_period']}")
        period_name = st.text_input(txt['period_name'], value=datetime.now().strftime("%b %Y"))
        
        if st.button("Add Current CPI to History", type='primary'):
            st.session_state['cpi_history'].append({
                'Period': period_name,
                'CPI': cpi_curr,
                'Inflation': inflation_rate,
                'Core Inflation': core_inflation
            })
            st.success(f"Added {period_name} to history!")
            st.rerun()
        
        if st.button("Clear History"):
            st.session_state['cpi_history'] = []
            st.rerun()
    
    with col2:
        if len(st.session_state['cpi_history']) > 0:
            history_df = pd.DataFrame(st.session_state['cpi_history'])
            
            fig = make_subplots(rows=2, cols=1,
                               subplot_titles=("CPI Trend", "Inflation Rate Trend"))
            
            fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['CPI'], 
                                    mode='lines+markers', name='CPI', line=dict(color='blue')),
                         row=1, col=1)
            
            fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['Inflation'], 
                                    mode='lines+markers', name='Headline', line=dict(color='red')),
                         row=2, col=1)
            fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['Core Inflation'], 
                                    mode='lines+markers', name='Core', line=dict(color='green', dash='dash')),
                         row=2, col=1)
            
            fig.update_xaxes(title_text="Period", row=2, col=1)
            fig.update_yaxes(title_text="CPI", row=1, col=1)
            fig.update_yaxes(title_text="Inflation (%)", row=2, col=1)
            fig.update_layout(height=600)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.info("No historical data yet. Add periods to track CPI over time.")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_central_bank'])
        st.write(txt['use_govt'])
        st.write(txt['use_business'])
