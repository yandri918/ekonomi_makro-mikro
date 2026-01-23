import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import minimize, differential_evolution
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Professional Macro Policy AI", page_icon="🎯", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

# ==================== TRANSLATIONS ====================
T = {
    'EN': {
        'title': "🎯 Professional AI Macroeconomic Policy Optimizer",
        'subtitle': "Central Bank-Grade: Multi-objective optimization with Monte Carlo risk analysis, real-time dashboard, and stress testing.",
        'tab1': "🎯 Policy Optimization",
        'tab2': "📊 Trade-off Analysis",
        'tab3': "🔮 Dynamic Simulation",
        'tab4': "📈 Stress Testing",
        'tab5': "🎛️ Real-Time Dashboard",
        'tab6': "📄 Reports",
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
        'optimize': "🚀 Run Professional Optimization",
        'monte_carlo': "Enable Monte Carlo Risk Analysis",
        'n_simulations': "Number of Simulations",
        'results': "Optimization Results",
        'optimal_policy': "Optimal Policy Mix",
        'risk_metrics': "Risk Metrics",
        'confidence_interval': "95% Confidence Interval",
        'var_95': "Value at Risk (95%)",
        'cvar_95': "Conditional VaR (95%)",
        'prob_recession': "Probability of Recession",
        'new_g': "Recommended G",
        'new_r': "Recommended Interest Rate",
        'predicted_outcomes': "Predicted Outcomes",
        'predicted_growth': "Predicted GDP Growth",
        'predicted_inflation': "Predicted Inflation",
        'predicted_unemployment': "Predicted Unemployment",
        'policy_score': "Policy Effectiveness Score",
        # Tab 4
        'stress_title': "Comprehensive Stress Testing",
        'stress_intro': "Test policy robustness under extreme economic scenarios",
        'select_stress': "Select Stress Scenario",
        'run_stress': "Run Stress Test",
        'stress_results': "Stress Test Results",
        'resilience_score': "Resilience Score",
        'max_drawdown': "Maximum Drawdown",
        'recovery_time': "Recovery Time (Quarters)",
        # Tab 5
        'dashboard_title': "Real-Time Policy Control Center",
        'current_status': "Current Economic Status",
        'policy_recommendations': "AI Policy Recommendations",
        'status_indicators': "Policy Status Indicators",
        # Tab 6
        'report_title': "Professional Reports & Communication",
        'policy_statement': "Policy Statement",
        'export_data': "Export Data",
        'download_csv': "Download CSV Report"
    },
    'ID': {
        'title': "🎯 AI Pengoptimal Kebijakan Makroekonomi Profesional",
        'subtitle': "Setara Bank Sentral: Optimasi multi-objektif dengan analisis risiko Monte Carlo, dashboard real-time, dan stress testing.",
        'tab1': "🎯 Optimasi Kebijakan",
        'tab2': "📊 Analisis Trade-off",
        'tab3': "🔮 Simulasi Dinamis",
        'tab4': "📈 Stress Testing",
        'tab5': "🎛️ Dashboard Real-Time",
        'tab6': "📄 Laporan",
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
        'optimize': "🚀 Jalankan Optimasi Profesional",
        'monte_carlo': "Aktifkan Analisis Risiko Monte Carlo",
        'n_simulations': "Jumlah Simulasi",
        'results': "Hasil Optimasi",
        'optimal_policy': "Bauran Kebijakan Optimal",
        'risk_metrics': "Metrik Risiko",
        'confidence_interval': "Interval Kepercayaan 95%",
        'var_95': "Value at Risk (95%)",
        'cvar_95': "Conditional VaR (95%)",
        'prob_recession': "Probabilitas Resesi",
        'new_g': "G yang Direkomendasikan",
        'new_r': "Suku Bunga yang Direkomendasikan",
        'predicted_outcomes': "Hasil Prediksi",
        'predicted_growth': "Pertumbuhan PDB Prediksi",
        'predicted_inflation': "Inflasi Prediksi",
        'predicted_unemployment': "Pengangguran Prediksi",
        'policy_score': "Skor Efektivitas Kebijakan",
        # Tab 4
        'stress_title': "Stress Testing Komprehensif",
        'stress_intro': "Uji ketahanan kebijakan di bawah skenario ekonomi ekstrem",
        'select_stress': "Pilih Skenario Stress",
        'run_stress': "Jalankan Stress Test",
        'stress_results': "Hasil Stress Test",
        'resilience_score': "Skor Ketahanan",
        'max_drawdown': "Penurunan Maksimum",
        'recovery_time': "Waktu Pemulihan (Kuartal)",
        # Tab 5
        'dashboard_title': "Pusat Kontrol Kebijakan Real-Time",
        'current_status': "Status Ekonomi Saat Ini",
        'policy_recommendations': "Rekomendasi Kebijakan AI",
        'status_indicators': "Indikator Status Kebijakan",
        # Tab 6
        'report_title': "Laporan & Komunikasi Profesional",
        'policy_statement': "Pernyataan Kebijakan",
        'export_data': "Ekspor Data",
        'download_csv': "Unduh Laporan CSV"
    }
}

