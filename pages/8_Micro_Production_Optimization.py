import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Production Optimization", page_icon="🏭", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🏭 Professional Production Optimization",
        'subtitle': "Minimize Cost by choosing the optimal mix of **Capital (K)** and **Labor (L)** using advanced industry methods.",
        'tab1': "📊 Cost Minimization",
        'tab2': "📈 Sensitivity Analysis",
        'tab3': "📋 Production Planning",
        'tab4': "🎯 Optimization Dashboard",
        'tab5': "🔄 Multi-Scenario Comparison",
        'theory': "**Theory**: The optimal point is where the slope of the Isoquant (MRTS) equals the slope of the Isocost line ($w/r$).",
        'params': "Production Parameters (Cobb-Douglas)",
        'wage': "Wage Rate (w) - Rp/Hour",
        'rent': "Rental Rate (r) - Rp/Hour",
        'target_q': "Target Quantity (Units)",
        'alpha': "Output Elast. Capital (α)",
        'beta': "Output Elast. Labor (β)",
        'cost_min_res': "💰 Cost Minimization Results",
        'opt_k': "Optimal Capital (K*)",
        'opt_l': "Optimal Labor (L*)",
        'min_c': "Minimum Total Cost",
        'viz_title': "Isoquant & Isocost Map",
        'isoquant': "Isoquant (Target Q)",
        'isocost': "Isocost (Min Cost)",
        'managerial': "📋 Managerial Insights",
        'insight_1': "To produce **{q} units** most efficiently, hire **{l:.1f} workers** and use **{k:.1f} machine hours**.",
        'insight_labor': "💡 **Labor-Intensive**: Labor is relatively cheaper/more productive.",
        'insight_capital': "💡 **Capital-Intensive**: Capital is relatively cheaper/more productive.",
        'rts': "Returns to Scale",
        'rts_constant': "Constant Returns to Scale (α+β=1)",
        'rts_increasing': "Increasing Returns to Scale (α+β>1)",
        'rts_decreasing': "Decreasing Returns to Scale (α+β<1)",
        'mrts': "MRTS (Marginal Rate of Technical Substitution)",
        'productivity': "Productivity Metrics",
        'apl': "Average Product of Labor (APL)",
        'mpl': "Marginal Product of Labor (MPL)",
        'apk': "Average Product of Capital (APK)",
        'mpk': "Marginal Product of Capital (MPK)",
        'cost_breakdown': "Cost Breakdown",
        'labor_cost': "Labor Cost",
        'capital_cost': "Capital Cost",
        # Dashboard
        'dashboard_title': "Optimization Performance Dashboard",
        'kpi_efficiency': "Production Efficiency",
        'kpi_cost_per_unit': "Cost per Unit",
        'kpi_productivity': "Total Factor Productivity",
        'kpi_optimization_score': "Optimization Score",
        'benchmark': "Industry Benchmark Comparison",
        # Multi-scenario
        'multi_scenario_title': "Multi-Scenario Comparison",
        'add_scenario': "Add Scenario",
        'scenario_name': "Scenario Name",
        'compare_scenarios': "Compare Scenarios",
        'best_scenario': "Best Scenario",
        'export_data': "Export Results",
        'download_csv': "Download CSV"
    },
    'ID': {
        'title': "🏭 Optimasi Produksi Profesional",
        'subtitle': "Minimalkan Biaya dengan memilih kombinasi optimal **Modal (K)** dan **Tenaga Kerja (L)** menggunakan metode industri lanjutan.",
        'tab1': "📊 Minimisasi Biaya",
        'tab2': "📈 Analisis Sensitivitas",
        'tab3': "📋 Perencanaan Produksi",
        'tab4': "🎯 Dashboard Optimasi",
        'tab5': "🔄 Perbandingan Multi-Skenario",
        'theory': "**Teori**: Titik optimal adalah di mana kemiringan Isokuan (MRTS) sama dengan kemiringan garis Isocost ($w/r$).",
        'params': "Parameter Produksi (Cobb-Douglas)",
        'wage': "Upah Tenaga Kerja (w) - Rp/Jam",
        'rent': "Harga Sewa Mesin (r) - Rp/Jam",
        'target_q': "Target Produksi (Unit)",
        'alpha': "Elast. Output Modal (α)",
        'beta': "Elast. Output TK (β)",
        'cost_min_res': "💰 Hasil Minimisasi Biaya",
        'opt_k': "Modal Optimal (K*)",
        'opt_l': "Tenaga Kerja Optimal (L*)",
        'min_c': "Total Biaya Minimum",
        'viz_title': "Peta Isokuan & Isocost",
        'isoquant': "Isokuan (Target Q)",
        'isocost': "Isocost (Biaya Min)",
        'managerial': "📋 Insight Manajerial",
        'insight_1': "Untuk memproduksi **{q} unit** termurah, pekerjakan **{l:.1f} pekerja** dan gunakan **{k:.1f} jam mesin**.",
        'insight_labor': "💡 **Padat Karya**: Tenaga kerja relatif lebih murah/produktif.",
        'insight_capital': "💡 **Padat Modal**: Modal relatif lebih murah/produktif.",
        'rts': "Returns to Scale",
        'rts_constant': "Constant Returns to Scale (α+β=1)",
        'rts_increasing': "Increasing Returns to Scale (α+β>1)",
        'rts_decreasing': "Decreasing Returns to Scale (α+β<1)",
        'mrts': "MRTS (Marginal Rate of Technical Substitution)",
        'productivity': "Metrik Produktivitas",
        'apl': "Produk Rata-rata Tenaga Kerja (APL)",
        'mpl': "Produk Marginal Tenaga Kerja (MPL)",
        'apk': "Produk Rata-rata Modal (APK)",
        'mpk': "Produk Marginal Modal (MPK)",
        'cost_breakdown': "Rincian Biaya",
        'labor_cost': "Biaya Tenaga Kerja",
        'capital_cost': "Biaya Modal",
        # Dashboard
        'dashboard_title': "Dashboard Kinerja Optimasi",
        'kpi_efficiency': "Efisiensi Produksi",
        'kpi_cost_per_unit': "Biaya per Unit",
        'kpi_productivity': "Total Factor Productivity",
        'kpi_optimization_score': "Skor Optimasi",
        'benchmark': "Perbandingan Benchmark Industri",
        # Multi-scenario
        'multi_scenario_title': "Perbandingan Multi-Skenario",
        'add_scenario': "Tambah Skenario",
        'scenario_name': "Nama Skenario",
        'compare_scenarios': "Bandingkan Skenario",
        'best_scenario': "Skenario Terbaik",
        'export_data': "Ekspor Hasil",
        'download_csv': "Unduh CSV"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Initialize session state
if 'scenarios' not in st.session_state:
    st.session_state['scenarios'] = []

# Shared parameters in sidebar
with st.sidebar:
    st.subheader(f"⚙️ {txt['params']}")
    st.markdown("$Q(K, L) = A K^\\alpha L^\\beta$")
    
    A = 10  # TFP Constant
    alpha = st.slider(txt['alpha'], 0.1, 0.9, 0.4, 0.1, help="High α = Capital is very productive")
    beta = st.slider(txt['beta'], 0.1, 0.9, 0.6, 0.1, help="High β = Labor is very productive")
    
    st.markdown("---")
    w = st.number_input(txt['wage'], value=50000.0, step=5000.0)
    r = st.number_input(txt['rent'], value=100000.0, step=5000.0)
    Q_target = st.number_input(txt['target_q'], value=1000.0, step=100.0)
    
    # Returns to Scale
    rts_sum = alpha + beta
    st.markdown(f"### {txt['rts']}")
    if abs(rts_sum - 1.0) < 0.01:
        st.success(txt['rts_constant'])
    elif rts_sum > 1.0:
        st.info(txt['rts_increasing'])
    else:
        st.warning(txt['rts_decreasing'])

# Calculate optimal values (used across tabs)
ratio_KL = (alpha * w) / (beta * r)
L_opt = (Q_target / (A * (ratio_KL**alpha))) ** (1 / (alpha + beta))
K_opt = L_opt * ratio_KL
Min_Cost = w * L_opt + r * K_opt

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4'], txt['tab5']])

# ========== TAB 1: COST MINIMIZATION ==========
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(txt['cost_min_res'])
        
        m1, m2, m3 = st.columns(3)
        m1.metric(txt['opt_l'], f"{L_opt:.1f}")
        m2.metric(txt['opt_k'], f"{K_opt:.1f}")
        m3.metric(txt['min_c'], f"Rp {Min_Cost:,.0f}")
        
        st.info(txt['managerial'])
        st.write(txt['insight_1'].format(q=Q_target, l=L_opt, k=K_opt))
        
        if L_opt > K_opt:
            st.success(txt['insight_labor'])
        else:
            st.warning(txt['insight_capital'])
        
        # MRTS
        st.markdown(f"### {txt['mrts']}")
        mrts = (beta / alpha) * (K_opt / L_opt)
        st.metric("MRTS at Optimum", f"{mrts:.2f}")
        st.caption(f"At optimal point, MRTS = w/r = {w/r:.2f}")
        
        # Productivity Metrics
        st.markdown(f"### {txt['productivity']}")
        Q_actual = A * (K_opt**alpha) * (L_opt**beta)
        apl = Q_actual / L_opt
        mpl = beta * Q_actual / L_opt
        apk = Q_actual / K_opt
        mpk = alpha * Q_actual / K_opt
        
        p1, p2 = st.columns(2)
        p1.metric(txt['apl'], f"{apl:.2f}")
        p1.metric(txt['mpl'], f"{mpl:.2f}")
        p2.metric(txt['apk'], f"{apk:.2f}")
        p2.metric(txt['mpk'], f"{mpk:.2f}")
    
    with col2:
        # Isoquant & Isocost Visualization
        L_vals = np.linspace(L_opt * 0.3, L_opt * 2.0, 100)
        K_iso = (Q_target / (A * L_vals**beta)) ** (1/alpha)
        K_cost = (Min_Cost - w * L_vals) / r
        
        fig = go.Figure()
        
        # Isoquant
        fig.add_trace(go.Scatter(
            x=L_vals, y=K_iso,
            mode='lines',
            name=txt['isoquant'],
            line=dict(color='blue', width=3)
        ))
        
        # Isocost
        fig.add_trace(go.Scatter(
            x=L_vals, y=K_cost,
            mode='lines',
            name=txt['isocost'],
            line=dict(color='red', width=3, dash='dash')
        ))
        
        # Optimal point
        fig.add_trace(go.Scatter(
            x=[L_opt], y=[K_opt],
            mode='markers+text',
            name='Optimal Point',
            marker=dict(size=15, color='gold', line=dict(color='black', width=2)),
            text=[f"({L_opt:.1f}, {K_opt:.1f})"],
            textposition="top center"
        ))
        
        fig.update_layout(
            title=txt['viz_title'],
            xaxis_title=txt['opt_l'],
            yaxis_title=txt['opt_k'],
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost Breakdown
        st.markdown(f"### {txt['cost_breakdown']}")
        labor_cost_val = w * L_opt
        capital_cost_val = r * K_opt
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=[txt['labor_cost'], txt['capital_cost']],
            values=[labor_cost_val, capital_cost_val],
            hole=.3,
            marker=dict(colors=['#3498db', '#e74c3c'])
        )])
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

