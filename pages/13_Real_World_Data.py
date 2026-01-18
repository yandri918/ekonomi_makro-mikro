import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import time

st.set_page_config(page_title="Global Economic Dashboard", page_icon="🌍", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🌍 Global Economic & Development Dashboard",
        'subtitle': "Live data from **World Bank API**. Compare Indonesia with global peers across economic and human development indicators.",
        'tab1': "📊 Economic Indicators",
        'tab2': "👥 Human Development",
        'tab3': "🏆 Country Rankings",
        'tab4': "📈 Composite Analysis",
        'select_indicator': "Select Indicator",
        'select_countries': "Select Countries (max 8)",
        'fetch_data': "🔄 Fetch Live Data",
        # Economic Indicators
        'gdp_growth': "GDP Growth (Annual %)",
        'inflation': "Inflation (CPI %)",
        'gdp_per_capita': "GDP per Capita (US$)",
        'unemployment': "Unemployment Rate (%)",
        'trade_balance': "Trade (% of GDP)",
        'fdi': "Foreign Direct Investment (% of GDP)",
        # Human Development
        'life_expectancy': "Life Expectancy (years)",
        'literacy_rate': "Literacy Rate (%)",
        'school_enrollment': "School Enrollment (%)",
        'infant_mortality': "Infant Mortality (per 1,000)",
        'access_electricity': "Access to Electricity (%)",
        'internet_users': "Internet Users (% of population)",
        # Countries
        'idn': "Indonesia",
        'mys': "Malaysia",
        'sgp': "Singapore",
        'tha': "Thailand",
        'vnm': "Vietnam",
        'phl': "Philippines",
        'chn': "China",
        'usa': "United States",
        'jpn': "Japan",
        'kor': "South Korea",
        'aus': "Australia",
        'ind': "India",
        'gbr': "United Kingdom",
        'deu': "Germany",
        'bra': "Brazil",
        'mex': "Mexico",
        'tur': "Turkey",
        'sau': "Saudi Arabia",
        # UI
        'loading': "Fetching data from World Bank API...",
        'success': "Data loaded successfully!",
        'error': "Error fetching data. Please try again.",
        'source': "Source: World Bank Open Data API",
        'latest_year': "Latest Available Year",
        'time_series': "Time Series (2010-2024)",
        'ranking': "Country Rankings",
        'insights': "Key Insights",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nComprehensive dashboard connecting to World Bank API for real-time economic and human development data.",
        'story_insight': "**Key Insight:**\nCombining economic and human development indicators provides a complete picture of national progress beyond GDP.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Policy Makers:** Benchmark performance and identify development gaps.",
        'use_researcher': "🎓 **Researchers:** Access real-time data for empirical analysis.",
        'use_investor': "💼 **Investors:** Assess country risk and growth potential."
    },
    'ID': {
        'title': "🌍 Dashboard Ekonomi & Pembangunan Global",
        'subtitle': "Data langsung dari **API Bank Dunia**. Bandingkan Indonesia dengan negara lain dalam indikator ekonomi dan pembangunan manusia.",
        'tab1': "📊 Indikator Ekonomi",
        'tab2': "👥 Pembangunan Manusia",
        'tab3': "🏆 Peringkat Negara",
        'tab4': "📈 Analisis Komposit",
        'select_indicator': "Pilih Indikator",
        'select_countries': "Pilih Negara (maks 8)",
        'fetch_data': "🔄 Ambil Data Langsung",
        # Economic Indicators
        'gdp_growth': "Pertumbuhan PDB (Tahunan %)",
        'inflation': "Inflasi (IHK %)",
        'gdp_per_capita': "PDB per Kapita (US$)",
        'unemployment': "Tingkat Pengangguran (%)",
        'trade_balance': "Perdagangan (% PDB)",
        'fdi': "Investasi Asing Langsung (% PDB)",
        # Human Development
        'life_expectancy': "Harapan Hidup (tahun)",
        'literacy_rate': "Tingkat Melek Huruf (%)",
        'school_enrollment': "Partisipasi Sekolah (%)",
        'infant_mortality': "Kematian Bayi (per 1.000)",
        'access_electricity': "Akses Listrik (%)",
        'internet_users': "Pengguna Internet (% populasi)",
        # Countries
        'idn': "Indonesia",
        'mys': "Malaysia",
        'sgp': "Singapura",
        'tha': "Thailand",
        'vnm': "Vietnam",
        'phl': "Filipina",
        'chn': "Tiongkok",
        'usa': "Amerika Serikat",
        'jpn': "Jepang",
        'kor': "Korea Selatan",
        'aus': "Australia",
        'ind': "India",
        'gbr': "Inggris",
        'deu': "Jerman",
        'bra': "Brasil",
        'mex': "Meksiko",
        'tur': "Turki",
        'sau': "Arab Saudi",
        # UI
        'loading': "Mengambil data dari API Bank Dunia...",
        'success': "Data berhasil dimuat!",
        'error': "Gagal mengambil data. Silakan coba lagi.",
        'source': "Sumber: World Bank Open Data API",
        'latest_year': "Tahun Terakhir Tersedia",
        'time_series': "Runtut Waktu (2010-2024)",
        'ranking': "Peringkat Negara",
        'insights': "Wawasan Utama",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nDashboard komprehensif yang terhubung ke API Bank Dunia untuk data ekonomi dan pembangunan manusia real-time.",
        'story_insight': "**Wawasan Utama:**\nMenggabungkan indikator ekonomi dan pembangunan manusia memberikan gambaran lengkap kemajuan nasional di luar PDB.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Pembuat Kebijakan:** Benchmark kinerja dan identifikasi kesenjangan pembangunan.",
        'use_researcher': "🎓 **Peneliti:** Akses data real-time untuk analisis empiris.",
        'use_investor': "💼 **Investor:** Menilai risiko negara dan potensi pertumbuhan."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# World Bank API Indicator Codes
INDICATORS = {
    # Economic
    txt['gdp_growth']: 'NY.GDP.MKTP.KD.ZG',
    txt['inflation']: 'FP.CPI.TOTL.ZG',
    txt['gdp_per_capita']: 'NY.GDP.PCAP.CD',
    txt['unemployment']: 'SL.UEM.TOTL.ZS',
    txt['trade_balance']: 'NE.TRD.GNFS.ZS',
    txt['fdi']: 'BX.KLT.DINV.WD.GD.ZS',
    # Human Development
    txt['life_expectancy']: 'SP.DYN.LE00.IN',
    txt['literacy_rate']: 'SE.ADT.LITR.ZS',
    txt['school_enrollment']: 'SE.PRM.NENR',
    txt['infant_mortality']: 'SP.DYN.IMRT.IN',
    txt['access_electricity']: 'EG.ELC.ACCS.ZS',
    txt['internet_users']: 'IT.NET.USER.ZS'
}

COUNTRIES = {
    txt['idn']: 'IDN',
    txt['mys']: 'MYS',
    txt['sgp']: 'SGP',
    txt['tha']: 'THA',
    txt['vnm']: 'VNM',
    txt['phl']: 'PHL',
    txt['chn']: 'CHN',
    txt['usa']: 'USA',
    txt['jpn']: 'JPN',
    txt['kor']: 'KOR',
    txt['aus']: 'AUS',
    txt['ind']: 'IND',
    txt['gbr']: 'GBR',
    txt['deu']: 'DEU',
    txt['bra']: 'BRA',
    txt['mex']: 'MEX',
    txt['tur']: 'TUR',
    txt['sau']: 'SAU'
}

def fetch_world_bank_data(indicator_code, country_codes, start_year=2010, end_year=2024):
    """Fetch data from World Bank API"""
    try:
        countries_str = ';'.join(country_codes)
        url = f"https://api.worldbank.org/v2/country/{countries_str}/indicator/{indicator_code}"
        params = {
            'date': f'{start_year}:{end_year}',
            'format': 'json',
            'per_page': 1000
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1]:
                df = pd.DataFrame(data[1])
                df = df[['country', 'date', 'value']].copy()
                df.columns = ['Country', 'Year', 'Value']
                df['Country'] = df['Country'].apply(lambda x: x['value'])
                df['Year'] = pd.to_numeric(df['Year'])
                df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
                return df.dropna()
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ========== TAB 1: ECONOMIC INDICATORS ==========
with tab1:
    st.markdown(f"### {txt['tab1']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        economic_indicators = [txt['gdp_growth'], txt['inflation'], txt['gdp_per_capita'], 
                              txt['unemployment'], txt['trade_balance'], txt['fdi']]
        
        selected_indicator = st.selectbox(txt['select_indicator'], economic_indicators)
        
        selected_countries = st.multiselect(
            txt['select_countries'],
            list(COUNTRIES.keys()),
            default=[txt['idn'], txt['mys'], txt['sgp'], txt['tha'], txt['vnm']]
        )
        
        if st.button(txt['fetch_data'], type='primary', key='eco_fetch'):
            if len(selected_countries) > 0:
                with st.spinner(txt['loading']):
                    indicator_code = INDICATORS[selected_indicator]
                    country_codes = [COUNTRIES[c] for c in selected_countries]
                    
                    df = fetch_world_bank_data(indicator_code, country_codes)
                    
                    if df is not None and not df.empty:
                        st.session_state['eco_data'] = df
                        st.session_state['eco_indicator'] = selected_indicator
                        st.success(txt['success'])
                    else:
                        st.error(txt['error'])
    
    with col2:
        if 'eco_data' in st.session_state:
            df = st.session_state['eco_data']
            indicator_name = st.session_state['eco_indicator']
            
            # Time series chart
            fig = go.Figure()
            
            for country in df['Country'].unique():
                country_data = df[df['Country'] == country].sort_values('Year')
                fig.add_trace(go.Scatter(
                    x=country_data['Year'],
                    y=country_data['Value'],
                    mode='lines+markers',
                    name=country,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title=f"{indicator_name} - {txt['time_series']}",
                xaxis_title="Year",
                yaxis_title=indicator_name,
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Latest year comparison
            latest_year = df['Year'].max()
            latest_data = df[df['Year'] == latest_year].sort_values('Value', ascending=False)
            
            st.markdown(f"### {txt['latest_year']}: {int(latest_year)}")
            
            fig_bar = go.Figure(go.Bar(
                x=latest_data['Country'],
                y=latest_data['Value'],
                marker_color=['red' if c == txt['idn'] else 'steelblue' for c in latest_data['Country']],
                text=latest_data['Value'].round(2),
                textposition='outside'
            ))
            
            fig_bar.update_layout(
                title=f"{indicator_name} Comparison",
                xaxis_title="Country",
                yaxis_title=indicator_name,
                height=400
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.caption(txt['source'])

# ========== TAB 2: HUMAN DEVELOPMENT ==========
with tab2:
    st.markdown(f"### {txt['tab2']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        hdi_indicators = [txt['life_expectancy'], txt['literacy_rate'], txt['school_enrollment'],
                         txt['infant_mortality'], txt['access_electricity'], txt['internet_users']]
        
        selected_hdi = st.selectbox(txt['select_indicator'], hdi_indicators, key='hdi_select')
        
        selected_countries_hdi = st.multiselect(
            txt['select_countries'],
            list(COUNTRIES.keys()),
            default=[txt['idn'], txt['mys'], txt['sgp'], txt['tha'], txt['vnm']],
            key='hdi_countries'
        )
        
        if st.button(txt['fetch_data'], type='primary', key='hdi_fetch'):
            if len(selected_countries_hdi) > 0:
                with st.spinner(txt['loading']):
                    indicator_code = INDICATORS[selected_hdi]
                    country_codes = [COUNTRIES[c] for c in selected_countries_hdi]
                    
                    df = fetch_world_bank_data(indicator_code, country_codes)
                    
                    if df is not None and not df.empty:
                        st.session_state['hdi_data'] = df
                        st.session_state['hdi_indicator'] = selected_hdi
                        st.success(txt['success'])
                    else:
                        st.error(txt['error'])
    
    with col2:
        if 'hdi_data' in st.session_state:
            df = st.session_state['hdi_data']
            indicator_name = st.session_state['hdi_indicator']
            
            # Time series
            fig = go.Figure()
            
            for country in df['Country'].unique():
                country_data = df[df['Country'] == country].sort_values('Year')
                fig.add_trace(go.Scatter(
                    x=country_data['Year'],
                    y=country_data['Value'],
                    mode='lines+markers',
                    name=country,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title=f"{indicator_name} - {txt['time_series']}",
                xaxis_title="Year",
                yaxis_title=indicator_name,
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Latest comparison
            latest_year = df['Year'].max()
            latest_data = df[df['Year'] == latest_year].sort_values('Value', ascending=False)
            
            st.markdown(f"### {txt['latest_year']}: {int(latest_year)}")
            
            st.dataframe(latest_data[['Country', 'Value']].reset_index(drop=True), 
                        use_container_width=True, hide_index=True)

# ========== TAB 3: COUNTRY RANKINGS ==========
with tab3:
    st.markdown(f"### {txt['ranking']}")
    
    if 'eco_data' in st.session_state or 'hdi_data' in st.session_state:
        # Combine latest data from both tabs
        rankings = []
        
        if 'eco_data' in st.session_state:
            df_eco = st.session_state['eco_data']
            latest_year_eco = df_eco['Year'].max()
            latest_eco = df_eco[df_eco['Year'] == latest_year_eco][['Country', 'Value']]
            latest_eco.columns = ['Country', st.session_state['eco_indicator']]
            rankings.append(latest_eco)
        
        if 'hdi_data' in st.session_state:
            df_hdi = st.session_state['hdi_data']
            latest_year_hdi = df_hdi['Year'].max()
            latest_hdi = df_hdi[df_hdi['Year'] == latest_year_hdi][['Country', 'Value']]
            latest_hdi.columns = ['Country', st.session_state['hdi_indicator']]
            rankings.append(latest_hdi)
        
        if len(rankings) > 0:
            df_ranking = rankings[0]
            for i in range(1, len(rankings)):
                df_ranking = df_ranking.merge(rankings[i], on='Country', how='outer')
            
            st.dataframe(df_ranking.style.highlight_max(axis=0, color='lightgreen')
                        .highlight_min(axis=0, color='lightcoral'),
                        use_container_width=True, hide_index=True)
            
            # Indonesia's position
            if txt['idn'] in df_ranking['Country'].values:
                idn_row = df_ranking[df_ranking['Country'] == txt['idn']]
                
                st.markdown(f"### {txt['insights']}: {txt['idn']}")
                
                for col in df_ranking.columns:
                    if col != 'Country':
                        idn_value = idn_row[col].values[0]
                        rank = (df_ranking[col] > idn_value).sum() + 1
                        total = df_ranking[col].notna().sum()
                        
                        st.write(f"**{col}**: Rank {rank}/{total} (Value: {idn_value:.2f})")
    else:
        st.info("Fetch data from Economic or Human Development tabs first")

# ========== TAB 4: COMPOSITE ANALYSIS ==========
with tab4:
    st.markdown(f"### {txt['tab4']}")
    
    if 'eco_data' in st.session_state and 'hdi_data' in st.session_state:
        df_eco = st.session_state['eco_data']
        df_hdi = st.session_state['hdi_data']
        
        # Get latest year data
        latest_eco = df_eco[df_eco['Year'] == df_eco['Year'].max()][['Country', 'Value']]
        latest_eco.columns = ['Country', 'Economic']
        
        latest_hdi = df_hdi[df_hdi['Year'] == df_hdi['Year'].max()][['Country', 'Value']]
        latest_hdi.columns = ['Country', 'Development']
        
        df_composite = latest_eco.merge(latest_hdi, on='Country')
        
        # Scatter plot
        fig = go.Figure()
        
        for _, row in df_composite.iterrows():
            color = 'red' if row['Country'] == txt['idn'] else 'blue'
            size = 15 if row['Country'] == txt['idn'] else 10
            
            fig.add_trace(go.Scatter(
                x=[row['Economic']],
                y=[row['Development']],
                mode='markers+text',
                name=row['Country'],
                marker=dict(size=size, color=color),
                text=[row['Country']],
                textposition='top center'
            ))
        
        fig.update_layout(
            title=f"{st.session_state['eco_indicator']} vs {st.session_state['hdi_indicator']}",
            xaxis_title=st.session_state['eco_indicator'],
            yaxis_title=st.session_state['hdi_indicator'],
            height=600,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Interpretation:**
        - Top-right quadrant: High economic performance + High human development (Ideal)
        - Bottom-right: High economic performance but lagging human development
        - Top-left: Good human development despite lower economic indicators
        - Bottom-left: Needs improvement in both dimensions
        """)
    else:
        st.info("Fetch data from both Economic and Human Development tabs for composite analysis")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_govt'])
        st.write(txt['use_researcher'])
        st.write(txt['use_investor'])
