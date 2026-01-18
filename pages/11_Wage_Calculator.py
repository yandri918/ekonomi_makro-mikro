import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Wage & Living Cost Analyzer", page_icon="👷", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "👷 Advanced Wage & Living Cost Analyzer",
        'subtitle': "Comprehensive analysis of minimum wage (PP 51/2023), living costs (KHL), and purchasing power across regions.",
        'tab1': "📜 Official Formula (PP 51/2023)",
        'tab2': "🛒 Detailed Living Cost (KHL)",
        'tab3': "📊 Regional Comparison",
        'tab4': "📈 Multi-Year Projection",
        # Tab 1
        'current_umr': "Current Minimum Wage (Rp)",
        'inflation': "Annual Inflation (%)",
        'growth': "Economic Growth (%)",
        'alpha': "Alpha (Labor Share)",
        'alpha_help': "Range: 0.10-0.30. Higher = Workers get bigger share of growth",
        'calculate': "Calculate New Wage",
        'results': "Calculation Results",
        'new_wage': "New Minimum Wage",
        'increase_amount': "Increase Amount",
        'increase_pct': "Increase Percentage",
        'formula': "Formula Breakdown",
        'inflation_component': "Inflation Component",
        'growth_component': "Growth Component",
        'total_component': "Total Increase",
        # Tab 2
        'khl_calculator': "Detailed KHL Calculator",
        'food_category': "Food & Beverages",
        'rice': "Rice (kg/month)",
        'rice_price': "Rice Price (Rp/kg)",
        'protein': "Protein (kg/month)",
        'protein_price': "Protein Price (Rp/kg)",
        'vegetables': "Vegetables (kg/month)",
        'veg_price': "Vegetable Price (Rp/kg)",
        'housing_category': "Housing",
        'rent': "Rent/Mortgage (Rp/month)",
        'utilities': "Utilities (Electricity, Water, Gas)",
        'transport_category': "Transportation",
        'fuel': "Fuel/Transport (Rp/month)",
        'health_edu_category': "Health & Education",
        'health': "Health (Rp/month)",
        'education': "Education (Rp/month)",
        'other_category': "Clothing & Others",
        'clothing': "Clothing (Rp/month)",
        'communication': "Communication (Rp/month)",
        'savings': "Savings/Emergency (Rp/month)",
        'total_khl': "Total KHL (Monthly)",
        'gap_analysis': "Gap Analysis",
        'wage_vs_khl': "Wage vs KHL",
        'surplus': "SURPLUS - Can Save",
        'deficit': "DEFICIT - Need Extra Income",
        'coverage_ratio': "Coverage Ratio",
        'purchasing_power': "Purchasing Power Indicators",
        'rice_equiv': "Rice Equivalent (kg)",
        'bigmac_equiv': "Big Mac Equivalent",
        # Tab 3
        'regional_comparison': "Regional Wage Comparison",
        'add_region': "Add Region",
        'region_name': "Region Name",
        'region_umr': "UMR (Rp)",
        'region_khl': "KHL (Rp)",
        'compare': "Compare Regions",
        'best_region': "Best Region (Highest Surplus)",
        'worst_region': "Worst Region (Highest Deficit)",
        # Tab 4
        'projection_title': "Multi-Year Wage Projection",
        'years': "Projection Years",
        'avg_inflation': "Average Inflation (%)",
        'avg_growth': "Average Growth (%)",
        'project': "Generate Projection",
        'year': "Year",
        'projected_wage': "Projected Wage",
        'projected_khl': "Projected KHL",
        'gap': "Gap",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nComprehensive tool for analyzing minimum wage adequacy, living costs, and purchasing power with regional comparisons and projections.",
        'story_insight': "**Key Insight:**\nOfficial wage formulas often lag behind real living costs. Understanding this gap is crucial for policy-making and labor negotiations.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Government:** Simulate policy impacts and set appropriate Alpha values.",
        'use_union': "📢 **Labor Unions:** Demonstrate wage inadequacy with data.",
        'use_hr': "🏢 **HR Departments:** Budget for wage increases and ensure compliance."
    },
    'ID': {
        'title': "👷 Analisis Lanjutan UMR & Biaya Hidup",
        'subtitle': "Analisis komprehensif upah minimum (PP 51/2023), biaya hidup (KHL), dan daya beli lintas wilayah.",
        'tab1': "📜 Rumus Resmi (PP 51/2023)",
        'tab2': "🛒 Rincian Biaya Hidup (KHL)",
        'tab3': "📊 Perbandingan Regional",
        'tab4': "📈 Proyeksi Multi-Tahun",
        # Tab 1
        'current_umr': "UMR Saat Ini (Rp)",
        'inflation': "Inflasi Tahunan (%)",
        'growth': "Pertumbuhan Ekonomi (%)",
        'alpha': "Alpha (Porsi Buruh)",
        'alpha_help': "Rentang: 0.10-0.30. Makin tinggi = Buruh dapat porsi lebih besar",
        'calculate': "Hitung Upah Baru",
        'results': "Hasil Perhitungan",
        'new_wage': "UMR Baru",
        'increase_amount': "Besar Kenaikan",
        'increase_pct': "Persentase Kenaikan",
        'formula': "Rincian Rumus",
        'inflation_component': "Komponen Inflasi",
        'growth_component': "Komponen Pertumbuhan",
        'total_component': "Total Kenaikan",
        # Tab 2
        'khl_calculator': "Kalkulator KHL Detail",
        'food_category': "Pangan & Minuman",
        'rice': "Beras (kg/bulan)",
        'rice_price': "Harga Beras (Rp/kg)",
        'protein': "Protein (kg/bulan)",
        'protein_price': "Harga Protein (Rp/kg)",
        'vegetables': "Sayuran (kg/bulan)",
        'veg_price': "Harga Sayuran (Rp/kg)",
        'housing_category': "Perumahan",
        'rent': "Sewa/Cicilan (Rp/bulan)",
        'utilities': "Utilitas (Listrik, Air, Gas)",
        'transport_category': "Transportasi",
        'fuel': "BBM/Transport (Rp/bulan)",
        'health_edu_category': "Kesehatan & Pendidikan",
        'health': "Kesehatan (Rp/bulan)",
        'education': "Pendidikan (Rp/bulan)",
        'other_category': "Sandang & Lainnya",
        'clothing': "Pakaian (Rp/bulan)",
        'communication': "Komunikasi (Rp/bulan)",
        'savings': "Tabungan/Darurat (Rp/bulan)",
        'total_khl': "Total KHL (Bulanan)",
        'gap_analysis': "Analisis Kesenjangan",
        'wage_vs_khl': "UMR vs KHL",
        'surplus': "SURPLUS - Bisa Nabung",
        'deficit': "DEFISIT - Perlu Tambahan",
        'coverage_ratio': "Rasio Cakupan",
        'purchasing_power': "Indikator Daya Beli",
        'rice_equiv': "Setara Beras (kg)",
        'bigmac_equiv': "Setara Big Mac",
        # Tab 3
        'regional_comparison': "Perbandingan UMR Regional",
        'add_region': "Tambah Wilayah",
        'region_name': "Nama Wilayah",
        'region_umr': "UMR (Rp)",
        'region_khl': "KHL (Rp)",
        'compare': "Bandingkan Wilayah",
        'best_region': "Wilayah Terbaik (Surplus Tertinggi)",
        'worst_region': "Wilayah Terburuk (Defisit Tertinggi)",
        # Tab 4
        'projection_title': "Proyeksi UMR Multi-Tahun",
        'years': "Tahun Proyeksi",
        'avg_inflation': "Rata-rata Inflasi (%)",
        'avg_growth': "Rata-rata Pertumbuhan (%)",
        'project': "Buat Proyeksi",
        'year': "Tahun",
        'projected_wage': "Proyeksi UMR",
        'projected_khl': "Proyeksi KHL",
        'gap': "Kesenjangan",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nAlat komprehensif untuk menganalisis kecukupan upah minimum, biaya hidup, dan daya beli dengan perbandingan regional dan proyeksi.",
        'story_insight': "**Wawasan Utama:**\nRumus upah resmi sering tertinggal dari biaya hidup riil. Memahami kesenjangan ini penting untuk pembuatan kebijakan dan negosiasi buruh.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Pemerintah:** Simulasi dampak kebijakan dan tetapkan nilai Alpha yang tepat.",
        'use_union': "📢 **Serikat Buruh:** Tunjukkan ketidakcukupan upah dengan data.",
        'use_hr': "🏢 **HRD:** Anggarkan kenaikan upah dan pastikan kepatuhan."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Initialize session state
if 'regions' not in st.session_state:
    st.session_state['regions'] = []

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ========== TAB 1: OFFICIAL FORMULA ==========
with tab1:
    st.markdown(f"### {txt['tab1']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        current_umr = st.number_input(txt['current_umr'], value=3500000.0, step=100000.0)
        inflation = st.slider(txt['inflation'], 0.0, 10.0, 3.5, 0.1)
        growth = st.slider(txt['growth'], -5.0, 10.0, 5.0, 0.1)
        alpha = st.slider(txt['alpha'], 0.10, 0.30, 0.20, 0.01, help=txt['alpha_help'])
        
        if st.button(txt['calculate'], type='primary'):
            # PP 51/2023 Formula
            inflation_component = inflation
            growth_component = growth * alpha
            total_increase_pct = inflation_component + growth_component
            
            increase_amount = current_umr * (total_increase_pct / 100)
            new_umr = current_umr + increase_amount
            
            st.session_state['official_results'] = {
                'new_umr': new_umr,
                'increase_amount': increase_amount,
                'increase_pct': total_increase_pct,
                'inflation_comp': inflation_component,
                'growth_comp': growth_component
            }
    
    with col2:
        if 'official_results' in st.session_state:
            results = st.session_state['official_results']
            
            st.markdown(f"### {txt['results']}")
            
            m1, m2, m3 = st.columns(3)
            m1.metric(txt['new_wage'], f"Rp {results['new_umr']:,.0f}")
            m2.metric(txt['increase_amount'], f"Rp {results['increase_amount']:,.0f}")
            m3.metric(txt['increase_pct'], f"{results['increase_pct']:.2f}%")
            
            st.markdown(f"### {txt['formula']}")
            
            # Formula breakdown
            fig = go.Figure(go.Waterfall(
                name="Components",
                orientation="v",
                measure=["absolute", "relative", "relative", "total"],
                x=[txt['current_umr'], txt['inflation_component'], txt['growth_component'], txt['new_wage']],
                y=[current_umr, results['increase_amount'] * (results['inflation_comp']/results['increase_pct']), 
                   results['increase_amount'] * (results['growth_comp']/results['increase_pct']), results['new_umr']],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            
            fig.update_layout(title="Wage Increase Breakdown", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Formula display
            st.latex(r"UMR_{new} = UMR_{old} \times (1 + \frac{Inflation + (Growth \times \alpha)}{100})")
            
            st.info(f"""
            **Breakdown:**
            - Inflation Component: {results['inflation_comp']:.2f}%
            - Growth Component: {growth:.2f}% × {alpha:.2f} = {results['growth_comp']:.2f}%
            - **Total Increase: {results['increase_pct']:.2f}%**
            """)

# ========== TAB 2: DETAILED KHL ==========
with tab2:
    st.markdown(f"### {txt['khl_calculator']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Food
        st.markdown(f"#### {txt['food_category']}")
        rice_qty = st.number_input(txt['rice'], value=10.0, step=0.5)
        rice_price = st.number_input(txt['rice_price'], value=13000.0, step=500.0)
        protein_qty = st.number_input(txt['protein'], value=5.0, step=0.5)
        protein_price = st.number_input(txt['protein_price'], value=35000.0, step=1000.0)
        veg_qty = st.number_input(txt['vegetables'], value=8.0, step=0.5)
        veg_price = st.number_input(txt['veg_price'], value=8000.0, step=500.0)
        
        food_cost = (rice_qty * rice_price) + (protein_qty * protein_price) + (veg_qty * veg_price)
        
        # Housing
        st.markdown(f"#### {txt['housing_category']}")
        rent = st.number_input(txt['rent'], value=1000000.0, step=50000.0)
        utilities = st.number_input(txt['utilities'], value=300000.0, step=10000.0)
        
        housing_cost = rent + utilities
        
        # Transport
        st.markdown(f"#### {txt['transport_category']}")
        fuel = st.number_input(txt['fuel'], value=400000.0, step=10000.0)
        
        # Health & Education
        st.markdown(f"#### {txt['health_edu_category']}")
        health = st.number_input(txt['health'], value=200000.0, step=10000.0)
        education = st.number_input(txt['education'], value=150000.0, step=10000.0)
        
        # Others
        st.markdown(f"#### {txt['other_category']}")
        clothing = st.number_input(txt['clothing'], value=150000.0, step=10000.0)
        communication = st.number_input(txt['communication'], value=100000.0, step=10000.0)
        savings = st.number_input(txt['savings'], value=200000.0, step=10000.0)
        
        total_khl = food_cost + housing_cost + fuel + health + education + clothing + communication + savings
        
        st.session_state['khl'] = total_khl
    
    with col2:
        st.markdown(f"### {txt['total_khl']}")
        st.metric("", f"Rp {total_khl:,.0f}")
        
        # Breakdown pie chart
        categories = {
            txt['food_category']: food_cost,
            txt['housing_category']: housing_cost,
            txt['transport_category']: fuel,
            'Health & Education': health + education,
            'Others': clothing + communication + savings
        }
        
        fig = go.Figure(data=[go.Pie(labels=list(categories.keys()), values=list(categories.values()), hole=.3)])
        fig.update_layout(title="KHL Breakdown by Category", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Gap analysis
        if 'official_results' in st.session_state:
            new_umr = st.session_state['official_results']['new_umr']
            
            st.markdown(f"### {txt['gap_analysis']}")
            
            gap = new_umr - total_khl
            coverage_ratio = (new_umr / total_khl) * 100
            
            g1, g2 = st.columns(2)
            g1.metric(txt['wage_vs_khl'], f"Rp {gap:,.0f}", delta=f"{gap:,.0f}")
            g2.metric(txt['coverage_ratio'], f"{coverage_ratio:.1f}%")
            
            if gap > 0:
                st.success(f"✅ {txt['surplus']}: Rp {gap:,.0f}")
            else:
                st.error(f"❌ {txt['deficit']}: Rp {abs(gap):,.0f}")
            
            # Purchasing power
            st.markdown(f"### {txt['purchasing_power']}")
            
            rice_equiv = new_umr / rice_price
            bigmac_equiv = new_umr / 50000  # Assuming Big Mac = Rp 50,000
            
            p1, p2 = st.columns(2)
            p1.metric(txt['rice_equiv'], f"{rice_equiv:,.1f} kg")
            p2.metric(txt['bigmac_equiv'], f"{bigmac_equiv:,.1f}")

# ========== TAB 3: REGIONAL COMPARISON ==========
with tab3:
    st.markdown(f"### {txt['regional_comparison']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['add_region']}")
        
        region_name = st.text_input(txt['region_name'], value="Jakarta")
        region_umr = st.number_input(txt['region_umr'], value=4900000.0, step=100000.0, key='reg_umr')
        region_khl = st.number_input(txt['region_khl'], value=4500000.0, step=100000.0, key='reg_khl')
        
        if st.button("Add to Comparison"):
            st.session_state['regions'].append({
                'Region': region_name,
                'UMR': region_umr,
                'KHL': region_khl,
                'Gap': region_umr - region_khl,
                'Coverage': (region_umr / region_khl) * 100
            })
            st.success(f"Added {region_name}!")
    
    with col2:
        if len(st.session_state['regions']) > 0:
            df_regions = pd.DataFrame(st.session_state['regions'])
            
            st.dataframe(df_regions.style.highlight_max(subset=['Gap'], color='lightgreen')
                        .highlight_min(subset=['Gap'], color='lightcoral'), 
                        use_container_width=True, hide_index=True)
            
            # Visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(name='UMR', x=df_regions['Region'], y=df_regions['UMR'], marker_color='blue'))
            fig.add_trace(go.Bar(name='KHL', x=df_regions['Region'], y=df_regions['KHL'], marker_color='red'))
            
            fig.update_layout(
                title="UMR vs KHL by Region",
                xaxis_title="Region",
                yaxis_title="Amount (Rp)",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Best/Worst
            best_idx = df_regions['Gap'].idxmax()
            worst_idx = df_regions['Gap'].idxmin()
            
            b1, b2 = st.columns(2)
            b1.success(f"🏆 {txt['best_region']}: {df_regions.iloc[best_idx]['Region']} (Rp {df_regions.iloc[best_idx]['Gap']:,.0f})")
            b2.error(f"⚠️ {txt['worst_region']}: {df_regions.iloc[worst_idx]['Region']} (Rp {df_regions.iloc[worst_idx]['Gap']:,.0f})")
        else:
            st.info("Add regions to compare")

# ========== TAB 4: MULTI-YEAR PROJECTION ==========
with tab4:
    st.markdown(f"### {txt['projection_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        years = st.slider(txt['years'], 1, 10, 5)
        avg_inflation = st.slider(txt['avg_inflation'], 0.0, 10.0, 3.5, 0.1, key='proj_inf')
        avg_growth = st.slider(txt['avg_growth'], 0.0, 10.0, 5.0, 0.1, key='proj_growth')
        alpha_proj = st.slider(txt['alpha'], 0.10, 0.30, 0.20, 0.01, key='proj_alpha')
        
        base_umr = st.number_input(txt['current_umr'], value=3500000.0, step=100000.0, key='proj_base')
        base_khl = st.number_input("Base KHL (Rp)", value=3200000.0, step=100000.0)
        
        if st.button(txt['project'], type='primary'):
            projections = []
            
            current_umr = base_umr
            current_khl = base_khl
            
            for year in range(1, years + 1):
                # UMR projection
                increase_pct = avg_inflation + (avg_growth * alpha_proj)
                current_umr = current_umr * (1 + increase_pct/100)
                
                # KHL projection (assume grows with inflation + 1%)
                current_khl = current_khl * (1 + (avg_inflation + 1)/100)
                
                gap = current_umr - current_khl
                
                projections.append({
                    txt['year']: year,
                    txt['projected_wage']: current_umr,
                    txt['projected_khl']: current_khl,
                    txt['gap']: gap
                })
            
            st.session_state['projections'] = projections
    
    with col2:
        if 'projections' in st.session_state:
            df_proj = pd.DataFrame(st.session_state['projections'])
            
            st.dataframe(df_proj, use_container_width=True, hide_index=True)
            
            # Visualization
            fig = make_subplots(rows=2, cols=1,
                               subplot_titles=("UMR vs KHL Projection", "Gap Projection"))
            
            fig.add_trace(go.Scatter(x=df_proj[txt['year']], y=df_proj[txt['projected_wage']], 
                                    mode='lines+markers', name='UMR', line=dict(color='blue')),
                         row=1, col=1)
            fig.add_trace(go.Scatter(x=df_proj[txt['year']], y=df_proj[txt['projected_khl']], 
                                    mode='lines+markers', name='KHL', line=dict(color='red')),
                         row=1, col=1)
            
            fig.add_trace(go.Bar(x=df_proj[txt['year']], y=df_proj[txt['gap']], name='Gap',
                                marker_color=['green' if x > 0 else 'red' for x in df_proj[txt['gap']]]),
                         row=2, col=1)
            
            fig.update_xaxes(title_text="Year", row=2, col=1)
            fig.update_yaxes(title_text="Amount (Rp)", row=1, col=1)
            fig.update_yaxes(title_text="Gap (Rp)", row=2, col=1)
            fig.update_layout(height=700)
            
            st.plotly_chart(fig, use_container_width=True)

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_govt'])
        st.write(txt['use_union'])
        st.write(txt['use_hr'])