# ========== TAB 2: SENSITIVITY ANALYSIS ==========
with tab2:
    st.markdown(f"### {txt['tab2']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Wage Rate Range**")
        w_min = st.number_input("Min Wage", value=w*0.5, step=5000.0)
        w_max = st.number_input("Max Wage", value=w*1.5, step=5000.0)
        
        if st.button("🔍 Run Sensitivity Analysis", type='primary'):
            st.session_state['run_sens'] = True
    
    with col2:
        if 'run_sens' in st.session_state and st.session_state['run_sens']:
            st.markdown("### 📊 Sensitivity Results")
            
            # Generate sensitivity data
            wage_range = np.linspace(w_min, w_max, 20)
            L_sens = []
            K_sens = []
            Cost_sens = []
            
            for w_test in wage_range:
                ratio_test = (alpha * w_test) / (beta * r)
                L_test = (Q_target / (A * (ratio_test**alpha))) ** (1 / (alpha + beta))
                K_test = L_test * ratio_test
                Cost_test = w_test * L_test + r * K_test
                
                L_sens.append(L_test)
                K_sens.append(K_test)
                Cost_sens.append(Cost_test)
            
            # Plot
            fig = make_subplots(rows=2, cols=1,
                                subplot_titles=("Optimal Input Mix vs Wage", "Total Cost vs Wage"))
            
            fig.add_trace(go.Scatter(x=wage_range, y=L_sens, name="Labor (L*)", line=dict(color='blue', width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(x=wage_range, y=K_sens, name="Capital (K*)", line=dict(color='red', width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(x=wage_range, y=Cost_sens, name="Total Cost", line=dict(color='green', width=2)), row=2, col=1)
            
            fig.update_xaxes(title_text="Wage Rate (Rp/Hour)", row=2, col=1)
            fig.update_yaxes(title_text="Input Units", row=1, col=1)
            fig.update_yaxes(title_text="Total Cost (Rp)", row=2, col=1)
            fig.update_layout(height=600)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("📊 **Insight**: As wages increase, optimal labor decreases and capital increases (substitution effect).")

# ========== TAB 3: PRODUCTION PLANNING ==========
with tab3:
    st.markdown(f"### {txt['tab3']}")
    
    n_levels = st.slider("Number of Output Levels", 3, 10, 5)
    
    if st.button("📋 Generate Production Plan", type='primary'):
        # Generate output levels
        Q_levels = np.linspace(Q_target * 0.5, Q_target * 1.5, n_levels)
        
        planning_data = []
        for Q in Q_levels:
            L_plan = (Q / (A * (ratio_KL**alpha))) ** (1 / (alpha + beta))
            K_plan = L_plan * ratio_KL
            Cost_plan = w * L_plan + r * K_plan
            
            planning_data.append({
                'Output (Q)': f"{Q:.0f}",
                'Labor (L*)': f"{L_plan:.1f}",
                'Capital (K*)': f"{K_plan:.1f}",
                'Total Cost (Rp)': f"{Cost_plan:,.0f}",
                'Unit Cost (Rp)': f"{Cost_plan/Q:,.0f}"
            })
        
        df_plan = pd.DataFrame(planning_data)
        st.dataframe(df_plan, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_plan.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Production Plan (CSV)",
            data=csv,
            file_name='production_plan.csv',
            mime='text/csv',
        )
        
        st.success("✅ Production plan generated! Use this table for capacity planning and budgeting.")

# ========== TAB 4: OPTIMIZATION DASHBOARD ==========
with tab4:
    st.markdown(f"### {txt['dashboard_title']}")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate KPIs
    efficiency = (Q_actual / Q_target) * 100
    cost_per_unit = Min_Cost / Q_target
    tfp = A  # Total Factor Productivity
    
    # Optimization score (0-100)
    # Based on: efficiency, cost minimization, productivity
    opt_score = min(100, (efficiency + (1000/cost_per_unit) + tfp*5) / 3)
    
    with col1:
        st.metric(txt['kpi_efficiency'], f"{efficiency:.1f}%", 
                 delta=f"{efficiency - 100:.1f}%")
    
    with col2:
        st.metric(txt['kpi_cost_per_unit'], f"Rp {cost_per_unit:,.0f}",
                 delta_color="inverse")
    
    with col3:
        st.metric(txt['kpi_productivity'], f"{tfp:.1f}",
                 help="Total Factor Productivity (A)")
    
    with col4:
        st.metric(txt['kpi_optimization_score'], f"{opt_score:.0f}/100")
    
    st.markdown("---")
    
    # Benchmark Comparison
    st.markdown(f"### {txt['benchmark']}")
    
    # Industry benchmarks (example values)
    benchmarks = {
        'Metric': ['Cost per Unit', 'Labor Productivity', 'Capital Productivity', 'Efficiency'],
        'Your Company': [f"Rp {cost_per_unit:,.0f}", f"{apl:.2f}", f"{apk:.2f}", f"{efficiency:.1f}%"],
        'Industry Average': ['Rp 1,200', '12.5', '8.0', '95%'],
        'Best in Class': ['Rp 900', '18.0', '12.0', '105%']
    }
    
    df_benchmark = pd.DataFrame(benchmarks)
    st.dataframe(df_benchmark, use_container_width=True, hide_index=True)
    
    # Visualization: Radar chart
    categories = ['Cost Efficiency', 'Labor Productivity', 'Capital Productivity', 'Overall Efficiency']
    
    # Normalize values for radar chart (0-100 scale)
    your_values = [
        min(100, 1200/cost_per_unit * 100),  # Cost efficiency (inverse)
        min(100, apl/12.5 * 100),  # Labor productivity
        min(100, apk/8.0 * 100),  # Capital productivity
        efficiency  # Overall efficiency
    ]
    
    industry_avg = [100, 100, 100, 95]
    best_in_class = [133, 144, 150, 105]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=your_values + [your_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Company',
        line=dict(color='blue')
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=industry_avg + [industry_avg[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Industry Average',
        line=dict(color='gray', dash='dash')
    ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 150])),
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Optimization Recommendations")
    
    if cost_per_unit > 1200:
        st.warning("⚠️ **Cost per unit is above industry average.** Consider optimizing input mix or improving productivity.")
    else:
        st.success("✅ **Cost per unit is competitive.** Maintain current efficiency levels.")
    
    if apl < 12.5:
        st.info("💡 **Labor productivity below average.** Consider training programs or process improvements.")
    
    if apk < 8.0:
        st.info("💡 **Capital productivity below average.** Review equipment utilization and maintenance.")

# ========== TAB 5: MULTI-SCENARIO COMPARISON ==========
with tab5:
    st.markdown(f"### {txt['multi_scenario_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Add New Scenario")
        
        scenario_name = st.text_input(txt['scenario_name'], value="Scenario A")
        scenario_w = st.number_input("Wage Rate (Rp/Hour)", value=w, step=5000.0, key='sc_w')
        scenario_r = st.number_input("Rental Rate (Rp/Hour)", value=r, step=5000.0, key='sc_r')
        
        if st.button(txt['add_scenario'], type='primary'):
            # Calculate for this scenario
            ratio_sc = (alpha * scenario_w) / (beta * scenario_r)
            L_sc = (Q_target / (A * (ratio_sc**alpha))) ** (1 / (alpha + beta))
            K_sc = L_sc * ratio_sc
            Cost_sc = scenario_w * L_sc + scenario_r * K_sc
            
            st.session_state['scenarios'].append({
                'Scenario': scenario_name,
                'Wage (Rp/h)': f"{scenario_w:,.0f}",
                'Rent (Rp/h)': f"{scenario_r:,.0f}",
                'Labor (L*)': f"{L_sc:.1f}",
                'Capital (K*)': f"{K_sc:.1f}",
                'Total Cost': f"{Cost_sc:,.0f}",
                'Cost/Unit': f"{Cost_sc/Q_target:,.0f}",
                '_cost_numeric': Cost_sc  # For sorting
            })
            st.success(f"✅ Added {scenario_name}!")
    
    with col2:
        if len(st.session_state['scenarios']) > 0:
            st.markdown("#### Scenario Comparison")
            
            df_scenarios = pd.DataFrame(st.session_state['scenarios'])
            
            # Drop numeric column for display
            df_display = df_scenarios.drop('_cost_numeric', axis=1)
            
            # Highlight best scenario (lowest cost)
            best_idx = df_scenarios['_cost_numeric'].idxmin()
            
            st.dataframe(df_display.style.apply(
                lambda x: ['background-color: lightgreen' if x.name == best_idx else '' for i in x],
                axis=1
            ), use_container_width=True, hide_index=True)
            
            st.success(f"🏆 {txt['best_scenario']}: {df_scenarios.iloc[best_idx]['Scenario']} (Cost: Rp {df_scenarios.iloc[best_idx]['_cost_numeric']:,.0f})")
            
            # Download button
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=txt['download_csv'],
                data=csv,
                file_name='scenario_comparison.csv',
                mime='text/csv',
            )
            
            # Clear scenarios button
            if st.button("🗑️ Clear All Scenarios"):
                st.session_state['scenarios'] = []
                st.rerun()
        else:
            st.info("Add scenarios to compare different wage and rental rate combinations.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Professional Production Optimization | Industry-Standard Methods</p>
    <p>🏭 Built for Operations Managers, Efficiency Consultants, and Industrial Engineers</p>
</div>
""", unsafe_allow_html=True)
