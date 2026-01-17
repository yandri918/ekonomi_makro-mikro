import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Production Optimization", page_icon="🏭", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🏭 Managerial Production Optimization",
        'subtitle': "Minimize Cost by choosing the optimal mix of **Capital (K)** and **Labor (L)**.",
        'theory': "**Theory**: The optimal point is where the slope of the Isoquant (MRTS) equals the slope of the Isocost line ($w/r$).",
        'params': "Production Parameters (Cobb-Douglas)",
        'wage': "Wage Rate (w) - Rp/Hour",
        'rent': "Rental Rate (r) - Rp/Hour",
        'target_q': "Target Quantity (Units)",
        'alpha': "Output Elast. Capital (α)",
        'beta': "Output Elast. Labor (β)",
        'cost_min_res': "💰 Cost Minimization Strategy",
        'opt_k': "Optimal Machines (K*)",
        'opt_l': "Optimal Workers (L*)",
        'min_c': "Minimum Total Cost",
        'viz_title': "Isoquant (Output) & Isocost (Budget) Map",
        'isoquant': "Isoquant (Target Q)",
        'isocost': "Isocost (Min Cost)",
        'managerial': "📋 Managerial Insights",
        'insight_1': "To produce **{q} units** most efficiently, you should hire **{l:.1f} workers** and use **{k:.1f} machine hours**.",
        'insight_labor': "💡 **Labor Strategy**: Since Labor is relatively cheaper/more productive, the model suggests a **Labor-Intensive** approach.",
        'insight_capital': "💡 **Capital Strategy**: Since Capital is relatively cheaper/more productive, the model suggests a **Capital-Intensive** approach.",
        'story_title': "📚 Story & Use Cases: Production Optimization",
        'story_meaning': "**What is this?**\nIt calculates the cheapest way to produce a target quantity (Cost Minimization) using the optimal mix of Labor and Machines.",
        'story_insight': "**Key Insight:**\nIf wages rise (Labor gets expensive), smart managers shift to machines (Capital). Use this to simulate 'Automation' decisions.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Industry Ministry:** To understand if rising Minimum Wages will trigger mass layoffs (Automation).",
        'use_corp': "🏢 **Factory Managers:** To balance the budget. 'Should we hire 100 more workers or buy 1 CNC Machine?'",
        'use_analyst': "📈 **Efficiency Consultants:** To optimize clients' OPEX structures."
    },
    'ID': {
        'title': "🏭 Optimasi Produksi Manajerial",
        'subtitle': "Minimalkan Biaya dengan memilih kombinasi optimal **Modal (K)** dan **Tenaga Kerja (L)**.",
        'theory': "**Teori**: Titik optimal adalah di mana kemiringan Isokuan (MRTS) sama dengan kemiringan garis Isocost ($w/r$).",
        'params': "Parameter Produksi (Cobb-Douglas)",
        'wage': "Upah Tenaga Kerja (w) - Rp/Jam",
        'rent': "Harga Sewa Mesin (r) - Rp/Jam",
        'target_q': "Target Produksi (Unit)",
        'alpha': "Elast. Output Modal (α)",
        'beta': "Elast. Output TK (β)",
        'cost_min_res': "💰 Strategi Minimisasi Biaya",
        'opt_k': "Mesin Optimal (K*)",
        'opt_l': "Pekerja Optimal (L*)",
        'min_c': "Total Biaya Minimum",
        'viz_title': "Peta Isokuan (Output) & Isocost (Anggaran)",
        'isoquant': "Isokuan (Target Q)",
        'isocost': "Isocost (Biaya Min)",
        'managerial': "📋 Insight Manajerial",
        'insight_1': "Untuk memproduksi **{q} unit** termurah, Anda harus mempekerjakan **{l:.1f} orang** dan menggunakan **{k:.1f} jam mesin**.",
        'insight_labor': "💡 **Strategi Padat Karya**: Karena Tenaga Kerja relatif lebih murah/produktif, model menyarankan pendekatan **Padat Karya**.",
        'insight_capital': "💡 **Strategi Padat Modal**: Karena Modal relatif lebih murah/produktif, model menyarankan pendekatan **Padat Modal**.",
        'story_title': "📚 Cerita & Kasus Penggunaan: Optimasi Produksi",
        'story_meaning': "**Apa artinya ini?**\nMenghitung cara termurah untuk memproduksi target output (Minimisasi Biaya) dengan kombinasi optimal Buruh dan Mesin.",
        'story_insight': "**Wawasan Utama:**\nJika upah naik (Buruh mahal), manajer cerdas beralih ke mesin (Modal). Gunakan ini untuk mensimulasikan keputusan 'Otomasi'.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Kemenperin:** Untuk memahami apakah kenaikan UMR akan memicu PHK massal (Otomasi Pabrik).",
        'use_corp': "🏢 **Manajer Pabrik:** Untuk menyeimbangkan anggaran. 'Lebih baik rekrut 100 buruh atau beli 1 Mesin CNC?'",
        'use_analyst': "📈 **Konsultan Efisiensi:** Untuk mengoptimalkan struktur biaya operasional (OPEX) klien."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"⚙️ {txt['params']}")
    st.markdown("$Q(K, L) = A K^\\alpha L^\\beta$")
    
    A = 10 # TFP Constant
    alpha = st.slider(txt['alpha'], 0.1, 0.9, 0.4, 0.1, help="High Alpha = Capital is very productive")
    beta = st.slider(txt['beta'], 0.1, 0.9, 0.6, 0.1, help="High Beta = Labor is very productive")
    
    st.markdown("---")
    w = st.number_input(txt['wage'], value=50000.0, step=5000.0)
    r = st.number_input(txt['rent'], value=100000.0, step=5000.0)
    Q_target = st.number_input(txt['target_q'], value=1000.0, step=100.0)

