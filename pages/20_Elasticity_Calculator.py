import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Elasticity Calculator", page_icon="📐", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "📐 Advanced Elasticity Calculator",
        'subtitle': "Comprehensive elasticity analysis for pricing strategy, revenue optimization, and market analysis.",
        'tab1': "📊 Price Elasticity of Demand (PED)",
        'tab2': "💰 Revenue Optimization",
        'tab3': "📈 Other Elasticities",
        'tab4': "🎯 Business Applications",
        # PED Tab
        'ped_title': "Price Elasticity of Demand Calculator",
        'calculation_method': "Calculation Method",
        'midpoint': "Midpoint Method (Arc Elasticity)",
        'point': "Point Method (Point Elasticity)",
        'regression': "Regression-Based",
        'input_data': "Input Data",
        'initial_price': "Initial Price (P₁)",
        'new_price': "New Price (P₂)",
        'initial_qty': "Initial Quantity (Q₁)",
        'new_qty': "New Quantity (Q₂)",
        'calculate': "Calculate Elasticity",
        'results': "Results",
        'elasticity_value': "Elasticity (ε)",
        'interpretation': "Interpretation",
        'elastic': "ELASTIC (|ε| > 1)",
        'inelastic': "INELASTIC (|ε| < 1)",
        'unit_elastic': "UNIT ELASTIC (|ε| = 1)",
        'perfectly_elastic': "PERFECTLY ELASTIC (|ε| = ∞)",
        'perfectly_inelastic': "PERFECTLY INELASTIC (|ε| = 0)",
        'price_change': "Price Change (%)",
        'qty_change': "Quantity Change (%)",
        'revenue_impact': "Revenue Impact",
        # Revenue Tab
        'revenue_title': "Revenue Optimization Analysis",
        'current_situation': "Current Situation",
        'current_price': "Current Price",
        'current_quantity': "Current Quantity",
        'elasticity_estimate': "Elasticity Estimate",
        'price_scenarios': "Price Change Scenarios",
        'scenario': "Scenario",
        'price_change_pct': "Price Change (%)",
        'new_price_val': "New Price",
        'new_quantity_val': "New Quantity",
        'new_revenue': "New Revenue",
        'revenue_change': "Revenue Change",
        'optimal_pricing': "Optimal Pricing Strategy",
        # Other Elasticities Tab
        'income_elasticity': "Income Elasticity of Demand (YED)",
        'cross_elasticity': "Cross-Price Elasticity (XED)",
        'supply_elasticity': "Price Elasticity of Supply (PES)",
        'income': "Income",
        'related_price': "Related Product Price",
        'quantity_supplied': "Quantity Supplied",
        'normal_good': "NORMAL GOOD (YED > 0)",
        'inferior_good': "INFERIOR GOOD (YED < 0)",
        'luxury_good': "LUXURY GOOD (YED > 1)",
        'necessity': "NECESSITY (0 < YED < 1)",
        'substitute': "SUBSTITUTE (XED > 0)",
        'complement': "COMPLEMENT (XED < 0)",
        'unrelated': "UNRELATED (XED ≈ 0)",
        # Business Applications Tab
        'business_title': "Business Applications & Recommendations",
        'pricing_strategy': "Pricing Strategy Recommendations",
        'market_analysis': "Market Analysis",
        'competitive_position': "Competitive Position",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nAdvanced elasticity calculator for pricing decisions, revenue optimization, and market strategy.",
        'story_insight': "**Key Insight:**\nElasticity determines whether raising prices increases or decreases revenue. Essential for pricing strategy.",
        'story_users': "**Who needs this?**",
        'use_business': "🏢 **Businesses:** Optimize pricing for maximum revenue.",
        'use_govt': "🏛️ **Government:** Predict tax revenue and subsidy impacts.",
        'use_analyst': "📊 **Analysts:** Assess market competitiveness and demand patterns."
    },
    'ID': {
        'title': "📐 Kalkulator Elastisitas Lanjutan",
        'subtitle': "Analisis elastisitas komprehensif untuk strategi harga, optimasi pendapatan, dan analisis pasar.",
        'tab1': "📊 Elastisitas Harga Permintaan (PED)",
        'tab2': "💰 Optimasi Pendapatan",
        'tab3': "📈 Elastisitas Lainnya",
        'tab4': "🎯 Aplikasi Bisnis",
        # PED Tab
        'ped_title': "Kalkulator Elastisitas Harga Permintaan",
        'calculation_method': "Metode Perhitungan",
        'midpoint': "Metode Titik Tengah (Arc Elasticity)",
        'point': "Metode Titik (Point Elasticity)",
        'regression': "Berbasis Regresi",
        'input_data': "Input Data",
        'initial_price': "Harga Awal (P₁)",
        'new_price': "Harga Baru (P₂)",
        'initial_qty': "Kuantitas Awal (Q₁)",
        'new_qty': "Kuantitas Baru (Q₂)",
        'calculate': "Hitung Elastisitas",
        'results': "Hasil",
        'elasticity_value': "Elastisitas (ε)",
        'interpretation': "Interpretasi",
        'elastic': "ELASTIS (|ε| > 1)",
        'inelastic': "INELASTIS (|ε| < 1)",
        'unit_elastic': "ELASTIS UNITER (|ε| = 1)",
        'perfectly_elastic': "ELASTIS SEMPURNA (|ε| = ∞)",
        'perfectly_inelastic': "INELASTIS SEMPURNA (|ε| = 0)",
        'price_change': "Perubahan Harga (%)",
        'qty_change': "Perubahan Kuantitas (%)",
        'revenue_impact': "Dampak Pendapatan",
        # Revenue Tab
        'revenue_title': "Analisis Optimasi Pendapatan",
        'current_situation': "Situasi Saat Ini",
        'current_price': "Harga Saat Ini",
        'current_quantity': "Kuantitas Saat Ini",
        'elasticity_estimate': "Estimasi Elastisitas",
        'price_scenarios': "Skenario Perubahan Harga",
        'scenario': "Skenario",
        'price_change_pct': "Perubahan Harga (%)",
        'new_price_val': "Harga Baru",
        'new_quantity_val': "Kuantitas Baru",
        'new_revenue': "Pendapatan Baru",
        'revenue_change': "Perubahan Pendapatan",
        'optimal_pricing': "Strategi Harga Optimal",
        # Other Elasticities Tab
        'income_elasticity': "Elastisitas Pendapatan Permintaan (YED)",
        'cross_elasticity': "Elastisitas Silang Harga (XED)",
        'supply_elasticity': "Elastisitas Harga Penawaran (PES)",
        'income': "Pendapatan",
        'related_price': "Harga Produk Terkait",
        'quantity_supplied': "Kuantitas Ditawarkan",
        'normal_good': "BARANG NORMAL (YED > 0)",
        'inferior_good': "BARANG INFERIOR (YED < 0)",
        'luxury_good': "BARANG MEWAH (YED > 1)",
        'necessity': "KEBUTUHAN POKOK (0 < YED < 1)",
        'substitute': "BARANG SUBSTITUSI (XED > 0)",
        'complement': "BARANG KOMPLEMENTER (XED < 0)",
        'unrelated': "TIDAK TERKAIT (XED ≈ 0)",
        # Business Applications Tab
        'business_title': "Aplikasi Bisnis & Rekomendasi",
        'pricing_strategy': "Rekomendasi Strategi Harga",
        'market_analysis': "Analisis Pasar",
        'competitive_position': "Posisi Kompetitif",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nKalkulator elastisitas lanjutan untuk keputusan harga, optimasi pendapatan, dan strategi pasar.",
        'story_insight': "**Wawasan Utama:**\nElastisitas menentukan apakah menaikkan harga meningkatkan atau menurunkan pendapatan. Penting untuk strategi harga.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_business': "🏢 **Bisnis:** Optimalkan harga untuk pendapatan maksimal.",
        'use_govt': "🏛️ **Pemerintah:** Prediksi pendapatan pajak dan dampak subsidi.",
        'use_analyst': "📊 **Analis:** Menilai kompetitivitas pasar dan pola permintaan."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ========== TAB 1: PRICE ELASTICITY OF DEMAND ==========
with tab1:
    st.markdown(f"### {txt['ped_title']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        method = st.selectbox(txt['calculation_method'], [txt['midpoint'], txt['point']])
        
        st.markdown(f"#### {txt['input_data']}")
        
        P1 = st.number_input(txt['initial_price'], value=100.0, step=1.0)
        P2 = st.number_input(txt['new_price'], value=120.0, step=1.0)
        Q1 = st.number_input(txt['initial_qty'], value=1000.0, step=10.0)
        Q2 = st.number_input(txt['new_qty'], value=800.0, step=10.0)
        
        if st.button(txt['calculate'], type='primary'):
            # Calculate percentage changes
            if method == txt['midpoint']:
                # Midpoint method
                price_change_pct = ((P2 - P1) / ((P1 + P2) / 2)) * 100
                qty_change_pct = ((Q2 - Q1) / ((Q1 + Q2) / 2)) * 100
            else:
                # Point method
                price_change_pct = ((P2 - P1) / P1) * 100
                qty_change_pct = ((Q2 - Q1) / Q1) * 100
            
            # Calculate elasticity
            if price_change_pct != 0:
                elasticity = qty_change_pct / price_change_pct
            else:
                elasticity = 0
            
            # Revenue calculation
            R1 = P1 * Q1
            R2 = P2 * Q2
            revenue_change = R2 - R1
            revenue_change_pct = (revenue_change / R1) * 100
            
            st.session_state['ped_results'] = {
                'elasticity': elasticity,
                'price_change_pct': price_change_pct,
                'qty_change_pct': qty_change_pct,
                'R1': R1,
                'R2': R2,
                'revenue_change': revenue_change,
                'revenue_change_pct': revenue_change_pct
            }
    
    with col2:
        if 'ped_results' in st.session_state:
            results = st.session_state['ped_results']
            
            st.markdown(f"### {txt['results']}")
            
            # Elasticity value
            st.metric(txt['elasticity_value'], f"{results['elasticity']:.4f}")
            
            # Interpretation
            st.markdown(f"#### {txt['interpretation']}")
            abs_e = abs(results['elasticity'])
            
            if abs_e > 1:
                st.success(txt['elastic'])
                st.info("💡 **Implication**: 1% price increase → >1% quantity decrease")
            elif abs_e < 1 and abs_e > 0:
                st.warning(txt['inelastic'])
                st.info("💡 **Implication**: 1% price increase → <1% quantity decrease")
            elif abs_e == 1:
                st.info(txt['unit_elastic'])
                st.info("💡 **Implication**: 1% price increase → 1% quantity decrease")
            
            # Changes
            m1, m2 = st.columns(2)
            m1.metric(txt['price_change'], f"{results['price_change_pct']:.2f}%")
            m2.metric(txt['qty_change'], f"{results['qty_change_pct']:.2f}%")
            
            # Revenue impact
            st.markdown(f"### {txt['revenue_impact']}")
            
            r1, r2, r3 = st.columns(3)
            r1.metric("Initial Revenue", f"Rp {results['R1']:,.0f}")
            r2.metric("New Revenue", f"Rp {results['R2']:,.0f}", delta=f"{results['revenue_change']:,.0f}")
            r3.metric("Change (%)", f"{results['revenue_change_pct']:.2f}%", delta_color="normal")
            
            # Formula display
            st.latex(r"PED = \frac{\% \Delta Q}{\% \Delta P} = \frac{" + f"{results['qty_change_pct']:.2f}" + r"}{"+ f"{results['price_change_pct']:.2f}" + r"} = " + f"{results['elasticity']:.4f}")

# ========== TAB 2: REVENUE OPTIMIZATION ==========
with tab2:
    st.markdown(f"### {txt['revenue_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['current_situation']}")
        
        current_P = st.number_input(txt['current_price'], value=100.0, step=1.0, key='rev_P')
        current_Q = st.number_input(txt['current_quantity'], value=1000.0, step=10.0, key='rev_Q')
        elasticity_est = st.number_input(txt['elasticity_estimate'], value=-1.5, step=0.1, key='rev_e')
        
        current_R = current_P * current_Q
        st.metric("Current Revenue", f"Rp {current_R:,.0f}")
    
    with col2:
        st.markdown(f"### {txt['price_scenarios']}")
        
        # Generate scenarios
        price_changes = [-20, -10, -5, 0, 5, 10, 20]
        scenarios = []
        
        for pct_change in price_changes:
            new_P = current_P * (1 + pct_change/100)
            # Using elasticity: %ΔQ = elasticity × %ΔP
            qty_change_pct = elasticity_est * pct_change
            new_Q = current_Q * (1 + qty_change_pct/100)
            new_R = new_P * new_Q
            revenue_change = new_R - current_R
            
            scenarios.append({
                txt['scenario']: f"{pct_change:+d}%",
                txt['price_change_pct']: pct_change,
                txt['new_price_val']: new_P,
                txt['new_quantity_val']: new_Q,
                txt['new_revenue']: new_R,
                txt['revenue_change']: revenue_change
            })
        
        df_scenarios = pd.DataFrame(scenarios)
        
        # Find optimal
        optimal_idx = df_scenarios[txt['new_revenue']].idxmax()
        
        st.dataframe(df_scenarios.style.highlight_max(subset=[txt['new_revenue']], color='lightgreen'), 
                    use_container_width=True, hide_index=True)
        
        # Visualization
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_scenarios[txt['price_change_pct']],
            y=df_scenarios[txt['new_revenue']],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='blue', width=3),
            marker=dict(size=10)
        ))
        
        # Highlight optimal
        fig.add_trace(go.Scatter(
            x=[df_scenarios.iloc[optimal_idx][txt['price_change_pct']]],
            y=[df_scenarios.iloc[optimal_idx][txt['new_revenue']]],
            mode='markers',
            name='Optimal',
            marker=dict(size=15, color='red', symbol='star')
        ))
        
        fig.update_layout(
            title="Revenue vs Price Change",
            xaxis_title="Price Change (%)",
            yaxis_title="Revenue (Rp)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation
        st.markdown(f"### {txt['optimal_pricing']}")
        optimal_change = df_scenarios.iloc[optimal_idx][txt['price_change_pct']]
        optimal_revenue = df_scenarios.iloc[optimal_idx][txt['new_revenue']]
        
        if optimal_change > 0:
            st.success(f"✅ **Increase price by {optimal_change}%** to maximize revenue (Rp {optimal_revenue:,.0f})")
        elif optimal_change < 0:
            st.success(f"✅ **Decrease price by {abs(optimal_change)}%** to maximize revenue (Rp {optimal_revenue:,.0f})")
        else:
            st.info("✅ **Maintain current price** - already optimal")

# ========== TAB 3: OTHER ELASTICITIES ==========
with tab3:
    elasticity_type = st.selectbox("Select Elasticity Type", 
                                   [txt['income_elasticity'], txt['cross_elasticity'], txt['supply_elasticity']])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if elasticity_type == txt['income_elasticity']:
            st.markdown(f"### {txt['income_elasticity']}")
            
            Y1 = st.number_input(f"{txt['income']} (Initial)", value=5000.0, step=100.0)
            Y2 = st.number_input(f"{txt['income']} (New)", value=6000.0, step=100.0)
            Q1_yed = st.number_input(f"{txt['initial_qty']}", value=100.0, step=1.0, key='yed_q1')
            Q2_yed = st.number_input(f"{txt['new_qty']}", value=130.0, step=1.0, key='yed_q2')
            
            if st.button(txt['calculate'], key='yed_calc'):
                income_change_pct = ((Y2 - Y1) / ((Y1 + Y2) / 2)) * 100
                qty_change_pct = ((Q2_yed - Q1_yed) / ((Q1_yed + Q2_yed) / 2)) * 100
                
                yed = qty_change_pct / income_change_pct if income_change_pct != 0 else 0
                
                st.session_state['yed'] = yed
        
        elif elasticity_type == txt['cross_elasticity']:
            st.markdown(f"### {txt['cross_elasticity']}")
            
            Px1 = st.number_input(f"{txt['related_price']} (Initial)", value=50.0, step=1.0)
            Px2 = st.number_input(f"{txt['related_price']} (New)", value=60.0, step=1.0)
            Qy1 = st.number_input(f"{txt['initial_qty']} (This Product)", value=100.0, step=1.0, key='xed_q1')
            Qy2 = st.number_input(f"{txt['new_qty']} (This Product)", value=120.0, step=1.0, key='xed_q2')
            
            if st.button(txt['calculate'], key='xed_calc'):
                price_change_pct = ((Px2 - Px1) / ((Px1 + Px2) / 2)) * 100
                qty_change_pct = ((Qy2 - Qy1) / ((Qy1 + Qy2) / 2)) * 100
                
                xed = qty_change_pct / price_change_pct if price_change_pct != 0 else 0
                
                st.session_state['xed'] = xed
        
        else:  # Supply elasticity
            st.markdown(f"### {txt['supply_elasticity']}")
            
            Ps1 = st.number_input(f"{txt['initial_price']}", value=100.0, step=1.0, key='pes_p1')
            Ps2 = st.number_input(f"{txt['new_price']}", value=120.0, step=1.0, key='pes_p2')
            Qs1 = st.number_input(f"{txt['quantity_supplied']} (Initial)", value=1000.0, step=10.0, key='pes_q1')
            Qs2 = st.number_input(f"{txt['quantity_supplied']} (New)", value=1300.0, step=10.0, key='pes_q2')
            
            if st.button(txt['calculate'], key='pes_calc'):
                price_change_pct = ((Ps2 - Ps1) / ((Ps1 + Ps2) / 2)) * 100
                qty_change_pct = ((Qs2 - Qs1) / ((Qs1 + Qs2) / 2)) * 100
                
                pes = qty_change_pct / price_change_pct if price_change_pct != 0 else 0
                
                st.session_state['pes'] = pes
    
    with col2:
        if elasticity_type == txt['income_elasticity'] and 'yed' in st.session_state:
            yed = st.session_state['yed']
            st.metric(txt['elasticity_value'], f"{yed:.4f}")
            
            if yed > 1:
                st.success(txt['luxury_good'])
            elif yed > 0:
                st.info(txt['normal_good'])
                if yed < 1:
                    st.caption(txt['necessity'])
            else:
                st.warning(txt['inferior_good'])
        
        elif elasticity_type == txt['cross_elasticity'] and 'xed' in st.session_state:
            xed = st.session_state['xed']
            st.metric(txt['elasticity_value'], f"{xed:.4f}")
            
            if xed > 0.5:
                st.success(txt['substitute'])
            elif xed < -0.5:
                st.warning(txt['complement'])
            else:
                st.info(txt['unrelated'])
        
        elif elasticity_type == txt['supply_elasticity'] and 'pes' in st.session_state:
            pes = st.session_state['pes']
            st.metric(txt['elasticity_value'], f"{pes:.4f}")
            
            if pes > 1:
                st.success("ELASTIC SUPPLY - Easy to increase production")
            else:
                st.warning("INELASTIC SUPPLY - Difficult to increase production")

# ========== TAB 4: BUSINESS APPLICATIONS ==========
with tab4:
    st.markdown(f"### {txt['business_title']}")
    
    if 'ped_results' in st.session_state:
        elasticity = st.session_state['ped_results']['elasticity']
        
        st.markdown(f"#### {txt['pricing_strategy']}")
        
        if abs(elasticity) > 1:
            st.success("✅ **ELASTIC DEMAND** - Price-sensitive market")
            st.write("**Recommended Strategies:**")
            st.write("- 🎯 Focus on **volume** over margin")
            st.write("- 💰 Consider **price reductions** to boost sales")
            st.write("- 🎁 Use **promotions and discounts** effectively")
            st.write("- 🏪 **Penetration pricing** for market share")
        else:
            st.success("✅ **INELASTIC DEMAND** - Price-insensitive market")
            st.write("**Recommended Strategies:**")
            st.write("- 💎 Focus on **margin** over volume")
            st.write("- 📈 Consider **price increases** to boost revenue")
            st.write("- 🎨 Emphasize **quality and differentiation**")
            st.write("- 👑 **Premium pricing** strategy viable")
        
        st.markdown(f"#### {txt['market_analysis']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Market Characteristics:**")
            if abs(elasticity) > 2:
                st.write("- 🔴 Highly competitive market")
                st.write("- 🔄 Many substitutes available")
                st.write("- 💸 Price wars likely")
            elif abs(elasticity) > 1:
                st.write("- 🟡 Moderately competitive")
                st.write("- 🔄 Some substitutes exist")
                st.write("- 💰 Price-conscious consumers")
            else:
                st.write("- 🟢 Low competition or unique product")
                st.write("- 🎯 Few substitutes")
                st.write("- 💎 Brand loyalty or necessity good")
        
        with col2:
            st.write("**Competitive Position:**")
            if abs(elasticity) < 0.5:
                st.success("🏆 **Strong Market Power**")
                st.write("- Pricing flexibility")
                st.write("- High barriers to entry")
            elif abs(elasticity) < 1:
                st.info("💼 **Moderate Market Power**")
                st.write("- Some pricing flexibility")
                st.write("- Differentiation important")
            else:
                st.warning("⚔️ **Weak Market Power**")
                st.write("- Limited pricing flexibility")
                st.write("- Must compete on price")
    else:
        st.info("Calculate PED in Tab 1 to see business recommendations")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_business'])
        st.write(txt['use_govt'])
        st.write(txt['use_analyst'])
