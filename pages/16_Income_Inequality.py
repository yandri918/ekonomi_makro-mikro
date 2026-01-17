import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Income Inequality", page_icon="📊", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "📊 Income Inequality Analyzer",
        'subtitle': "Measure inequality using **Gini Coefficient** and **Lorenz Curve** for poverty analysis.",
        'input_method': "Select Input Method:",
        'manual': "Manual Income Data",
        'quintile': "Quintile Distribution",
        'manual_label': "📝 Enter Income Data (Editable)",
        'manual_help': "Enter individual or household incomes. Each row represents one person/household.",
        'add_row': "➕ Add Row",
        'quintile_label': "📊 Income Share by Quintile (%)",
        'quintile_help': "Enter the percentage of total income owned by each 20% population group.",
        'q1': "Bottom 20% (Poorest)",
        'q2': "Second 20%",
        'q3': "Middle 20%",
        'q4': "Fourth 20%",
        'q5': "Top 20% (Richest)",
        'total_check': "Total must equal 100%",
        'calc_btn': "📈 Calculate Inequality",
        'results': "📋 Inequality Analysis Results",
        'gini': "Gini Coefficient",
        'gini_interpretation': "Interpretation",
        'gini_low': "Low Inequality (Relatively Equal)",
        'gini_medium': "Medium Inequality",
        'gini_high': "High Inequality",
        'gini_very_high': "Very High Inequality (Severe)",
        'lorenz_title': "Lorenz Curve",
        'lorenz_subtitle': "Cumulative Income Distribution",
        'pop_pct': "Cumulative % of Population",
        'income_pct': "Cumulative % of Income",
        'line_equality': "Line of Equality",
        'actual_distribution': "Actual Distribution",
        'additional_metrics': "📊 Additional Inequality Metrics",
        'palma_ratio': "Palma Ratio",
        'palma_help': "Top 10% income / Bottom 40% income. Higher = More inequality.",
        'ratio_2020': "20:20 Ratio",
        'ratio_help': "Top 20% income / Bottom 20% income.",
        'insights': "💡 Key Insights",
        'insight_bottom': "The **bottom {pct}%** of the population owns only **{income:.1f}%** of total income.",
        'insight_top': "The **top {pct}%** owns **{income:.1f}%** of total income.",
        'benchmark': "🌍 Global Benchmark Comparison",
        'benchmark_text': "Indonesia (2023): ~0.38 | ASEAN Average: ~0.40 | Nordic Countries: ~0.25-0.28",
        # Story
        'story_title': "📚 Story & Use Cases: Income Inequality Analyzer",
        'story_meaning': "**What is this?**\nThis module measures income inequality using the Gini Coefficient (0 = perfect equality, 1 = perfect inequality) and visualizes it with the Lorenz Curve.",
        'story_insight': "**Key Insight:**\nHigh inequality (Gini > 0.40) indicates wealth concentration. This can lead to social instability and reduced economic mobility.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **BPS/Kemenkeu:** To monitor poverty trends and evaluate the impact of social programs (PKH, BLT) on inequality.",
        'use_corp': "🏢 **CSR Departments:** To identify target regions for poverty alleviation programs based on inequality data.",
        'use_analyst': "📈 **Development Economists:** To research the relationship between inequality and economic growth."
    },
    'ID': {
        'title': "📊 Analisis Ketimpangan Pendapatan",
        'subtitle': "Ukur ketimpangan menggunakan **Koefisien Gini** dan **Kurva Lorenz** untuk analisis kemiskinan.",
        'input_method': "Pilih Metode Input:",
        'manual': "Data Pendapatan Manual",
        'quintile': "Distribusi Kuintil",
        'manual_label': "📝 Masukkan Data Pendapatan (Dapat Diedit)",
        'manual_help': "Masukkan pendapatan individu atau rumah tangga. Setiap baris mewakili satu orang/rumah tangga.",
        'add_row': "➕ Tambah Baris",
        'quintile_label': "📊 Pangsa Pendapatan per Kuintil (%)",
        'quintile_help': "Masukkan persentase total pendapatan yang dimiliki setiap kelompok 20% populasi.",
        'q1': "20% Terbawah (Termiskin)",
        'q2': "20% Kedua",
        'q3': "20% Tengah",
        'q4': "20% Keempat",
        'q5': "20% Teratas (Terkaya)",
        'total_check': "Total harus 100%",
        'calc_btn': "📈 Hitung Ketimpangan",
        'results': "📋 Hasil Analisis Ketimpangan",
        'gini': "Koefisien Gini",
        'gini_interpretation': "Interpretasi",
        'gini_low': "Ketimpangan Rendah (Relatif Merata)",
        'gini_medium': "Ketimpangan Sedang",
        'gini_high': "Ketimpangan Tinggi",
        'gini_very_high': "Ketimpangan Sangat Tinggi (Parah)",
        'lorenz_title': "Kurva Lorenz",
        'lorenz_subtitle': "Distribusi Pendapatan Kumulatif",
        'pop_pct': "% Kumulatif Populasi",
        'income_pct': "% Kumulatif Pendapatan",
        'line_equality': "Garis Kesetaraan",
        'actual_distribution': "Distribusi Aktual",
        'additional_metrics': "📊 Metrik Ketimpangan Tambahan",
        'palma_ratio': "Rasio Palma",
        'palma_help': "Pendapatan 10% Teratas / 40% Terbawah. Lebih tinggi = Lebih timpang.",
        'ratio_2020': "Rasio 20:20",
        'ratio_help': "Pendapatan 20% Teratas / 20% Terbawah.",
        'insights': "💡 Wawasan Utama",
        'insight_bottom': "**{pct}% terbawah** populasi hanya memiliki **{income:.1f}%** dari total pendapatan.",
        'insight_top': "**{pct}% teratas** memiliki **{income:.1f}%** dari total pendapatan.",
        'benchmark': "🌍 Perbandingan Benchmark Global",
        'benchmark_text': "Indonesia (2023): ~0.38 | Rata-rata ASEAN: ~0.40 | Negara Nordik: ~0.25-0.28",
        # Story
        'story_title': "📚 Cerita & Kasus Penggunaan: Analisis Ketimpangan",
        'story_meaning': "**Apa artinya ini?**\nModul ini mengukur ketimpangan pendapatan menggunakan Koefisien Gini (0 = kesetaraan sempurna, 1 = ketimpangan sempurna) dan memvisualisasikannya dengan Kurva Lorenz.",
        'story_insight': "**Wawasan Utama:**\nKetimpangan tinggi (Gini > 0.40) menunjukkan konsentrasi kekayaan. Ini dapat menyebabkan ketidakstabilan sosial dan berkurangnya mobilitas ekonomi.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **BPS/Kemenkeu:** Untuk memantau tren kemiskinan dan mengevaluasi dampak program sosial (PKH, BLT) terhadap ketimpangan.",
        'use_corp': "🏢 **Departemen CSR:** Untuk mengidentifikasi wilayah target program pengentasan kemiskinan berdasarkan data ketimpangan.",
        'use_analyst': "📈 **Ekonom Pembangunan:** Untuk meneliti hubungan antara ketimpangan dan pertumbuhan ekonomi."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- INPUT METHOD SELECTION ---
input_method = st.radio(txt['input_method'], [txt['manual'], txt['quintile']], horizontal=True)

col1, col2 = st.columns([1, 2])

# Initialize variables
gini = 0
lorenz_data = None
incomes = []

# ========== MANUAL INPUT ==========
if input_method == txt['manual']:
    with col1:
        st.subheader(txt['manual_label'])
        st.caption(txt['manual_help'])
        
        # Default data
        if 'income_data' not in st.session_state:
            st.session_state['income_data'] = pd.DataFrame({
                'Income (Rp Million)': [5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
            })
        
        # Editable dataframe
        edited_df = st.data_editor(
            st.session_state['income_data'],
            num_rows="dynamic",
            use_container_width=True,
            key='income_editor'
        )
        
        st.session_state['income_data'] = edited_df
        
        if st.button(txt['calc_btn'], type='primary'):
            incomes = edited_df['Income (Rp Million)'].dropna().values
            incomes = np.sort(incomes)  # Sort ascending
            
            if len(incomes) < 2:
                st.error("Please enter at least 2 income values.")
                st.stop()
            
            # Calculate Gini Coefficient
            n = len(incomes)
            cumsum_income = np.cumsum(incomes)
            total_income = cumsum_income[-1]
            
            # Gini formula: G = (2 * Σ(i * y_i)) / (n * Σy_i) - (n+1)/n
            gini = (2 * np.sum((np.arange(1, n+1) * incomes))) / (n * total_income) - (n + 1) / n
            
            # Lorenz Curve Data
            cumsum_pct_income = cumsum_income / total_income * 100
            cumsum_pct_pop = np.arange(1, n+1) / n * 100
            
            lorenz_data = pd.DataFrame({
                'Population %': np.concatenate([[0], cumsum_pct_pop]),
                'Income %': np.concatenate([[0], cumsum_pct_income])
            })

# ========== QUINTILE INPUT ==========
else:
    with col1:
        st.subheader(txt['quintile_label'])
        st.caption(txt['quintile_help'])
        
        q1 = st.number_input(txt['q1'], value=7.0, step=0.5, min_value=0.0, max_value=100.0)
        q2 = st.number_input(txt['q2'], value=11.0, step=0.5, min_value=0.0, max_value=100.0)
        q3 = st.number_input(txt['q3'], value=15.0, step=0.5, min_value=0.0, max_value=100.0)
        q4 = st.number_input(txt['q4'], value=22.0, step=0.5, min_value=0.0, max_value=100.0)
        q5 = st.number_input(txt['q5'], value=45.0, step=0.5, min_value=0.0, max_value=100.0)
        
        total = q1 + q2 + q3 + q4 + q5
        
        if abs(total - 100) > 0.1:
            st.warning(f"{txt['total_check']}: {total:.1f}%")
        else:
            st.success(f"✅ Total: {total:.1f}%")
        
        if st.button(txt['calc_btn'], type='primary'):
            # Convert quintile shares to Lorenz Curve
            quintiles = np.array([q1, q2, q3, q4, q5])
            cumsum_income_pct = np.cumsum(quintiles)
            cumsum_pop_pct = np.array([20, 40, 60, 80, 100])
            
            lorenz_data = pd.DataFrame({
                'Population %': np.concatenate([[0], cumsum_pop_pct]),
                'Income %': np.concatenate([[0], cumsum_income_pct])
            })
            
            # Calculate Gini from Lorenz Curve (Trapezoidal Rule)
            # Area under Lorenz = Σ (0.5 * (y_i + y_{i+1}) * Δx)
            area_lorenz = 0
            for i in range(len(cumsum_pop_pct)):
                if i == 0:
                    y_prev = 0
                    x_prev = 0
                else:
                    y_prev = cumsum_income_pct[i-1]
                    x_prev = cumsum_pop_pct[i-1]
                
                y_curr = cumsum_income_pct[i]
                x_curr = cumsum_pop_pct[i]
                
                area_lorenz += 0.5 * (y_prev + y_curr) * (x_curr - x_prev)
            
            # Area under line of equality = 0.5 * 100 * 100 = 5000
            area_equality = 5000
            gini = (area_equality - area_lorenz) / area_equality

# ========== RESULTS DISPLAY ==========
with col2:
    if lorenz_data is not None:
        st.subheader(txt['results'])
        
        # Gini Coefficient
        m1, m2 = st.columns(2)
        m1.metric(txt['gini'], f"{gini:.3f}")
        
        # Interpretation
        if gini < 0.30:
            interpretation = txt['gini_low']
            color = "🟢"
        elif gini < 0.40:
            interpretation = txt['gini_medium']
            color = "🟡"
        elif gini < 0.50:
            interpretation = txt['gini_high']
            color = "🟠"
        else:
            interpretation = txt['gini_very_high']
            color = "🔴"
        
        m2.metric(txt['gini_interpretation'], f"{color} {interpretation}")
        
        st.info(txt['benchmark'])
        st.caption(txt['benchmark_text'])
        
        # Lorenz Curve
        st.markdown("---")
        st.subheader(txt['lorenz_title'])
        
        fig = go.Figure()
        
        # Line of Equality
        fig.add_trace(go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode='lines',
            name=txt['line_equality'],
            line=dict(color='gray', dash='dash')
        ))
        
        # Actual Lorenz Curve
        fig.add_trace(go.Scatter(
            x=lorenz_data['Population %'],
            y=lorenz_data['Income %'],
            mode='lines+markers',
            name=txt['actual_distribution'],
            line=dict(color='blue', width=3),
            fill='tonexty',
            fillcolor='rgba(0, 100, 255, 0.2)'
        ))
        
        fig.update_layout(
            title=txt['lorenz_subtitle'],
            xaxis_title=txt['pop_pct'],
            yaxis_title=txt['income_pct'],
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional Metrics
        st.markdown("---")
        st.subheader(txt['additional_metrics'])
        
        if input_method == txt['quintile']:
            # Palma Ratio (Top 10% / Bottom 40%)
            # Approximate: Top 10% ≈ Half of Q5, Bottom 40% = Q1 + Q2
            top_10_approx = q5 / 2
            bottom_40 = q1 + q2
            palma = top_10_approx / bottom_40 if bottom_40 > 0 else 0
            
            # 20:20 Ratio
            ratio_2020 = q5 / q1 if q1 > 0 else 0
            
            a1, a2 = st.columns(2)
            a1.metric(txt['palma_ratio'], f"{palma:.2f}", help=txt['palma_help'])
            a2.metric(txt['ratio_2020'], f"{ratio_2020:.2f}", help=txt['ratio_help'])
        
        # Insights
        st.markdown("---")
        st.subheader(txt['insights'])
        
        if input_method == txt['quintile']:
            st.write(txt['insight_bottom'].format(pct=40, income=q1+q2))
            st.write(txt['insight_top'].format(pct=20, income=q5))
        else:
            # For manual input
            n = len(incomes)
            bottom_40_idx = int(n * 0.4)
            top_20_idx = int(n * 0.8)
            
            total_income = np.sum(incomes)
            bottom_40_income = np.sum(incomes[:bottom_40_idx]) / total_income * 100
            top_20_income = np.sum(incomes[top_20_idx:]) / total_income * 100
            
            st.write(txt['insight_bottom'].format(pct=40, income=bottom_40_income))
            st.write(txt['insight_top'].format(pct=20, income=top_20_income))

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
