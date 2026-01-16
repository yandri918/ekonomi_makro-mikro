import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

st.set_page_config(page_title="Production Optimization", page_icon="🏭", layout="wide")

# Check for language in session state
if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
    
lang = st.session_state['language']

# Translations for this page
T = {
    'EN': {
        'title': "🏭 Production Optimization: Isoquant & Isocost",
        'intro': "Visualize how firms minimize costs by choosing the optimal combination of **Capital (K)** and **Labor (L)**.",
        'theory': "**Theory**: The optimal point is where the slope of the Isoquant (MRTS) equals the slope of the Isocost line ($w/r$).",
        'params': "Production Parameters (Cobb-Douglas)",
        'wage': "Wage Rate (w) - Rp",
        'rent': "Rental Rate (r) - Rp",
        'target_q': "Target Quantity (Q*)",
        'alpha': "Output Elast. Capital (α)",
        'beta': "Output Elast. Labor (β)",
        'cost_min_res': "💰 Cost Minimization Results",
        'opt_k': "Optimal Capital (K*)",
        'opt_l': "Optimal Labor (L*)",
        'min_c': "Minimum Cost (Rp)",
        'viz_title': "Isoquant & Isocost Visualization",
        'isoquant': "Isoquant (Q*)",
        'isocost': "Isocost (Min Cost)",
        'expansion': "Expansion Path"
    },
    'ID': {
        'title': "🏭 Optimasi Produksi: Isokuan & Isocost",
        'intro': "Visualisasikan bagaimana perusahaan meminimalkan biaya dengan memilih kombinasi optimal **Modal (K)** dan **Tenaga Kerja (L)**.",
        'theory': "**Teori**: Titik optimal adalah di mana kemiringan Isokuan (MRTS) sama dengan kemiringan garis Isocost ($w/r$).",
        'params': "Parameter Produksi (Cobb-Douglas)",
        'wage': "Upah Tenaga Kerja (w) - Rp",
        'rent': "Harga Sewa Modal (r) - Rp",
        'target_q': "Target Produksi (Q*)",
        'alpha': "Elast. Output Modal (α)",
        'beta': "Elast. Output TK (β)",
        'cost_min_res': "💰 Hasil Minimisasi Biaya",
        'opt_k': "Modal Optimal (K*)",
        'opt_l': "Tenaga Kerja Optimal (L*)",
        'min_c': "Biaya Minimum (Rp)",
        'viz_title': "Visualisasi Isokuan & Isocost",
        'isoquant': "Isokuan (Q*)",
        'isocost': "Isocost (Biaya Min)",
        'expansion': "Jalur Ekspansi"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['intro'])

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"⚙️ {txt['params']}")
    st.markdown("$Q(K, L) = A K^\\alpha L^\\beta$")
    
    A = 10 # TFP Constant
    alpha = st.slider(txt['alpha'], 0.1, 0.9, 0.5, 0.1)
    beta = st.slider(txt['beta'], 0.1, 0.9, 0.5, 0.1)
    
    st.markdown("---")
    w = st.number_input(txt['wage'], value=20000.0, step=1000.0)
    r = st.number_input(txt['rent'], value=30000.0, step=1000.0)
    Q_target = st.number_input(txt['target_q'], value=100.0, step=10.0)

with col2:
    # LAGRANGE OPTIMIZATION
    # Minimize C = wL + rK subject to A K^alpha L^beta = Q
    # Solution for Cobb Douglas:
    # K* = (alpha/beta) * (w/r) * L*
    # Substitute back into Q eq...
    # Analytical solution for Cost Minimization:
    # L* = (Q/A) * ( (r*beta)/(w*alpha) ) ^ alpha  ... raised to 1/(alpha+beta)
    # Actually:
    # K/L = (alpha/beta) * (w/r) => K = L * (alpha w)/(beta r)
    # Q = A * (L * alpha w / beta r)^alpha * L^beta
    # Q = A * L^(alpha+beta) * (alpha w / beta r)^alpha
    # L^(alpha+beta) = Q / [A * (alpha w / beta r)^alpha]
    # L* = (Q / (A * ((alpha * w) / (beta * r))**alpha)) ** (1 / (alpha + beta))
    
    ratio = (alpha * w) / (beta * r)
    L_opt = (Q_target / (A * (ratio**alpha))) ** (1 / (alpha + beta))
    K_opt = L_opt * ratio
    
    Min_Cost = w * L_opt + r * K_opt
    
    # Visualization Data
    # 1. Isoquant Curve: K = (Q / (A * L^beta)) ^ (1/alpha)
    L_range = np.linspace(L_opt * 0.2, L_opt * 2.5, 100)
    K_isoquant = (Q_target / (A * L_range**beta)) ** (1/alpha)
    
    # 2. Isocost Line: C = wL + rK => K = (C - wL) / r
    K_isocost = (Min_Cost - w * L_range) / r
    
    # Create DF
    df_iso = pd.DataFrame({'Labor': L_range, 'Capital': K_isoquant, 'Type': txt['isoquant']})
    df_cost = pd.DataFrame({'Labor': L_range, 'Capital': K_isocost, 'Type': txt['isocost']})
    
    # Filter negative K for Isocost
    df_cost = df_cost[df_cost['Capital'] >= 0]
    
    df_chart = pd.concat([df_iso, df_cost])
    
    # Altair Plot
    base = alt.Chart(df_chart).mark_line().encode(
        x=alt.X('Labor', title=txt['opt_l']),
        y=alt.Y('Capital', title=txt['opt_k']),
        color=alt.Color('Type', scale=alt.Scale(domain=[txt['isoquant'], txt['isocost']], range=['blue', 'red']))
    )
    
    # Point
    point = alt.Chart(pd.DataFrame({'Labor': [L_opt], 'Capital': [K_opt]})).mark_point(
        size=300, fill='black', color='black'
    ).encode(
        x='Labor', y='Capital',
        tooltip=[alt.Tooltip('Labor', format=',.2f'), alt.Tooltip('Capital', format=',.2f')]
    )
    
    st.altair_chart((base + point).interactive(), use_container_width=True)
    
    # Results
    st.subheader(txt['cost_min_res'])
    r1, r2, r3 = st.columns(3)
    r1.metric(txt['opt_l'], f"{L_opt:.2f}")
    r2.metric(txt['opt_k'], f"{K_opt:.2f}")
    r3.metric(txt['min_c'], f"Rp {Min_Cost:,.2f}")
    
    st.info(f"{txt['theory']} \n\n MRTS = $\\frac{{MP_L}}{{MP_K}} = \\frac{{w}}{{r}}$")