txt = T[lang]

# Initialize session state
if 'scenarios' not in st.session_state:
    st.session_state['scenarios'] = []

# ==================== HELPER FUNCTIONS ====================

@st.cache_data
def monte_carlo_risk_analysis(G_opt, r_opt, C, I, G, NX, r, inflation, unemployment, 
                               target_growth, target_inflation, target_unemployment, n_sim=5000):
    """Monte Carlo simulation for risk analysis"""
    
    # Parameter distributions (uncertainty)
    MPC_dist = np.random.normal(0.75, 0.05, n_sim)
    alpha_I_dist = np.random.normal(200, 20, n_sim)
    alpha_NX_dist = np.random.normal(100, 15, n_sim)
    
    # Shock distributions
    demand_shocks = np.random.normal(0, 0.5, n_sim)
    supply_shocks = np.random.normal(0, 0.3, n_sim)
    
    growth_dist = []
    inflation_dist = []
    unemployment_dist = []
    
    current_gdp = C + I + G + NX
    
    for i in range(n_sim):
        MPC = np.clip(MPC_dist[i], 0.5, 0.9)
        alpha_I = np.clip(alpha_I_dist[i], 100, 300)
        alpha_NX = np.clip(alpha_NX_dist[i], 50, 150)
        
        # Calculate with uncertainty
        I_new = I - alpha_I * (r_opt - r) + demand_shocks[i] * 100
        NX_new = NX - alpha_NX * (r_opt - r) + demand_shocks[i] * 50
        C_new = C + MPC * (G_opt - G) + demand_shocks[i] * 200
        
        GDP_new = C_new + I_new + G_opt + NX_new
        growth = ((GDP_new - current_gdp) / current_gdp) * 100
        
        # Inflation with uncertainty
        output_gap = (GDP_new - current_gdp) / current_gdp * 100
        inflation_new = inflation + 0.3 * output_gap - 0.2 * (r_opt - r) + supply_shocks[i]
        
        # Unemployment
        unemployment_new = unemployment - 0.5 * (growth - 2)
        
        growth_dist.append(growth)
        inflation_dist.append(inflation_new)
        unemployment_dist.append(unemployment_new)
    
    # Calculate risk metrics
    growth_mean = np.mean(growth_dist)
    growth_std = np.std(growth_dist)
    growth_ci_lower = np.percentile(growth_dist, 2.5)
    growth_ci_upper = np.percentile(growth_dist, 97.5)
    growth_var_95 = np.percentile(growth_dist, 5)
    growth_cvar_95 = np.mean([g for g in growth_dist if g <= growth_var_95])
    prob_recession = np.mean([g < 0 for g in growth_dist]) * 100
    
    inflation_mean = np.mean(inflation_dist)
    inflation_std = np.std(inflation_dist)
    inflation_ci_lower = np.percentile(inflation_dist, 2.5)
    inflation_ci_upper = np.percentile(inflation_dist, 97.5)
    
    unemployment_mean = np.mean(unemployment_dist)
    unemployment_std = np.std(unemployment_dist)
    
    return {
        'growth': {'mean': growth_mean, 'std': growth_std, 
                  'ci_lower': growth_ci_lower, 'ci_upper': growth_ci_upper,
                  'var_95': growth_var_95, 'cvar_95': growth_cvar_95,
                  'dist': growth_dist},
        'inflation': {'mean': inflation_mean, 'std': inflation_std,
                     'ci_lower': inflation_ci_lower, 'ci_upper': inflation_ci_upper,
                     'dist': inflation_dist},
        'unemployment': {'mean': unemployment_mean, 'std': unemployment_std,
                        'dist': unemployment_dist},
        'prob_recession': prob_recession
    }

