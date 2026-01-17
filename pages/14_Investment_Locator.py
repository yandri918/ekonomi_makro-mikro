import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Investment Location Finder", page_icon="📍", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "📍 Investment Location Finder (MCDA)",
        'subtitle': "Use **Data-Driven Analysis** to find the optimal region for your business expansion.",
        'criteria': "🎯 Assessment Criteria (Set Weights)",
        'w_labor': "Priority: Low Labor Cost (UMR) %",
        'w_land': "Priority: Low Land Price %",
        'w_infra': "Priority: Infrastructure Quality %",
        'w_market': "Priority: Market Size (GDP) %",
        'total_w': "Total Weight (Must be 100%)",
        'candidates': "🏙️ Candidate Regions (Hypothetical Data)",
        'rank_res': "🏆 Optimization Ranking",
        'best_choice': "Best Choice:",
        'score': "Composite Score (0-100)",
        'details': "Analysis Details",
        'labor': "Labor Cost",
        'land': "Land Price",
        'infra': "Infrastructure",
        'gdp': "Regional GDP",
        'insight': "💡 **AI Insight:** Region **{winner}** wins because it offers the best balance for your specific priorities.",
        'insight_labor': "Since you prioritize **Low Wages**, this region's low UMR drove the score up.",
        'insight_infra': "Since you prioritize **Infrastructure**, this region's developed logistics drove the score up.",
        'viz_title': "Weighted Score Breakdown"
    },
    'ID': {
        'title': "📍 Pencari Lokasi Investasi (MCDA)",
        'subtitle': "Gunakan **Analisis Berbasis Data** untuk menemukan wilayah optimal bagi ekspansi bisnis Anda.",
        'criteria': "🎯 Kriteria Penilaian (Atur Bobot)",
        'w_labor': "Prioritas: Upah Murah (UMR) %",
        'w_land': "Prioritas: Harga Tanah Murah %",
        'w_infra': "Prioritas: Kualitas Infrastruktur %",
        'w_market': "Prioritas: Ukuran Pasar (PDB) %",
        'total_w': "Total Bobot (Harus 100%)",
        'candidates': "🏙️ Wilayah Kandidat (Data Hipotetis)",
        'rank_res': "🏆 Peringkat Optimasi",
        'best_choice': "Pilihan Terbaik:",
        'score': "Skor Komposit (0-100)",
        'details': "Detail Analisis",
        'labor': "Biaya Tenaga Kerja",
        'land': "Harga Tanah",
        'infra': "Infrastruktur",
        'gdp': "PDRB Regional",
        'insight': "💡 **Insight AI:** Wilayah **{winner}** menang karena menawarkan keseimbangan terbaik untuk prioritas spesifik Anda.",
        'insight_labor': "Karena Anda memprioritaskan **Upah Murah**, UMR rendah di wilayah ini mendongkrak skor.",
        'insight_infra': "Karena Anda memprioritaskan **Infrastruktur**, logistik maju di wilayah ini mendongkrak skor.",
        'viz_title': "Rincian Skor Terbobot"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

col1, col2 = st.columns([1, 2])

# --- 1. USER WEIGHTS ---
with col1:
    st.subheader(txt['criteria'])
    
    # Sliders for weights
    w_labor = st.slider(txt['w_labor'], 0, 100, 40, 5)
    w_land = st.slider(txt['w_land'], 0, 100, 20, 5)
    w_infra = st.slider(txt['w_infra'], 0, 100, 20, 5)
    w_market = st.slider(txt['w_market'], 0, 100, 20, 5)
    
    total_weight = w_labor + w_land + w_infra + w_market
    
    if total_weight != 100:
        st.warning(f"⚠️ {txt['total_w']}: **{total_weight}%**. Please adjust to 100%.")
    else:
        st.success(f"✅ {txt['total_w']}: **100%**")

# --- 2. DATA GENERATION & LOGIC ---
# Hypothetical Data for Regions
data = {
    'Region': ['Zone A (Industrial)', 'Zone B (Rural)', 'Zone C (Metro)', 'Zone D (Port City)'],
    'UMR (Rp)': [4500000, 2500000, 5200000, 4800000],          # Cost (Lower is better)
    'Land Price (Rp/m2)': [2500000, 500000, 8000000, 5000000], # Cost (Lower is better)
    'Infra Score (0-100)': [85, 40, 95, 90],                   # Benefit (Higher is better)
    'GDP (Trillion Rp)': [300, 50, 800, 400]                   # Benefit (Higher is better)
}
df = pd.DataFrame(data)

with col2:
    st.subheader(txt['candidates'])
    # Make data editable
    df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key='editor_1')

    if total_weight == 100:
        st.divider()
        st.subheader(txt['rank_res'])
        
        # --- MCDA LOGIC (Min-Max Normalization) ---
        # 1. Normalize
        # For Cost (Lower better): (Max - Value) / (Max - Min)
        # For Benefit (Higher better): (Value - Min) / (Max - Min)
        
        df_norm = df.copy()
        
        # UMR (Cost)
        min_u, max_u = df['UMR (Rp)'].min(), df['UMR (Rp)'].max()
        df_norm['Norm_Labor'] = (max_u - df['UMR (Rp)']) / (max_u - min_u)
        
        # Land (Cost)
        min_l, max_l = df['Land Price (Rp/m2)'].min(), df['Land Price (Rp/m2)'].max()
        df_norm['Norm_Land'] = (max_l - df['Land Price (Rp/m2)']) / (max_l - min_l)
        
        # Infra (Benefit)
        min_i, max_i = df['Infra Score (0-100)'].min(), df['Infra Score (0-100)'].max()
        df_norm['Norm_Infra'] = (df['Infra Score (0-100)'] - min_i) / (max_i - min_i)
        
        # GDP (Benefit)
        min_g, max_g = df['GDP (Trillion Rp)'].min(), df['GDP (Trillion Rp)'].max()
        df_norm['Norm_Market'] = (df['GDP (Trillion Rp)'] - min_g) / (max_g - min_g)
        
        # 2. Apply Weights
        df_norm['Score'] = (
            df_norm['Norm_Labor'] * (w_labor/100) +
            df_norm['Norm_Land'] * (w_land/100) +
            df_norm['Norm_Infra'] * (w_infra/100) +
            df_norm['Norm_Market'] * (w_market/100)
        ) * 100
        
        df_norm['Score'] = df_norm['Score'].round(1)
        
        # Sort
        df_sorted = df_norm.sort_values('Score', ascending=False).reset_index(drop=True)
        winner = df_sorted.iloc[0]['Region']
        
        # Display Winner
        st.success(f"### 🥇 {txt['best_choice']} {winner} ({txt['score']}: {df_sorted.iloc[0]['Score']})")
        
        # Explanation
        reason = txt['insight'].format(winner=winner)
        if w_labor > 30 and df_sorted.iloc[0]['Norm_Labor'] > 0.7:
             reason += "\n\n" + txt['insight_labor']
        if w_infra > 30 and df_sorted.iloc[0]['Norm_Infra'] > 0.7:
             reason += "\n\n" + txt['insight_infra']
             
        st.info(reason)
        
        # --- VISUALIZATION ---
        # Stacked Bar Chart of Contributions
        # Breakdown score contribution by category
        
        viz_data = []
        for index, row in df_norm.iterrows():
            viz_data.append({'Region': row['Region'], 'Type': txt['labor'], 'Value': row['Norm_Labor'] * w_labor})
            viz_data.append({'Region': row['Region'], 'Type': txt['land'], 'Value': row['Norm_Land'] * w_land})
            viz_data.append({'Region': row['Region'], 'Type': txt['infra'], 'Value': row['Norm_Infra'] * w_infra})
            viz_data.append({'Region': row['Region'], 'Type': txt['gdp'], 'Value': row['Norm_Market'] * w_market})
            
        df_viz = pd.DataFrame(viz_data)
        
        chart = alt.Chart(df_viz).mark_bar().encode(
            x=alt.X('Region', sort='-y'),
            y=alt.Y('Value', title='Weighted Score Contribution'),
            color=alt.Color('Type', scale=alt.Scale(scheme='category10')),
            tooltip=['Region', 'Type', alt.Tooltip('Value', format='.1f')]
        ).properties(title=txt['viz_title'], height=400)
        
        st.altair_chart(chart, use_container_width=True)
