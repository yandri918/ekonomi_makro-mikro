import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, acorr_ljungbox
from statsmodels.stats.stattools import durbin_watson
from scipy import stats
import io

st.set_page_config(page_title="Econometrics Lab", page_icon="🧪", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🧪 Professional Econometrics Lab",
        'subtitle': "Comprehensive OLS regression analysis with diagnostic tests and model validation.",
        'tab1': "📊 Data & Regression",
        'tab2': "🔍 Diagnostics",
        'tab3': "📈 Residual Analysis",
        'data_source': "Data Source",
        'upload_data': "Upload CSV/Excel File",
        'generate_data': "Generate Synthetic Data",
        'upload_file': "Upload your data file",
        'select_vars': "Select Variables",
        'dependent_var': "Dependent Variable (Y)",
        'independent_vars': "Independent Variables (X)",
        'model_type': "Select Model Type",
        'demand': "Demand Function",
        'consumption': "Consumption Function",
        'phillips': "Phillips Curve",
        'production': "Production Function",
        'n_samples': "Number of Samples",
        'noise_level': "Error Variance",
        'generate_btn': "Generate Data",
        'data_preview': "Data Preview & Edit",
        'run_regression': "Run OLS Regression",
        'regression_results': "Regression Results",
        'coefficients': "Estimated Coefficients",
        'model_fit': "Model Fit Statistics",
        'r_squared': "R-squared",
        'adj_r_squared': "Adjusted R-squared",
        'f_statistic': "F-statistic",
        'prob_f': "Prob (F-statistic)",
        'aic': "AIC",
        'bic': "BIC",
        'diagnostic_tests': "Diagnostic Tests",
        'normality': "Normality Test (Jarque-Bera)",
        'heteroskedasticity': "Heteroskedasticity (Breusch-Pagan)",
        'autocorrelation': "Autocorrelation (Durbin-Watson)",
        'multicollinearity': "Multicollinearity (VIF)",
        'residual_plots': "Residual Analysis Plots",
        'fitted_vs_residuals': "Fitted vs Residuals",
        'qq_plot': "Q-Q Plot (Normality)",
        'histogram': "Residuals Histogram",
        'interpretation': "Interpretation Guide",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nProfessional econometrics tool for regression analysis, matching capabilities of Stata/EViews/R.",
        'story_insight': "**Key Insight:**\nOLS is the foundation of econometrics. Understanding diagnostics is crucial for valid inference.",
        'story_users': "**Who needs this?**",
        'use_researcher': "🎓 **Researchers:** Empirical analysis and hypothesis testing.",
        'use_analyst': "📊 **Data Analysts:** Predictive modeling and forecasting.",
        'use_student': "📚 **Students:** Learn econometrics with real tools."
    },
    'ID': {
        'title': "🧪 Lab Ekonometrika Profesional",
        'subtitle': "Analisis regresi OLS komprehensif dengan tes diagnostik dan validasi model.",
        'tab1': "📊 Data & Regresi",
        'tab2': "🔍 Diagnostik",
        'tab3': "📈 Analisis Residual",
        'data_source': "Sumber Data",
        'upload_data': "Upload File CSV/Excel",
        'generate_data': "Generate Data Sintetis",
        'upload_file': "Upload file data Anda",
        'select_vars': "Pilih Variabel",
        'dependent_var': "Variabel Dependen (Y)",
        'independent_vars': "Variabel Independen (X)",
        'model_type': "Pilih Jenis Model",
        'demand': "Fungsi Permintaan",
        'consumption': "Fungsi Konsumsi",
        'phillips': "Kurva Phillips",
        'production': "Fungsi Produksi",
        'n_samples': "Jumlah Sampel",
        'noise_level': "Varians Error",
        'generate_btn': "Generate Data",
        'data_preview': "Pratinjau & Edit Data",
        'run_regression': "Jalankan Regresi OLS",
        'regression_results': "Hasil Regresi",
        'coefficients': "Koefisien Terestimasi",
        'model_fit': "Statistik Kesesuaian Model",
        'r_squared': "R-squared",
        'adj_r_squared': "Adjusted R-squared",
        'f_statistic': "F-statistik",
        'prob_f': "Prob (F-statistik)",
        'aic': "AIC",
        'bic': "BIC",
        'diagnostic_tests': "Tes Diagnostik",
        'normality': "Tes Normalitas (Jarque-Bera)",
        'heteroskedasticity': "Heteroskedastisitas (Breusch-Pagan)",
        'autocorrelation': "Autokorelasi (Durbin-Watson)",
        'multicollinearity': "Multikolinearitas (VIF)",
        'residual_plots': "Plot Analisis Residual",
        'fitted_vs_residuals': "Fitted vs Residual",
        'qq_plot': "Q-Q Plot (Normalitas)",
        'histogram': "Histogram Residual",
        'interpretation': "Panduan Interpretasi",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nAlat ekonometrika profesional untuk analisis regresi, setara dengan Stata/EViews/R.",
        'story_insight': "**Wawasan Utama:**\nOLS adalah fondasi ekonometrika. Memahami diagnostik sangat penting untuk inferensi yang valid.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_researcher': "🎓 **Peneliti:** Analisis empiris dan pengujian hipotesis.",
        'use_analyst': "📊 **Analis Data:** Pemodelan prediktif dan peramalan.",
        'use_student': "📚 **Mahasiswa:** Belajar ekonometrika dengan alat nyata."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Sidebar for data source
with st.sidebar:
    st.markdown(f"### {txt['data_source']}")
    data_source = st.radio("", [txt['upload_data'], txt['generate_data']])
    
    if data_source == txt['upload_data']:
        uploaded_file = st.file_uploader(txt['upload_file'], type=['csv', 'xlsx'])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.session_state['data'] = df
                st.success(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
            except Exception as e:
                st.error(f"Error loading file: {e}")
    
    else:  # Generate synthetic data
        st.markdown(f"### {txt['model_type']}")
        model_type = st.selectbox("", [txt['demand'], txt['consumption'], txt['phillips'], txt['production']])
        
        n_samples = st.slider(txt['n_samples'], 50, 1000, 200)
        noise_level = st.slider(txt['noise_level'], 0.1, 10.0, 2.0)
        
        if st.button(txt['generate_btn'], type='primary'):
            np.random.seed(np.random.randint(0, 10000))
            
            if model_type == txt['demand']:
                # Q = 100 - 2*P + 0.5*Income + e
                P = np.random.uniform(10, 50, n_samples)
                Income = np.random.uniform(1000, 5000, n_samples)
                error = np.random.normal(0, noise_level, n_samples)
                Q = 100 - 2*P + 0.01*Income + error
                df = pd.DataFrame({'Quantity': Q, 'Price': P, 'Income': Income})
                
            elif model_type == txt['consumption']:
                # C = 50 + 0.8*Y - 0.02*Interest + e
                Y = np.random.uniform(1000, 10000, n_samples)
                Interest = np.random.uniform(2, 10, n_samples)
                error = np.random.normal(0, noise_level*10, n_samples)
                C = 50 + 0.8*Y - 20*Interest + error
                df = pd.DataFrame({'Consumption': C, 'Income': Y, 'Interest_Rate': Interest})
                
            elif model_type == txt['phillips']:
                # Inflation = 5 - 0.5*Unemployment + 0.3*Money_Growth + e
                Unemp = np.random.uniform(3, 12, n_samples)
                Money = np.random.uniform(0, 10, n_samples)
                error = np.random.normal(0, noise_level*0.5, n_samples)
                Inf = 5 - 0.5*Unemp + 0.3*Money + error
                df = pd.DataFrame({'Inflation': Inf, 'Unemployment': Unemp, 'Money_Growth': Money})
                
            else:  # Production function
                # Q = 10 + 0.5*K + 0.3*L + e (Cobb-Douglas linearized)
                K = np.random.uniform(10, 100, n_samples)
                L = np.random.uniform(10, 100, n_samples)
                error = np.random.normal(0, noise_level, n_samples)
                Q = 10 + 0.5*K + 0.3*L + error
                df = pd.DataFrame({'Output': Q, 'Capital': K, 'Labor': L})
            
            st.session_state['data'] = df
            st.success("✅ Data generated!")
            st.rerun()

# TABS
tab1, tab2, tab3 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3']])

# ========== TAB 1: DATA & REGRESSION ==========
with tab1:
    if 'data' in st.session_state:
        df = st.session_state['data']
        
        st.markdown(f"### {txt['data_preview']}")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        st.markdown(f"### {txt['select_vars']}")
        col1, col2 = st.columns(2)
        
        with col1:
            y_var = st.selectbox(txt['dependent_var'], edited_df.columns)
        
        with col2:
            x_vars = st.multiselect(txt['independent_vars'], 
                                    [col for col in edited_df.columns if col != y_var])
        
        if st.button(txt['run_regression'], type='primary') and len(x_vars) > 0:
            # Prepare data
            Y = edited_df[y_var].dropna()
            X = edited_df[x_vars].dropna()
            
            # Align indices
            common_idx = Y.index.intersection(X.index)
            Y = Y.loc[common_idx]
            X = X.loc[common_idx]
            
            # Add constant
            X_const = sm.add_constant(X)
            
            # Fit model
            model = sm.OLS(Y, X_const).fit()
            
            # Store in session state
            st.session_state['model'] = model
            st.session_state['Y'] = Y
            st.session_state['X'] = X
            st.session_state['y_var'] = y_var
            st.session_state['x_vars'] = x_vars
            
            # Display results
            st.markdown(f"### {txt['regression_results']}")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"#### {txt['coefficients']}")
                coef_df = pd.DataFrame({
                    'Variable': model.params.index,
                    'Coefficient': model.params.values,
                    'Std Error': model.bse.values,
                    't-statistic': model.tvalues.values,
                    'P-value': model.pvalues.values
                })
                st.dataframe(coef_df, use_container_width=True, hide_index=True)
                
                # Significance stars
                st.caption("*** p<0.01, ** p<0.05, * p<0.1")
            
            with col2:
                st.markdown(f"#### {txt['model_fit']}")
                
                m1, m2 = st.columns(2)
                m1.metric(txt['r_squared'], f"{model.rsquared:.4f}")
                m2.metric(txt['adj_r_squared'], f"{model.rsquared_adj:.4f}")
                
                m3, m4 = st.columns(2)
                m3.metric(txt['f_statistic'], f"{model.fvalue:.2f}")
                m4.metric(txt['prob_f'], f"{model.f_pvalue:.4f}")
                
                m5, m6 = st.columns(2)
                m5.metric(txt['aic'], f"{model.aic:.2f}")
                m6.metric(txt['bic'], f"{model.bic:.2f}")
            
            # Full summary
            with st.expander("📋 Full Regression Output"):
                st.text(model.summary())
            
            # Scatter plot with regression line (for single X)
            if len(x_vars) == 1:
                st.markdown("### Visualization")
                
                fig = go.Figure()
                
                # Scatter
                fig.add_trace(go.Scatter(
                    x=X[x_vars[0]],
                    y=Y,
                    mode='markers',
                    name='Actual',
                    marker=dict(size=8, opacity=0.6)
                ))
                
                # Regression line
                y_pred = model.predict(X_const)
                sorted_idx = X[x_vars[0]].argsort()
                fig.add_trace(go.Scatter(
                    x=X[x_vars[0]].iloc[sorted_idx],
                    y=y_pred.iloc[sorted_idx],
                    mode='lines',
                    name='Fitted',
                    line=dict(color='red', width=3)
                ))
                
                fig.update_layout(
                    title=f"{y_var} vs {x_vars[0]}",
                    xaxis_title=x_vars[0],
                    yaxis_title=y_var,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please upload data or generate synthetic data from the sidebar.")

# ========== TAB 2: DIAGNOSTICS ==========
with tab2:
    if 'model' in st.session_state:
        model = st.session_state['model']
        Y = st.session_state['Y']
        X = st.session_state['X']
        
        st.markdown(f"### {txt['diagnostic_tests']}")
        
        residuals = model.resid
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Normality test
            st.markdown(f"#### {txt['normality']}")
            jb_stat, jb_pvalue = stats.jarque_bera(residuals)
            
            if jb_pvalue > 0.05:
                st.success(f"✅ Residuals are normally distributed (p={jb_pvalue:.4f})")
            else:
                st.warning(f"⚠️ Residuals may not be normal (p={jb_pvalue:.4f})")
            
            st.caption(f"JB Statistic: {jb_stat:.4f}")
            
            # Heteroskedasticity test
            st.markdown(f"#### {txt['heteroskedasticity']}")
            try:
                X_const = sm.add_constant(X)
                bp_stat, bp_pvalue, _, _ = het_breuschpagan(residuals, X_const)
                
                if bp_pvalue > 0.05:
                    st.success(f"✅ Homoskedastic (p={bp_pvalue:.4f})")
                else:
                    st.warning(f"⚠️ Heteroskedasticity detected (p={bp_pvalue:.4f})")
                
                st.caption(f"BP Statistic: {bp_stat:.4f}")
            except:
                st.info("Could not perform Breusch-Pagan test")
        
        with col2:
            # Autocorrelation test
            st.markdown(f"#### {txt['autocorrelation']}")
            dw_stat = durbin_watson(residuals)
            
            if 1.5 < dw_stat < 2.5:
                st.success(f"✅ No autocorrelation (DW={dw_stat:.4f})")
            else:
                st.warning(f"⚠️ Possible autocorrelation (DW={dw_stat:.4f})")
            
            st.caption("DW ≈ 2 indicates no autocorrelation")
            
            # Multicollinearity (VIF)
            st.markdown(f"#### {txt['multicollinearity']}")
            if len(X.columns) > 1:
                from statsmodels.stats.outliers_influence import variance_inflation_factor
                
                vif_data = pd.DataFrame()
                vif_data["Variable"] = X.columns
                vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
                
                st.dataframe(vif_data, use_container_width=True, hide_index=True)
                
                if (vif_data["VIF"] > 10).any():
                    st.warning("⚠️ High multicollinearity detected (VIF > 10)")
                else:
                    st.success("✅ No severe multicollinearity (VIF < 10)")
            else:
                st.info("VIF requires multiple independent variables")
        
        # Interpretation guide
        with st.expander(txt['interpretation']):
            st.markdown("""
            **Diagnostic Tests Interpretation:**
            
            1. **Normality (Jarque-Bera)**:
               - H0: Residuals are normally distributed
               - If p > 0.05: Accept H0 (good)
               - If p < 0.05: Reject H0 (residuals not normal)
            
            2. **Heteroskedasticity (Breusch-Pagan)**:
               - H0: Homoskedasticity (constant variance)
               - If p > 0.05: Accept H0 (good)
               - If p < 0.05: Heteroskedasticity present
            
            3. **Autocorrelation (Durbin-Watson)**:
               - DW ≈ 2: No autocorrelation (good)
               - DW < 1.5: Positive autocorrelation
               - DW > 2.5: Negative autocorrelation
            
            4. **Multicollinearity (VIF)**:
               - VIF < 5: No problem
               - VIF 5-10: Moderate multicollinearity
               - VIF > 10: Severe multicollinearity
            """)
    else:
        st.info("Run regression first to see diagnostics.")

# ========== TAB 3: RESIDUAL ANALYSIS ==========
with tab3:
    if 'model' in st.session_state:
        model = st.session_state['model']
        Y = st.session_state['Y']
        
        st.markdown(f"### {txt['residual_plots']}")
        
        residuals = model.resid
        fitted = model.fittedvalues
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(txt['fitted_vs_residuals'], txt['qq_plot'], 
                          txt['histogram'], "Residuals Over Time")
        )
        
        # 1. Fitted vs Residuals
        fig.add_trace(go.Scatter(x=fitted, y=residuals, mode='markers', name='Residuals',
                                marker=dict(size=6, opacity=0.6)), row=1, col=1)
        fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=1)
        
        # 2. Q-Q Plot
        qq = stats.probplot(residuals, dist="norm")
        fig.add_trace(go.Scatter(x=qq[0][0], y=qq[0][1], mode='markers', name='Q-Q',
                                marker=dict(size=6, opacity=0.6)), row=1, col=2)
        fig.add_trace(go.Scatter(x=qq[0][0], y=qq[1][1] + qq[1][0]*qq[0][0], 
                                mode='lines', name='Normal', line=dict(color='red')), row=1, col=2)
        
        # 3. Histogram
        fig.add_trace(go.Histogram(x=residuals, name='Histogram', nbinsx=30), row=2, col=1)
        
        # 4. Residuals over time
        fig.add_trace(go.Scatter(y=residuals, mode='lines+markers', name='Time Series',
                                marker=dict(size=4)), row=2, col=2)
        fig.add_hline(y=0, line_dash="dash", line_color="red", row=2, col=2)
        
        fig.update_xaxes(title_text="Fitted Values", row=1, col=1)
        fig.update_yaxes(title_text="Residuals", row=1, col=1)
        fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=2)
        fig.update_yaxes(title_text="Sample Quantiles", row=1, col=2)
        fig.update_xaxes(title_text="Residuals", row=2, col=1)
        fig.update_xaxes(title_text="Observation", row=2, col=2)
        fig.update_yaxes(title_text="Residuals", row=2, col=2)
        
        fig.update_layout(height=800, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Residual statistics
        st.markdown("### Residual Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean", f"{residuals.mean():.4f}")
        col2.metric("Std Dev", f"{residuals.std():.4f}")
        col3.metric("Min", f"{residuals.min():.4f}")
        col4.metric("Max", f"{residuals.max():.4f}")
    else:
        st.info("Run regression first to see residual analysis.")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_researcher'])
        st.write(txt['use_analyst'])
        st.write(txt['use_student'])
