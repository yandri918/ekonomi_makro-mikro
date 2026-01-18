import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Advanced Macro Policy AI", page_icon="🎯", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🎯 Advanced AI Macroeconomic Policy Optimizer",
        'subtitle': "PhD-level policy simulation: Multi-objective optimization with trade-offs, constraints, and dynamic macroeconomic modeling.",
        'tab1': "🎯 Policy Optimization",
        'tab2': "📊 Trade-off Analysis",
        'tab3': "🔮 Dynamic Simulation",
        'tab4': "📈 Policy Scenarios",
        # Tab 1
        'baseline': "Economic Baseline",
        'consumption': "Consumption (C) - Trillion Rp",
        'investment': "Investment (I) - Trillion Rp",
        'govt_spending': "Government Spending (G) - Trillion Rp",
        'net_exports': "Net Exports (NX) - Trillion Rp",
        'interest_rate': "Current Interest Rate (%)",
        'inflation': "Current Inflation (%)",
        'unemployment': "Current Unemployment (%)",
        'targets': "Policy Targets",
        'target_growth': "Target GDP Growth (%)",
        'target_inflation': "Target Inflation (%)",
        'target_unemployment': "Target Unemployment (%)",
        'constraints': "Policy Constraints",
        'max_deficit': "Max Budget Deficit (% of GDP)",
        'max_rate_change': "Max Interest Rate Change (%)",
        'min_rate': "Minimum Interest Rate (%)",
        'max_rate': "Maximum Interest Rate (%)",
        'preferences': "Policy Preferences",
        'growth_weight': "Growth Priority Weight",
        'inflation_weight': "Inflation Control Weight",
        'unemployment_weight': "Employment Priority Weight",
        'optimize': "🚀 Run Advanced Optimization",
        'results': "Optimization Results",
        'optimal_policy': "Optimal Policy Mix",
        'new_g': "Recommended G",
        'new_r': "Recommended Interest Rate",
        'new_tax': "Recommended Tax Rate",
        'predicted_outcomes': "Predicted Outcomes",
        'predicted_growth': "Predicted GDP Growth",
        'predicted_inflation': "Predicted Inflation",
        'predicted_unemployment': "Predicted Unemployment",
        'policy_score': "Policy Effectiveness Score",
        # Tab 2
        'tradeoff_title': "Policy Trade-off Analysis",
        'growth_inflation': "Growth vs Inflation Trade-off",
        'growth_unemployment': "Growth vs Unemployment (Phillips Curve)",
        'fiscal_monetary': "Fiscal vs Monetary Mix",
        'pareto_frontier': "Pareto Frontier",
        # Tab 3
        'dynamic_title': "Dynamic Policy Simulation",
        'simulation_periods': "Simulation Periods (Quarters)",
        'shock_type': "Economic Shock",
        'no_shock': "No Shock (Baseline)",
        'demand_shock': "Demand Shock (-10%)",
        'supply_shock': "Supply Shock (+5% inflation)",
        'financial_shock': "Financial Crisis (+3% rate)",
        'run_simulation': "Run Dynamic Simulation",
        'simulation_results': "Simulation Results",
        # Tab 4
        'scenario_title': "Policy Scenario Comparison",
        'scenario_name': "Scenario Name",
        'add_scenario': "Add Scenario",
        'comparison_table': "Scenario Comparison",
        'best_scenario': "Best Scenario",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nAdvanced macroeconomic policy optimization tool using multi-objective AI to find optimal fiscal-monetary policy mix.",
        'story_insight': "**Key Insight:**\nPolicy-making involves trade-offs. You can't maximize growth, minimize inflation, and minimize unemployment simultaneously. AI helps find the best compromise.",
        'story_users': "**Who needs this?**",
        'use_central_bank': "🏦 **Central Banks:** Coordinate fiscal-monetary policy for optimal outcomes.",
        'use_ministry': "🏛️ **Ministry of Finance:** Determine optimal budget allocation and deficit levels.",
        'use_researcher': "🎓 **Economists:** Analyze policy effectiveness and trade-offs."
    },
    'ID': {
        'title': "🎯 AI Pengoptimal Kebijakan Makroekonomi Lanjutan",
        'subtitle': "Simulasi kebijakan setara S3: Optimasi multi-objektif dengan trade-off, batasan, dan pemodelan makroekonomi dinamis.",
        'tab1': "🎯 Optimasi Kebijakan",
        'tab2': "📊 Analisis Trade-off",
        'tab3': "🔮 Simulasi Dinamis",
        'tab4': "📈 Skenario Kebijakan",
        # Tab 1
        'baseline': "Baseline Ekonomi",
        'consumption': "Konsumsi (C) - Triliun Rp",
        'investment': "Investasi (I) - Triliun Rp",
        'govt_spending': "Belanja Pemerintah (G) - Triliun Rp",
        'net_exports': "Ekspor Neto (NX) - Triliun Rp",
        'interest_rate': "Suku Bunga Saat Ini (%)",
        'inflation': "Inflasi Saat Ini (%)",
        'unemployment': "Pengangguran Saat Ini (%)",
        'targets': "Target Kebijakan",
        'target_growth': "Target Pertumbuhan PDB (%)",
        'target_inflation': "Target Inflasi (%)",
        'target_unemployment': "Target Pengangguran (%)",
        'constraints': "Batasan Kebijakan",
        'max_deficit': "Defisit Anggaran Maks (% PDB)",
        'max_rate_change': "Perubahan Suku Bunga Maks (%)",
        'min_rate': "Suku Bunga Minimum (%)",
        'max_rate': "Suku Bunga Maksimum (%)",
        'preferences': "Preferensi Kebijakan",
        'growth_weight': "Bobot Prioritas Pertumbuhan",
        'inflation_weight': "Bobot Kontrol Inflasi",
        'unemployment_weight': "Bobot Prioritas Lapangan Kerja",
        'optimize': "🚀 Jalankan Optimasi Lanjutan",
        'results': "Hasil Optimasi",
        'optimal_policy': "Bauran Kebijakan Optimal",
        'new_g': "G yang Direkomendasikan",
        'new_r': "Suku Bunga yang Direkomendasikan",
        'new_tax': "Tarif Pajak yang Direkomendasikan",
        'predicted_outcomes': "Hasil Prediksi",
        'predicted_growth': "Pertumbuhan PDB Prediksi",
        'predicted_inflation': "Inflasi Prediksi",
        'predicted_unemployment': "Pengangguran Prediksi",
        'policy_score': "Skor Efektivitas Kebijakan",
        # Tab 2
        'tradeoff_title': "Analisis Trade-off Kebijakan",
        'growth_inflation': "Trade-off Pertumbuhan vs Inflasi",
        'growth_unemployment': "Pertumbuhan vs Pengangguran (Kurva Phillips)",
        'fiscal_monetary': "Bauran Fiskal vs Moneter",
        'pareto_frontier': "Pareto Frontier",
        # Tab 3
        'dynamic_title': "Simulasi Kebijakan Dinamis",
        'simulation_periods': "Periode Simulasi (Kuartal)",
        'shock_type': "Guncangan Ekonomi",
        'no_shock': "Tanpa Guncangan (Baseline)",
        'demand_shock': "Guncangan Permintaan (-10%)",
        'supply_shock': "Guncangan Penawaran (+5% inflasi)",
        'financial_shock': "Krisis Keuangan (+3% suku bunga)",
        'run_simulation': "Jalankan Simulasi Dinamis",
        'simulation_results': "Hasil Simulasi",
        # Tab 4
        'scenario_title': "Perbandingan Skenario Kebijakan",
        'scenario_name': "Nama Skenario",
        'add_scenario': "Tambah Skenario",
        'comparison_table': "Tabel Perbandingan",
        'best_scenario': "Skenario Terbaik",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nAlat optimasi kebijakan makroekonomi lanjutan menggunakan AI multi-objektif untuk menemukan bauran kebijakan fiskal-moneter optimal.",
        'story_insight': "**Wawasan Utama:**\nPembuatan kebijakan melibatkan trade-off. Anda tidak bisa memaksimalkan pertumbuhan, meminimalkan inflasi, dan meminimalkan pengangguran secara bersamaan. AI membantu menemukan kompromi terbaik.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_central_bank': "🏦 **Bank Sentral:** Koordinasi kebijakan fiskal-moneter untuk hasil optimal.",
        'use_ministry': "🏛️ **Kementerian Keuangan:** Tentukan alokasi anggaran dan tingkat defisit optimal.",
        'use_researcher': "🎓 **Ekonom:** Analisis efektivitas kebijakan dan trade-off."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Initialize session state
if 'scenarios' not in st.session_state:
    st.session_state['scenarios'] = []

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ========== TAB 1: POLICY OPTIMIZATION ==========
with tab1:
    st.markdown(f"### {txt['tab1']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['baseline']}")
        
        C = st.number_input(txt['consumption'], value=11000.0, step=100.0)
        I = st.number_input(txt['investment'], value=6000.0, step=100.0)
        G = st.number_input(txt['govt_spending'], value=3000.0, step=100.0)
        NX = st.number_input(txt['net_exports'], value=500.0, step=50.0)
        r = st.number_input(txt['interest_rate'], value=5.0, step=0.25)
        inflation = st.number_input(txt['inflation'], value=3.5, step=0.1)
        unemployment = st.number_input(txt['unemployment'], value=5.5, step=0.1)
        
        current_gdp = C + I + G + NX
        st.metric("Current GDP", f"Rp {current_gdp:,.0f}T")
        
        st.markdown(f"#### {txt['targets']}")
        
        target_growth = st.number_input(txt['target_growth'], value=5.5, step=0.1)
        target_inflation = st.number_input(txt['target_inflation'], value=3.0, step=0.1)
        target_unemployment = st.number_input(txt['target_unemployment'], value=4.5, step=0.1)
        
        st.markdown(f"#### {txt['constraints']}")
        
        max_deficit = st.slider(txt['max_deficit'], 0.0, 10.0, 3.0, 0.5)
        max_rate_change = st.slider(txt['max_rate_change'], 0.0, 5.0, 2.0, 0.25)
        min_rate = st.number_input(txt['min_rate'], value=2.0, step=0.25)
        max_rate = st.number_input(txt['max_rate'], value=10.0, step=0.25)
        
        st.markdown(f"#### {txt['preferences']}")
        
        w_growth = st.slider(txt['growth_weight'], 0.0, 1.0, 0.5, 0.1)
        w_inflation = st.slider(txt['inflation_weight'], 0.0, 1.0, 0.3, 0.1)
        w_unemployment = st.slider(txt['unemployment_weight'], 0.0, 1.0, 0.2, 0.1)
        
        # Normalize weights
        total_weight = w_growth + w_inflation + w_unemployment
        if total_weight > 0:
            w_growth /= total_weight
            w_inflation /= total_weight
            w_unemployment /= total_weight
        
        if st.button(txt['optimize'], type='primary'):
            # Advanced macroeconomic model
            # Parameters
            MPC = 0.75  # Marginal propensity to consume
            alpha_I = 200  # Investment sensitivity to interest rate
            alpha_NX = 100  # Net export sensitivity to interest rate
            phillips_slope = 0.5  # Phillips curve slope
            nairu = 5.5  # Natural rate of unemployment
            
            # Objective function: Multi-objective optimization
            def objective(x):
                G_new, r_new = x
                
                # Predict new GDP components
                I_new = I - alpha_I * (r_new - r)
                NX_new = NX - alpha_NX * (r_new - r)
                C_new = C + MPC * (G_new - G)
                
                GDP_new = C_new + I_new + G_new + NX_new
                growth_actual = ((GDP_new - current_gdp) / current_gdp) * 100
                
                # Predict inflation (Phillips curve + demand-pull)
                output_gap = (GDP_new - current_gdp) / current_gdp * 100
                inflation_new = inflation + 0.3 * output_gap - 0.2 * (r_new - r)
                
                # Predict unemployment (Okun's law)
                unemployment_new = unemployment - 0.5 * (growth_actual - 2)
                
                # Multi-objective loss function
                loss_growth = w_growth * (growth_actual - target_growth)**2
                loss_inflation = w_inflation * (inflation_new - target_inflation)**2
                loss_unemployment = w_unemployment * (unemployment_new - target_unemployment)**2
                
                return loss_growth + loss_inflation + loss_unemployment
            
            # Constraints
            def constraint_deficit(x):
                G_new, r_new = x
                deficit = (G_new - G) / current_gdp * 100
                return max_deficit - deficit
            
            def constraint_rate_change(x):
                G_new, r_new = x
                return max_rate_change - abs(r_new - r)
            
            # Bounds
            bounds = [(G * 0.8, G * 1.5), (min_rate, max_rate)]
            
            # Constraints
            constraints = [
                {'type': 'ineq', 'fun': constraint_deficit},
                {'type': 'ineq', 'fun': constraint_rate_change}
            ]
            
            # Initial guess
            x0 = [G, r]
            
            # Optimize
            result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                G_opt, r_opt = result.x
                
                # Calculate predicted outcomes
                I_opt = I - alpha_I * (r_opt - r)
                NX_opt = NX - alpha_NX * (r_opt - r)
                C_opt = C + MPC * (G_opt - G)
                GDP_opt = C_opt + I_opt + G_opt + NX_opt
                
                growth_pred = ((GDP_opt - current_gdp) / current_gdp) * 100
                output_gap = (GDP_opt - current_gdp) / current_gdp * 100
                inflation_pred = inflation + 0.3 * output_gap - 0.2 * (r_opt - r)
                unemployment_pred = unemployment - 0.5 * (growth_pred - 2)
                
                # Policy effectiveness score
                score_growth = max(0, 100 - abs(growth_pred - target_growth) * 20)
                score_inflation = max(0, 100 - abs(inflation_pred - target_inflation) * 20)
                score_unemployment = max(0, 100 - abs(unemployment_pred - target_unemployment) * 20)
                overall_score = (score_growth + score_inflation + score_unemployment) / 3
                
                st.session_state['optimization_results'] = {
                    'G_opt': G_opt,
                    'r_opt': r_opt,
                    'GDP_opt': GDP_opt,
                    'growth_pred': growth_pred,
                    'inflation_pred': inflation_pred,
                    'unemployment_pred': unemployment_pred,
                    'score': overall_score,
                    'C_opt': C_opt,
                    'I_opt': I_opt,
                    'NX_opt': NX_opt
                }
            else:
                st.error("Optimization failed. Try adjusting constraints.")
    
    with col2:
        if 'optimization_results' in st.session_state:
            results = st.session_state['optimization_results']
            
            st.markdown(f"### {txt['results']}")
            
            # Optimal policy
            st.markdown(f"#### {txt['optimal_policy']}")
            
            p1, p2 = st.columns(2)
            p1.metric(txt['new_g'], f"Rp {results['G_opt']:,.0f}T", 
                     delta=f"{results['G_opt'] - G:+,.0f}T")
            p2.metric(txt['new_r'], f"{results['r_opt']:.2f}%",
                     delta=f"{results['r_opt'] - r:+.2f}%")
            
            # Predicted outcomes
            st.markdown(f"#### {txt['predicted_outcomes']}")
            
            o1, o2, o3 = st.columns(3)
            o1.metric(txt['predicted_growth'], f"{results['growth_pred']:.2f}%",
                     delta=f"{results['growth_pred'] - target_growth:+.2f}%")
            o2.metric(txt['predicted_inflation'], f"{results['inflation_pred']:.2f}%",
                     delta=f"{results['inflation_pred'] - target_inflation:+.2f}%")
            o3.metric(txt['predicted_unemployment'], f"{results['unemployment_pred']:.2f}%",
                     delta=f"{results['unemployment_pred'] - target_unemployment:+.2f}%")
            
            st.metric(txt['policy_score'], f"{results['score']:.1f}/100")
            
            # GDP breakdown
            fig = go.Figure()
            
            categories = ['C', 'I', 'G', 'NX']
            current_values = [C, I, G, NX]
            new_values = [results['C_opt'], results['I_opt'], results['G_opt'], results['NX_opt']]
            
            fig.add_trace(go.Bar(name='Current', x=categories, y=current_values, marker_color='lightblue'))
            fig.add_trace(go.Bar(name='Optimal', x=categories, y=new_values, marker_color='darkblue'))
            
            fig.update_layout(
                title="GDP Components: Current vs Optimal",
                xaxis_title="Component",
                yaxis_title="Value (Trillion Rp)",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Policy recommendations
            st.markdown("### 💡 Policy Recommendations")
            
            if results['G_opt'] > G:
                st.success(f"✅ **Expansionary Fiscal Policy**: Increase government spending by Rp {results['G_opt'] - G:,.0f}T")
            else:
                st.warning(f"⚠️ **Contractionary Fiscal Policy**: Reduce government spending by Rp {G - results['G_opt']:,.0f}T")
            
            if results['r_opt'] < r:
                st.success(f"✅ **Accommodative Monetary Policy**: Cut interest rate by {r - results['r_opt']:.2f}%")
            else:
                st.warning(f"⚠️ **Tight Monetary Policy**: Raise interest rate by {results['r_opt'] - r:.2f}%")

# ========== TAB 2: TRADE-OFF ANALYSIS ==========
with tab2:
    st.markdown(f"### {txt['tradeoff_title']}")
    
    if 'optimization_results' in st.session_state:
        # Generate trade-off curves
        growth_range = np.linspace(2, 8, 50)
        
        # Growth vs Inflation trade-off
        inflation_tradeoff = inflation + 0.3 * (growth_range - ((current_gdp * 1.05 - current_gdp) / current_gdp * 100))
        
        # Growth vs Unemployment trade-off (Phillips Curve)
        unemployment_tradeoff = unemployment - 0.5 * (growth_range - 2)
        
        fig = make_subplots(rows=1, cols=2,
                           subplot_titles=(txt['growth_inflation'], txt['growth_unemployment']))
        
        # Growth vs Inflation
        fig.add_trace(go.Scatter(x=growth_range, y=inflation_tradeoff,
                                mode='lines', name='Trade-off Curve',
                                line=dict(color='red', width=3)),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=[target_growth], y=[target_inflation],
                                mode='markers', name='Target',
                                marker=dict(size=15, color='green', symbol='star')),
                     row=1, col=1)
        
        # Growth vs Unemployment
        fig.add_trace(go.Scatter(x=growth_range, y=unemployment_tradeoff,
                                mode='lines', name='Phillips Curve',
                                line=dict(color='blue', width=3)),
                     row=1, col=2)
        fig.add_trace(go.Scatter(x=[target_growth], y=[target_unemployment],
                                mode='markers', name='Target',
                                marker=dict(size=15, color='green', symbol='star')),
                     row=1, col=2)
        
        fig.update_xaxes(title_text="GDP Growth (%)", row=1, col=1)
        fig.update_yaxes(title_text="Inflation (%)", row=1, col=1)
        fig.update_xaxes(title_text="GDP Growth (%)", row=1, col=2)
        fig.update_yaxes(title_text="Unemployment (%)", row=1, col=2)
        fig.update_layout(height=500, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Trade-off Interpretation:**
        - **Growth vs Inflation**: Higher growth typically leads to higher inflation (demand-pull)
        - **Growth vs Unemployment**: Higher growth reduces unemployment (Okun's Law)
        - The green star shows your target - AI finds the policy mix to get closest to it
        """)
    else:
        st.info("Run optimization in Tab 1 first to see trade-off analysis")

# ========== TAB 3: DYNAMIC SIMULATION ==========
with tab3:
    st.markdown(f"### {txt['dynamic_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        periods = st.slider(txt['simulation_periods'], 4, 20, 12)
        shock = st.selectbox(txt['shock_type'], 
                            [txt['no_shock'], txt['demand_shock'], txt['supply_shock'], txt['financial_shock']])
        
        if st.button(txt['run_simulation'], type='primary'):
            # Dynamic simulation with policy response
            time = np.arange(periods)
            
            # Initialize arrays
            gdp_path = np.zeros(periods)
            inflation_path = np.zeros(periods)
            unemployment_path = np.zeros(periods)
            rate_path = np.zeros(periods)
            
            # Initial values
            gdp_path[0] = current_gdp
            inflation_path[0] = inflation
            unemployment_path[0] = unemployment
            rate_path[0] = r
            
            # Apply shock
            for t in range(1, periods):
                if t == 2:  # Shock hits in period 2
                    if shock == txt['demand_shock']:
                        gdp_path[t] = gdp_path[t-1] * 0.9
                    elif shock == txt['supply_shock']:
                        inflation_path[t] = inflation_path[t-1] + 5
                    elif shock == txt['financial_shock']:
                        rate_path[t] = rate_path[t-1] + 3
                
                # Policy response (Taylor Rule)
                if t > 2:
                    inflation_gap = inflation_path[t-1] - target_inflation
                    output_gap = (gdp_path[t-1] - current_gdp) / current_gdp * 100
                    rate_path[t] = r + 0.5 * inflation_gap + 0.5 * output_gap
                    rate_path[t] = np.clip(rate_path[t], min_rate, max_rate)
                
                # Economic dynamics
                if t > 0:
                    gdp_growth = -0.5 * (rate_path[t] - rate_path[t-1]) + 0.3 * (inflation_path[t-1] - 2)
                    gdp_path[t] = gdp_path[t-1] * (1 + gdp_growth/100) if gdp_path[t] == 0 else gdp_path[t]
                    
                    if inflation_path[t] == 0:
                        inflation_path[t] = inflation_path[t-1] + 0.2 * gdp_growth - 0.3 * (rate_path[t] - rate_path[t-1])
                    
                    unemployment_path[t] = unemployment_path[t-1] - 0.5 * gdp_growth
            
            st.session_state['simulation'] = {
                'time': time,
                'gdp': gdp_path,
                'inflation': inflation_path,
                'unemployment': unemployment_path,
                'rate': rate_path
            }
    
    with col2:
        if 'simulation' in st.session_state:
            sim = st.session_state['simulation']
            
            fig = make_subplots(rows=2, cols=2,
                               subplot_titles=("GDP Path", "Inflation Path", 
                                             "Unemployment Path", "Interest Rate Path"))
            
            fig.add_trace(go.Scatter(x=sim['time'], y=sim['gdp'], mode='lines+markers',
                                    name='GDP', line=dict(color='blue', width=2)),
                         row=1, col=1)
            fig.add_trace(go.Scatter(x=sim['time'], y=sim['inflation'], mode='lines+markers',
                                    name='Inflation', line=dict(color='red', width=2)),
                         row=1, col=2)
            fig.add_trace(go.Scatter(x=sim['time'], y=sim['unemployment'], mode='lines+markers',
                                    name='Unemployment', line=dict(color='green', width=2)),
                         row=2, col=1)
            fig.add_trace(go.Scatter(x=sim['time'], y=sim['rate'], mode='lines+markers',
                                    name='Interest Rate', line=dict(color='purple', width=2)),
                         row=2, col=2)
            
            fig.update_xaxes(title_text="Quarter", row=2, col=1)
            fig.update_xaxes(title_text="Quarter", row=2, col=2)
            fig.update_layout(height=700, showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 4: SCENARIO COMPARISON ==========
with tab4:
    st.markdown(f"### {txt['scenario_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        scenario_name = st.text_input(txt['scenario_name'], value="Scenario A")
        scenario_g = st.number_input("G", value=3000.0, step=100.0, key='sc_g')
        scenario_r = st.number_input("Interest Rate", value=5.0, step=0.25, key='sc_r')
        
        if st.button(txt['add_scenario']):
            # Calculate outcomes
            I_sc = I - 200 * (scenario_r - r)
            NX_sc = NX - 100 * (scenario_r - r)
            C_sc = C + 0.75 * (scenario_g - G)
            GDP_sc = C_sc + I_sc + scenario_g + NX_sc
            growth_sc = ((GDP_sc - current_gdp) / current_gdp) * 100
            
            st.session_state['scenarios'].append({
                'Name': scenario_name,
                'G': scenario_g,
                'Rate': scenario_r,
                'GDP': GDP_sc,
                'Growth': growth_sc
            })
            st.success(f"Added {scenario_name}!")
    
    with col2:
        if len(st.session_state['scenarios']) > 0:
            df_scenarios = pd.DataFrame(st.session_state['scenarios'])
            
            st.dataframe(df_scenarios.style.highlight_max(subset=['Growth'], color='lightgreen'),
                        use_container_width=True, hide_index=True)
            
            best_idx = df_scenarios['Growth'].idxmax()
            st.success(f"🏆 {txt['best_scenario']}: {df_scenarios.iloc[best_idx]['Name']} (Growth: {df_scenarios.iloc[best_idx]['Growth']:.2f}%)")
        else:
            st.info("Add scenarios to compare")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_central_bank'])
        st.write(txt['use_ministry'])
        st.write(txt['use_researcher'])