def run_stress_test(G_opt, r_opt, C, I, G, NX, r, inflation, unemployment, scenario_params):
    """Run stress test for a specific scenario"""
    
    current_gdp = C + I + G + NX
    periods = 12
    
    # Initialize paths
    gdp_path = np.zeros(periods)
    inflation_path = np.zeros(periods)
    unemployment_path = np.zeros(periods)
    rate_path = np.zeros(periods)
    
    gdp_path[0] = current_gdp
    inflation_path[0] = inflation
    unemployment_path[0] = unemployment
    rate_path[0] = r_opt
    
    # Apply shocks
    for t in range(1, periods):
        if t == 2:  # Shock hits in period 2
            gdp_path[t] = gdp_path[t-1] * (1 + scenario_params['demand_shock']/100)
            inflation_path[t] = inflation_path[t-1] + scenario_params['supply_shock']
            rate_path[t] = rate_path[t-1] + scenario_params['financial_shock']
        
        # Policy response (Taylor Rule)
        if t > 2:
            inflation_gap = inflation_path[t-1] - 3.0  # Target inflation
            output_gap = (gdp_path[t-1] - current_gdp) / current_gdp * 100
            rate_path[t] = r_opt + 0.5 * inflation_gap + 0.5 * output_gap
            rate_path[t] = np.clip(rate_path[t], 2.0, 10.0)
        
        # Economic dynamics
        if t > 0 and gdp_path[t] == 0:
            gdp_growth = -0.5 * (rate_path[t] - rate_path[t-1]) + 0.3 * (inflation_path[t-1] - 2)
            gdp_path[t] = gdp_path[t-1] * (1 + gdp_growth/100)
            
            if inflation_path[t] == 0:
                inflation_path[t] = inflation_path[t-1] + 0.2 * gdp_growth - 0.3 * (rate_path[t] - rate_path[t-1])
            
            unemployment_path[t] = unemployment_path[t-1] - 0.5 * gdp_growth
    
    # Calculate resilience metrics
    max_drawdown = min((gdp_path - current_gdp) / current_gdp * 100)
    recovery_time = 0
    for t in range(len(gdp_path)):
        if gdp_path[t] >= current_gdp * 0.99:
            recovery_time = t
            break
    if recovery_time == 0:
        recovery_time = periods
    
    avg_inflation = np.mean(inflation_path)
    max_unemployment = max(unemployment_path)
    
    resilience_score = max(0, 100 - abs(max_drawdown) * 10 - recovery_time * 5)
    
    return {
        'gdp_path': gdp_path,
        'inflation_path': inflation_path,
        'unemployment_path': unemployment_path,
        'rate_path': rate_path,
        'max_drawdown': max_drawdown,
        'recovery_time': recovery_time,
        'avg_inflation': avg_inflation,
        'max_unemployment': max_unemployment,
        'resilience_score': resilience_score
    }

def generate_policy_statement(results, lang='ID'):
    """Generate central bank-style policy statement"""
    
    if lang == 'ID':
        statement = f"""
### PERNYATAAN KEBIJAKAN EKONOMI

**Berdasarkan analisis ekonomi terkini dan proyeksi ke depan, kami merekomendasikan:**

#### 1. KEBIJAKAN FISKAL
- **Belanja Pemerintah:** Rp {results['G_opt']:,.0f} Triliun
- **Perubahan:** {results['G_opt'] - results['G_current']:+,.0f} Triliun ({(results['G_opt']/results['G_current'] - 1)*100:+.1f}%)
- **Rasionale:** {"Stimulus fiskal diperlukan untuk mendorong pertumbuhan ekonomi" if results['G_opt'] > results['G_current'] else "Konsolidasi fiskal untuk menjaga keberlanjutan"}

#### 2. KEBIJAKAN MONETER
- **Suku Bunga Acuan:** {results['r_opt']:.2f}%
- **Perubahan:** {results['r_opt'] - results['r_current']:+.2f}%
- **Rasionale:** {"Pelonggaran moneter untuk mendukung aktivitas ekonomi" if results['r_opt'] < results['r_current'] else "Pengetatan untuk mengendalikan inflasi"}

#### 3. PROYEKSI EKONOMI
- **Pertumbuhan PDB:** {results['growth_pred']:.1f}% (Target: {results['growth_target']:.1f}%)
- **Inflasi:** {results['inflation_pred']:.1f}% (Target: {results['inflation_target']:.1f}%)
- **Pengangguran:** {results['unemployment_pred']:.1f}% (Target: {results['unemployment_target']:.1f}%)

#### 4. ANALISIS RISIKO
- **Probabilitas Resesi:** {results.get('prob_recession', 0):.1f}%
- **Interval Kepercayaan Pertumbuhan:** [{results.get('growth_ci_lower', 0):.1f}%, {results.get('growth_ci_upper', 0):.1f}%]
- **Skor Efektivitas Kebijakan:** {results['score']:.1f}/100

**Kebijakan ini akan ditinjau kembali pada periode berikutnya berdasarkan perkembangan data ekonomi.**
        """
    else:
        statement = f"""
### ECONOMIC POLICY STATEMENT

**Based on current economic analysis and forward projections, we recommend:**

#### 1. FISCAL POLICY
- **Government Spending:** Rp {results['G_opt']:,.0f} Trillion
- **Change:** {results['G_opt'] - results['G_current']:+,.0f} Trillion ({(results['G_opt']/results['G_current'] - 1)*100:+.1f}%)
- **Rationale:** {"Fiscal stimulus needed to support economic growth" if results['G_opt'] > results['G_current'] else "Fiscal consolidation for sustainability"}

#### 2. MONETARY POLICY
- **Policy Rate:** {results['r_opt']:.2f}%
- **Change:** {results['r_opt'] - results['r_current']:+.2f}%
- **Rationale:** {"Monetary easing to support economic activity" if results['r_opt'] < results['r_current'] else "Tightening to control inflation"}

#### 3. ECONOMIC PROJECTIONS
- **GDP Growth:** {results['growth_pred']:.1f}% (Target: {results['growth_target']:.1f}%)
- **Inflation:** {results['inflation_pred']:.1f}% (Target: {results['inflation_target']:.1f}%)
- **Unemployment:** {results['unemployment_pred']:.1f}% (Target: {results['unemployment_target']:.1f}%)

#### 4. RISK ANALYSIS
- **Recession Probability:** {results.get('prob_recession', 0):.1f}%
- **Growth Confidence Interval:** [{results.get('growth_ci_lower', 0):.1f}%, {results.get('growth_ci_upper', 0):.1f}%]
- **Policy Effectiveness Score:** {results['score']:.1f}/100

**This policy will be reviewed in the next period based on economic data developments.**
        """
    
    return statement

