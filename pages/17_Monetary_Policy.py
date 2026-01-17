import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Monetary Policy", page_icon="💰", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "💰 Monetary Policy Dashboard",
        'subtitle': "Determine optimal interest rates using **Taylor Rule** and analyze **Phillips Curve** trade-offs.",
        'tab1': "📈 Taylor Rule Calculator",
        'tab2': "📉 Phillips Curve",
        # Tab 1: Taylor Rule
        'taylor_theory': "**Taylor Rule**: Determines optimal policy interest rate based on inflation gap and output gap.",
        'taylor_formula': "**Formula**: r* = r_neutral + π + α(π - π*) + β(Y - Y*)",
        'current_conditions': "📊 Current Economic Conditions",
        'current_inflation': "Current Inflation Rate (%)",
        'target_inflation': "Target Inflation Rate (%)",
        'output_gap': "Output Gap (%) - (Actual GDP - Potential GDP) / Potential GDP",
        'output_gap_help': "Positive = Economy overheating, Negative = Recession",
        'taylor_params': "⚙️ Taylor Rule Parameters",
        'neutral_rate': "Neutral Real Interest Rate (%)",
        'neutral_help': "Long-run equilibrium rate (~2% for developed economies)",
        'alpha': "α (Inflation Gap Weight)",
        'alpha_help': "Standard Taylor Rule uses 0.5",
        'beta': "β (Output Gap Weight)",
        'beta_help': "Standard Taylor Rule uses 0.5",
        'calc_taylor': "🎯 Calculate Optimal Rate",
        'taylor_results': "📋 Taylor Rule Recommendation",
        'recommended_rate': "Recommended BI Rate",
        'current_bi_rate': "Current BI Rate (for comparison)",
        'policy_stance': "Policy Stance",
        'tighten': "🔴 TIGHTEN (Raise Rate)",
        'ease': "🟢 EASE (Cut Rate)",
        'maintain': "🟡 MAINTAIN (Hold Rate)",
        'gap_analysis': "Gap: {gap:.2f}%",
        'explanation': "💡 Explanation",
        'exp_tighten': "Inflation is {inf:.1f}% above target. Raising rates will cool down the economy and reduce inflation.",
        'exp_ease': "Inflation is {inf:.1f}% below target and/or economy is {out:.1f}% below potential. Cutting rates will stimulate growth.",
        'exp_maintain': "Economy is near equilibrium. Maintain current policy stance.",
        # Tab 2: Phillips Curve
        'phillips_theory': "**Phillips Curve**: Shows the short-run trade-off between inflation and unemployment.",
        'phillips_formula': "**Formula**: π = π_e - β(u - u_n)",
        'phillips_inputs': "📊 Phillips Curve Parameters",
        'expected_inflation': "Expected Inflation (%)",
        'nairu': "Natural Unemployment Rate - NAIRU (%)",
        'nairu_help': "Non-Accelerating Inflation Rate of Unemployment (~5-6% for Indonesia)",
        'phillips_slope': "β (Slope Coefficient)",
        'phillips_slope_help': "How much inflation changes per 1% change in unemployment",
        'current_unemployment': "Current Unemployment Rate (%)",
        'calc_phillips': "📉 Calculate Phillips Curve",
        'phillips_results': "📋 Phillips Curve Analysis",
        'predicted_inflation': "Predicted Inflation",
        'unemployment_gap': "Unemployment Gap",
        'phillips_chart': "Phillips Curve Visualization",
        'short_run': "Short-Run Phillips Curve",
        'long_run': "Long-Run (Vertical at NAIRU)",
        'current_point': "Current Economy",
        'phillips_insight': "💡 **Insight**: If unemployment is {u:.1f}% (vs NAIRU {nairu:.1f}%), predicted inflation is {pi:.2f}%.",
        # Story
        'story_title': "📚 Story & Use Cases: Monetary Policy Dashboard",
        'story_meaning': "**What is this?**\nThis module helps central banks set optimal interest rates using the Taylor Rule and understand inflation-unemployment dynamics via the Phillips Curve.",
        'story_insight': "**Key Insight:**\nThe Taylor Rule provides a systematic, data-driven approach to monetary policy. The Phillips Curve shows why central banks face trade-offs in the short run.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Bank Indonesia (BI):** To determine the optimal BI Rate based on inflation and output gaps.",
        'use_corp': "🏢 **Financial Institutions:** To forecast central bank policy decisions and adjust investment strategies.",
        'use_analyst': "📈 **Macro Economists:** To evaluate whether central bank policy is too tight or too loose."
    },
    'ID': {
        'title': "💰 Dashboard Kebijakan Moneter",
        'subtitle': "Tentukan suku bunga optimal menggunakan **Taylor Rule** dan analisis trade-off **Kurva Phillips**.",
        'tab1': "📈 Kalkulator Taylor Rule",
        'tab2': "📉 Kurva Phillips",
        # Tab 1: Taylor Rule
        'taylor_theory': "**Taylor Rule**: Menentukan suku bunga kebijakan optimal berdasarkan gap inflasi dan gap output.",
        'taylor_formula': "**Rumus**: r* = r_netral + π + α(π - π*) + β(Y - Y*)",
        'current_conditions': "📊 Kondisi Ekonomi Saat Ini",
        'current_inflation': "Inflasi Saat Ini (%)",
        'target_inflation': "Target Inflasi (%)",
        'output_gap': "Gap Output (%) - (PDB Aktual - PDB Potensial) / PDB Potensial",
        'output_gap_help': "Positif = Ekonomi overheating, Negatif = Resesi",
        'taylor_params': "⚙️ Parameter Taylor Rule",
        'neutral_rate': "Suku Bunga Riil Netral (%)",
        'neutral_help': "Tingkat keseimbangan jangka panjang (~2% untuk negara maju)",
        'alpha': "α (Bobot Gap Inflasi)",
        'alpha_help': "Taylor Rule standar menggunakan 0.5",
        'beta': "β (Bobot Gap Output)",
        'beta_help': "Taylor Rule standar menggunakan 0.5",
        'calc_taylor': "🎯 Hitung Suku Bunga Optimal",
        'taylor_results': "📋 Rekomendasi Taylor Rule",
        'recommended_rate': "BI Rate yang Direkomendasikan",
        'current_bi_rate': "BI Rate Saat Ini (untuk perbandingan)",
        'policy_stance': "Sikap Kebijakan",
        'tighten': "🔴 KETAT (Naikkan Suku Bunga)",
        'ease': "🟢 LONGGAR (Turunkan Suku Bunga)",
        'maintain': "🟡 PERTAHANKAN (Tahan Suku Bunga)",
        'gap_analysis': "Selisih: {gap:.2f}%",
        'explanation': "💡 Penjelasan",
        'exp_tighten': "Inflasi {inf:.1f}% di atas target. Menaikkan suku bunga akan mendinginkan ekonomi dan menurunkan inflasi.",
        'exp_ease': "Inflasi {inf:.1f}% di bawah target dan/atau ekonomi {out:.1f}% di bawah potensial. Menurunkan suku bunga akan memacu pertumbuhan.",
        'exp_maintain': "Ekonomi mendekati keseimbangan. Pertahankan sikap kebijakan saat ini.",
        # Tab 2: Phillips Curve
        'phillips_theory': "**Kurva Phillips**: Menunjukkan trade-off jangka pendek antara inflasi dan pengangguran.",
        'phillips_formula': "**Rumus**: π = π_e - β(u - u_n)",
        'phillips_inputs': "📊 Parameter Kurva Phillips",
        'expected_inflation': "Inflasi yang Diharapkan (%)",
        'nairu': "Tingkat Pengangguran Alamiah - NAIRU (%)",
        'nairu_help': "Non-Accelerating Inflation Rate of Unemployment (~5-6% untuk Indonesia)",
        'phillips_slope': "β (Koefisien Kemiringan)",
        'phillips_slope_help': "Seberapa besar inflasi berubah per 1% perubahan pengangguran",
        'current_unemployment': "Tingkat Pengangguran Saat Ini (%)",
        'calc_phillips': "📉 Hitung Kurva Phillips",
        'phillips_results': "📋 Analisis Kurva Phillips",
        'predicted_inflation': "Inflasi yang Diprediksi",
        'unemployment_gap': "Gap Pengangguran",
        'phillips_chart': "Visualisasi Kurva Phillips",
        'short_run': "Kurva Phillips Jangka Pendek",
        'long_run': "Jangka Panjang (Vertikal di NAIRU)",
        'current_point': "Ekonomi Saat Ini",
        'phillips_insight': "💡 **Wawasan**: Jika pengangguran {u:.1f}% (vs NAIRU {nairu:.1f}%), inflasi diprediksi {pi:.2f}%.",
        # Story
        'story_title': "📚 Cerita & Kasus Penggunaan: Dashboard Kebijakan Moneter",
        'story_meaning': "**Apa artinya ini?**\nModul ini membantu bank sentral menetapkan suku bunga optimal menggunakan Taylor Rule dan memahami dinamika inflasi-pengangguran via Kurva Phillips.",
        'story_insight': "**Wawasan Utama:**\nTaylor Rule memberikan pendekatan sistematis berbasis data untuk kebijakan moneter. Kurva Phillips menunjukkan mengapa bank sentral menghadapi trade-off di jangka pendek.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Bank Indonesia (BI):** Untuk menentukan BI Rate optimal berdasarkan gap inflasi dan output.",
        'use_corp': "🏢 **Lembaga Keuangan:** Untuk memprediksi keputusan kebijakan bank sentral dan menyesuaikan strategi investasi.",
        'use_analyst': "📈 **Ekonom Makro:** Untuk mengevaluasi apakah kebijakan bank sentral terlalu ketat atau terlalu longgar."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- TABS ---
tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])

