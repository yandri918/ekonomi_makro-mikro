import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from numpy_financial import npv, irr

st.set_page_config(page_title="Infrastructure Project Evaluator", page_icon="🏗️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🏗️ Advanced Infrastructure Project Evaluator",
        'subtitle': "Comprehensive cost-benefit analysis: NPV, IRR, BCR, economic value assessment, and sensitivity analysis for infrastructure projects.",
        'tab1': "💰 Financial Analysis",
        'tab2': "🌍 Economic Value",
        'tab3': "📊 Sensitivity Analysis",
        'tab4': "📈 Scenario Comparison",
        # Tab 1
        'financial_title': "Financial Feasibility Analysis",
        'project_setup': "Project Setup",
        'project_name': "Project Name",
        'initial_investment': "Initial Investment (Rp Billion)",
        'project_lifetime': "Project Lifetime (years)",
        'discount_rate': "Discount Rate (%)",
        'discount_help': "WACC or government bond rate",
        'cash_flows': "Annual Cash Flows (Rp Billion)",
        'year': "Year",
        'cash_flow': "Cash Flow",
        'calculate': "Calculate Metrics",
        'financial_metrics': "Financial Metrics",
        'npv': "Net Present Value (NPV)",
        'irr': "Internal Rate of Return (IRR)",
        'payback': "Payback Period",
        'pi': "Profitability Index (PI)",
        'bcr': "Benefit-Cost Ratio (BCR)",
        'decision': "Investment Decision",
        'accept': "✅ ACCEPT",
        'reject': "❌ REJECT",
        'marginal': "⚠️ MARGINAL",
        'cash_flow_chart': "Cash Flow Timeline",
        'cumulative': "Cumulative",
        'annual': "Annual",
        # Tab 2
        'economic_title': "Economic Value Assessment",
        'economic_benefits': "Economic Benefits (Externalities)",
        'time_savings': "Time Savings Value (Rp Billion/year)",
        'time_help': "Value of reduced travel time",
        'accident_reduction': "Accident Reduction Value (Rp Billion/year)",
        'accident_help': "Value of lives saved and injuries prevented",
        'environmental': "Environmental Benefits (Rp Billion/year)",
        'env_help': "Reduced emissions, pollution",
        'employment': "Employment Creation (person-years)",
        'emp_help': "Direct and indirect jobs created",
        'multiplier': "Economic Multiplier",
        'mult_help': "Indirect economic impact (typically 1.5-2.5)",
        'economic_metrics': "Economic Impact Metrics",
        'enpv': "Economic NPV (ENPV)",
        'ebcr': "Economic BCR (EBCR)",
        'social_roi': "Social Return on Investment",
        'jobs_created': "Total Jobs Created",
        'economic_value': "Total Economic Value",
        # Tab 3
        'sensitivity_title': "Sensitivity & Risk Analysis",
        'sensitivity_params': "Sensitivity Parameters",
        'discount_range': "Discount Rate Range (%)",
        'cf_variation': "Cash Flow Variation (%)",
        'cf_help': "Test optimistic/pessimistic scenarios",
        'run_sensitivity': "Run Sensitivity Analysis",
        'sensitivity_results': "Sensitivity Results",
        'breakeven_rate': "Break-Even Discount Rate",
        'risk_level': "Risk Level",
        'low_risk': "🟢 LOW RISK",
        'medium_risk': "🟡 MEDIUM RISK",
        'high_risk': "🔴 HIGH RISK",
        'tornado_chart': "Tornado Diagram (Impact on NPV)",
        # Tab 4
        'scenario_title': "Scenario Comparison",
        'add_scenario': "Add Scenario",
        'scenario_name': "Scenario Name",
        'scenario_investment': "Investment",
        'scenario_annual_cf': "Annual Cash Flow",
        'add_btn': "Add to Comparison",
        'comparison_table': "Scenario Comparison Table",
        'best_scenario': "Best Scenario",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nComprehensive infrastructure project evaluation tool combining financial analysis with economic value assessment.",
        'story_insight': "**Key Insight:**\nInfrastructure projects create value beyond financial returns - time savings, safety, environmental benefits, and economic multipliers.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Government:** Evaluate public infrastructure investments.",
        'use_developer': "🏢 **Developers:** Assess PPP project viability.",
        'use_analyst': "📊 **Analysts:** Compare infrastructure alternatives."
    },
    'ID': {
        'title': "🏗️ Evaluator Proyek Infrastruktur Lanjutan",
        'subtitle': "Analisis biaya-manfaat komprehensif: NPV, IRR, BCR, penilaian nilai ekonomi, dan analisis sensitivitas untuk proyek infrastruktur.",
        'tab1': "💰 Analisis Keuangan",
        'tab2': "🌍 Nilai Ekonomi",
        'tab3': "📊 Analisis Sensitivitas",
        'tab4': "📈 Perbandingan Skenario",
        # Tab 1
        'financial_title': "Analisis Kelayakan Keuangan",
        'project_setup': "Pengaturan Proyek",
        'project_name': "Nama Proyek",
        'initial_investment': "Investasi Awal (Rp Miliar)",
        'project_lifetime': "Umur Proyek (tahun)",
        'discount_rate': "Tingkat Diskonto (%)",
        'discount_help': "WACC atau suku bunga obligasi pemerintah",
        'cash_flows': "Arus Kas Tahunan (Rp Miliar)",
        'year': "Tahun",
        'cash_flow': "Arus Kas",
        'calculate': "Hitung Metrik",
        'financial_metrics': "Metrik Keuangan",
        'npv': "Net Present Value (NPV)",
        'irr': "Internal Rate of Return (IRR)",
        'payback': "Periode Pengembalian",
        'pi': "Indeks Profitabilitas (PI)",
        'bcr': "Rasio Manfaat-Biaya (BCR)",
        'decision': "Keputusan Investasi",
        'accept': "✅ TERIMA",
        'reject': "❌ TOLAK",
        'marginal': "⚠️ MARGINAL",
        'cash_flow_chart': "Timeline Arus Kas",
        'cumulative': "Kumulatif",
        'annual': "Tahunan",
        # Tab 2
        'economic_title': "Penilaian Nilai Ekonomi",
        'economic_benefits': "Manfaat Ekonomi (Eksternalitas)",
        'time_savings': "Nilai Penghematan Waktu (Rp Miliar/tahun)",
        'time_help': "Nilai dari pengurangan waktu perjalanan",
        'accident_reduction': "Nilai Pengurangan Kecelakaan (Rp Miliar/tahun)",
        'accident_help': "Nilai nyawa yang diselamatkan dan cedera yang dicegah",
        'environmental': "Manfaat Lingkungan (Rp Miliar/tahun)",
        'env_help': "Pengurangan emisi, polusi",
        'employment': "Penciptaan Lapangan Kerja (orang-tahun)",
        'emp_help': "Pekerjaan langsung dan tidak langsung yang tercipta",
        'multiplier': "Multiplier Ekonomi",
        'mult_help': "Dampak ekonomi tidak langsung (biasanya 1.5-2.5)",
        'economic_metrics': "Metrik Dampak Ekonomi",
        'enpv': "NPV Ekonomi (ENPV)",
        'ebcr': "BCR Ekonomi (EBCR)",
        'social_roi': "Return on Investment Sosial",
        'jobs_created': "Total Lapangan Kerja Tercipta",
        'economic_value': "Total Nilai Ekonomi",
        # Tab 3
        'sensitivity_title': "Analisis Sensitivitas & Risiko",
        'sensitivity_params': "Parameter Sensitivitas",
        'discount_range': "Rentang Tingkat Diskonto (%)",
        'cf_variation': "Variasi Arus Kas (%)",
        'cf_help': "Uji skenario optimis/pesimis",
        'run_sensitivity': "Jalankan Analisis Sensitivitas",
        'sensitivity_results': "Hasil Sensitivitas",
        'breakeven_rate': "Tingkat Diskonto Titik Impas",
        'risk_level': "Tingkat Risiko",
        'low_risk': "🟢 RISIKO RENDAH",
        'medium_risk': "🟡 RISIKO SEDANG",
        'high_risk': "🔴 RISIKO TINGGI",
        'tornado_chart': "Diagram Tornado (Dampak pada NPV)",
        # Tab 4
        'scenario_title': "Perbandingan Skenario",
        'add_scenario': "Tambah Skenario",
        'scenario_name': "Nama Skenario",
        'scenario_investment': "Investasi",
        'scenario_annual_cf': "Arus Kas Tahunan",
        'add_btn': "Tambah ke Perbandingan",
        'comparison_table': "Tabel Perbandingan Skenario",
        'best_scenario': "Skenario Terbaik",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nAlat evaluasi proyek infrastruktur komprehensif yang menggabungkan analisis keuangan dengan penilaian nilai ekonomi.",
        'story_insight': "**Wawasan Utama:**\nProyek infrastruktur menciptakan nilai di luar pengembalian finansial - penghematan waktu, keselamatan, manfaat lingkungan, dan multiplier ekonomi.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Pemerintah:** Evaluasi investasi infrastruktur publik.",
        'use_developer': "🏢 **Pengembang:** Menilai kelayakan proyek PPP.",
        'use_analyst': "📊 **Analis:** Membandingkan alternatif infrastruktur."
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

# ========== TAB 1: FINANCIAL ANALYSIS ==========
with tab1:
    st.markdown(f"### {txt['financial_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['project_setup']}")
        
        project_name = st.text_input(txt['project_name'], value="Jalan Tol Trans-Java")
        initial_investment = st.number_input(txt['initial_investment'], value=10.0, step=0.5)
        lifetime = st.slider(txt['project_lifetime'], 5, 50, 20)
        discount_rate = st.number_input(txt['discount_rate'], value=8.0, step=0.5, help=txt['discount_help'])
        
        st.markdown(f"#### {txt['cash_flows']}")
        
        # Cash flow input
        cash_flows = []
        for year in range(1, lifetime + 1):
            cf = st.number_input(f"{txt['year']} {year}", value=1.0, step=0.1, key=f'cf_{year}')
            cash_flows.append(cf)
        
        if st.button(txt['calculate'], type='primary'):
            # Financial calculations
            all_cash_flows = [-initial_investment] + cash_flows
            
            npv_value = npv(discount_rate/100, all_cash_flows)
            
            try:
                irr_value = irr(all_cash_flows) * 100
            except:
                irr_value = None
            
            # Payback period
            cumulative = np.cumsum(all_cash_flows)
            payback_idx = np.where(cumulative > 0)[0]
            payback_period = payback_idx[0] if len(payback_idx) > 0 else None
            
            # Profitability Index
            pv_benefits = sum([cf / (1 + discount_rate/100)**i for i, cf in enumerate(cash_flows, 1)])
            pi_value = pv_benefits / initial_investment if initial_investment > 0 else 0
            
            # Benefit-Cost Ratio
            bcr_value = (npv_value + initial_investment) / initial_investment if initial_investment > 0 else 0
            
            st.session_state['financial_results'] = {
                'npv': npv_value,
                'irr': irr_value,
                'payback': payback_period,
                'pi': pi_value,
                'bcr': bcr_value,
                'cash_flows': all_cash_flows,
                'discount_rate': discount_rate,
                'initial_investment': initial_investment
            }
    
    with col2:
        if 'financial_results' in st.session_state:
            results = st.session_state['financial_results']
            
            st.markdown(f"### {txt['financial_metrics']}")
            
            m1, m2, m3 = st.columns(3)
            m1.metric(txt['npv'], f"Rp {results['npv']:.2f}B")
            if results['irr'] is not None:
                m2.metric(txt['irr'], f"{results['irr']:.2f}%")
            else:
                m2.metric(txt['irr'], "N/A")
            
            if results['payback'] is not None:
                m3.metric(txt['payback'], f"{results['payback']} years")
            else:
                m3.metric(txt['payback'], "Never")
            
            m4, m5 = st.columns(2)
            m4.metric(txt['pi'], f"{results['pi']:.2f}")
            m5.metric(txt['bcr'], f"{results['bcr']:.2f}")
            
            # Decision
            st.markdown(f"### {txt['decision']}")
            
            if results['npv'] > 0 and (results['irr'] is None or results['irr'] > results['discount_rate']):
                st.success(f"{txt['accept']} - NPV > 0 and IRR > Discount Rate")
            elif results['npv'] < 0:
                st.error(f"{txt['reject']} - NPV < 0")
            else:
                st.warning(f"{txt['marginal']} - Requires further analysis")
            
            # Cash flow chart
            st.markdown(f"### {txt['cash_flow_chart']}")
            
            years = list(range(len(results['cash_flows'])))
            cumulative_cf = np.cumsum(results['cash_flows'])
            
            fig = make_subplots(rows=2, cols=1,
                               subplot_titles=(txt['annual'], txt['cumulative']))
            
            fig.add_trace(go.Bar(x=years, y=results['cash_flows'], name=txt['annual'],
                                marker_color=['red' if x < 0 else 'green' for x in results['cash_flows']]),
                         row=1, col=1)
            
            fig.add_trace(go.Scatter(x=years, y=cumulative_cf, mode='lines+markers',
                                    name=txt['cumulative'], line=dict(color='blue', width=3)),
                         row=2, col=1)
            fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
            
            fig.update_xaxes(title_text="Year", row=2, col=1)
            fig.update_yaxes(title_text="Cash Flow (Rp B)", row=1, col=1)
            fig.update_yaxes(title_text="Cumulative (Rp B)", row=2, col=1)
            fig.update_layout(height=700, showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 2: ECONOMIC VALUE ==========
with tab2:
    st.markdown(f"### {txt['economic_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['economic_benefits']}")
        
        time_savings = st.number_input(txt['time_savings'], value=2.0, step=0.1, help=txt['time_help'])
        accident_reduction = st.number_input(txt['accident_reduction'], value=0.5, step=0.1, help=txt['accident_help'])
        environmental = st.number_input(txt['environmental'], value=0.3, step=0.1, help=txt['env_help'])
        employment = st.number_input(txt['employment'], value=5000, step=100, help=txt['emp_help'])
        multiplier = st.number_input(txt['multiplier'], value=2.0, step=0.1, help=txt['mult_help'])
        
        if st.button(txt['calculate'], type='primary', key='econ_calc'):
            if 'financial_results' in st.session_state:
                fin = st.session_state['financial_results']
                
                # Economic benefits per year
                annual_econ_benefits = time_savings + accident_reduction + environmental
                
                # Total economic cash flows
                econ_cash_flows = [-fin['initial_investment']]
                for i, cf in enumerate(fin['cash_flows'][1:], 1):
                    econ_cash_flows.append(cf + annual_econ_benefits)
                
                # Economic NPV
                enpv = npv(fin['discount_rate']/100, econ_cash_flows)
                
                # Economic BCR
                pv_econ_benefits = sum([(cf + annual_econ_benefits) / (1 + fin['discount_rate']/100)**i 
                                       for i, cf in enumerate(fin['cash_flows'], 1)])
                ebcr = pv_econ_benefits / fin['initial_investment'] if fin['initial_investment'] > 0 else 0
                
                # Social ROI
                total_econ_value = enpv + fin['initial_investment']
                social_roi = (total_econ_value / fin['initial_investment']) * 100 if fin['initial_investment'] > 0 else 0
                
                # Total jobs (direct + indirect via multiplier)
                total_jobs = employment * multiplier
                
                st.session_state['economic_results'] = {
                    'enpv': enpv,
                    'ebcr': ebcr,
                    'social_roi': social_roi,
                    'total_jobs': total_jobs,
                    'total_value': total_econ_value,
                    'annual_benefits': annual_econ_benefits
                }
            else:
                st.warning("Run financial analysis first!")
    
    with col2:
        if 'economic_results' in st.session_state:
            results = st.session_state['economic_results']
            
            st.markdown(f"### {txt['economic_metrics']}")
            
            e1, e2, e3 = st.columns(3)
            e1.metric(txt['enpv'], f"Rp {results['enpv']:.2f}B")
            e2.metric(txt['ebcr'], f"{results['ebcr']:.2f}")
            e3.metric(txt['social_roi'], f"{results['social_roi']:.1f}%")
            
            e4, e5 = st.columns(2)
            e4.metric(txt['jobs_created'], f"{results['total_jobs']:,.0f}")
            e5.metric(txt['economic_value'], f"Rp {results['total_value']:.2f}B")
            
            # Comparison chart
            if 'financial_results' in st.session_state:
                fin = st.session_state['financial_results']
                
                fig = go.Figure()
                
                categories = ['NPV', 'BCR']
                financial = [fin['npv'], fin['bcr']]
                economic = [results['enpv'], results['ebcr']]
                
                fig.add_trace(go.Bar(name='Financial', x=categories, y=financial, marker_color='blue'))
                fig.add_trace(go.Bar(name='Economic', x=categories, y=economic, marker_color='green'))
                
                fig.update_layout(
                    title="Financial vs Economic Value",
                    barmode='group',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.info(f"""
                **Economic Value Added:**
                - Annual economic benefits: Rp {results['annual_benefits']:.2f}B
                - Economic NPV exceeds Financial NPV by: Rp {results['enpv'] - fin['npv']:.2f}B
                - This represents the social value created beyond financial returns
                """)

# ========== TAB 3: SENSITIVITY ANALYSIS ==========
with tab3:
    st.markdown(f"### {txt['sensitivity_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['sensitivity_params']}")
        
        min_rate, max_rate = st.slider(txt['discount_range'], 0.0, 20.0, (5.0, 15.0), 0.5)
        cf_variation = st.slider(txt['cf_variation'], -50, 50, (-20, 20), 5, help=txt['cf_help'])
        
        if st.button(txt['run_sensitivity'], type='primary'):
            if 'financial_results' in st.session_state:
                fin = st.session_state['financial_results']
                
                # Discount rate sensitivity
                rates = np.linspace(min_rate, max_rate, 50)
                npvs = [npv(r/100, fin['cash_flows']) for r in rates]
                
                # Find break-even rate
                breakeven_idx = np.where(np.array(npvs) < 0)[0]
                breakeven_rate = rates[breakeven_idx[0]] if len(breakeven_idx) > 0 else max_rate
                
                # Cash flow sensitivity
                base_cf = fin['cash_flows'][1:]  # Exclude initial investment
                pessimistic_cf = [-fin['initial_investment']] + [cf * (1 + cf_variation[0]/100) for cf in base_cf]
                optimistic_cf = [-fin['initial_investment']] + [cf * (1 + cf_variation[1]/100) for cf in base_cf]
                
                npv_pessimistic = npv(fin['discount_rate']/100, pessimistic_cf)
                npv_optimistic = npv(fin['discount_rate']/100, optimistic_cf)
                
                # Risk assessment
                if breakeven_rate > fin['discount_rate'] + 5:
                    risk = txt['low_risk']
                elif breakeven_rate > fin['discount_rate'] + 2:
                    risk = txt['medium_risk']
                else:
                    risk = txt['high_risk']
                
                st.session_state['sensitivity_results'] = {
                    'rates': rates,
                    'npvs': npvs,
                    'breakeven': breakeven_rate,
                    'risk': risk,
                    'npv_pessimistic': npv_pessimistic,
                    'npv_optimistic': npv_optimistic,
                    'cf_variation': cf_variation
                }
            else:
                st.warning("Run financial analysis first!")
    
    with col2:
        if 'sensitivity_results' in st.session_state:
            results = st.session_state['sensitivity_results']
            
            st.markdown(f"### {txt['sensitivity_results']}")
            
            s1, s2 = st.columns(2)
            s1.metric(txt['breakeven_rate'], f"{results['breakeven']:.2f}%")
            s2.metric(txt['risk_level'], results['risk'])
            
            # NPV vs Discount Rate
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=results['rates'], y=results['npvs'],
                                    mode='lines', name='NPV',
                                    line=dict(color='blue', width=3)))
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            fig.add_vline(x=results['breakeven'], line_dash="dash", line_color="orange")
            
            fig.update_layout(
                title="NPV Sensitivity to Discount Rate",
                xaxis_title="Discount Rate (%)",
                yaxis_title="NPV (Rp Billion)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tornado diagram
            fin = st.session_state['financial_results']
            base_npv = fin['npv']
            
            impacts = {
                f"Cash Flow ({results['cf_variation'][0]}%)": results['npv_pessimistic'] - base_npv,
                f"Cash Flow (+{results['cf_variation'][1]}%)": results['npv_optimistic'] - base_npv
            }
            
            fig_tornado = go.Figure()
            
            for label, impact in impacts.items():
                color = 'red' if impact < 0 else 'green'
                fig_tornado.add_trace(go.Bar(
                    y=[label],
                    x=[abs(impact)],
                    orientation='h',
                    marker_color=color,
                    name=label
                ))
            
            fig_tornado.update_layout(
                title=txt['tornado_chart'],
                xaxis_title="Impact on NPV (Rp Billion)",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig_tornado, use_container_width=True)

# ========== TAB 4: SCENARIO COMPARISON ==========
with tab4:
    st.markdown(f"### {txt['scenario_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['add_scenario']}")
        
        scenario_name = st.text_input(txt['scenario_name'], value="Scenario A")
        scenario_investment = st.number_input(txt['scenario_investment'], value=10.0, step=0.5, key='sc_inv')
        scenario_annual_cf = st.number_input(txt['scenario_annual_cf'], value=1.5, step=0.1, key='sc_cf')
        scenario_years = st.slider("Years", 5, 30, 15, key='sc_years')
        
        if st.button(txt['add_btn']):
            cash_flows = [-scenario_investment] + [scenario_annual_cf] * scenario_years
            npv_val = npv(0.08, cash_flows)
            
            try:
                irr_val = irr(cash_flows) * 100
            except:
                irr_val = None
            
            st.session_state['scenarios'].append({
                'Name': scenario_name,
                'Investment': scenario_investment,
                'Annual CF': scenario_annual_cf,
                'Years': scenario_years,
                'NPV': npv_val,
                'IRR': irr_val if irr_val else 0
            })
            st.success(f"Added {scenario_name}!")
    
    with col2:
        if len(st.session_state['scenarios']) > 0:
            df_scenarios = pd.DataFrame(st.session_state['scenarios'])
            
            st.markdown(f"### {txt['comparison_table']}")
            
            st.dataframe(df_scenarios.style.highlight_max(subset=['NPV', 'IRR'], color='lightgreen'),
                        use_container_width=True, hide_index=True)
            
            # Best scenario
            best_idx = df_scenarios['NPV'].idxmax()
            st.success(f"🏆 {txt['best_scenario']}: {df_scenarios.iloc[best_idx]['Name']} (NPV: Rp {df_scenarios.iloc[best_idx]['NPV']:.2f}B)")
            
            # Comparison chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(name='NPV', x=df_scenarios['Name'], y=df_scenarios['NPV'],
                                marker_color='blue'))
            
            fig.update_layout(
                title="NPV Comparison Across Scenarios",
                xaxis_title="Scenario",
                yaxis_title="NPV (Rp Billion)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add scenarios to compare")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_govt'])
        st.write(txt['use_developer'])
        st.write(txt['use_analyst'])