# ==================== MAIN UI ====================

st.title(txt['title'])
st.markdown(txt['subtitle'])

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4'], txt['tab5'], txt['tab6']])

# ========== TAB 1: ENHANCED POLICY OPTIMIZATION ==========
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
        
        st.markdown("---")
        enable_mc = st.checkbox(txt['monte_carlo'], value=True)
        if enable_mc:
            n_sim = st.select_slider(txt['n_simulations'], 
                                     options=[1000, 2500, 5000, 10000], 
                                     value=5000)
        
        if st.button(txt['optimize'], type='primary'):
            with st.spinner('Running professional optimization...'):
                # Parameters
                MPC = 0.75
                alpha_I = 200
                alpha_NX = 100
                
                # Objective function
                def objective(x):
                    G_new, r_new = x
                    
                    I_new = I - alpha_I * (r_new - r)
                    NX_new = NX - alpha_NX * (r_new - r)
                    C_new = C + MPC * (G_new - G)
                    
                    GDP_new = C_new + I_new + G_new + NX_new
                    growth_actual = ((GDP_new - current_gdp) / current_gdp) * 100
                    
                    output_gap = (GDP_new - current_gdp) / current_gdp * 100
                    inflation_new = inflation + 0.3 * output_gap - 0.2 * (r_new - r)
                    
                    unemployment_new = unemployment - 0.5 * (growth_actual - 2)
                    
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
                
                bounds = [(G * 0.8, G * 1.5), (min_rate, max_rate)]
                constraints = [
                    {'type': 'ineq', 'fun': constraint_deficit},
                    {'type': 'ineq', 'fun': constraint_rate_change}
                ]
                
                x0 = [G, r]
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
                    
                    score_growth = max(0, 100 - abs(growth_pred - target_growth) * 20)
                    score_inflation = max(0, 100 - abs(inflation_pred - target_inflation) * 20)
                    score_unemployment = max(0, 100 - abs(unemployment_pred - target_unemployment) * 20)
                    overall_score = (score_growth + score_inflation + score_unemployment) / 3
                    
                    results = {
                        'G_opt': G_opt,
                        'r_opt': r_opt,
                        'GDP_opt': GDP_opt,
                        'growth_pred': growth_pred,
                        'inflation_pred': inflation_pred,
                        'unemployment_pred': unemployment_pred,
                        'score': overall_score,
                        'C_opt': C_opt,
                        'I_opt': I_opt,
                        'NX_opt': NX_opt,
                        'G_current': G,
                        'r_current': r,
                        'growth_target': target_growth,
                        'inflation_target': target_inflation,
                        'unemployment_target': target_unemployment
                    }
                    
                    # Monte Carlo Risk Analysis
                    if enable_mc:
                        with st.spinner(f'Running Monte Carlo simulation ({n_sim:,} iterations)...'):
                            mc_results = monte_carlo_risk_analysis(
                                G_opt, r_opt, C, I, G, NX, r, inflation, unemployment,
                                target_growth, target_inflation, target_unemployment, n_sim
                            )
                            results['mc'] = mc_results
                            results['prob_recession'] = mc_results['prob_recession']
                            results['growth_ci_lower'] = mc_results['growth']['ci_lower']
                            results['growth_ci_upper'] = mc_results['growth']['ci_upper']
                    
                    st.session_state['optimization_results'] = results
                    st.success("✅ Optimization complete!")
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
            
            if 'mc' in results:
                mc = results['mc']
                o1.metric(txt['predicted_growth'], 
                         f"{mc['growth']['mean']:.2f}%",
                         delta=f"±{mc['growth']['std']:.2f}%",
                         help=f"95% CI: [{mc['growth']['ci_lower']:.2f}%, {mc['growth']['ci_upper']:.2f}%]")
                o2.metric(txt['predicted_inflation'], 
                         f"{mc['inflation']['mean']:.2f}%",
                         delta=f"±{mc['inflation']['std']:.2f}%",
                         help=f"95% CI: [{mc['inflation']['ci_lower']:.2f}%, {mc['inflation']['ci_upper']:.2f}%]")
                o3.metric(txt['predicted_unemployment'], 
                         f"{mc['unemployment']['mean']:.2f}%",
                         delta=f"±{mc['unemployment']['std']:.2f}%")
            else:
                o1.metric(txt['predicted_growth'], f"{results['growth_pred']:.2f}%")
                o2.metric(txt['predicted_inflation'], f"{results['inflation_pred']:.2f}%")
                o3.metric(txt['predicted_unemployment'], f"{results['unemployment_pred']:.2f}%")
            
            st.metric(txt['policy_score'], f"{results['score']:.1f}/100")
            
            # Risk Metrics (if Monte Carlo enabled)
            if 'mc' in results:
                st.markdown(f"#### {txt['risk_metrics']}")
                
                r1, r2, r3 = st.columns(3)
                r1.metric(txt['var_95'], f"{mc['growth']['var_95']:.2f}%",
                         help="5% worst-case growth scenario")
                r2.metric(txt['cvar_95'], f"{mc['growth']['cvar_95']:.2f}%",
                         help="Average of worst 5% scenarios")
                r3.metric(txt['prob_recession'], f"{results['prob_recession']:.1f}%",
                         delta_color="inverse")
                
                # Probability distribution
                fig_dist = go.Figure()
                fig_dist.add_trace(go.Histogram(
                    x=mc['growth']['dist'],
                    nbinsx=50,
                    name='Growth Distribution',
                    marker_color='lightblue',
                    opacity=0.7
                ))
                fig_dist.add_vline(x=target_growth, line_dash="dash", line_color="green",
                                  annotation_text="Target")
                fig_dist.add_vline(x=mc['growth']['mean'], line_dash="dash", line_color="blue",
                                  annotation_text="Mean")
                fig_dist.update_layout(
                    title="GDP Growth Probability Distribution",
                    xaxis_title="Growth (%)",
                    yaxis_title="Frequency",
                    height=300
                )
                st.plotly_chart(fig_dist, use_container_width=True)
            
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

