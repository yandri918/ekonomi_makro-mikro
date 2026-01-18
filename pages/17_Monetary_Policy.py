import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Monetary Policy Analyzer", page_icon="💰", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "💰 Advanced Monetary Policy Analyzer",
        'subtitle': "Comprehensive central bank decision support: Taylor Rule, Phillips Curve dynamics, and policy simulation tools.",
        'tab1': "📈 Taylor Rule Calculator",
        'tab2': "📉 Phillips Curve Analysis",
        'tab3': "🎯 Policy Simulation",
        'tab4': "📊 Historical Analysis",
        # Tab 1: Taylor Rule
        'taylor_title': "Taylor Rule: Optimal Interest Rate",
        'taylor_theory': "**Taylor Rule** determines optimal policy rate based on inflation and output gaps.",
        'taylor_formula': "r* = r_neutral + π + α(π - π*) + β(Y - Y*)",
        'current_conditions': "Current Economic Conditions",
        'current_inflation': "Current Inflation (%)",
        'target_inflation': "Target Inflation (%)",
        'output_gap': "Output Gap (%)",
        'output_gap_help': "Positive = Overheating, Negative = Recession",
        'taylor_params': "Taylor Rule Parameters",
        'neutral_rate': "Neutral Real Rate (%)",
        'alpha': "α (Inflation Weight)",
        'beta': "β (Output Weight)",
        'current_rate': "Current Policy Rate (%)",
        'calculate': "Calculate Optimal Rate",
        'results': "Results",
        'recommended_rate': "Recommended Rate",
        'policy_stance': "Policy Stance",
        'tighten': "🔴 TIGHTEN (Raise Rate)",
        'ease': "🟢 EASE (Cut Rate)",
        'maintain': "🟡 MAINTAIN (Hold)",
        'breakdown': "Component Breakdown",
        'neutral_comp': "Neutral Rate",
        'inflation_comp': "Current Inflation",
        'inf_gap_comp': "Inflation Gap × α",
        'out_gap_comp': "Output Gap × β",
        # Tab 2: Phillips Curve
        'phillips_title': "Phillips Curve: Inflation-Unemployment Trade-off",
        'phillips_theory': "**Phillips Curve** shows short-run trade-off between inflation and unemployment.",
        'phillips_formula': "π = π_e - β(u - u_n) + ε",
        'phillips_inputs': "Phillips Curve Parameters",
        'expected_inflation': "Expected Inflation (%)",
        'nairu': "NAIRU (%)",
        'nairu_help': "Natural rate of unemployment (~5-6% for Indonesia)",
        'phillips_slope': "β (Slope)",
        'current_unemployment': "Current Unemployment (%)",
        'supply_shock': "Supply Shock (ε)",
        'shock_help': "Oil price shock, pandemic, etc.",
        'phillips_results': "Phillips Curve Results",
        'predicted_inflation': "Predicted Inflation",
        'unemployment_gap': "Unemployment Gap",
        'sacrifice_ratio': "Sacrifice Ratio",
        'sacrifice_help': "% GDP loss per 1% inflation reduction",
        # Tab 3: Policy Simulation
        'simulation_title': "Policy Simulation & Scenario Analysis",
        'scenario_setup': "Scenario Setup",
        'rate_change': "Interest Rate Change (%)",
        'simulation_periods': "Simulation Periods (quarters)",
        'transmission_lag': "Transmission Lag (quarters)",
        'lag_help': "Time for policy to affect economy",
        'run_simulation': "Run Simulation",
        'simulation_results': "Simulation Results",
        'inflation_path': "Inflation Path",
        'output_path': "Output Gap Path",
        'unemployment_path': "Unemployment Path",
        'policy_effectiveness': "Policy Effectiveness Score",
        # Tab 4: Historical Analysis
        'historical_title': "Historical Policy Analysis",
        'add_period': "Add Historical Period",
        'period_name': "Period Name",
        'period_inflation': "Inflation (%)",
        'period_unemployment': "Unemployment (%)",
        'period_rate': "Policy Rate (%)",
        'add_data': "Add to History",
        'clear_history': "Clear History",
        'historical_chart': "Historical Trends",
        'taylor_deviation': "Taylor Rule Deviation",
        'deviation_help': "How much actual rate deviated from Taylor recommendation",
        # Insights
        'insights': "Key Insights",
        'recommendation': "Policy Recommendation",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nComprehensive monetary policy analysis tool for central bank decision-making and policy evaluation.",
        'story_insight': "**Key Insight:**\nCombining Taylor Rule with Phillips Curve provides complete framework for understanding monetary policy trade-offs.",
        'story_users': "**Who needs this?**",
        'use_central_bank': "🏦 **Central Banks:** Systematic framework for rate decisions.",
        'use_analyst': "📊 **Analysts:** Predict and evaluate monetary policy.",
        'use_researcher': "🎓 **Researchers:** Study policy effectiveness and transmission."
    },
    'ID': {
        'title': "💰 Analisis Kebijakan Moneter Lanjutan",
        'subtitle': "Dukungan keputusan bank sentral komprehensif: Taylor Rule, dinamika Kurva Phillips, dan simulasi kebijakan.",
        'tab1': "📈 Kalkulator Taylor Rule",
        'tab2': "📉 Analisis Kurva Phillips",
        'tab3': "🎯 Simulasi Kebijakan",
        'tab4': "📊 Analisis Historis",
        # Tab 1: Taylor Rule
        'taylor_title': "Taylor Rule: Suku Bunga Optimal",
        'taylor_theory': "**Taylor Rule** menentukan suku bunga kebijakan optimal berdasarkan gap inflasi dan output.",
        'taylor_formula': "r* = r_netral + π + α(π - π*) + β(Y - Y*)",
        'current_conditions': "Kondisi Ekonomi Saat Ini",
        'current_inflation': "Inflasi Saat Ini (%)",
        'target_inflation': "Target Inflasi (%)",
        'output_gap': "Gap Output (%)",
        'output_gap_help': "Positif = Overheating, Negatif = Resesi",
        'taylor_params': "Parameter Taylor Rule",
        'neutral_rate': "Suku Bunga Riil Netral (%)",
        'alpha': "α (Bobot Inflasi)",
        'beta': "β (Bobot Output)",
        'current_rate': "Suku Bunga Kebijakan Saat Ini (%)",
        'calculate': "Hitung Suku Bunga Optimal",
        'results': "Hasil",
        'recommended_rate': "Suku Bunga Rekomendasi",
        'policy_stance': "Sikap Kebijakan",
        'tighten': "🔴 KETAT (Naikkan)",
        'ease': "🟢 LONGGAR (Turunkan)",
        'maintain': "🟡 PERTAHANKAN",
        'breakdown': "Rincian Komponen",
        'neutral_comp': "Suku Bunga Netral",
        'inflation_comp': "Inflasi Saat Ini",
        'inf_gap_comp': "Gap Inflasi × α",
        'out_gap_comp': "Gap Output × β",
        # Tab 2: Phillips Curve
        'phillips_title': "Kurva Phillips: Trade-off Inflasi-Pengangguran",
        'phillips_theory': "**Kurva Phillips** menunjukkan trade-off jangka pendek antara inflasi dan pengangguran.",
        'phillips_formula': "π = π_e - β(u - u_n) + ε",
        'phillips_inputs': "Parameter Kurva Phillips",
        'expected_inflation': "Inflasi yang Diharapkan (%)",
        'nairu': "NAIRU (%)",
        'nairu_help': "Tingkat pengangguran alamiah (~5-6% untuk Indonesia)",
        'phillips_slope': "β (Kemiringan)",
        'current_unemployment': "Pengangguran Saat Ini (%)",
        'supply_shock': "Guncangan Penawaran (ε)",
        'shock_help': "Guncangan harga minyak, pandemi, dll.",
        'phillips_results': "Hasil Kurva Phillips",
        'predicted_inflation': "Inflasi Terprediksi",
        'unemployment_gap': "Gap Pengangguran",
        'sacrifice_ratio': "Rasio Pengorbanan",
        'sacrifice_help': "% kehilangan PDB per 1% penurunan inflasi",
        # Tab 3: Policy Simulation
        'simulation_title': "Simulasi Kebijakan & Analisis Skenario",
        'scenario_setup': "Pengaturan Skenario",
        'rate_change': "Perubahan Suku Bunga (%)",
        'simulation_periods': "Periode Simulasi (kuartal)",
        'transmission_lag': "Lag Transmisi (kuartal)",
        'lag_help': "Waktu kebijakan mempengaruhi ekonomi",
        'run_simulation': "Jalankan Simulasi",
        'simulation_results': "Hasil Simulasi",
        'inflation_path': "Jalur Inflasi",
        'output_path': "Jalur Gap Output",
        'unemployment_path': "Jalur Pengangguran",
        'policy_effectiveness': "Skor Efektivitas Kebijakan",
        # Tab 4: Historical Analysis
        'historical_title': "Analisis Kebijakan Historis",
        'add_period': "Tambah Periode Historis",
        'period_name': "Nama Periode",
        'period_inflation': "Inflasi (%)",
        'period_unemployment': "Pengangguran (%)",
        'period_rate': "Suku Bunga Kebijakan (%)",
        'add_data': "Tambah ke Riwayat",
        'clear_history': "Hapus Riwayat",
        'historical_chart': "Tren Historis",
        'taylor_deviation': "Deviasi Taylor Rule",
        'deviation_help': "Seberapa jauh suku bunga aktual dari rekomendasi Taylor",
        # Insights
        'insights': "Wawasan Utama",
        'recommendation': "Rekomendasi Kebijakan",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nAlat analisis kebijakan moneter komprehensif untuk pengambilan keputusan dan evaluasi kebijakan bank sentral.",
        'story_insight': "**Wawasan Utama:**\nMenggabungkan Taylor Rule dengan Kurva Phillips memberikan kerangka lengkap untuk memahami trade-off kebijakan moneter.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_central_bank': "🏦 **Bank Sentral:** Kerangka sistematis untuk keputusan suku bunga.",
        'use_analyst': "📊 **Analis:** Prediksi dan evaluasi kebijakan moneter.",
        'use_researcher': "🎓 **Peneliti:** Studi efektivitas kebijakan dan transmisi."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Initialize session state
if 'history' not in st.session_state:
    st.session_state['history'] = []

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ========== TAB 1: TAYLOR RULE ==========
with tab1:
    st.markdown(f"### {txt['taylor_title']}")
    st.info(txt['taylor_theory'])
    st.latex(txt['taylor_formula'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['current_conditions']}")
        current_inflation = st.number_input(txt['current_inflation'], value=3.5, step=0.1)
        target_inflation = st.number_input(txt['target_inflation'], value=2.0, step=0.1)
        output_gap = st.number_input(txt['output_gap'], value=1.0, step=0.5, help=txt['output_gap_help'])
        
        st.markdown(f"#### {txt['taylor_params']}")
        neutral_rate = st.number_input(txt['neutral_rate'], value=2.0, step=0.1)
        alpha = st.slider(txt['alpha'], 0.0, 2.0, 0.5, 0.1)
        beta = st.slider(txt['beta'], 0.0, 2.0, 0.5, 0.1)
        
        current_rate = st.number_input(txt['current_rate'], value=5.75, step=0.25)
        
        if st.button(txt['calculate'], type='primary', key='taylor_calc'):
            # Taylor Rule Calculation
            inflation_gap = current_inflation - target_inflation
            
            # Components
            comp_neutral = neutral_rate
            comp_inflation = current_inflation
            comp_inf_gap = alpha * inflation_gap
            comp_out_gap = beta * output_gap
            
            recommended_rate = comp_neutral + comp_inflation + comp_inf_gap + comp_out_gap
            
            st.session_state['taylor_results'] = {
                'recommended': recommended_rate,
                'current': current_rate,
                'neutral': comp_neutral,
                'inflation': comp_inflation,
                'inf_gap': comp_inf_gap,
                'out_gap': comp_out_gap,
                'inflation_gap': inflation_gap,
                'output_gap': output_gap
            }
    
    with col2:
        if 'taylor_results' in st.session_state:
            results = st.session_state['taylor_results']
            
            st.markdown(f"### {txt['results']}")
            
            gap = results['recommended'] - results['current']
            
            m1, m2, m3 = st.columns(3)
            m1.metric(txt['recommended_rate'], f"{results['recommended']:.2f}%")
            m2.metric(txt['current_rate'], f"{results['current']:.2f}%")
            
            if gap > 0.25:
                stance = txt['tighten']
                color = "🔴"
            elif gap < -0.25:
                stance = txt['ease']
                color = "🟢"
            else:
                stance = txt['maintain']
                color = "🟡"
            
            m3.metric(txt['policy_stance'], f"{color} {gap:+.2f}%")
            
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=results['recommended'],
                delta={'reference': results['current']},
                title={'text': txt['recommended_rate']},
                gauge={
                    'axis': {'range': [0, 12]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 4], 'color': "lightgreen"},
                        {'range': [4, 7], 'color': "lightyellow"},
                        {'range': [7, 12], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': results['current']
                    }
                }
            ))
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            # Component breakdown
            st.markdown(f"### {txt['breakdown']}")
            
            components = {
                txt['neutral_comp']: results['neutral'],
                txt['inflation_comp']: results['inflation'],
                txt['inf_gap_comp']: results['inf_gap'],
                txt['out_gap_comp']: results['out_gap']
            }
            
            fig_waterfall = go.Figure(go.Waterfall(
                name="Components",
                orientation="v",
                measure=["absolute", "relative", "relative", "relative", "total"],
                x=list(components.keys()) + [txt['recommended_rate']],
                y=list(components.values()) + [results['recommended']],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            
            fig_waterfall.update_layout(title="Taylor Rule Component Breakdown", height=400)
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
            # Recommendation
            st.markdown(f"### {txt['recommendation']}")
            if gap > 0.25:
                st.error(f"🔴 **{txt['tighten']}**: Recommended rate ({results['recommended']:.2f}%) is {gap:.2f}% above current rate. Consider raising rates to combat inflation.")
            elif gap < -0.25:
                st.success(f"🟢 **{txt['ease']}**: Recommended rate ({results['recommended']:.2f}%) is {abs(gap):.2f}% below current rate. Consider cutting rates to stimulate economy.")
            else:
                st.info(f"🟡 **{txt['maintain']}**: Current rate is appropriate. Maintain current policy stance.")

# ========== TAB 2: PHILLIPS CURVE ==========
with tab2:
    st.markdown(f"### {txt['phillips_title']}")
    st.info(txt['phillips_theory'])
    st.latex(txt['phillips_formula'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['phillips_inputs']}")
        expected_inflation = st.number_input(txt['expected_inflation'], value=3.0, step=0.1)
        nairu = st.number_input(txt['nairu'], value=5.5, step=0.1, help=txt['nairu_help'])
        phillips_slope = st.number_input(txt['phillips_slope'], value=0.5, step=0.1)
        current_unemployment = st.number_input(txt['current_unemployment'], value=5.0, step=0.1)
        supply_shock = st.number_input(txt['supply_shock'], value=0.0, step=0.1, help=txt['shock_help'])
        
        if st.button(txt['calculate'], type='primary', key='phillips_calc'):
            unemployment_gap = current_unemployment - nairu
            predicted_inflation = expected_inflation - phillips_slope * unemployment_gap + supply_shock
            
            # Sacrifice ratio: % output loss per 1% inflation reduction
            sacrifice_ratio = 1 / phillips_slope if phillips_slope != 0 else 0
            
            st.session_state['phillips_results'] = {
                'predicted_inflation': predicted_inflation,
                'unemployment_gap': unemployment_gap,
                'sacrifice_ratio': sacrifice_ratio,
                'expected_inflation': expected_inflation,
                'nairu': nairu,
                'slope': phillips_slope,
                'current_u': current_unemployment
            }
    
    with col2:
        if 'phillips_results' in st.session_state:
            results = st.session_state['phillips_results']
            
            st.markdown(f"### {txt['phillips_results']}")
            
            p1, p2, p3 = st.columns(3)
            p1.metric(txt['predicted_inflation'], f"{results['predicted_inflation']:.2f}%")
            p2.metric(txt['unemployment_gap'], f"{results['unemployment_gap']:+.2f}%")
            p3.metric(txt['sacrifice_ratio'], f"{results['sacrifice_ratio']:.2f}", help=txt['sacrifice_help'])
            
            # Phillips Curve visualization
            u_range = np.linspace(2, 10, 100)
            pi_short_run = results['expected_inflation'] - results['slope'] * (u_range - results['nairu'])
            
            fig = make_subplots(rows=1, cols=2,
                               subplot_titles=("Phillips Curve", "Policy Trade-off Space"))
            
            # Short-run Phillips Curve
            fig.add_trace(go.Scatter(
                x=u_range, y=pi_short_run,
                mode='lines', name='Short-Run PC',
                line=dict(color='blue', width=3)
            ), row=1, col=1)
            
            # Long-run (vertical at NAIRU)
            fig.add_trace(go.Scatter(
                x=[results['nairu'], results['nairu']], y=[-2, 10],
                mode='lines', name='Long-Run PC',
                line=dict(color='gray', dash='dash', width=2)
            ), row=1, col=1)
            
            # Current point
            fig.add_trace(go.Scatter(
                x=[results['current_u']], y=[results['predicted_inflation']],
                mode='markers', name='Current',
                marker=dict(size=15, color='red', symbol='star')
            ), row=1, col=1)
            
            # Trade-off space (different expected inflations)
            for exp_inf in [2, 3, 4, 5]:
                pi_curve = exp_inf - results['slope'] * (u_range - results['nairu'])
                fig.add_trace(go.Scatter(
                    x=u_range, y=pi_curve,
                    mode='lines', name=f'πₑ={exp_inf}%',
                    line=dict(width=2)
                ), row=1, col=2)
            
            fig.update_xaxes(title_text="Unemployment (%)", row=1, col=1)
            fig.update_yaxes(title_text="Inflation (%)", row=1, col=1)
            fig.update_xaxes(title_text="Unemployment (%)", row=1, col=2)
            fig.update_yaxes(title_text="Inflation (%)", row=1, col=2)
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            st.markdown(f"### {txt['insights']}")
            if results['unemployment_gap'] < 0:
                st.warning(f"⚠️ Unemployment ({results['current_u']:.1f}%) is below NAIRU ({results['nairu']:.1f}%). Inflationary pressure expected.")
            elif results['unemployment_gap'] > 0:
                st.info(f"ℹ️ Unemployment ({results['current_u']:.1f}%) is above NAIRU ({results['nairu']:.1f}%). Disinflationary pressure expected.")
            else:
                st.success(f"✅ Unemployment is at NAIRU. Inflation should remain stable.")

# ========== TAB 3: POLICY SIMULATION ==========
with tab3:
    st.markdown(f"### {txt['simulation_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['scenario_setup']}")
        
        rate_change = st.slider(txt['rate_change'], -3.0, 3.0, 0.5, 0.25)
        periods = st.slider(txt['simulation_periods'], 4, 20, 12)
        lag = st.slider(txt['transmission_lag'], 1, 6, 2, help=txt['lag_help'])
        
        if st.button(txt['run_simulation'], type='primary'):
            # Simplified monetary transmission mechanism
            # Rate change affects output gap, which affects inflation and unemployment
            
            time = np.arange(periods)
            
            # Output gap response (with lag)
            output_response = np.zeros(periods)
            for t in range(periods):
                if t >= lag:
                    output_response[t] = -0.5 * rate_change * (1 - np.exp(-(t-lag)/3))
            
            # Inflation response (follows output gap)
            inflation_response = np.zeros(periods)
            base_inflation = 3.0
            for t in range(periods):
                if t > 0:
                    inflation_response[t] = base_inflation + 0.3 * output_response[t] + 0.5 * inflation_response[t-1]
                else:
                    inflation_response[t] = base_inflation
            
            # Unemployment response (Okun's Law)
            unemployment_response = np.zeros(periods)
            base_unemployment = 5.5
            for t in range(periods):
                unemployment_response[t] = base_unemployment - 0.5 * output_response[t]
            
            st.session_state['simulation'] = {
                'time': time,
                'output': output_response,
                'inflation': inflation_response,
                'unemployment': unemployment_response,
                'rate_change': rate_change
            }
    
    with col2:
        if 'simulation' in st.session_state:
            sim = st.session_state['simulation']
            
            st.markdown(f"### {txt['simulation_results']}")
            
            # Create subplots
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=(txt['inflation_path'], txt['output_path'], txt['unemployment_path'])
            )
            
            fig.add_trace(go.Scatter(x=sim['time'], y=sim['inflation'], mode='lines+markers',
                                    name='Inflation', line=dict(color='red', width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(x=sim['time'], y=sim['output'], mode='lines+markers',
                                    name='Output Gap', line=dict(color='blue', width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=sim['time'], y=sim['unemployment'], mode='lines+markers',
                                    name='Unemployment', line=dict(color='green', width=2)), row=3, col=1)
            
            fig.update_xaxes(title_text="Quarters", row=3, col=1)
            fig.update_yaxes(title_text="Inflation (%)", row=1, col=1)
            fig.update_yaxes(title_text="Output Gap (%)", row=2, col=1)
            fig.update_yaxes(title_text="Unemployment (%)", row=3, col=1)
            fig.update_layout(height=800, showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Effectiveness score
            final_inflation = sim['inflation'][-1]
            inflation_change = final_inflation - sim['inflation'][0]
            effectiveness = 100 * (1 - abs(inflation_change) / 5)  # Normalize to 0-100
            
            st.metric(txt['policy_effectiveness'], f"{max(0, effectiveness):.1f}/100")
            
            if sim['rate_change'] > 0:
                st.info(f"📈 Rate increase of {sim['rate_change']:.2f}% → Inflation decreases to {final_inflation:.2f}% over {len(sim['time'])} quarters")
            else:
                st.info(f"📉 Rate cut of {abs(sim['rate_change']):.2f}% → Inflation increases to {final_inflation:.2f}% over {len(sim['time'])} quarters")

# ========== TAB 4: HISTORICAL ANALYSIS ==========
with tab4:
    st.markdown(f"### {txt['historical_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['add_period']}")
        
        period_name = st.text_input(txt['period_name'], value="Q1 2024")
        period_inflation = st.number_input(txt['period_inflation'], value=3.5, step=0.1, key='hist_inf')
        period_unemployment = st.number_input(txt['period_unemployment'], value=5.5, step=0.1, key='hist_u')
        period_rate = st.number_input(txt['period_rate'], value=5.75, step=0.25, key='hist_rate')
        
        if st.button(txt['add_data']):
            st.session_state['history'].append({
                'Period': period_name,
                'Inflation': period_inflation,
                'Unemployment': period_unemployment,
                'Rate': period_rate
            })
            st.success(f"Added {period_name}!")
        
        if st.button(txt['clear_history']):
            st.session_state['history'] = []
            st.rerun()
    
    with col2:
        if len(st.session_state['history']) > 0:
            df_history = pd.DataFrame(st.session_state['history'])
            
            st.dataframe(df_history, use_container_width=True, hide_index=True)
            
            # Historical charts
            fig = make_subplots(rows=2, cols=1,
                               subplot_titles=("Policy Rate & Inflation", "Unemployment Trend"))
            
            fig.add_trace(go.Scatter(x=df_history['Period'], y=df_history['Rate'],
                                    mode='lines+markers', name='Policy Rate',
                                    line=dict(color='blue', width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(x=df_history['Period'], y=df_history['Inflation'],
                                    mode='lines+markers', name='Inflation',
                                    line=dict(color='red', width=2)), row=1, col=1)
            fig.add_trace(go.Scatter(x=df_history['Period'], y=df_history['Unemployment'],
                                    mode='lines+markers', name='Unemployment',
                                    line=dict(color='green', width=2)), row=2, col=1)
            
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add historical periods to see trends")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_central_bank'])
        st.write(txt['use_analyst'])
        st.write(txt['use_researcher'])
