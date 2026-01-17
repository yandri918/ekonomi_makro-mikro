import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Forecasting", page_icon="📈", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "📈 Economic Forecasting Lab",
        'subtitle': "Predict future economic trends using **Holt-Winters Exponential Smoothing**.",
        'setup': "⚙️ Data & Model Setup",
        'dataset': "Select Indicator:",
        'cpi': "Inflation (CPI)",
        'gdp': "GDP Growth",
        'sales': "Retail Sales",
        'params': "Forecast Parameters",
        'horizon': "Forecast Horizon (Months)",
        'period': "Seasonal Period (Months)",
        'trend': "Trend Type",
        'seasonal': "Seasonal Type",
        'additive': "Additive",
        'multiplicative': "Multiplicative",
        'none': "None",
        'gen_data': "🔄 Generate New Data",
        'results': "📊 Forecast Results",
        'metrics': "Model Accuracy Metrics",
        'mae': "Mean Absolute Error (MAE):",
        'rmse': "Root Mean Sq. Error (RMSE):",
        'chart_title': "Actual Data vs Forecast",
        'date': "Date",
        'value': "Value",
        'type': "Type",
        'actual': "Actual Data",
        'forecast': "Forecast",
        'train_rng': "Training Range (Months)",
        'insufficient': "Not enough data for this seasonal period. Try reducing the period.",
        'edit_data': "📝 View & Edit Data"
    },
    'ID': {
        'title': "📈 Lab Peramalan Ekonomi",
        'subtitle': "Prediksi tren ekonomi masa depan menggunakan **Holt-Winters Exponential Smoothing**.",
        'setup': "⚙️ Pengaturan Data & Model",
        'dataset': "Pilih Indikator:",
        'cpi': "Inflasi (IHK)",
        'gdp': "Pertumbuhan PDB",
        'sales': "Penjualan Ritel",
        'params': "Parameter Peramalan",
        'horizon': "Cakupan Peramalan (Bulan)",
        'period': "Periode Musiman (Bulan)",
        'trend': "Tipe Tren",
        'seasonal': "Tipe Musiman",
        'additive': "Aditif",
        'multiplicative': "Multiplikatif",
        'none': "Tidak Ada (None)",
        'gen_data': "🔄 Hasilkan Data Baru",
        'results': "📊 Hasil Peramalan",
        'metrics': "Metrik Akurasi Model",
        'mae': "Rata-rata Kesalahan Absolut (MAE):",
        'rmse': "Akar Kuadrat Tengah Kesalahan (RMSE):",
        'chart_title': "Data Aktual vs Ramalan",
        'date': "Tanggal",
        'value': "Nilai",
        'type': "Tipe",
        'actual': "Data Aktual",
        'forecast': "Ramalan",
        'train_rng': "Rentang Training (Bulan)",
        'insufficient': "Data tidak cukup untuk periode musiman ini. Coba kurangi periode.",
        'edit_data': "📝 Lihat & Edit Data"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- 1. Data Generation & Setup ---
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### {txt['setup']}")
    indicator = st.selectbox(txt['dataset'], [txt['cpi'], txt['sales'], txt['gdp']])
    
    n_points = st.slider(txt['train_rng'], 24, 120, 60)
    
    # Generate Synthetic Data
    # Used caching/session state to prevent regeneration on every interaction
    if 'ts_data' not in st.session_state or st.button(txt['gen_data']):
        np.random.seed(np.random.randint(0, 1000))
        dates = pd.date_range(start='2020-01-01', periods=n_points, freq='M')
        
        if indicator == txt['cpi']:
            # Trend + Random + Seasonality
            trend = np.linspace(100, 120, n_points)
            season = 2 * np.sin(np.linspace(0, 3.14 * 4, n_points)) 
            noise = np.random.normal(0, 0.5, n_points)
            values = trend + season + noise
        elif indicator == txt['sales']:
             # Multiplicative Seasonality
             trend = np.linspace(1000, 2000, n_points)
             season = 1 + 0.2 * np.sin(np.linspace(0, 3.14 * 8, n_points))
             noise = np.random.normal(0, 50, n_points)
             values = trend * season + noise
        else: # GDP
             trend = np.linspace(5000, 6000, n_points) + np.random.normal(0, 50, n_points).cumsum()
             values = trend
             
        st.session_state['ts_data'] = pd.DataFrame({'Date': dates, 'Value': values})
        st.success("Data Generated!")

    st.markdown("---")
    
    # EDITABLE DATA SECTION
    if 'ts_data' in st.session_state:
        with st.expander(txt['edit_data']):
            edited_df = st.data_editor(
                st.session_state['ts_data'], 
                num_rows="dynamic", 
                column_config={
                    "Date": st.column_config.DatetimeColumn("Date", format="D MMM YYYY"),
                    "Value": st.column_config.NumberColumn("Value", format="%.2f")
                },
                key='ts_editor'
            )
            # Update df to be used in model
            df_model = edited_df
    else:
        df_model = None

    st.markdown("---")
    st.markdown(f"### {txt['params']}")
    
    horizon = st.slider(txt['horizon'], 1, 24, 12)
    seasonal_periods = st.slider(txt['period'], 2, 12, 12)
    
    trend_type = st.selectbox(txt['trend'], ["add", "mul", None], format_func=lambda x: txt['additive'] if x == 'add' else (txt['multiplicative'] if x == 'mul' else txt['none']))
    seasonal_type = st.selectbox(txt['seasonal'], ["add", "mul", None], format_func=lambda x: txt['additive'] if x == 'add' else (txt['multiplicative'] if x == 'mul' else txt['none']))

with col2:
    if df_model is not None and not df_model.empty:
        df = df_model
        
        # --- 2. Model Fitting & Forecasting ---
        try:
            # Statsmodels Holt-Winters
            model = ExponentialSmoothing(
                df['Value'],
                trend=trend_type,
                seasonal=seasonal_type,
                seasonal_periods=seasonal_periods,
                initialization_method="estimated"
            ).fit()
            
            forecast_values = model.forecast(horizon)
            
            # --- 3. Metrics Calculation (In-Sample) ---
            fitted_values = model.fittedvalues
            residuals = df['Value'] - fitted_values
            mae = np.mean(np.abs(residuals))
            rmse = np.sqrt(np.mean(residuals**2))
            
            # --- 4. Visualization ---
            # Prepare Forecast DataFrame
            last_date = df['Date'].iloc[-1]
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon, freq='M')
            
            df_forecast = pd.DataFrame({
                'Date': future_dates,
                'Value': forecast_values,
                'Type': txt['forecast']
            })
            
            df_actual = df.copy()
            df_actual['Type'] = txt['actual']
            
            # Combine for plotting
            df_chart = pd.concat([df_actual, df_forecast])
            
            st.markdown(f"### {txt['results']}")
            
            chart = alt.Chart(df_chart).mark_line().encode(
                x=alt.X('Date', title=txt['date']),
                y=alt.Y('Value', title=txt['value'], scale=alt.Scale(zero=False)),
                color=alt.Color('Type', scale=alt.Scale(domain=[txt['actual'], txt['forecast']], range=['steelblue', 'orange'])),
                tooltip=['Date', 'Value', 'Type']
            ).properties(
                title=txt['chart_title'],
                height=400
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            
            # Display Metrics
            m1, m2 = st.columns(2)
            m1.metric(txt['mae'], f"{mae:.4f}")
            m2.metric(txt['rmse'], f"{rmse:.4f}")
            
            with st.expander("Show Model Summary"):
                 st.text(model.summary())
                 
        except Exception as e:
            st.error(f"Error fitting model: {e}")
            st.warning(txt['insufficient'])
    else:
        st.info("Please generate data first.")