# ========== TAB 2: TRADE-OFF ANALYSIS (Keep existing) ==========
with tab2:
    st.markdown("### 📊 Policy Trade-off Analysis")
    
    if 'optimization_results' in st.session_state:
        growth_range = np.linspace(2, 8, 50)
        inflation_tradeoff = inflation + 0.3 * (growth_range - ((current_gdp * 1.05 - current_gdp) / current_gdp * 100))
        unemployment_tradeoff = unemployment - 0.5 * (growth_range - 2)
        
        fig = make_subplots(rows=1, cols=2,
                           subplot_titles=("Growth vs Inflation Trade-off", "Growth vs Unemployment (Phillips Curve)"))
        
        fig.add_trace(go.Scatter(x=growth_range, y=inflation_tradeoff,
                                mode='lines', name='Trade-off Curve',
                                line=dict(color='red', width=3)),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=[target_growth], y=[target_inflation],
                                mode='markers', name='Target',
                                marker=dict(size=15, color='green', symbol='star')),
                     row=1, col=1)
        
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

# ========== TAB 3: DYNAMIC SIMULATION (Keep existing) ==========
with tab3:
    st.markdown("### 🔮 Dynamic Policy Simulation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        sim_current_gdp = C + I + G + NX
        sim_inflation = inflation
        sim_unemployment = unemployment
        sim_r = r
        sim_target_inflation = target_inflation
        sim_min_rate = min_rate
        sim_max_rate = max_rate
        
        periods = st.slider("Simulation Periods (Quarters)", 4, 20, 12)
        shock_options = ["No Shock (Baseline)", "Demand Shock (-10%)", "Supply Shock (+5% inflation)", "Financial Crisis (+3% rate)"]
        shock = st.selectbox("Economic Shock", shock_options)
        
        if st.button("Run Dynamic Simulation", type='primary'):
            time = np.arange(periods)
            
            gdp_path = np.zeros(periods)
            inflation_path = np.zeros(periods)
            unemployment_path = np.zeros(periods)
            rate_path = np.zeros(periods)
            
            gdp_path[0] = sim_current_gdp
            inflation_path[0] = sim_inflation
            unemployment_path[0] = sim_unemployment
            rate_path[0] = sim_r
            
            for t in range(1, periods):
                if t == 2:
                    if shock == "Demand Shock (-10%)":
                        gdp_path[t] = gdp_path[t-1] * 0.9
                    elif shock == "Supply Shock (+5% inflation)":
                        inflation_path[t] = inflation_path[t-1] + 5
                    elif shock == "Financial Crisis (+3% rate)":
                        rate_path[t] = rate_path[t-1] + 3
                
                if t > 2:
                    inflation_gap = inflation_path[t-1] - sim_target_inflation
                    output_gap = (gdp_path[t-1] - sim_current_gdp) / sim_current_gdp * 100
                    rate_path[t] = sim_r + 0.5 * inflation_gap + 0.5 * output_gap
                    rate_path[t] = np.clip(rate_path[t], sim_min_rate, sim_max_rate)
                
                if t > 0:
                    gdp_growth = -0.5 * (rate_path[t] - rate_path[t-1]) + 0.3 * (inflation_path[t-1] - 2)
                    gdp_path[t] = gdp_path[t-1] * (1 + gdp_growth/100) if gdp_path[t] == 0 else gdp_path[t]
                    
                    if inflation_path[t] == 0:
                        inflation_path[t] = inflation_path[t-1] + 0.2 * gdp_growth - 0.3 * (rate_path[t] - rate_path[t-1])
                    
                    unemployment_path[t] = unemployment_path[t-1] - 0.5 * gdp_growth
            
            st.session_state['simulation_results'] = {
                'time': time,
                'gdp': gdp_path,
                'inflation': inflation_path,
                'unemployment': unemployment_path,
                'rate': rate_path
            }
    
    with col2:
        if 'simulation_results' in st.session_state:
            sim = st.session_state['simulation_results']
            
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
        else:
            st.info("Click 'Run Dynamic Simulation' to see results")

# ========== TAB 4: STRESS TESTING ==========
with tab4:
    st.markdown(f"### {txt['stress_title']}")
    st.markdown(txt['stress_intro'])
    
    if 'optimization_results' in st.session_state:
        results = st.session_state['optimization_results']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            stress_scenarios = {
                'Mild Recession': {'demand_shock': -5, 'supply_shock': 0, 'financial_shock': 1},
                'Severe Recession': {'demand_shock': -15, 'supply_shock': 0, 'financial_shock': 3},
                'Stagflation': {'demand_shock': -5, 'supply_shock': 5, 'financial_shock': 2},
                'Financial Crisis': {'demand_shock': -10, 'supply_shock': 0, 'financial_shock': 5},
                'Supply Shock (Oil)': {'demand_shock': 0, 'supply_shock': 8, 'financial_shock': 0},
                'Demand Boom': {'demand_shock': 10, 'supply_shock': 0, 'financial_shock': -1}
            }
            
            selected_scenario = st.selectbox(txt['select_stress'], list(stress_scenarios.keys()))
            
            if st.button(txt['run_stress'], type='primary'):
                with st.spinner('Running stress test...'):
                    stress_result = run_stress_test(
                        results['G_opt'], results['r_opt'],
                        C, I, G, NX, r, inflation, unemployment,
                        stress_scenarios[selected_scenario]
                    )
                    st.session_state['stress_result'] = stress_result
                    st.session_state['stress_scenario'] = selected_scenario
        
        with col2:
            if 'stress_result' in st.session_state:
                stress = st.session_state['stress_result']
                scenario_name = st.session_state['stress_scenario']
                
                st.markdown(f"#### {txt['stress_results']}: {scenario_name}")
                
                # Metrics
                m1, m2, m3, m4 = st.columns(4)
                m1.metric(txt['resilience_score'], f"{stress['resilience_score']:.0f}/100")
                m2.metric(txt['max_drawdown'], f"{stress['max_drawdown']:.1f}%",
                         delta_color="inverse")
                m3.metric(txt['recovery_time'], f"{stress['recovery_time']} Q")
                m4.metric("Max Unemployment", f"{stress['max_unemployment']:.1f}%",
                         delta_color="inverse")
                
                # Paths visualization
                fig_stress = make_subplots(rows=2, cols=2,
                                          subplot_titles=("GDP Path", "Inflation Path",
                                                        "Unemployment Path", "Interest Rate Response"))
                
                quarters = list(range(len(stress['gdp_path'])))
                
                fig_stress.add_trace(go.Scatter(x=quarters, y=stress['gdp_path'],
                                               mode='lines+markers', name='GDP',
                                               line=dict(color='blue', width=2)),
                                    row=1, col=1)
                fig_stress.add_trace(go.Scatter(x=quarters, y=stress['inflation_path'],
                                               mode='lines+markers', name='Inflation',
                                               line=dict(color='red', width=2)),
                                    row=1, col=2)
                fig_stress.add_trace(go.Scatter(x=quarters, y=stress['unemployment_path'],
                                               mode='lines+markers', name='Unemployment',
                                               line=dict(color='green', width=2)),
                                    row=2, col=1)
                fig_stress.add_trace(go.Scatter(x=quarters, y=stress['rate_path'],
                                               mode='lines+markers', name='Rate',
                                               line=dict(color='purple', width=2)),
                                    row=2, col=2)
                
                fig_stress.update_xaxes(title_text="Quarter", row=2, col=1)
                fig_stress.update_xaxes(title_text="Quarter", row=2, col=2)
                fig_stress.update_layout(height=600, showlegend=False)
                
                st.plotly_chart(fig_stress, use_container_width=True)
                
                # Interpretation
                if stress['resilience_score'] >= 70:
                    st.success(f"✅ **High Resilience**: Policy performs well under {scenario_name} scenario")
                elif stress['resilience_score'] >= 50:
                    st.warning(f"⚠️ **Moderate Resilience**: Policy shows some vulnerability to {scenario_name}")
                else:
                    st.error(f"🔴 **Low Resilience**: Policy may need adjustment for {scenario_name} scenario")
            else:
                st.info("Select a stress scenario and click 'Run Stress Test'")
    else:
        st.info("Run optimization in Tab 1 first")

# ========== TAB 5: REAL-TIME DASHBOARD ==========
with tab5:
    st.markdown(f"### {txt['dashboard_title']}")
    
    if 'optimization_results' in st.session_state:
        results = st.session_state['optimization_results']
        
        # Current Status Gauges
        st.markdown(f"#### {txt['current_status']}")
        
        col1, col2, col3 = st.columns(3)
        
        # GDP Growth Gauge
        with col1:
            fig_gauge_growth = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = results.get('growth_pred', 0) if 'mc' not in results else results['mc']['growth']['mean'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "GDP Growth (%)"},
                delta = {'reference': target_growth},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 3], 'color': "lightgray"},
                        {'range': [3, 6], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': target_growth}
                }
            ))
            fig_gauge_growth.update_layout(height=250)
            st.plotly_chart(fig_gauge_growth, use_container_width=True)
        
        # Inflation Gauge
        with col2:
            fig_gauge_inflation = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = results.get('inflation_pred', 0) if 'mc' not in results else results['mc']['inflation']['mean'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Inflation (%)"},
                delta = {'reference': target_inflation},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkred"},
                    'steps': [
                        {'range': [0, 2], 'color': "lightgray"},
                        {'range': [2, 4], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': target_inflation}
                }
            ))
            fig_gauge_inflation.update_layout(height=250)
            st.plotly_chart(fig_gauge_inflation, use_container_width=True)
        
        # Unemployment Gauge
        with col3:
            fig_gauge_unemployment = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = results.get('unemployment_pred', 0) if 'mc' not in results else results['mc']['unemployment']['mean'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Unemployment (%)"},
                delta = {'reference': target_unemployment, 'increasing': {'color': "red"}},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 4], 'color': "lightgray"},
                        {'range': [4, 7], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': target_unemployment}
                }
            ))
            fig_gauge_unemployment.update_layout(height=250)
            st.plotly_chart(fig_gauge_unemployment, use_container_width=True)
        
        st.markdown("---")
        
        # Traffic Light Indicators
        st.markdown(f"#### {txt['status_indicators']}")
        
        col_tl1, col_tl2, col_tl3 = st.columns(3)
        
        growth_actual = results.get('growth_pred', 0) if 'mc' not in results else results['mc']['growth']['mean']
        inflation_actual = results.get('inflation_pred', 0) if 'mc' not in results else results['mc']['inflation']['mean']
        unemployment_actual = results.get('unemployment_pred', 0) if 'mc' not in results else results['mc']['unemployment']['mean']
        
        with col_tl1:
            growth_diff = abs(growth_actual - target_growth)
            if growth_diff < 0.5:
                st.markdown("### 🟢 **Growth: ON TARGET**")
            elif growth_diff < 1.0:
                st.markdown("### 🟡 **Growth: NEAR TARGET**")
            else:
                st.markdown("### 🔴 **Growth: OFF TARGET**")
            st.write(f"Deviation: {growth_diff:.2f}%")
        
        with col_tl2:
            inflation_diff = abs(inflation_actual - target_inflation)
            if inflation_diff < 0.5:
                st.markdown("### 🟢 **Inflation: ON TARGET**")
            elif inflation_diff < 1.0:
                st.markdown("### 🟡 **Inflation: NEAR TARGET**")
            else:
                st.markdown("### 🔴 **Inflation: OFF TARGET**")
            st.write(f"Deviation: {inflation_diff:.2f}%")
        
        with col_tl3:
            unemployment_diff = abs(unemployment_actual - target_unemployment)
            if unemployment_diff < 0.5:
                st.markdown("### 🟢 **Unemployment: ON TARGET**")
            elif unemployment_diff < 1.0:
                st.markdown("### 🟡 **Unemployment: NEAR TARGET**")
            else:
                st.markdown("### 🔴 **Unemployment: OFF TARGET**")
            st.write(f"Deviation: {unemployment_diff:.2f}%")
        
        st.markdown("---")
        
        # AI Policy Recommendations
        st.markdown(f"#### {txt['policy_recommendations']}")
        
        if inflation_actual > target_inflation + 0.5:
            st.error(f"⚠️ **URGENT**: Inflation {inflation_actual:.2f}% above target {target_inflation:.2f}%")
            st.write(f"**Recommended Action**: Raise interest rate by {0.5 * (inflation_actual - target_inflation):.2f}%")
        
        if growth_actual < target_growth - 1.0:
            st.warning(f"⚠️ **ATTENTION**: Growth {growth_actual:.2f}% below target {target_growth:.2f}%")
            st.write(f"**Recommended Action**: Consider fiscal stimulus of Rp {(target_growth - growth_actual) * 100:.0f}T")
        
        if unemployment_actual > target_unemployment + 0.5:
            st.warning(f"⚠️ **ATTENTION**: Unemployment {unemployment_actual:.2f}% above target {target_unemployment:.2f}%")
            st.write("**Recommended Action**: Implement job creation programs and accommodative monetary policy")
        
        if 'prob_recession' in results and results['prob_recession'] > 10:
            st.error(f"🔴 **HIGH RISK**: Recession probability at {results['prob_recession']:.1f}%")
            st.write("**Recommended Action**: Prepare counter-cyclical policy measures")
        
        # Overall Policy Effectiveness
        st.markdown("---")
        st.markdown("### 📊 Overall Policy Effectiveness")
        
        effectiveness = results['score']
        
        fig_effectiveness = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = effectiveness,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Policy Effectiveness Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "green"}],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 75}
            }
        ))
        fig_effectiveness.update_layout(height=300)
        st.plotly_chart(fig_effectiveness, use_container_width=True)
        
        if effectiveness >= 75:
            st.success("✅ **Excellent**: Policy mix is highly effective")
        elif effectiveness >= 50:
            st.warning("⚠️ **Good**: Policy mix is moderately effective, some adjustments may help")
        else:
            st.error("🔴 **Poor**: Policy mix needs significant revision")
    
    else:
        st.info("Run optimization in Tab 1 first to see the real-time dashboard")