# ========== TAB 1: TAYLOR RULE ==========
with tab1:
    st.info(txt['taylor_theory'])
    st.caption(txt['taylor_formula'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['current_conditions'])
        current_inflation = st.number_input(txt['current_inflation'], value=3.5, step=0.1)
        target_inflation = st.number_input(txt['target_inflation'], value=2.0, step=0.1)
        output_gap = st.number_input(txt['output_gap'], value=1.0, step=0.5, help=txt['output_gap_help'])
        
        st.markdown("---")
        st.subheader(txt['taylor_params'])
        neutral_rate = st.number_input(txt['neutral_rate'], value=2.0, step=0.1, help=txt['neutral_help'])
        alpha = st.slider(txt['alpha'], 0.0, 2.0, 0.5, 0.1, help=txt['alpha_help'])
        beta = st.slider(txt['beta'], 0.0, 2.0, 0.5, 0.1, help=txt['beta_help'])
        
        current_bi = st.number_input(txt['current_bi_rate'], value=5.75, step=0.25)
        
        calc_btn = st.button(txt['calc_taylor'], type='primary')
    
    with col2:
        if calc_btn:
            # Taylor Rule Calculation
            # r* = r_neutral + π + α(π - π*) + β(Y - Y*)
            inflation_gap = current_inflation - target_inflation
            recommended_rate = neutral_rate + current_inflation + alpha * inflation_gap + beta * output_gap
            
            gap = recommended_rate - current_bi
            
            st.subheader(txt['taylor_results'])
            
            m1, m2, m3 = st.columns(3)
            m1.metric(txt['recommended_rate'], f"{recommended_rate:.2f}%")
            m2.metric(txt['current_bi_rate'], f"{current_bi:.2f}%")
            
            # Policy Stance
            if gap > 0.25:
                stance = txt['tighten']
                color = "error"
            elif gap < -0.25:
                stance = txt['ease']
                color = "success"
            else:
                stance = txt['maintain']
                color = "warning"
            
            m3.metric(txt['policy_stance'], stance, delta=txt['gap_analysis'].format(gap=gap))
            
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=recommended_rate,
                delta={'reference': current_bi, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                title={'text': txt['recommended_rate']},
                gauge={
                    'axis': {'range': [0, 10]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 3], 'color': "lightgreen"},
                        {'range': [3, 6], 'color': "lightyellow"},
                        {'range': [6, 10], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': current_bi
                    }
                }
            ))
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Explanation
            st.markdown("---")
            st.subheader(txt['explanation'])
            
            if gap > 0.25:
                st.warning(txt['exp_tighten'].format(inf=inflation_gap))
            elif gap < -0.25:
                st.success(txt['exp_ease'].format(inf=abs(inflation_gap), out=abs(output_gap)))
            else:
                st.info(txt['exp_maintain'])