with col2:
    # LAGRANGE OPTIMIZATION
    # Minimize C = wL + rK subject to A K^alpha L^beta = Q
    
    # Formula for Optimal L and K:
    # Ratio K/L = (alpha * w) / (beta * r)
    ratio_KL = (alpha * w) / (beta * r)
    
    # Derived from Algebra:
    # L_opt = (Q / (A * ratio_KL^alpha)) ^ (1/(alpha+beta))
    L_opt = (Q_target / (A * (ratio_KL**alpha))) ** (1 / (alpha + beta))
    K_opt = L_opt * ratio_KL
    
    Min_Cost = w * L_opt + r * K_opt
    
    # Visualization Data
    # 1. Isoquant Curve (Fixed Q): K = (Q / (A * L^beta)) ^ (1/alpha)
    L_vals = np.linspace(L_opt * 0.3, L_opt * 2.0, 100)
    K_iso = (Q_target / (A * L_vals**beta)) ** (1/alpha)
    
    # 2. Isocost Line (Fixed Cost): K = (C - wL) / r
    K_cost = (Min_Cost - w * L_vals) / r
    
    # Dataframes
    df_iso = pd.DataFrame({'Labor': L_vals, 'Capital': K_iso, 'Label': txt['isoquant']})
    df_ln = pd.DataFrame({'Labor': L_vals, 'Capital': K_cost, 'Label': txt['isocost']})
    df_ln = df_ln[df_ln['Capital'] >= 0] # Remove negative capital
    
    df_plot = pd.concat([df_iso, df_ln])
    
    # Charts
    chart_lines = alt.Chart(df_plot).mark_line().encode(
        x=alt.X('Labor', title=txt['opt_l']),
        y=alt.Y('Capital', title=txt['opt_k']),
        color=alt.Color('Label', scale=alt.Scale(domain=[txt['isoquant'], txt['isocost']], range=['blue', 'red'])),
        tooltip=['Labor', 'Capital', 'Label']
    ).properties(title=txt['viz_title'], height=400)
    
    # Tangency Point
    chart_point = alt.Chart(pd.DataFrame({'L': [L_opt], 'K': [K_opt]})).mark_point(size=200, fill='black', color='black').encode(
        x='L', y='K', tooltip=[alt.Tooltip('L', format='.1f'), alt.Tooltip('K', format='.1f')]
    )
    
    text_point = chart_point.mark_text(dy=-15, text=f"({L_opt:.1f}, {K_opt:.1f})").encode()
    
    st.altair_chart((chart_lines + chart_point + text_point).interactive(), use_container_width=True)
    
    # --- MANAGERIAL RESULTS ---
    st.divider()
    st.subheader(txt['cost_min_res'])
    
    c1, c2, c3 = st.columns(3)
    c1.metric(txt['opt_l'], f"{L_opt:.1f}")
    c2.metric(txt['opt_k'], f"{K_opt:.1f}")
    c3.metric(txt['min_c'], f"Rp {Min_Cost:,.0f}")
    
    st.info(txt['managerial'])
    st.write(txt['insight_1'].format(q=Q_target, l=L_opt, k=K_opt))
    
    # Simple Heuristic for insight
    if L_opt > K_opt:
        st.success(txt['insight_labor'])
    else:
        st.warning(txt['insight_capital'])

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
