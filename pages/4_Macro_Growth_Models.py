import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Growth Models", page_icon="📈", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "📈 Solow Growth Model Simulation",
        'subtitle': "Explore how saving, population growth, and technology affect long-run economic growth.",
        'params': "⚙️ Model Parameters",
        'saving': "Savings Rate (s)",
        'capital_share': "Capital Share (α)",
        'depreciation': "Depreciation Rate (δ)",
        'pop_growth': "Population Growth (n)",
        'tech_growth': "Tech Growth (g)",
        'init_k': "Initial Capital per Worker (k0)",
        'periods': "Time Periods",
        'theory': "**Theory:**",
        'model_eq': "The change in capital per effective worker is given by:",
        'steady_state': "At **Steady State** ($\Delta k = 0$):",
        'results': "🔍 Simulation Results",
        'ss_k': "Steady State Capital ($k^*$)",
        'ss_y': "Steady State Output ($y^*$)",
        'final_k': "Final Capital ($k_T$)",
        'final_y': "Final Output ($y_T$)",
        'dynamics': "Dynamics over Time",
        'var': "Variable",
        'cap': "Capital (k)",
        'out': "Output (y)",
        'cons': "Consumption (c)",
        'inv': "Investment (i)"
    },
    'ID': {
        'title': "📈 Simulasi Model Pertumbuhan Solow",
        'subtitle': "Jelajahi bagaimana tabungan, pertumbuhan populasi, dan teknologi mempengaruhi pertumbuhan ekonomi jangka panjang.",
        'params': "⚙️ Parameter Model",
        'saving': "Tingkat Tabungan (s)",
        'capital_share': "Pangsa Modal (α)",
        'depreciation': "Tingkat Depresiasi (δ)",
        'pop_growth': "Pertumbuhan Populasi (n)",
        'tech_growth': "Pertumbuhan Teknologi (g)",
        'init_k': "Modal Awal per Pekerja (k0)",
        'periods': "Periode Waktu",
        'theory': "**Teori:**",
        'model_eq': "Perubahan modal per pekerja efektif diberikan oleh:",
        'steady_state': "Pada **Steady State** ($\Delta k = 0$):",
        'results': "🔍 Hasil Simulasi",
        'ss_k': "Modal Steady State ($k^*$)",
        'ss_y': "Output Steady State ($y^*$)",
        'final_k': "Modal Akhir ($k_T$)",
        'final_y': "Output Akhir ($y_T$)",
        'dynamics': "Dinamika Seiring Waktu",
        'var': "Variabel",
        'cap': "Modal (k)",
        'out': "Output (y)",
        'cons': "Konsumsi (c)",
        'inv': "Investasi (i)"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### {txt['params']}")
    s = st.slider(txt['saving'], 0.0, 0.5, 0.25)
    alpha = st.slider(txt['capital_share'], 0.1, 0.9, 0.33)
    delta = st.slider(txt['depreciation'], 0.0, 0.2, 0.1)
    n = st.slider(txt['pop_growth'], 0.0, 0.1, 0.02)
    g = st.slider(txt['tech_growth'], 0.0, 0.1, 0.02)
    
    st.markdown("---")
    k0 = st.number_input(txt['init_k'], value=1.0)
    periods = st.slider(txt['periods'], 20, 100, 50)
    
    st.info(f"""
    {txt['theory']}
    {txt['model_eq']}
    $$ \Delta k = s y - (n + g + \delta) k $$
    
    {txt['steady_state']}
    $$ k^* = \left( \\frac{{s}}{{n + g + \delta}} \\right)^{{\\frac{{1}}{{1 - \\alpha}}}} $$
    """)

with col2:
    # Simulation
    k = np.zeros(periods)
    y = np.zeros(periods)
    c = np.zeros(periods)
    i = np.zeros(periods)
    
    k[0] = k0
    y[0] = k[0]**alpha
    c[0] = (1-s)*y[0]
    i[0] = s*y[0]
    
    for t in range(1, periods):
        # k_next = k_current + s*y - (n+g+delta)*k
        change = s*y[t-1] - (n + g + delta)*k[t-1]
        k[t] = k[t-1] + change
        y[t] = k[t]**alpha
        c[t] = (1-s)*y[t]
        i[t] = s*y[t]
        
    # Steady State Calculation
    # s k^a = (n+g+d)k => s k^a / k = n+g+d => s k^(a-1) = ...
    # k^(a-1) = (n+g+d)/s => k^(1-a) = s/(n+g+d)
    denom = (n + g + delta)
    if denom == 0:
        k_ss = 0
    else:
        k_ss = (s / denom) ** (1 / (1 - alpha))
    y_ss = k_ss**alpha
    
    # Visualization
    time = np.arange(periods)
    df = pd.DataFrame({
        'Time': time,
        txt['cap']: k,
        txt['out']: y,
        txt['cons']: c,
        txt['inv']: i
    })
    
    df_melted = df.melt('Time', var_name='Variable', value_name='Value')
    
    st.markdown(f"### {txt['dynamics']}")
    chart = alt.Chart(df_melted).mark_line().encode(
        x='Time',
        y='Value',
        color=alt.Color('Variable', title=txt['var']),
        tooltip=['Time', 'Variable', alt.Tooltip('Value', format='.2f')]
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    st.markdown(f"### {txt['results']}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(txt['ss_k'], f"{k_ss:.2f}")
    c2.metric(txt['ss_y'], f"{y_ss:.2f}")
    c3.metric(txt['final_k'], f"{k[-1]:.2f}")
    c4.metric(txt['final_y'], f"{y[-1]:.2f}")

