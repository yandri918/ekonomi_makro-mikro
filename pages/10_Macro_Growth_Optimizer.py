import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from scipy.optimize import minimize

st.set_page_config(page_title="AI Policy Optimizer", page_icon="🎯", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🎯 AI Macro Policy Optimizer",
        'subtitle': "Use AI to find the optimal **Fiscal & Monetary Policy** mix to achieve your Target GDP Growth.",
        'inputs': "📊 Economic Baseline",
        'C': "Consumption (C)",
        'I': "Investment (I)",
        'G': "Govt Spending (G)",
        'NX': "Net Exports (X-M)",
        'r': "Current Interest Rate (%)",
        'target_sec': "🎯 Growth Target",
        'target_growth': "Target GDP Growth (%)",
        'constraints': "⚙️ Optimization Constraints & Preferences",
        'max_g': "Max Allowed Increase in G (%)",
        'min_r': "Min Allowed Interest Rate (%)",
        'preference': "Policy Preference",
        'balanced': "Balanced Approach",
        'fiscal': "Prioritize Fiscal (G)",
        'monetary': "Prioritize Monetary (r)",
        'optimize_btn': "🚀 Run AI Optimizer",
        'results': "📋 Optimization Results",
        'rec_policy': "Recommended Policy Mix",
        'new_g': "New Govt Spending:",
        'new_r': "New Interest Rate:",
        'required_stimulus': "Required Stimulus",
        'analysis': "Impact Analysis",
        'waterfall_title': "Path to Target GDP",
        'explanation': "**AI Logic:** The optimizer minimized structural changes while prioritizing your preference for **{}**.",
        'param_sens': "Investment Sensitivity to Interest Rate (Linear)",
        'mpc_label': "Marginal Propensity to Consume (MPC)"
    },
    'ID': {
        'title': "🎯 AI Pengoptimal Kebijakan Makro",
        'subtitle': "Gunakan AI untuk mencari kombinasi **Kebijakan Fiskal & Moneter** optimal demi mencapai Target Pertumbuhan PDB.",
        'inputs': "📊 Baseline Ekonomi (Triliun Rp)",
        'C': "Konsumsi (C)",
        'I': "Investasi (I)",
        'G': "Belanja Pemerintah (G)",
        'NX': "Ekspor Neto (X-M)",
        'r': "Suku Bunga Saat Ini (%)",
        'target_sec': "🎯 Target Pertumbuhan",
        'target_growth': "Target Pertumbuhan PDB (%)",
        'constraints': "⚙️ Batasan & Preferensi Optimasi",
        'max_g': "Maks. Kenaikan G yang Diizinkan (%)",
        'min_r': "Batas Bawah Suku Bunga (%)",
        'preference': "Preferensi Kebijakan",
        'balanced': "Pendekatan Seimbang",
        'fiscal': "Prioritas Fiskal (G)",
        'monetary': "Prioritas Moneter (r)",
        'optimize_btn': "🚀 Jalankan AI Optimizer",
        'results': "📋 Hasil Optimasi",
        'rec_policy': "Rekomendasi Bauran Kebijakan",
        'new_g': "Belanja Pemerintah Baru:",
        'new_r': "Suku Bunga Baru:",
        'required_stimulus': "Stimulus yang Dibutuhkan",
        'analysis': "Analisis Dampak",
        'waterfall_title': "Jalur Menuju Target PDB",
        'explanation': "**Logika AI:** Optimizer meminimalkan perubahan struktural drastis sambil memprioritaskan preferensi Anda untuk **{}**.",
        'param_sens': "Sensitivitas Investasi thd Suku Bunga",
        'mpc_label': "Marginal Propensity to Consume (MPC)"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- SIDEBAR / EXPANDER FOR ADVANCED PARAMS ---
with st.sidebar:
    st.header("Model Parameters")
    MPC = st.slider(txt['mpc_label'], 0.1, 0.9, 0.75)
    # Sensitivity: How much Investment (Trillion Rp) increases for 1% drop in r
    alpha_I = st.number_input(txt['param_sens'], value=200.0, step=10.0, help="Delta I / Delta r")

# --- MAIN INPUTS ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader(txt['inputs'])
    # Default values roughly approximating Indonesia logic or textbook examples
    C0 = st.number_input(txt['C'], value=11000.0)
    I0 = st.number_input(txt['I'], value=6000.0)
    G0 = st.number_input(txt['G'], value=3000.0)
    NX0 = st.number_input(txt['NX'], value=500.0)
    
    current_GDP = C0 + I0 + G0 + NX0
    st.metric("Current GDP / PDB Saat Ini", f"Rp {current_GDP:,.0f} T")
    
    st.markdown("---")
    st.subheader(txt['target_sec'])
    r0 = st.number_input(txt['r'], value=5.00, step=0.25)
    target_pct = st.number_input(txt['target_growth'], value=5.5, step=0.1)

with col2:
    st.subheader(txt['constraints'])
    
    preference = st.radio(txt['preference'], [txt['balanced'], txt['fiscal'], txt['monetary']])
    
    c1, c2 = st.columns(2)
    max_g_pct = c1.number_input(txt['max_g'], value=20.0, step=5.0)
    min_r_val = c2.number_input(txt['min_r'], value=2.0, step=0.25)
    
    st.markdown("---")
    
    target_GDP = current_GDP * (1 + target_pct/100)
    required_gap = target_GDP - current_GDP
    
    st.info(f"""
    **Target GDP:** Rp {target_GDP:,.0f} T 
    \n**Required Gap:** Rp {required_gap:,.0f} T
    """)

    if st.button(txt['optimize_btn'], type="primary"):
        # --- OPTIMIZATION LOGIC ---
        
        # Variables to optimize: x = [G_new, r_new]
        # We need to hit Target GDP.
        # GDP = C + I + G + NX
        # Assume C depends on Y (Multiplier effect captured somewhat or simplified)
        # Let's use simple multiplier logic:
        # Delta Y = (Delta G + Delta I) * Multiplier
        # Multiplier = 1 / (1 - MPC)
        # Delta I = alpha_I * (r0 - r_new)
        # Delta G = G_new - G0
        
        # Objective Function: Minimize specific "Pain" or "Deviation" based on preference
        def objective(x):
            G_new, r_new = x
            delta_G = G_new - G0
            delta_r = r0 - r_new # positive if rate cut
            
            # Costs (Squared deviations)
            cost_G = (delta_G / G0) ** 2
            cost_r = (delta_r / r0) ** 2 if r0 > 0 else 0
            
            # Apply Weights based on Preference
            w_fiscal = 1.0
            w_monetary = 1.0
            
            if preference == txt['fiscal']:
                w_fiscal = 0.1 # Cheaper to use Fiscal
                w_monetary = 10.0 # Expensive to use Monetary
            elif preference == txt['monetary']:
                w_fiscal = 10.0
                w_monetary = 0.1
            
            return w_fiscal * cost_G + w_monetary * cost_r

        # Constraint: GDP matches Target
        def constraint_eq(x):
            G_new, r_new = x
            delta_G = G_new - G0
            delta_r = r0 - r_new # Interest rate cut increases I
            delta_I = alpha_I * delta_r
            
            multiplier = 1 / (1 - MPC)
            total_stimulus = delta_G + delta_I
            
            projected_growth_val = total_stimulus * multiplier
            projected_GDP = current_GDP + projected_growth_val
            
            return projected_GDP - target_GDP

        # Bounds
        # G_new must be betwen G0 and G0 * (1 + max_g_pct/100)
        # r_new must be between min_r_val and 20%
        b_G = (G0, G0 * (1 + max_g_pct/100))
        b_r = (min_r_val, 20.0)
        
        # Initial Guess
        x0 = [G0 * 1.05, r0 - 0.5]
        
        # Run Optimization
        sol = minimize(objective, x0, method='SLSQP', bounds=[b_G, b_r], constraints={'type': 'eq', 'fun': constraint_eq})
        
        if sol.success:
            opt_G, opt_r = sol.x
            
            # Calculate Implications
            delta_G = opt_G - G0
            delta_r = r0 - opt_r
            delta_I = alpha_I * delta_r
            multiplier = 1 / (1 - MPC)
            
            stimulus_G = delta_G * multiplier
            stimulus_I = delta_I * multiplier
            
            total_increase = stimulus_G + stimulus_I
            final_GDP = current_GDP + total_increase
            
            # --- RESULTS VISUALIZATION ---
            st.success("✅ Optimization Successful! Solution Found.")
            
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.markdown(f"#### {txt['rec_policy']}")
                st.metric(txt['new_g'], f"Rp {opt_G:,.0f} T", delta=f"{delta_G:+,.0f} T ({((opt_G-G0)/G0)*100:+.1f}%)")
                st.metric(txt['new_r'], f"{opt_r:.2f}%", delta=f"{-delta_r:+.2f}%", delta_color="inverse")
            
            with res_col2:
                st.markdown(f"#### {txt['analysis']}")
                st.write(txt['explanation'].format(preference))
                
                # Waterfall Chart Data
                df_waterfall = pd.DataFrame({
                    'Category': ['Current GDP', 'Effect of G', 'Effect of r (via I)', 'Target GDP'],
                    'Value': [current_GDP, stimulus_G, stimulus_I, final_GDP],
                    'Delta': [current_GDP, stimulus_G, stimulus_I, 0] # For waterfall logic
                })
                
                # Simple Bar Chart for composition
                chart_data = pd.DataFrame([
                    {'Label': 'Baseline', 'Value': current_GDP, 'Type': 'Base'},
                    {'Label': 'Stimulus (G)', 'Value': stimulus_G, 'Type': 'Fiscal'},
                    {'Label': 'Stimulus (r)', 'Value': stimulus_I, 'Type': 'Monetary'},
                ])
                
                base_chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('Label', sort=None),
                    y=alt.Y('Value', title='Contribution (Rp T)'),
                    color='Type',
                    tooltip=['Label', 'Value']
                ).properties(title=txt['waterfall_title'])
                
                st.altair_chart(base_chart, use_container_width=True)
                
            st.warning(f"Note: Multiplier used = {multiplier:.2f} (1 / (1 - {MPC})). Assumes excess capacity.")
            
        else:
            st.error("❌ Optimization Failed. The target might be too high for the given constraints.")
            st.write(sol.message)
