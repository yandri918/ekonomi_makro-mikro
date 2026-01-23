import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from scipy import stats

st.set_page_config(page_title="CPI & Inflation Analysis", page_icon="🔢", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🔢 Advanced CPI & Inflation Analysis",
        'subtitle': "Professional CPI calculation with advanced statistical analysis, decomposition methods, and scientific insights.",
        'tab1': "🛒 CPI Calculator",
        'tab2': "📊 Inflation Analysis",
        'tab3': "📈 Time Series Tracker",
        'tab4': "📊 Statistical Analysis",
        'tab5': "🔬 Inflation Decomposition",
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
        # Statistical
        'stats_title': "Statistical Analysis",
        'volatility_metrics': "Volatility Metrics",
        'price_dispersion': "Price Dispersion Analysis",
        'std_dev': "Standard Deviation",
        'coef_var': "Coefficient of Variation",
        'price_range': "Price Range",
        'iqr': "Interquartile Range",
        # Decomposition
        'decomp_title': "Inflation Decomposition",
        'demand_pull': "Demand-Pull Inflation",
        'cost_push': "Cost-Push Inflation",
        'persistent': "Persistent Component",
        'transitory': "Transitory Component"
    },
    'ID': {
        'title': "🔢 Analisis IHK & Inflasi Lanjutan",
        'subtitle': "Perhitungan IHK profesional dengan analisis statistik lanjutan, metode dekomposisi, dan wawasan ilmiah.",
        'tab1': "🛒 Kalkulator IHK",
        'tab2': "📊 Analisis Inflasi",
        'tab3': "📈 Pelacak Time Series",
        'tab4': "📊 Analisis Statistik",
        'tab5': "🔬 Dekomposisi Inflasi",
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
        # Statistical
        'stats_title': "Analisis Statistik",
        'volatility_metrics': "Metrik Volatilitas",
        'price_dispersion': "Analisis Dispersi Harga",
        'std_dev': "Standar Deviasi",
        'coef_var': "Koefisien Variasi",
        'price_range': "Rentang Harga",
        'iqr': "Rentang Interkuartil",
        # Decomposition
        'decomp_title': "Dekomposisi Inflasi",
        'demand_pull': "Inflasi Tarikan Permintaan",
        'cost_push': "Inflasi Dorongan Biaya",
        'persistent': "Komponen Persisten",
        'transitory': "Komponen Sementara"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Initialize session state for time series
if 'cpi_history' not in st.session_state:
    st.session_state['cpi_history'] = []

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4'], txt['tab5']])

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

# ========== TAB 3: ENHANCED TIME SERIES TRACKER ==========
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
            
            # Calculate moving averages if enough data
            if len(history_df) >= 3:
                history_df['MA_3'] = history_df['Inflation'].rolling(window=3).mean()
            if len(history_df) >= 6:
                history_df['MA_6'] = history_df['Inflation'].rolling(window=6).mean()
            
            fig = make_subplots(rows=2, cols=1,
                               subplot_titles=("CPI Trend", "Inflation Rate Trend with Moving Averages"))
            
            fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['CPI'], 
                                    mode='lines+markers', name='CPI', line=dict(color='blue', width=2)),
                         row=1, col=1)
            
            fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['Inflation'], 
                                    mode='lines+markers', name='Headline', line=dict(color='red', width=2)),
                         row=2, col=1)
            fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['Core Inflation'], 
                                    mode='lines+markers', name='Core', line=dict(color='green', width=2, dash='dash')),
                         row=2, col=1)
            
            # Add moving averages if available
            if 'MA_3' in history_df.columns:
                fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['MA_3'], 
                                        mode='lines', name='MA(3)', line=dict(color='orange', width=1, dash='dot')),
                             row=2, col=1)
            if 'MA_6' in history_df.columns:
                fig.add_trace(go.Scatter(x=history_df['Period'], y=history_df['MA_6'], 
                                        mode='lines', name='MA(6)', line=dict(color='purple', width=1, dash='dot')),
                             row=2, col=1)
            
            fig.update_xaxes(title_text="Period", row=2, col=1)
            fig.update_yaxes(title_text="CPI", row=1, col=1)
            fig.update_yaxes(title_text="Inflation (%)", row=2, col=1)
            fig.update_layout(height=600)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Trend analysis
            if len(history_df) >= 3:
                st.markdown("### 📊 Trend Analysis")
                
                # Linear regression
                x = np.arange(len(history_df))
                y = history_df['Inflation'].values
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                
                col_t1, col_t2, col_t3 = st.columns(3)
                col_t1.metric("Trend Slope", f"{slope:.3f}%/period")
                col_t2.metric("R² (Fit Quality)", f"{r_value**2:.3f}")
                col_t3.metric("P-value", f"{p_value:.4f}")
                
                if slope > 0.1:
                    st.warning("⚠️ **Upward Trend**: Inflation is increasing over time")
                elif slope < -0.1:
                    st.success("✅ **Downward Trend**: Inflation is decreasing over time")
                else:
                    st.info("➡️ **Stable Trend**: Inflation is relatively stable")
            
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.info("No historical data yet. Add periods to track CPI over time.")

