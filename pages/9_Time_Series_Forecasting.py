import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Forecasting", page_icon="📈", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "📈 Economic Forecasting Lab",
        'subtitle': "Predict future economic trends using **Holt-Winters** and **ARIMA** models.",
        'tab1': "📊 Holt-Winters",
        'tab2': "🤖 ARIMA Model",
        'setup': "⚙️ Data & Model Setup",
        'dataset': "Select Indicator:",
        'cpi': "Inflation (CPI)",
        'gdp': "Nominal GDP (Trillion Rp)",
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
        'aic': "AIC (Akaike Information Criterion):",
        'bic': "BIC (Bayesian Information Criterion):",
        'chart_title': "Actual Data vs Forecast",
        'date': "Date",
        'value': "Value",
        'type': "Type",
        'actual': "Actual Data",
        'forecast': "Forecast",
        'train_rng': "Training Range (Months)",
        'insufficient': "Not enough data for this seasonal period. Try reducing the period.",
        'edit_data': "📝 Input & Edit Data",
        'clear_data': "🗑️ Clear Data",
        # ARIMA specific
        'arima_params': "ARIMA Parameters",
        'auto_select': "Auto-Select Parameters (Recommended)",
        'manual_params': "Manual Parameters",
        'ar_order': "AR Order (p)",
        'diff_order': "Differencing (d)",
        'ma_order': "MA Order (q)",
        'fit_arima': "🎯 Fit ARIMA Model",
        'optimal_model': "Optimal Model",
        'stationarity': "Stationarity Test (ADF)",
        'stationary': "✅ Data is STATIONARY (p-value < 0.05)",
        'non_stationary': "⚠️ Data is NON-STATIONARY (p-value ≥ 0.05) - Differencing recommended",
        'diagnostics': "📊 Diagnostic Plots",
        'acf_plot': "ACF (Autocorrelation Function)",
        'pacf_plot': "PACF (Partial Autocorrelation Function)"
    },
    'ID': {
        'title': "📈 Lab Peramalan Ekonomi",
        'subtitle': "Prediksi tren ekonomi masa depan menggunakan **Holt-Winters** dan **ARIMA**.",
        'tab1': "📊 Holt-Winters",
        'tab2': "🤖 Model ARIMA",
        'setup': "⚙️ Pengaturan Data & Model",
        'dataset': "Pilih Indikator:",
        'cpi': "Inflasi (IHK)",
        'gdp': "PDB Nominal (Triliun Rp)",
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
        'aic': "AIC (Akaike Information Criterion):",
        'bic': "BIC (Bayesian Information Criterion):",
        'chart_title': "Data Aktual vs Ramalan",
        'date': "Tanggal",
        'value': "Nilai",
        'type': "Tipe",
        'actual': "Data Aktual",
        'forecast': "Ramalan",
        'train_rng': "Rentang Gen. Data (Bulan)",
        'insufficient': "Data tidak cukup untuk periode musiman ini. Coba kurangi periode.",
        'edit_data': "📝 Input & Edit Data",
        'clear_data': "🗑️ Hapus Data",
        # ARIMA specific
        'arima_params': "Parameter ARIMA",
        'auto_select': "Pilih Parameter Otomatis (Direkomendasikan)",
        'manual_params': "Parameter Manual",
        'ar_order': "Orde AR (p)",
        'diff_order': "Diferensiasi (d)",
        'ma_order': "Orde MA (q)",
        'fit_arima': "🎯 Fit Model ARIMA",
        'optimal_model': "Model Optimal",
        'stationarity': "Tes Stasioneritas (ADF)",
        'stationary': "✅ Data STASIONER (p-value < 0.05)",
        'non_stationary': "⚠️ Data TIDAK STASIONER (p-value ≥ 0.05) - Diferensiasi direkomendasikan",
        'diagnostics': "📊 Plot Diagnostik",
        'acf_plot': "ACF (Fungsi Autokorelasi)",
        'pacf_plot': "PACF (Fungsi Autokorelasi Parsial)"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- DATA GENERATION & SETUP (SHARED) ---
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### {txt['setup']}")
    indicator = st.selectbox(txt['dataset'], [txt['cpi'], txt['sales'], txt['gdp']])
    
    n_points = st.slider(txt['train_rng'], 24, 120, 60)
    
    # Data Controls
    b1, b2 = st.columns(2)
    with b1:
        if st.button(txt['gen_data']):
            np.random.seed(np.random.randint(0, 1000))
            dates = pd.date_range(start='2020-01-01', periods=n_points, freq='M')
            
            if indicator == txt['cpi']:
                trend = np.linspace(100, 120, n_points)
                season = 2 * np.sin(np.linspace(0, 3.14 * 4, n_points)) 
                noise = np.random.normal(0, 0.5, n_points)
                values = trend + season + noise
            elif indicator == txt['sales']:
                trend = np.linspace(1000, 2000, n_points)
                season = 1 + 0.2 * np.sin(np.linspace(0, 3.14 * 8, n_points))
                noise = np.random.normal(0, 50, n_points)
                values = trend * season + noise
            else:  # GDP
                trend = np.linspace(5000, 6000, n_points) + np.random.normal(0, 50, n_points).cumsum()
                values = trend
                
            st.session_state['ts_data'] = pd.DataFrame({'Date': dates, 'Value': values})
            st.rerun()

    with b2:
        if st.button(txt['clear_data']):
            st.session_state['ts_data'] = pd.DataFrame({
                'Date': pd.Series(dtype='datetime64[ns]'),
                'Value': pd.Series(dtype='float64')
            })
            st.rerun()

    # Initialize session state
    if 'ts_data' not in st.session_state:
        st.session_state['ts_data'] = pd.DataFrame({
                'Date': pd.Series(dtype='datetime64[ns]'),
                'Value': pd.Series(dtype='float64')
            })

    st.markdown("---")
    
    # EDITABLE DATA SECTION
    st.markdown(f"### {txt['edit_data']}")
    
    if 'ts_data' in st.session_state:
        edited_df = st.data_editor(
            st.session_state['ts_data'], 
            num_rows="dynamic", 
            column_config={
                "Date": st.column_config.DatetimeColumn("Date", format="D MMM YYYY", required=True),
                "Value": st.column_config.NumberColumn("Value", format="%.2f", required=True)
            },
            key='ts_editor',
            use_container_width=True
        )
        df_model = edited_df

# --- TABS ---
with col2:
    if df_model is not None and not df_model.empty:
        tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])
        
        # ========== TAB 1: HOLT-WINTERS ==========
        with tab1:
            st.markdown(f"### {txt['params']}")
            
            horizon_hw = st.slider(txt['horizon'], 1, 24, 12, key='hw_horizon')
            seasonal_periods = st.slider(txt['period'], 2, 12, 12, key='hw_period')
            
            trend_type = st.selectbox(txt['trend'], ["add", "mul", None], format_func=lambda x: txt['additive'] if x == 'add' else (txt['multiplicative'] if x == 'mul' else txt['none']), key='hw_trend')
            seasonal_type = st.selectbox(txt['seasonal'], ["add", "mul", None], format_func=lambda x: txt['additive'] if x == 'add' else (txt['multiplicative'] if x == 'mul' else txt['none']), key='hw_seasonal')
            
            df = df_model
            
            try:
                model = ExponentialSmoothing(
                    df['Value'],
                    trend=trend_type,
                    seasonal=seasonal_type,
                    seasonal_periods=seasonal_periods,
                    initialization_method="estimated"
                ).fit()
                
                forecast_values = model.forecast(horizon_hw)
                
                fitted_values = model.fittedvalues
                residuals = df['Value'] - fitted_values
                mae = np.mean(np.abs(residuals))
                rmse = np.sqrt(np.mean(residuals**2))
                
                last_date = df['Date'].iloc[-1]
                future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon_hw, freq='M')
                
                st.markdown(f"### {txt['results']}")
                
                # Plotly chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df['Value'],
                    mode='lines',
                    name=txt['actual'],
                    line=dict(color='steelblue')
                ))
                
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=forecast_values,
                    mode='lines',
                    name=txt['forecast'],
                    line=dict(color='orange', dash='dash')
                ))
                
                fig.update_layout(
                    title=txt['chart_title'],
                    xaxis_title=txt['date'],
                    yaxis_title=txt['value'],
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                m1, m2 = st.columns(2)
                m1.metric(txt['mae'], f"{mae:.4f}")
                m2.metric(txt['rmse'], f"{rmse:.4f}")
                
                with st.expander("Show Model Summary"):
                     st.text(model.summary())
                     
            except Exception as e:
                st.error(f"Error fitting model: {e}")
                st.warning(txt['insufficient'])
        
        # ========== TAB 2: ARIMA MODEL ==========
        with tab2:
            st.markdown(f"### {txt['arima_params']}")
            
            auto_select = st.checkbox(txt['auto_select'], value=True)
            
            if not auto_select:
                st.markdown(f"**{txt['manual_params']}**")
                col_p, col_d, col_q = st.columns(3)
                with col_p:
                    p = st.number_input(txt['ar_order'], 0, 5, 1)
                with col_d:
                    d = st.number_input(txt['diff_order'], 0, 2, 1)
                with col_q:
                    q = st.number_input(txt['ma_order'], 0, 5, 1)
            
            horizon_arima = st.slider(txt['horizon'], 1, 24, 12, key='arima_horizon')
            
            if st.button(txt['fit_arima'], type='primary'):
                df = df_model
                
                try:
                    # Stationarity Test
                    st.markdown(f"### {txt['stationarity']}")
                    adf_result = adfuller(df['Value'])
                    adf_pvalue = adf_result[1]
                    
                    if adf_pvalue < 0.05:
                        st.success(txt['stationary'])
                        st.caption(f"ADF Statistic: {adf_result[0]:.4f}, p-value: {adf_pvalue:.4f}")
                    else:
                        st.warning(txt['non_stationary'])
                        st.caption(f"ADF Statistic: {adf_result[0]:.4f}, p-value: {adf_pvalue:.4f}")
                    
                    st.markdown("---")
                    
                    # Auto-select parameters using grid search
                    if auto_select:
                        st.info("🔍 Searching for optimal ARIMA parameters...")
                        
                        best_aic = np.inf
                        best_order = None
                        
                        # Grid search
                        for p_test in range(0, 3):
                            for d_test in range(0, 2):
                                for q_test in range(0, 3):
                                    try:
                                        temp_model = ARIMA(df['Value'], order=(p_test, d_test, q_test)).fit()
                                        if temp_model.aic < best_aic:
                                            best_aic = temp_model.aic
                                            best_order = (p_test, d_test, q_test)
                                    except:
                                        continue
                        
                        p, d, q = best_order
                        st.success(f"{txt['optimal_model']}: ARIMA({p},{d},{q})")
                    
                    # Fit final model
                    model_arima = ARIMA(df['Value'], order=(p, d, q)).fit()
                    
                    # Forecast
                    forecast_arima = model_arima.forecast(steps=horizon_arima)
                    
                    # Metrics
                    fitted_values = model_arima.fittedvalues
                    residuals = df['Value'][len(df['Value']) - len(fitted_values):] - fitted_values
                    mae_arima = np.mean(np.abs(residuals))
                    rmse_arima = np.sqrt(np.mean(residuals**2))
                    aic_arima = model_arima.aic
                    bic_arima = model_arima.bic
                    
                    st.markdown(f"### {txt['results']}")
                    
                    # Plotly chart
                    last_date = df['Date'].iloc[-1]
                    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon_arima, freq='M')
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=df['Date'],
                        y=df['Value'],
                        mode='lines',
                        name=txt['actual'],
                        line=dict(color='steelblue')
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=forecast_arima,
                        mode='lines',
                        name=txt['forecast'],
                        line=dict(color='red', dash='dash')
                    ))
                    
                    fig.update_layout(
                        title=f"{txt['chart_title']} - ARIMA({p},{d},{q})",
                        xaxis_title=txt['date'],
                        yaxis_title=txt['value'],
                        height=400,
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric(txt['mae'], f"{mae_arima:.4f}")
                    m2.metric(txt['rmse'], f"{rmse_arima:.4f}")
                    m3.metric(txt['aic'], f"{aic_arima:.2f}")
                    m4.metric(txt['bic'], f"{bic_arima:.2f}")
                    
                    # Diagnostic Plots
                    st.markdown(f"### {txt['diagnostics']}")
                    
                    col_acf, col_pacf = st.columns(2)
                    
                    with col_acf:
                        st.markdown(f"**{txt['acf_plot']}**")
                        fig_acf = go.Figure()
                        from statsmodels.tsa.stattools import acf
                        acf_values = acf(residuals, nlags=20)
                        fig_acf.add_trace(go.Bar(x=list(range(len(acf_values))), y=acf_values))
                        fig_acf.update_layout(height=300, showlegend=False)
                        st.plotly_chart(fig_acf, use_container_width=True)
                    
                    with col_pacf:
                        st.markdown(f"**{txt['pacf_plot']}**")
                        fig_pacf = go.Figure()
                        from statsmodels.tsa.stattools import pacf
                        pacf_values = pacf(residuals, nlags=20)
                        fig_pacf.add_trace(go.Bar(x=list(range(len(pacf_values))), y=pacf_values))
                        fig_pacf.update_layout(height=300, showlegend=False)
                        st.plotly_chart(fig_pacf, use_container_width=True)
                    
                    with st.expander("Show ARIMA Model Summary"):
                        st.text(model_arima.summary())
                        
                except Exception as e:
                    st.error(f"Error fitting ARIMA model: {e}")
                    st.warning("Try adjusting parameters or generating more data.")
    else:
        st.info("Please generate data first using the controls on the left.")
