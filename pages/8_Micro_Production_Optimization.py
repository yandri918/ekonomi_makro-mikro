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
        'title': "🏭 Managerial Production Optimization",
        'subtitle': "Minimize Cost by choosing the optimal mix of **Capital (K)** and **Labor (L)** using industry-standard methods.",
        'tab1': "📊 Cost Minimization",
        'tab2': "📈 Sensitivity Analysis",
        'tab3': "📋 Production Planning",
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
        # Sensitivity
        'sensitivity_title': "Sensitivity Analysis: How Optimal Mix Changes",
        'wage_range': "Wage Rate Range (Rp/Hour)",
        'rent_range': "Rental Rate Range (Rp/Hour)",
        'run_sensitivity': "🔍 Run Sensitivity Analysis",
        'sensitivity_results': "📊 Sensitivity Results",
        # Planning
        'planning_title': "Production Planning Table",
        'planning_desc': "Compare optimal input mix for different output levels",
        'output_levels': "Number of Output Levels",
        'generate_plan': "📋 Generate Production Plan",
        'story_title': "📚 Story & Use Cases: Production Optimization",
        'story_meaning': "**What is this?**\nIndustry-standard tool for cost minimization using Cobb-Douglas production function with advanced analytics.",
        'story_insight': "**Key Insight:**\nOptimal input mix depends on relative prices. When wages rise, firms substitute capital for labor (automation).",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Industry Ministry:** Analyze impact of minimum wage changes on automation decisions.",
        'use_corp': "🏢 **Operations Managers:** Optimize production costs and plan capacity expansion.",
        'use_analyst': "📈 **Efficiency Consultants:** Benchmark productivity and recommend cost-saving strategies."
    },
    'ID': {
        'title': "🏭 Optimasi Produksi Manajerial",
        'subtitle': "Minimalkan Biaya dengan memilih kombinasi optimal **Modal (K)** dan **Tenaga Kerja (L)** menggunakan metode standar industri.",
        'tab1': "📊 Minimisasi Biaya",
        'tab2': "📈 Analisis Sensitivitas",
        'tab3': "📋 Perencanaan Produksi",
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
        # Sensitivity
        'sensitivity_title': "Analisis Sensitivitas: Bagaimana Mix Optimal Berubah",
        'wage_range': "Rentang Upah (Rp/Jam)",
        'rent_range': "Rentang Sewa (Rp/Jam)",
        'run_sensitivity': "🔍 Jalankan Analisis Sensitivitas",
        'sensitivity_results': "📊 Hasil Sensitivitas",
        # Planning
        'planning_title': "Tabel Perencanaan Produksi",
        'planning_desc': "Bandingkan kombinasi input optimal untuk berbagai tingkat output",
        'output_levels': "Jumlah Tingkat Output",
        'generate_plan': "📋 Buat Rencana Produksi",
        'story_title': "📚 Cerita & Kasus Penggunaan: Optimasi Produksi",
        'story_meaning': "**Apa artinya ini?**\nAlat standar industri untuk minimisasi biaya menggunakan fungsi produksi Cobb-Douglas dengan analitik lanjutan.",
        'story_insight': "**Wawasan Utama:**\nKombinasi input optimal tergantung harga relatif. Ketika upah naik, perusahaan substitusi modal untuk tenaga kerja (otomasi).",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Kemenperin:** Analisis dampak perubahan UMR terhadap keputusan otomasi.",
        'use_corp': "🏢 **Manajer Operasional:** Optimalkan biaya produksi dan rencanakan ekspansi kapasitas.",
        'use_analyst': "📈 **Konsultan Efisiensi:** Benchmark produktivitas dan rekomendasikan strategi penghematan biaya."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

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
tab1, tab2, tab3 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3']])

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
            marker=dict(size=15, color='black'),
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
            hole=.3
        )])
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

# ========== TAB 2: SENSITIVITY ANALYSIS ==========
with tab2:
    st.markdown(f"### {txt['sensitivity_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"**{txt['wage_range']}**")
        w_min = st.number_input("Min Wage", value=w*0.5, step=5000.0)
        w_max = st.number_input("Max Wage", value=w*1.5, step=5000.0)
        
        if st.button(txt['run_sensitivity'], type='primary'):
            st.session_state['run_sens'] = True
    
    with col2:
        if 'run_sens' in st.session_state and st.session_state['run_sens']:
            st.markdown(f"### {txt['sensitivity_results']}")
            
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
            
            fig.add_trace(go.Scatter(x=wage_range, y=L_sens, name="Labor (L*)", line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Scatter(x=wage_range, y=K_sens, name="Capital (K*)", line=dict(color='red')), row=1, col=1)
            fig.add_trace(go.Scatter(x=wage_range, y=Cost_sens, name="Total Cost", line=dict(color='green')), row=2, col=1)
            
            fig.update_xaxes(title_text="Wage Rate (Rp/Hour)", row=2, col=1)
            fig.update_yaxes(title_text="Input Units", row=1, col=1)
            fig.update_yaxes(title_text="Total Cost (Rp)", row=2, col=1)
            fig.update_layout(height=600)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("📊 **Insight**: As wages increase, optimal labor decreases and capital increases (substitution effect).")

# ========== TAB 3: PRODUCTION PLANNING ==========
with tab3:
    st.markdown(f"### {txt['planning_title']}")
    st.caption(txt['planning_desc'])
    
    n_levels = st.slider(txt['output_levels'], 3, 10, 5)
    
    if st.button(txt['generate_plan'], type='primary'):
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
        
        st.success("✅ Production plan generated! Use this table for capacity planning and budgeting.")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_govt'])
        st.write(txt['use_corp'])
        st.write(txt['use_analyst'])