# ========== TAB 6: PROFESSIONAL REPORTS ==========
with tab6:
    st.markdown(f"### {txt['report_title']}")
    
    if 'optimization_results' in st.session_state:
        results = st.session_state['optimization_results']
        
        # Policy Statement
        st.markdown(f"#### {txt['policy_statement']}")
        
        statement = generate_policy_statement(results, lang)
        st.markdown(statement)
        
        st.markdown("---")
        
        # Export Data
        st.markdown(f"#### {txt['export_data']}")
        
        # Prepare data for export
        export_data = {
            'Metric': [
                'Government Spending (G)',
                'Interest Rate (r)',
                'GDP Growth',
                'Inflation',
                'Unemployment',
                'Policy Effectiveness Score'
            ],
            'Current': [
                f"{G:,.0f}",
                f"{r:.2f}%",
                f"{((current_gdp * 1.05 - current_gdp) / current_gdp * 100):.2f}%",
                f"{inflation:.2f}%",
                f"{unemployment:.2f}%",
                "-"
            ],
            'Optimal': [
                f"{results['G_opt']:,.0f}",
                f"{results['r_opt']:.2f}%",
                f"{results.get('growth_pred', 0) if 'mc' not in results else results['mc']['growth']['mean']:.2f}%",
                f"{results.get('inflation_pred', 0) if 'mc' not in results else results['mc']['inflation']['mean']:.2f}%",
                f"{results.get('unemployment_pred', 0) if 'mc' not in results else results['mc']['unemployment']['mean']:.2f}%",
                f"{results['score']:.1f}/100"
            ],
            'Change': [
                f"{results['G_opt'] - G:+,.0f}",
                f"{results['r_opt'] - r:+.2f}%",
                "-",
                "-",
                "-",
                "-"
            ]
        }
        
        df_export = pd.DataFrame(export_data)
        st.dataframe(df_export, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=txt['download_csv'],
            data=csv,
            file_name='policy_analysis_report.csv',
            mime='text/csv',
        )
        
        st.success("✅ Report ready for download")
        
    else:
        st.info("Run optimization in Tab 1 first to generate reports")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Professional AI Macroeconomic Policy Optimizer | Central Bank-Grade Analysis</p>
    <p>🏦 Built for Central Banks, Ministries, and Economic Research Institutions</p>
</div>
""", unsafe_allow_html=True)
