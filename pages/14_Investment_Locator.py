import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
        'w_tax': "Priority: Low Tax Rate %",
        'w_education': "Priority: Skilled Workforce (Education) %",
        'w_logistics': "Priority: Logistics Performance %",
        'w_poverty': "Priority: Low Poverty Rate %",
        'total_w': "Total Weight (Must be 100%)",
        'candidates': "🏙️ Candidate Regions (Edit Data)",
        'rank_res': "🏆 Optimization Ranking",
        'best_choice': "Best Choice:",
        'score': "Composite Score (0-100)",
        'details': "Analysis Details",
        'labor': "Labor Cost",
        'land': "Land Price",
        'infra': "Infrastructure",
        'gdp': "Regional GDP",
        'tax': "Tax Rate",
        'education': "Education Level",
        'logistics': "Logistics",
        'poverty': "Poverty Rate",
        'insight': "💡 **AI Insight:** Region **{winner}** wins because it offers the best balance for your specific priorities.",
        'insight_labor': "Since you prioritize **Low Wages**, this region's low UMR drove the score up.",
        'insight_infra': "Since you prioritize **Infrastructure**, this region's developed logistics drove the score up.",
        'insight_education': "Since you prioritize **Skilled Workforce**, this region's high education level is a major advantage.",
        'viz_title': "Weighted Score Breakdown by Region",
        'story_title': "📚 Story & Use Cases: Investment Locator",
        'story_meaning': "**What is this?**\nA Decision Support System (MCDA) that ranks locations based on your specific business priorities using 8 economic indicators.",
        'story_insight': "**Key Insight:**\nThere is no 'Best Place' for everyone. A Garment factory needs cheap labor (Central Java), while a Tech Firm needs infrastructure + skilled workforce (Jakarta). Weights matter!",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Investment Board (BKPM):** To simulate how improving infrastructure could boost their region's attractiveness rating.",
        'use_corp': "🏢 **Expansion Managers:** To scientifically choose the next factory location using data, not just gut feeling.",
        'use_analyst': "📈 **Regional Economists:** To benchmark competitiveness between provinces."
    },
    'ID': {
        'title': "📍 Pencari Lokasi Investasi (MCDA)",
        'subtitle': "Gunakan **Analisis Berbasis Data** untuk menemukan wilayah optimal bagi ekspansi bisnis Anda.",
        'criteria': "🎯 Kriteria Penilaian (Atur Bobot)",
        'w_labor': "Prioritas: Upah Murah (UMR) %",
        'w_land': "Prioritas: Harga Tanah Murah %",
        'w_infra': "Prioritas: Kualitas Infrastruktur %",
        'w_market': "Prioritas: Ukuran Pasar (PDB) %",
        'w_tax': "Prioritas: Tarif Pajak Rendah %",
        'w_education': "Prioritas: Tenaga Kerja Terampil (Pendidikan) %",
        'w_logistics': "Prioritas: Kinerja Logistik %",
        'w_poverty': "Prioritas: Tingkat Kemiskinan Rendah %",
        'total_w': "Total Bobot (Harus 100%)",
        'candidates': "🏙️ Wilayah Kandidat (Edit Data)",
        'rank_res': "🏆 Peringkat Optimasi",
        'best_choice': "Pilihan Terbaik:",
        'score': "Skor Komposit (0-100)",
        'details': "Detail Analisis",
        'labor': "Biaya Tenaga Kerja",
        'land': "Harga Tanah",
        'infra': "Infrastruktur",
        'gdp': "PDRB Regional",
        'tax': "Tarif Pajak",
        'education': "Tingkat Pendidikan",
        'logistics': "Logistik",
        'poverty': "Tingkat Kemiskinan",
        'insight': "💡 **Insight AI:** Wilayah **{winner}** menang karena menawarkan keseimbangan terbaik untuk prioritas spesifik Anda.",
        'insight_labor': "Karena Anda memprioritaskan **Upah Murah**, UMR rendah di wilayah ini mendongkrak skor.",
        'insight_infra': "Karena Anda memprioritaskan **Infrastruktur**, logistik maju di wilayah ini mendongkrak skor.",
        'insight_education': "Karena Anda memprioritaskan **Tenaga Kerja Terampil**, tingkat pendidikan tinggi di wilayah ini adalah keunggulan utama.",
        'viz_title': "Rincian Skor Terbobot per Wilayah",
        'story_title': "📚 Cerita & Kasus Penggunaan: Pencari Lokasi",
        'story_meaning': "**Apa artinya ini?**\nSistem Pendukung Keputusan (MCDA) yang meranking lokasi berdasarkan prioritas bisnis spesifik Anda menggunakan 8 indikator ekonomi.",
        'story_insight': "**Wawasan Utama:**\nTidak ada 'Tempat Terbaik' untuk semua. Pabrik Tekstil butuh upah murah (Jateng), sementara Startup butuh infrastruktur + SDM terampil (Jakarta). Bobot itu penting!",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **BKPM/Pemda:** Untuk mensimulasikan bagaimana perbaikan jalan/tol bisa mendongkrak skor investasi daerah mereka.",
        'use_corp': "🏢 **Manajer Ekspansi:** Untuk memilih lokasi pabrik baru secara ilmiah menggunakan data, bukan tebakan.",
        'use_analyst': "📈 **Ekonom Regional:** Untuk membandingkan daya saing antar provinsi."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

col1, col2 = st.columns([1, 2])

# --- 1. USER WEIGHTS ---
with col1:
    st.subheader(txt['criteria'])
    
    # 8 Criteria with sliders
    w_labor = st.slider(txt['w_labor'], 0, 100, 15, 5)
    w_land = st.slider(txt['w_land'], 0, 100, 10, 5)
    w_infra = st.slider(txt['w_infra'], 0, 100, 15, 5)
    w_market = st.slider(txt['w_market'], 0, 100, 15, 5)
    w_tax = st.slider(txt['w_tax'], 0, 100, 10, 5)
    w_education = st.slider(txt['w_education'], 0, 100, 15, 5)
    w_logistics = st.slider(txt['w_logistics'], 0, 100, 10, 5)
    w_poverty = st.slider(txt['w_poverty'], 0, 100, 10, 5)
    
    total_weight = w_labor + w_land + w_infra + w_market + w_tax + w_education + w_logistics + w_poverty
    
    if total_weight != 100:
        st.warning(f"⚠️ {txt['total_w']}: **{total_weight}%**. Please adjust to 100%.")
    else:
        st.success(f"✅ {txt['total_w']}: **100%**")

# --- 2. DATA GENERATION & LOGIC ---
# Enhanced data with 8 parameters
data = {
    'Region': ['Jakarta (Metro)', 'Jawa Tengah (Industrial)', 'Jawa Timur (Port)', 'Bali (Tourism)', 'Kalimantan (Resource)'],
    'UMR (Rp Juta)': [5.2, 2.5, 2.8, 3.0, 3.5],                    # Cost (Lower is better)
    'Land Price (Rp Juta/m2)': [8.0, 0.5, 1.2, 2.5, 0.8],         # Cost (Lower is better)
    'Infra Score (0-100)': [95, 70, 80, 85, 60],                   # Benefit (Higher is better)
    'GDP (Triliun Rp)': [800, 300, 450, 150, 200],                 # Benefit (Higher is better)
    'Tax Rate (%)': [12, 10, 11, 10, 9],                           # Cost (Lower is better)
    'Education Index (0-100)': [85, 65, 70, 75, 60],               # Benefit (Higher is better)
    'Logistics Score (0-100)': [90, 60, 75, 70, 55],               # Benefit (Higher is better)
    'Poverty Rate (%)': [4.5, 12.0, 10.5, 8.0, 11.0]               # Cost (Lower is better)
}
df = pd.DataFrame(data)

with col2:
    st.subheader(txt['candidates'])
    # Make data editable
    df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key='editor_mcda')

    if total_weight == 100:
        st.divider()
        st.subheader(txt['rank_res'])
        
        # --- MCDA LOGIC (Min-Max Normalization) ---
        df_norm = df.copy()
        
        # Normalize each criterion
        # COST criteria (Lower is better): (Max - Value) / (Max - Min)
        # BENEFIT criteria (Higher is better): (Value - Min) / (Max - Min)
        
        # 1. UMR (Cost)
        min_val, max_val = df['UMR (Rp Juta)'].min(), df['UMR (Rp Juta)'].max()
        df_norm['Norm_Labor'] = (max_val - df['UMR (Rp Juta)']) / (max_val - min_val) if max_val != min_val else 0.5
        
        # 2. Land (Cost)
        min_val, max_val = df['Land Price (Rp Juta/m2)'].min(), df['Land Price (Rp Juta/m2)'].max()
        df_norm['Norm_Land'] = (max_val - df['Land Price (Rp Juta/m2)']) / (max_val - min_val) if max_val != min_val else 0.5
        
        # 3. Infra (Benefit)
        min_val, max_val = df['Infra Score (0-100)'].min(), df['Infra Score (0-100)'].max()
        df_norm['Norm_Infra'] = (df['Infra Score (0-100)'] - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        
        # 4. GDP (Benefit)
        min_val, max_val = df['GDP (Triliun Rp)'].min(), df['GDP (Triliun Rp)'].max()
        df_norm['Norm_Market'] = (df['GDP (Triliun Rp)'] - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        
        # 5. Tax (Cost)
        min_val, max_val = df['Tax Rate (%)'].min(), df['Tax Rate (%)'].max()
        df_norm['Norm_Tax'] = (max_val - df['Tax Rate (%)']) / (max_val - min_val) if max_val != min_val else 0.5
        
        # 6. Education (Benefit)
        min_val, max_val = df['Education Index (0-100)'].min(), df['Education Index (0-100)'].max()
        df_norm['Norm_Education'] = (df['Education Index (0-100)'] - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        
        # 7. Logistics (Benefit)
        min_val, max_val = df['Logistics Score (0-100)'].min(), df['Logistics Score (0-100)'].max()
        df_norm['Norm_Logistics'] = (df['Logistics Score (0-100)'] - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        
        # 8. Poverty (Cost)
        min_val, max_val = df['Poverty Rate (%)'].min(), df['Poverty Rate (%)'].max()
        df_norm['Norm_Poverty'] = (max_val - df['Poverty Rate (%)']) / (max_val - min_val) if max_val != min_val else 0.5
        
        # Apply Weights
        df_norm['Score'] = (
            df_norm['Norm_Labor'] * (w_labor/100) +
            df_norm['Norm_Land'] * (w_land/100) +
            df_norm['Norm_Infra'] * (w_infra/100) +
            df_norm['Norm_Market'] * (w_market/100) +
            df_norm['Norm_Tax'] * (w_tax/100) +
            df_norm['Norm_Education'] * (w_education/100) +
            df_norm['Norm_Logistics'] * (w_logistics/100) +
            df_norm['Norm_Poverty'] * (w_poverty/100)
        ) * 100
        
        df_norm['Score'] = df_norm['Score'].round(1)
        
        # Sort
        df_sorted = df_norm.sort_values('Score', ascending=False).reset_index(drop=True)
        winner = df_sorted.iloc[0]['Region']
        
        # Display Winner
        st.success(f"### 🥇 {txt['best_choice']} {winner} ({txt['score']}: {df_sorted.iloc[0]['Score']})") 
        
        # Explanation
        reason = txt['insight'].format(winner=winner)
        if w_labor > 20 and df_sorted.iloc[0]['Norm_Labor'] > 0.7:
             reason += "\n\n" + txt['insight_labor']
        if w_infra > 20 and df_sorted.iloc[0]['Norm_Infra'] > 0.7:
             reason += "\n\n" + txt['insight_infra']
        if w_education > 20 and df_sorted.iloc[0]['Norm_Education'] > 0.7:
             reason += "\n\n" + txt['insight_education']
             
        st.info(reason)
        
        # --- VISUALIZATION (Plotly Stacked Bar) ---
        viz_data = []
        for index, row in df_norm.iterrows():
            viz_data.append({'Region': row['Region'], 'Criteria': txt['labor'], 'Contribution': row['Norm_Labor'] * w_labor})
            viz_data.append({'Region': row['Region'], 'Criteria': txt['land'], 'Contribution': row['Norm_Land'] * w_land})
            viz_data.append({'Region': row['Region'], 'Criteria': txt['infra'], 'Contribution': row['Norm_Infra'] * w_infra})
            viz_data.append({'Region': row['Region'], 'Criteria': txt['gdp'], 'Contribution': row['Norm_Market'] * w_market})
            viz_data.append({'Region': row['Region'], 'Criteria': txt['tax'], 'Contribution': row['Norm_Tax'] * w_tax})
            viz_data.append({'Region': row['Region'], 'Criteria': txt['education'], 'Contribution': row['Norm_Education'] * w_education})
            viz_data.append({'Region': row['Region'], 'Criteria': txt['logistics'], 'Contribution': row['Norm_Logistics'] * w_logistics})
            viz_data.append({'Region': row['Region'], 'Criteria': txt['poverty'], 'Contribution': row['Norm_Poverty'] * w_poverty})
            
        df_viz = pd.DataFrame(viz_data)
        
        # Create stacked bar chart
        fig = go.Figure()
        
        criteria_list = [txt['labor'], txt['land'], txt['infra'], txt['gdp'], txt['tax'], txt['education'], txt['logistics'], txt['poverty']]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        
        for i, criteria in enumerate(criteria_list):
            df_criteria = df_viz[df_viz['Criteria'] == criteria]
            fig.add_trace(go.Bar(
                name=criteria,
                x=df_criteria['Region'],
                y=df_criteria['Contribution'],
                marker_color=colors[i]
            ))
        
        fig.update_layout(
            barmode='stack',
            title=txt['viz_title'],
            xaxis_title='Region',
            yaxis_title='Weighted Score Contribution',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Ranking Table
        st.markdown("### 📊 Complete Ranking")
        ranking_df = df_sorted[['Region', 'Score']].copy()
        ranking_df['Rank'] = range(1, len(ranking_df) + 1)
        ranking_df = ranking_df[['Rank', 'Region', 'Score']]
        st.dataframe(ranking_df, use_container_width=True, hide_index=True)

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
