import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from numpy_financial import npv, irr

st.set_page_config(page_title="Cost-Benefit Analysis", page_icon="🏗️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🏗️ Cost-Benefit Analysis Tool",
        'subtitle': "Evaluate infrastructure projects using **NPV**, **IRR**, and **Sensitivity Analysis**.",
        'tab1': "💰 NPV/IRR Calculator",
        'tab2': "📊 Sensitivity Analysis",
        # Tab 1
        'npv_theory': "**What is NPV?** Net Present Value = Total value of future cash flows minus initial investment (in today's money).",
        'irr_theory': "**What is IRR?** Internal Rate of Return = The discount rate that makes NPV = 0 (break-even rate).",
        'tutorial_btn': "📖 Tutorial: How to Use This Tool",
        'project_inputs': "🏗️ Project Details",
        'project_name': "Project Name",
        'initial_investment': "Initial Investment (Rp Billion)",
        'investment_help': "Total upfront cost (negative number)",
        'project_lifetime': "Project Lifetime (Years)",
        'discount_rate': "Discount Rate (%)",
        'discount_help': "Minimum acceptable return rate (WACC or government bond rate)",
        'cash_flows': "💵 Annual Cash Flows (Rp Billion)",
        'cash_flow_help': "Expected net income per year. Positive = profit, Negative = loss.",
        'calc_npv': "🎯 Calculate NPV & IRR",
        'results': "📋 Financial Analysis Results",
        'npv_result': "Net Present Value (NPV)",
        'irr_result': "Internal Rate of Return (IRR)",
        'payback_period': "Payback Period",
        'profitability_index': "Profitability Index (PI)",
        'decision': "Investment Decision",
        'accept': "✅ ACCEPT - Project is profitable",
        'reject': "❌ REJECT - Project is not profitable",
        'npv_positive': "NPV > 0: Project creates value",
        'npv_negative': "NPV < 0: Project destroys value",
        'irr_high': "IRR ({irr:.2f}%) > Discount Rate ({dr:.2f}%): Good investment",
        'irr_low': "IRR ({irr:.2f}%) < Discount Rate ({dr:.2f}%): Poor investment",
        'payback_info': "Time to recover initial investment: {pb:.1f} years",
        'pi_info': "Return per Rp 1 invested: Rp {pi:.2f}",
        'chart_title': "Cash Flow Timeline",
        'cumulative_cf': "Cumulative Cash Flow",
        # Tab 2
        'sensitivity_theory': "**Sensitivity Analysis**: Shows how NPV changes when discount rate changes (risk assessment).",
        'sensitivity_inputs': "📊 Sensitivity Parameters",
        'min_rate': "Minimum Discount Rate (%)",
        'max_rate': "Maximum Discount Rate (%)",
        'calc_sensitivity': "📈 Run Sensitivity Analysis",
        'sensitivity_results': "📋 Sensitivity Analysis Results",
        'breakeven_rate': "Break-Even Discount Rate",
        'risk_assessment': "Risk Assessment",
        'low_risk': "🟢 LOW RISK - NPV remains positive across wide range",
        'medium_risk': "🟡 MEDIUM RISK - NPV sensitive to discount rate changes",
        'high_risk': "🔴 HIGH RISK - NPV turns negative at modest rate increases",
        'sensitivity_chart': "NPV Sensitivity to Discount Rate",
        # Story
        'story_title': "📚 Story & Use Cases: Cost-Benefit Analysis",
        'story_meaning': "**What is this?**\nThis tool helps evaluate whether an infrastructure project (toll road, bridge, airport) is financially viable using NPV and IRR metrics.",
        'story_insight': "**Key Insight:**\nNPV tells you HOW MUCH value a project creates. IRR tells you the RETURN RATE. Sensitivity Analysis shows RISK.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Kementerian PUPR:** To evaluate feasibility of infrastructure projects before budget allocation.",
        'use_corp': "🏢 **Private Developers:** To decide whether to invest in toll roads, power plants, or real estate projects.",
        'use_analyst': "📈 **Financial Analysts:** To compare multiple projects and recommend the best investment."
    },
    'ID': {
        'title': "🏗️ Alat Analisis Biaya-Manfaat",
        'subtitle': "Evaluasi proyek infrastruktur menggunakan **NPV**, **IRR**, dan **Analisis Sensitivitas**.",
        'tab1': "💰 Kalkulator NPV/IRR",
        'tab2': "📊 Analisis Sensitivitas",
        # Tab 1
        'npv_theory': "**Apa itu NPV?** Net Present Value = Total nilai arus kas masa depan dikurangi investasi awal (dalam nilai uang hari ini).",
        'irr_theory': "**Apa itu IRR?** Internal Rate of Return = Tingkat diskonto yang membuat NPV = 0 (titik impas).",
        'tutorial_btn': "📖 Tutorial: Cara Menggunakan Alat Ini",
        'project_inputs': "🏗️ Detail Proyek",
        'project_name': "Nama Proyek",
        'initial_investment': "Investasi Awal (Rp Miliar)",
        'investment_help': "Total biaya di muka (angka negatif)",
        'project_lifetime': "Umur Proyek (Tahun)",
        'discount_rate': "Tingkat Diskonto (%)",
        'discount_help': "Tingkat pengembalian minimum yang dapat diterima (WACC atau suku bunga obligasi pemerintah)",
        'cash_flows': "💵 Arus Kas Tahunan (Rp Miliar)",
        'cash_flow_help': "Pendapatan bersih yang diharapkan per tahun. Positif = untung, Negatif = rugi.",
        'calc_npv': "🎯 Hitung NPV & IRR",
        'results': "📋 Hasil Analisis Keuangan",
        'npv_result': "Net Present Value (NPV)",
        'irr_result': "Internal Rate of Return (IRR)",
        'payback_period': "Periode Pengembalian",
        'profitability_index': "Indeks Profitabilitas (PI)",
        'decision': "Keputusan Investasi",
        'accept': "✅ TERIMA - Proyek menguntungkan",
        'reject': "❌ TOLAK - Proyek tidak menguntungkan",
        'npv_positive': "NPV > 0: Proyek menciptakan nilai",
        'npv_negative': "NPV < 0: Proyek menghancurkan nilai",
        'irr_high': "IRR ({irr:.2f}%) > Tingkat Diskonto ({dr:.2f}%): Investasi bagus",
        'irr_low': "IRR ({irr:.2f}%) < Tingkat Diskonto ({dr:.2f}%): Investasi buruk",
        'payback_info': "Waktu untuk kembali modal: {pb:.1f} tahun",
        'pi_info': "Pengembalian per Rp 1 yang diinvestasikan: Rp {pi:.2f}",
        'chart_title': "Timeline Arus Kas",
        'cumulative_cf': "Arus Kas Kumulatif",
        # Tab 2
        'sensitivity_theory': "**Analisis Sensitivitas**: Menunjukkan bagaimana NPV berubah ketika tingkat diskonto berubah (penilaian risiko).",
        'sensitivity_inputs': "📊 Parameter Sensitivitas",
        'min_rate': "Tingkat Diskonto Minimum (%)",
        'max_rate': "Tingkat Diskonto Maksimum (%)",
        'calc_sensitivity': "📈 Jalankan Analisis Sensitivitas",
        'sensitivity_results': "📋 Hasil Analisis Sensitivitas",
        'breakeven_rate': "Tingkat Diskonto Titik Impas",
        'risk_assessment': "Penilaian Risiko",
        'low_risk': "🟢 RISIKO RENDAH - NPV tetap positif di berbagai tingkat",
        'medium_risk': "🟡 RISIKO SEDANG - NPV sensitif terhadap perubahan tingkat diskonto",
        'high_risk': "🔴 RISIKO TINGGI - NPV menjadi negatif pada kenaikan tingkat yang moderat",
        'sensitivity_chart': "Sensitivitas NPV terhadap Tingkat Diskonto",
        # Story
        'story_title': "📚 Cerita & Kasus Penggunaan: Analisis Biaya-Manfaat",
        'story_meaning': "**Apa artinya ini?**\nAlat ini membantu mengevaluasi apakah proyek infrastruktur (jalan tol, jembatan, bandara) layak secara finansial menggunakan metrik NPV dan IRR.",
        'story_insight': "**Wawasan Utama:**\nNPV memberi tahu Anda BERAPA BANYAK nilai yang diciptakan proyek. IRR memberi tahu Anda TINGKAT PENGEMBALIAN. Analisis Sensitivitas menunjukkan RISIKO.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Kementerian PUPR:** Untuk mengevaluasi kelayakan proyek infrastruktur sebelum alokasi anggaran.",
        'use_corp': "🏢 **Pengembang Swasta:** Untuk memutuskan apakah akan berinvestasi di jalan tol, pembangkit listrik, atau proyek real estat.",
        'use_analyst': "📈 **Analis Keuangan:** Untuk membandingkan beberapa proyek dan merekomendasikan investasi terbaik."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Tutorial Expander
with st.expander(txt['tutorial_btn']):
    if lang == 'ID':
        st.markdown("""
        ### 📖 Panduan Lengkap: Analisis Biaya-Manfaat
        
        #### **1. Apa itu NPV (Net Present Value)?**
        NPV adalah **total nilai uang** yang akan Anda dapatkan dari proyek, dihitung dalam nilai uang **hari ini**.
        
        **Contoh Sederhana:**
        - Anda investasi **Rp 1 Miliar** untuk membangun jalan tol.
        - Setiap tahun, jalan tol menghasilkan **Rp 300 Juta** selama 5 tahun.
        - **Pertanyaan**: Apakah investasi ini menguntungkan?
        
        **Rumus NPV:**
        ```
        NPV = (Arus Kas Tahun 1 / (1+r)^1) + (Arus Kas Tahun 2 / (1+r)^2) + ... - Investasi Awal
        ```
        Dimana `r` = Tingkat diskonto (misal 10%)
        
        **Interpretasi:**
        - **NPV > 0** → Proyek **UNTUNG** ✅
        - **NPV < 0** → Proyek **RUGI** ❌
        - **NPV = 0** → Proyek **IMPAS** (tidak untung, tidak rugi)
        
        ---
        
        #### **2. Apa itu IRR (Internal Rate of Return)?**
        IRR adalah **tingkat pengembalian** yang membuat NPV = 0. Ini adalah "bunga" yang Anda dapatkan dari proyek.
        
        **Contoh:**
        - Jika IRR = **15%**, artinya proyek memberikan return **15% per tahun**.
        - Jika tingkat diskonto Anda (misal suku bunga bank) = **10%**, maka proyek ini **lebih baik** dari menyimpan uang di bank.
        
        **Keputusan:**
        - **IRR > Tingkat Diskonto** → **TERIMA** proyek ✅
        - **IRR < Tingkat Diskonto** → **TOLAK** proyek ❌
        
        ---
        
        #### **3. Apa itu Tingkat Diskonto?**
        Tingkat diskonto adalah **tingkat pengembalian minimum** yang Anda harapkan. Biasanya:
        - **Pemerintah**: Suku bunga obligasi pemerintah (~6-7%)
        - **Perusahaan Swasta**: WACC (Weighted Average Cost of Capital) (~10-15%)
        
        **Mengapa penting?**
        Uang **hari ini** lebih berharga daripada uang **masa depan** karena inflasi dan risiko.
        
        ---
        
        #### **4. Contoh Praktis:**
        **Proyek**: Membangun Jembatan Tol
        - **Investasi Awal**: Rp 10 Miliar
        - **Arus Kas Tahunan**: Rp 2 Miliar (Tahun 1-7)
        - **Tingkat Diskonto**: 8%
        
        **Hasil:**
        - **NPV** ≈ Rp 1.5 Miliar (POSITIF → Proyek layak!)
        - **IRR** ≈ 12% (Lebih tinggi dari 8% → Investasi bagus!)
        - **Payback Period** ≈ 5 tahun (Modal kembali dalam 5 tahun)
        """)
    else:
        st.markdown("""
        ### 📖 Complete Guide: Cost-Benefit Analysis
        
        #### **1. What is NPV (Net Present Value)?**
        NPV is the **total money value** you will get from a project, calculated in **today's money**.
        
        **Simple Example:**
        - You invest **Rp 1 Billion** to build a toll road.
        - Each year, the toll road generates **Rp 300 Million** for 5 years.
        - **Question**: Is this investment profitable?
        
        **NPV Formula:**
        ```
        NPV = (Cash Flow Year 1 / (1+r)^1) + (Cash Flow Year 2 / (1+r)^2) + ... - Initial Investment
        ```
        Where `r` = Discount rate (e.g., 10%)
        
        **Interpretation:**
        - **NPV > 0** → Project is **PROFITABLE** ✅
        - **NPV < 0** → Project is **UNPROFITABLE** ❌
        - **NPV = 0** → Project **BREAKS EVEN**
        
        ---
        
        #### **2. What is IRR (Internal Rate of Return)?**
        IRR is the **return rate** that makes NPV = 0. It's the "interest" you earn from the project.
        
        **Example:**
        - If IRR = **15%**, the project gives a return of **15% per year**.
        - If your discount rate (e.g., bank interest) = **10%**, then this project is **better** than saving money in a bank.
        
        **Decision:**
        - **IRR > Discount Rate** → **ACCEPT** project ✅
        - **IRR < Discount Rate** → **REJECT** project ❌
        
        ---
        
        #### **3. What is Discount Rate?**
        Discount rate is the **minimum return rate** you expect. Typically:
        - **Government**: Government bond rate (~6-7%)
        - **Private Companies**: WACC (Weighted Average Cost of Capital) (~10-15%)
        
        **Why important?**
        Money **today** is more valuable than money **in the future** due to inflation and risk.
        
        ---
        
        #### **4. Practical Example:**
        **Project**: Building a Toll Bridge
        - **Initial Investment**: Rp 10 Billion
        - **Annual Cash Flow**: Rp 2 Billion (Years 1-7)
        - **Discount Rate**: 8%
        
        **Results:**
        - **NPV** ≈ Rp 1.5 Billion (POSITIVE → Project is feasible!)
        - **IRR** ≈ 12% (Higher than 8% → Good investment!)
        - **Payback Period** ≈ 5 years (Capital recovered in 5 years)
        """)

# --- TABS ---
tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])