# ========== TAB 4: STATISTICAL ANALYSIS ==========
with tab4:
    st.markdown(f"### {txt['stats_title']}")
    
    # Volatility Metrics
    st.markdown(f"#### {txt['volatility_metrics']}")
    
    price_changes = edited_df['Price Change (%)'].values
    
    col1, col2, col3, col4 = st.columns(4)
    
    std_dev = np.std(price_changes)
    mean_change = np.mean(price_changes)
    coef_var = (std_dev / abs(mean_change)) * 100 if mean_change != 0 else 0
    price_range = np.max(price_changes) - np.min(price_changes)
    q75, q25 = np.percentile(price_changes, [75, 25])
    iqr = q75 - q25
    
    col1.metric(txt['std_dev'], f"{std_dev:.2f}%")
    col2.metric(txt['coef_var'], f"{coef_var:.1f}%")
    col3.metric(txt['price_range'], f"{price_range:.2f}%")
    col4.metric(txt['iqr'], f"{iqr:.2f}%")
    
    # Price Dispersion Analysis
    st.markdown(f"#### {txt['price_dispersion']}")
    
    fig_box = go.Figure()
    
    for category in edited_df[txt['category']].unique():
        cat_data = edited_df[edited_df[txt['category']] == category]['Price Change (%)']
        fig_box.add_trace(go.Box(y=cat_data, name=category))
    
    fig_box.update_layout(
        title="Price Change Distribution by Category",
        yaxis_title="Price Change (%)",
        height=400
    )
    
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Distribution Analysis
    st.markdown("#### Distribution Analysis")
    
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=price_changes, nbinsx=15, name='Price Changes',
                                    marker_color='lightblue'))
    fig_hist.update_layout(
        title="Distribution of Price Changes",
        xaxis_title="Price Change (%)",
        yaxis_title="Frequency",
        height=300
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Statistical Tests
    st.markdown("#### Statistical Insights")
    
    # Normality test
    _, p_norm = stats.normaltest(price_changes)
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.metric("Skewness", f"{stats.skew(price_changes):.3f}",
                 help="Measures asymmetry. 0 = symmetric, >0 = right-skewed, <0 = left-skewed")
        st.metric("Kurtosis", f"{stats.kurtosis(price_changes):.3f}",
                 help="Measures tail heaviness. 0 = normal, >0 = heavy tails, <0 = light tails")
    
    with col_s2:
        if p_norm < 0.05:
            st.warning("⚠️ **Non-Normal Distribution**: Price changes are not normally distributed")
        else:
            st.success("✅ **Normal Distribution**: Price changes follow normal distribution")
        
        if std_dev > 5:
            st.error("🔴 **High Volatility**: Significant price dispersion detected")
        elif std_dev > 2:
            st.warning("🟡 **Moderate Volatility**: Some price variation present")
        else:
            st.success("🟢 **Low Volatility**: Prices are relatively stable")

# ========== TAB 5: INFLATION DECOMPOSITION ==========
with tab5:
    st.markdown(f"### {txt['decomp_title']}")
    
    # Categorize inflation sources
    demand_categories = ['Perumahan', 'Pendidikan', 'Komunikasi']
    cost_categories = ['Pangan', 'Transportasi', 'Kesehatan']
    
    demand_df = edited_df[edited_df[txt['category']].isin(demand_categories)]
    cost_df = edited_df[edited_df[txt['category']].isin(cost_categories)]
    
    demand_base = demand_df['Weighted Base'].sum()
    demand_curr = demand_df['Weighted Current'].sum()
    demand_inflation = ((demand_curr - demand_base) / demand_base) * 100 if demand_base > 0 else 0
    
    cost_base = cost_df['Weighted Base'].sum()
    cost_curr = cost_df['Weighted Current'].sum()
    cost_inflation = ((cost_curr - cost_base) / cost_base) * 100 if cost_base > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(txt['demand_pull'], f"{demand_inflation:.2f}%",
                 help="Inflation from demand-side factors (housing, education, services)")
        st.metric(txt['cost_push'], f"{cost_inflation:.2f}%",
                 help="Inflation from supply-side factors (food, energy, health)")
    
    with col2:
        # Waterfall chart
        fig_waterfall = go.Figure(go.Waterfall(
            name="Inflation Decomposition",
            orientation="v",
            measure=["relative", "relative", "total"],
            x=["Demand-Pull", "Cost-Push", "Total Inflation"],
            y=[demand_inflation, cost_inflation, inflation_rate],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig_waterfall.update_layout(
            title="Inflation Decomposition Waterfall",
            height=300
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
    
    # Persistent vs Transitory
    st.markdown("### Persistent vs Transitory Components")
    
    # Items with high volatility are considered transitory
    volatility_threshold = std_dev
    persistent_items = edited_df[edited_df['Price Change (%)'].abs() <= volatility_threshold]
    transitory_items = edited_df[edited_df['Price Change (%)'].abs() > volatility_threshold]
    
    persistent_base = persistent_items['Weighted Base'].sum()
    persistent_curr = persistent_items['Weighted Current'].sum()
    persistent_inflation = ((persistent_curr - persistent_base) / persistent_base) * 100 if persistent_base > 0 else 0
    
    transitory_base = transitory_items['Weighted Base'].sum()
    transitory_curr = transitory_items['Weighted Current'].sum()
    transitory_inflation = ((transitory_curr - transitory_base) / transitory_base) * 100 if transitory_base > 0 else 0
    
    col_p1, col_p2 = st.columns(2)
    col_p1.metric(txt['persistent'], f"{persistent_inflation:.2f}%",
                 help="Stable, long-term inflation component")
    col_p2.metric(txt['transitory'], f"{transitory_inflation:.2f}%",
                 help="Temporary, volatile inflation component")
    
    # Insights
    st.markdown("### 🔬 Scientific Insights")
    
    if abs(demand_inflation) > abs(cost_inflation):
        st.info("📊 **Demand-Driven Inflation**: Inflation is primarily driven by demand-side factors. Monetary policy may be effective.")
    else:
        st.warning("📊 **Cost-Driven Inflation**: Inflation is primarily driven by supply-side factors. Supply-side policies may be needed.")
    
    if abs(transitory_inflation) > abs(persistent_inflation):
        st.success("✅ **Transitory Inflation**: Most inflation is temporary and may self-correct.")
    else:
        st.error("⚠️ **Persistent Inflation**: Inflation has become entrenched and may require policy intervention.")
    
    # Export data
    st.markdown("---")
    st.markdown("### 📥 Export Analysis")
    
    export_data = {
        'Metric': ['Headline Inflation', 'Core Inflation', 'Demand-Pull', 'Cost-Push', 'Persistent', 'Transitory', 'Volatility (Std Dev)'],
        'Value (%)': [inflation_rate, core_inflation, demand_inflation, cost_inflation, persistent_inflation, transitory_inflation, std_dev]
    }
    
    df_export = pd.DataFrame(export_data)
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Analysis (CSV)",
        data=csv,
        file_name='cpi_inflation_analysis.csv',
        mime='text/csv',
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Advanced CPI & Inflation Analysis | Scientific Methods</p>
    <p>🔢 Built for Central Banks, Statistical Agencies, and Economic Research</p>
</div>
""", unsafe_allow_html=True)
