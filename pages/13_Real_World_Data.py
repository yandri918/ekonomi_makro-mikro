import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Real-World Data", page_icon="🌍", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🌍 Real-World Economic Dashboard",
        'subtitle': "Live data from **World Bank API**. Compare Indonesia vs ASEAN Peers.",
        'indicators': "Select Indicator:",
        'gdp_growth': "GDP Growth (Annual %)",
        'inflation': "Inflation (CPI, Annual %)",
        'gdp_pcap': "GDP per Capita (Current US$)",
        'countries': "Select Countries:",
        'idn': "Indonesia",
        'mys': "Malaysia",
        'sgp': "Singapore",
        'tha': "Thailand",
        'vnm': "Vietnam",
        'phl': "Philippines",
        'chn': "China",
        'usa': "United States",
        'fetch': "🔄 Fetch Live Data",
        'source': "Source: World Bank Open Data (API)",
        'error': "Error fetching data. World Bank API might be busy.",
        'chart_title': "Time Series Comparison (2010 - 2024)",
        'latest_title': "Latest Available Year Comparison",
        'explanation': "💡 **Insight:**"
    },
    'ID': {
        'title': "🌍 Dashboard Ekonomi Data Riil",
        'subtitle': "Data langsung dari **API Bank Dunia**. Bandingkan Indonesia vs Negara ASEAN.",
        'indicators': "Pilih Indikator:",
        'gdp_growth': "Pertumbuhan PDB (Tahunan %)",
        'inflation': "Inflasi (IHK, Tahunan %)",
        'gdp_pcap': "PDB per Kapita (US$ Saat Ini)",
        'countries': "Pilih Negara:",
        'idn': "Indonesia",
        'mys': "Malaysia",
        'sgp': "Singapura",
        'tha': "Thailand",
        'vnm': "Vietnam",
        'phl': "Filipina",
        'chn': "Tiongkok",
        'usa': "Amerika Serikat",
        'fetch': "🔄 Ambil Data Langsung",
        'source': "Sumber: World Bank Open Data (API)",
        'error': "Gagal mengambil data. API Bank Dunia mungkin sibuk.",
        'chart_title': "Perbandingan Runtut Waktu (2010 - 2024)",
        'latest_title': "Perbandingan Tahun Terakhir Tersedia",
        'explanation': "💡 **Wawasan:**"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- MAPPING ---
indicator_map = {
    txt['gdp_growth']: 'NY.GDP.MKTP.KD.ZG',
    txt['inflation']: 'FP.CPI.TOTL.ZG',
    txt['gdp_pcap']: 'NY.GDP.PCAP.CD'
}

country_map = {
    txt['idn']: 'IDN',
    txt['mys']: 'MYS',
    txt['sgp']: 'SGP',
    txt['tha']: 'THA',
    txt['vnm']: 'VNM',
    txt['phl']: 'PHL',
    txt['chn']: 'CHN',
    txt['usa']: 'USA'
}

# --- SIDEBAR INPUTS ---
col1, col2 = st.columns([1, 2.5])

with col1:
    selected_ind_name = st.selectbox(txt['indicators'], list(indicator_map.keys()))
    indicator_code = indicator_map[selected_ind_name]
    
    default_countries = [txt['idn'], txt['mys'], txt['vnm']]
    selected_countries_names = st.multiselect(txt['countries'], list(country_map.keys()), default=default_countries)
    selected_iso3 = [country_map[name] for name in selected_countries_names]
    
    fetch_btn = st.button(txt['fetch'], type="primary")

# --- DATA FETCHING ---
@st.cache_data(ttl=3600) # Cache for 1 hour to avoid spamming API
def fetch_world_bank_data(countries, indicator, start_year=2010, end_year=2024):
    # API Format: http://api.worldbank.org/v2/country/id;my;sg/indicator/NY.GDP.MKTP.KD.ZG?source=2&date=2010:2023&format=json&per_page=1000
    
    country_str = ";".join(countries).lower()
    url = f"http://api.worldbank.org/v2/country/{country_str}/indicator/{indicator}"
    params = {
        'source': 2,
        'date': f"{start_year}:{end_year}",
        'format': 'json',
        'per_page': 1000
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # World Bank API returns [metadata, data]
        if len(data) < 2:
            return pd.DataFrame()
        
        records = []
        for item in data[1]:
            records.append({
                'Country': item['country']['value'],
                'ISO3': item['countryiso3code'],
                'Year': int(item['date']),
                'Value': item['value']
            })
            
        df = pd.DataFrame(records)
        return df.dropna()
        
    except Exception as e:
        st.error(f"{e}")
        return pd.DataFrame()

# --- MAIN DISPLAY ---
with col2:
    if fetch_btn and selected_countries_names:
        with st.spinner("Connecting to World Bank..."):
            df = fetch_world_bank_data(selected_iso3, indicator_code)
        
        if not df.empty:
            # Sort for line chart
            df = df.sort_values(by=['Country', 'Year'])
            
            # 1. Line Chart
            fig_line = px.line(df, x='Year', y='Value', color='Country', markers=True,
                               title=f"{selected_ind_name} - {txt['chart_title']}",
                               template="plotly_white")
            
            st.plotly_chart(fig_line, use_container_width=True)
            
            # 2. Bar Chart (Latest Year)
            latest_year = df['Year'].max()
            df_latest = df[df['Year'] == latest_year].sort_values('Value', ascending=False)
            
            fig_bar = px.bar(df_latest, x='Country', y='Value', color='Country', 
                             title=f"{selected_ind_name} ({latest_year})", text_auto='.2s')
            
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # 3. Simple Insight
            winner = df_latest.iloc[0]['Country']
            st.info(f"{txt['explanation']} Data shows **{winner}** has the highest **{selected_ind_name}** in {latest_year}.")
            st.caption(txt['source'])
            
        else:
            st.error(txt['error'])
    elif not selected_countries_names:
        st.warning("Please select at least one country.")
    else:
        st.info("👈 Click **Fetch Live Data** to start.")