# ========== TAB 2: PHILLIPS CURVE ==========
with tab2:
    st.info(txt['phillips_theory'])
    st.caption(txt['phillips_formula'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['phillips_inputs'])
        expected_inflation = st.number_input(txt['expected_inflation'], value=3.0, step=0.1)
        nairu = st.number_input(txt['nairu'], value=5.5, step=0.1, help=txt['nairu_help'])
        phillips_slope = st.number_input(txt['phillips_slope'], value=0.5, step=0.1, help=txt['phillips_slope_help'])
        current_unemployment = st.number_input(txt['current_unemployment'], value=5.0, step=0.1)
        
        calc_phillips_btn = st.button(txt['calc_phillips'], type='primary')
    
    with col2:
        if calc_phillips_btn:
            # Phillips Curve Calculation
            # π = π_e - β(u - u_n)
            unemployment_gap = current_unemployment - nairu
            predicted_inflation = expected_inflation - phillips_slope * unemployment_gap
            
            st.subheader(txt['phillips_results'])
            
            p1, p2 = st.columns(2)
            p1.metric(txt['predicted_inflation'], f"{predicted_inflation:.2f}%")
            p2.metric(txt['unemployment_gap'], f"{unemployment_gap:.2f}%")
            
            st.info(txt['phillips_insight'].format(u=current_unemployment, nairu=nairu, pi=predicted_inflation))
            
            # Phillips Curve Visualization
            st.markdown("---")
            st.subheader(txt['phillips_chart'])
            
            # Generate Phillips Curve data
            u_range = np.linspace(2, 10, 100)
            # Short-run Phillips Curve
            pi_short_run = expected_inflation - phillips_slope * (u_range - nairu)
            
            fig = go.Figure()
            
            # Short-run Phillips Curve
            fig.add_trace(go.Scatter(
                x=u_range,
                y=pi_short_run,
                mode='lines',
                name=txt['short_run'],
                line=dict(color='blue', width=3)
            ))
            
            # Long-run Phillips Curve (Vertical at NAIRU)
            fig.add_trace(go.Scatter(
                x=[nairu, nairu],
                y=[-2, 10],
                mode='lines',
                name=txt['long_run'],
                line=dict(color='gray', dash='dash', width=2)
            ))
            
            # Current Point
            fig.add_trace(go.Scatter(
                x=[current_unemployment],
                y=[predicted_inflation],
                mode='markers',
                name=txt['current_point'],
                marker=dict(size=15, color='red', symbol='star')
            ))
            
            fig.update_layout(
                title=txt['phillips_chart'],
                xaxis_title="Unemployment Rate (%)" if lang == 'EN' else "Tingkat Pengangguran (%)",
                yaxis_title="Inflation Rate (%)" if lang == 'EN' else "Tingkat Inflasi (%)",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

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