# ========== TAB 1: NPV/IRR CALCULATOR ==========
with tab1:
    st.info(txt['npv_theory'])
    st.caption(txt['irr_theory'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['project_inputs'])
        project_name = st.text_input(txt['project_name'], value="Toll Road Project")
        initial_investment = st.number_input(txt['initial_investment'], value=-10.0, step=0.5, help=txt['investment_help'])
        project_lifetime = st.slider(txt['project_lifetime'], 1, 20, 10)
        discount_rate_pct = st.number_input(txt['discount_rate'], value=8.0, step=0.5, help=txt['discount_help'])
        
        st.markdown("---")
        st.subheader(txt['cash_flows'])
        st.caption(txt['cash_flow_help'])
        
        # Initialize cash flows
        if 'cash_flows' not in st.session_state:
            st.session_state['cash_flows'] = pd.DataFrame({
                'Year': list(range(1, 11)),
                'Cash Flow (Rp Billion)': [2.0] * 10
            })
        
        # Adjust dataframe size based on project lifetime
        current_years = len(st.session_state['cash_flows'])
        if project_lifetime != current_years:
            if project_lifetime > current_years:
                # Add rows
                new_rows = pd.DataFrame({
                    'Year': list(range(current_years + 1, project_lifetime + 1)),
                    'Cash Flow (Rp Billion)': [2.0] * (project_lifetime - current_years)
                })
                st.session_state['cash_flows'] = pd.concat([st.session_state['cash_flows'], new_rows], ignore_index=True)
            else:
                # Remove rows
                st.session_state['cash_flows'] = st.session_state['cash_flows'].iloc[:project_lifetime]
        
        edited_cf = st.data_editor(
            st.session_state['cash_flows'],
            use_container_width=True,
            hide_index=True,
            key='cf_editor'
        )
        
        # Update session state with edited values
        if edited_cf is not None:
            st.session_state['cash_flows'] = edited_cf.copy()
        
        calc_btn = st.button(txt['calc_npv'], type='primary', key='calc_npv_btn')
    
    with col2:
        # Always show results if calculation has been done
        if calc_btn or 'npv_results' in st.session_state:
            if calc_btn:
                # Prepare cash flows from session state
                cash_flows_array = np.concatenate([[initial_investment], st.session_state['cash_flows']['Cash Flow (Rp Billion)'].values])
            discount_rate = discount_rate_pct / 100
            
            # Calculate NPV
            npv_value = npv(discount_rate, cash_flows_array)
            
            # Calculate IRR
            try:
                irr_value = irr(cash_flows_array) * 100
            except:
                irr_value = None
            
            # Calculate Payback Period
            cumulative_cf = np.cumsum(cash_flows_array)
            payback_idx = np.where(cumulative_cf > 0)[0]
            if len(payback_idx) > 0:
                payback_period = payback_idx[0]
            else:
                payback_period = None
            
            # Profitability Index
            pv_future_cf = npv_value - initial_investment
            pi = pv_future_cf / abs(initial_investment) if initial_investment != 0 else 0
            
            st.subheader(txt['results'])
            
            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(txt['npv_result'], f"Rp {npv_value:.2f}B")
            if irr_value is not None:
                m2.metric(txt['irr_result'], f"{irr_value:.2f}%")
            else:
                m2.metric(txt['irr_result'], "N/A")
            
            if payback_period is not None:
                m3.metric(txt['payback_period'], f"{payback_period} years")
            else:
                m3.metric(txt['payback_period'], "> Lifetime")
            
            m4.metric(txt['profitability_index'], f"{pi:.2f}")
            
            # Decision
            st.markdown("---")
            st.subheader(txt['decision'])
            
            if npv_value > 0:
                st.success(txt['accept'])
                st.info(txt['npv_positive'])
            else:
                st.error(txt['reject'])
                st.warning(txt['npv_negative'])
            
            if irr_value is not None:
                if irr_value > discount_rate_pct:
                    st.success(txt['irr_high'].format(irr=irr_value, dr=discount_rate_pct))
                else:
                    st.warning(txt['irr_low'].format(irr=irr_value, dr=discount_rate_pct))
            
            if payback_period is not None:
                st.info(txt['payback_info'].format(pb=payback_period))
            
            st.info(txt['pi_info'].format(pi=pi))
            
            # Visualization
            st.markdown("---")
            st.subheader(txt['chart_title'])
            
            years = ['Year 0'] + [f'Year {i}' for i in range(1, project_lifetime + 1)]
            
            fig = go.Figure()
            
            # Cash Flow Bars
            fig.add_trace(go.Bar(
                x=years,
                y=cash_flows_array,
                name='Cash Flow',
                marker_color=['red' if cf < 0 else 'green' for cf in cash_flows_array]
            ))
            
            # Cumulative Cash Flow Line
            fig.add_trace(go.Scatter(
                x=years,
                y=cumulative_cf,
                name=txt['cumulative_cf'],
                mode='lines+markers',
                line=dict(color='blue', width=3)
            ))
            
            # Zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            
            fig.update_layout(
                title=txt['chart_title'],
                xaxis_title="Year",
                yaxis_title="Rp Billion",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 2: SENSITIVITY ANALYSIS ==========
with tab2:
    st.info(txt['sensitivity_theory'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['sensitivity_inputs'])
        min_rate = st.number_input(txt['min_rate'], value=2.0, step=0.5)
        max_rate = st.number_input(txt['max_rate'], value=20.0, step=0.5)
        
        calc_sens_btn = st.button(txt['calc_sensitivity'], type='primary')
    
    with col2:
        if calc_sens_btn and 'cash_flows' in st.session_state:
            # Prepare cash flows
            cash_flows_array = np.concatenate([[initial_investment], st.session_state['cash_flows']['Cash Flow (Rp Billion)'].values])
            
            # Generate discount rate range
            discount_rates = np.linspace(min_rate, max_rate, 100) / 100
            npv_values = [npv(r, cash_flows_array) for r in discount_rates]
            
            # Find break-even rate (where NPV = 0)
            try:
                breakeven_rate = irr(cash_flows_array) * 100
            except:
                breakeven_rate = None
            
            st.subheader(txt['sensitivity_results'])
            
            if breakeven_rate is not None:
                st.metric(txt['breakeven_rate'], f"{breakeven_rate:.2f}%")
                
                # Risk Assessment
                if breakeven_rate > max_rate:
                    st.success(txt['low_risk'])
                elif breakeven_rate > (min_rate + max_rate) / 2:
                    st.warning(txt['medium_risk'])
                else:
                    st.error(txt['high_risk'])
            
            # Visualization
            st.markdown("---")
            st.subheader(txt['sensitivity_chart'])
            
            fig = go.Figure()
            
            # NPV Line
            fig.add_trace(go.Scatter(
                x=discount_rates * 100,
                y=npv_values,
                mode='lines',
                name='NPV',
                line=dict(color='blue', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 100, 255, 0.2)'
            ))
            
            # Zero line
            fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="NPV = 0")
            
            # Current discount rate
            fig.add_vline(x=discount_rate_pct, line_dash="dot", line_color="green", annotation_text=f"Current: {discount_rate_pct}%")
            
            fig.update_layout(
                title=txt['sensitivity_chart'],
                xaxis_title="Discount Rate (%)",
                yaxis_title="NPV (Rp Billion)",
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
