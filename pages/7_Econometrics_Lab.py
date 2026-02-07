import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, acorr_ljungbox, linear_reset
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import io

st.set_page_config(page_title="Professional Econometrics Lab", page_icon="🧪", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

# Translation dictionary
T = {
    'EN': {
        'title': "🧪 Professional Econometrics Lab",
        'subtitle': "Comprehensive OLS regression analysis with diagnostic tests, robust standard errors, and influence diagnostics.",
        'tab1': "📊 Data & Regression",
        'tab2': "🔍 Diagnostics",
        'tab3': "📈 Residual Analysis",
        'tab4': "🎯 Influence & Outliers",
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
        'use_robust': "Use Robust Standard Errors",
        'prediction': "Prediction & Confidence Intervals",
        'diagnostic_dashboard': "Diagnostic Dashboard",
        'diagnostic_tests': "Detailed Diagnostic Tests",
        'residual_plots': "Residual Analysis Plots",
        'influence_plots': "Influence Diagnostics",
    },
    'ID': {
        'title': "🧪 Lab Ekonometrika Profesional",
        'subtitle': "Analisis regresi OLS komprehensif dengan tes diagnostik, robust standard errors, dan diagnostik pengaruh.",
        'tab1': "📊 Data & Regresi",
        'tab2': "🔍 Diagnostik",
        'tab3': "📈 Analisis Residual",
        'tab4': "🎯 Pengaruh & Outlier",
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
        'use_robust': "Gunakan Robust Standard Errors",
        'prediction': "Prediksi & Interval Kepercayaan",
        'diagnostic_dashboard': "Dashboard Diagnostik",
        'diagnostic_tests': "Tes Diagnostik Detail",
        'residual_plots': "Plot Analisis Residual",
        'influence_plots': "Diagnostik Pengaruh",
    }
}

txt = T[lang]

# Header
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
                P = np.random.uniform(10, 50, n_samples)
                Income = np.random.uniform(1000, 5000, n_samples)
                error = np.random.normal(0, noise_level, n_samples)
                Q = 100 - 2*P + 0.01*Income + error
                df = pd.DataFrame({'Quantity': Q, 'Price': P, 'Income': Income})
                
            elif model_type == txt['consumption']:
                Y = np.random.uniform(1000, 10000, n_samples)
                Interest = np.random.uniform(2, 10, n_samples)
                error = np.random.normal(0, noise_level*10, n_samples)
                C = 50 + 0.8*Y - 20*Interest + error
                df = pd.DataFrame({'Consumption': C, 'Income': Y, 'Interest_Rate': Interest})
                
            elif model_type == txt['phillips']:
                Unemp = np.random.uniform(3, 12, n_samples)
                Money = np.random.uniform(0, 10, n_samples)
                error = np.random.normal(0, noise_level*0.5, n_samples)
                Inf = 5 - 0.5*Unemp + 0.3*Money + error
                df = pd.DataFrame({'Inflation': Inf, 'Unemployment': Unemp, 'Money_Growth': Money})
                
            else:  # Production function
                K = np.random.uniform(10, 100, n_samples)
                L = np.random.uniform(10, 100, n_samples)
                error = np.random.normal(0, noise_level, n_samples)
                Q = 10 + 0.5*K + 0.3*L + error
                df = pd.DataFrame({'Output': Q, 'Capital': K, 'Labor': L})
            
            st.session_state['data'] = df
            st.success("✅ Data generated!")
            st.rerun()

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

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
        
        # Robust SE option
        use_robust = st.checkbox(txt['use_robust'], value=False, 
                                 help="Use White heteroskedasticity-consistent standard errors (HC3)")
        
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
            
            # Robust covariance if requested
            if use_robust:
                model_robust = model.get_robustcov_results(cov_type='HC3')
            else:
                model_robust = None
            
            # Store in session state
            st.session_state['model'] = model
            st.session_state['model_robust'] = model_robust
            st.session_state['Y'] = Y
            st.session_state['X'] = X
            st.session_state['y_var'] = y_var
            st.session_state['x_vars'] = x_vars
            st.session_state['use_robust'] = use_robust
            
            # Display results
            st.markdown(f"### {txt['regression_results']}")
            
            # Choose which model to display (use robust if available and requested)
            display_model = model_robust if (use_robust and model_robust is not None) else model
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"#### {txt['coefficients']}")
                
                # Build coefficient table
                coef_df = pd.DataFrame({
                    'Variable': display_model.params.index,
                    'Coefficient': display_model.params.values,
                    'Std Error': display_model.bse.values,
                    't-statistic': display_model.tvalues.values,
                    'P-value': display_model.pvalues.values
                })
                
                # Add significance stars
                def add_stars(p):
                    if p < 0.01:
                        return '***'
                    elif p < 0.05:
                        return '**'
                    elif p < 0.1:
                        return '*'
                    return ''
                
                coef_df['Sig'] = coef_df['P-value'].apply(add_stars)
                
                st.dataframe(coef_df.style.format({
                    'Coefficient': '{:.4f}',
                    'Std Error': '{:.4f}',
                    't-statistic': '{:.4f}',
                    'P-value': '{:.4f}'
                }), use_container_width=True, hide_index=True)
                
                st.caption("*** p<0.01, ** p<0.05, * p<0.1")
                
                if use_robust:
                    st.info("✅ Using White robust standard errors (HC3)")
            
            with col2:
                st.markdown(f"#### {txt['model_fit']}")
                
                m1, m2 = st.columns(2)
                m1.metric("R²", f"{model.rsquared:.4f}",
                         help="Proportion of variance explained by the model")
                m2.metric("Adj R²", f"{model.rsquared_adj:.4f}",
                         help="R² adjusted for number of predictors")
                
                m3, m4 = st.columns(2)
                m3.metric("F-statistic", f"{model.fvalue:.2f}",
                         help="Test if all coefficients are zero")
                m4.metric("Prob (F)", f"{model.f_pvalue:.4f}",
                         help="P-value for F-test")
                
                m5, m6 = st.columns(2)
                m5.metric("AIC", f"{model.aic:.2f}",
                         help="Akaike Information Criterion (lower is better)")
                m6.metric("BIC", f"{model.bic:.2f}",
                         help="Bayesian Information Criterion (lower is better)")
                
                m7, m8 = st.columns(2)
                m7.metric("N", f"{int(model.nobs)}",
                         help="Number of observations")
                m8.metric("Df Residual", f"{int(model.df_resid)}",
                         help="Degrees of freedom for residuals")
            
            # Full summary
            with st.expander("📋 Full Regression Output"):
                if use_robust:
                    st.text(model_robust.summary())
                else:
                    st.text(model.summary())
            
            # Prediction & Confidence Intervals
            st.markdown(f"### {txt['prediction']}")
            
            # Get predictions with intervals
            predictions = model.get_prediction(X_const)
            pred_summary = predictions.summary_frame(alpha=0.05)
            
            # Visualization for single X
            if len(x_vars) == 1:
                fig = go.Figure()
                
                # Sort by X for clean lines
                sorted_idx = X[x_vars[0]].argsort()
                x_sorted = X[x_vars[0]].iloc[sorted_idx]
                y_sorted = Y.iloc[sorted_idx]
                pred_sorted = pred_summary.iloc[sorted_idx]
                
                # Confidence band (for mean)
                fig.add_trace(go.Scatter(
                    x=x_sorted,
                    y=pred_sorted['mean_ci_upper'],
                    mode='lines',
                    name='95% CI (Mean)',
                    line=dict(width=0),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=x_sorted,
                    y=pred_sorted['mean_ci_lower'],
                    mode='lines',
                    name='95% CI (Mean)',
                    fill='tonexty',
                    fillcolor='rgba(0,100,250,0.2)',
                    line=dict(width=0)
                ))
                
                # Prediction band (for individual obs)
                fig.add_trace(go.Scatter(
                    x=x_sorted,
                    y=pred_sorted['obs_ci_upper'],
                    mode='lines',
                    name='95% PI (Individual)',
                    line=dict(width=1, dash='dash', color='lightblue'),
                    showlegend=True
                ))
                
                fig.add_trace(go.Scatter(
                    x=x_sorted,
                    y=pred_sorted['obs_ci_lower'],
                    mode='lines',
                    name='95% PI (Individual)',
                    line=dict(width=1, dash='dash', color='lightblue'),
                    showlegend=False
                ))
                
                # Actual data
                fig.add_trace(go.Scatter(
                    x=X[x_vars[0]],
                    y=Y,
                    mode='markers',
                    name='Actual Data',
                    marker=dict(size=8, opacity=0.6, color='darkblue')
                ))
                
                # Fitted line
                fig.add_trace(go.Scatter(
                    x=x_sorted,
                    y=pred_sorted['mean'],
                    mode='lines',
                    name='Fitted Values',
                    line=dict(color='red', width=3)
                ))
                
                fig.update_layout(
                    title=f"{y_var} vs {x_vars[0]} with Confidence & Prediction Intervals",
                    xaxis_title=x_vars[0],
                    yaxis_title=y_var,
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("""
                **📊 Interpretation:**
                - **Blue shaded area:** 95% Confidence Interval for the **mean** prediction
                - **Dashed lines:** 95% Prediction Interval for **individual** observations
                - Prediction intervals are wider because they account for individual variation
                """)
            
            else:
                st.info("Prediction intervals visualization available for single independent variable models.")
                
                # Show prediction table for first 10 observations
                st.markdown("**Sample Predictions:**")
                pred_display = pred_summary[['mean', 'mean_se', 'mean_ci_lower', 'mean_ci_upper']].head(10)
                pred_display.columns = ['Predicted', 'SE', '95% CI Lower', '95% CI Upper']
                st.dataframe(pred_display.style.format('{:.4f}'), use_container_width=True)
    
    else:
        st.info("Please upload data or generate synthetic data from the sidebar.")

# ========== TAB 2: DIAGNOSTICS ==========
with tab2:
    if 'model' in st.session_state:
        model = st.session_state['model']
        Y = st.session_state['Y']
        X = st.session_state['X']
        use_robust = st.session_state.get('use_robust', False)
        
        residuals = model.resid
        X_const = sm.add_constant(X)
        
        # DIAGNOSTIC DASHBOARD
        st.markdown(f"### {txt['diagnostic_dashboard']}")
        
        # Run all tests
        tests_passed = 0
        tests_total = 0
        
        # 1. Normality (Jarque-Bera)
        jb_stat, jb_pvalue = stats.jarque_bera(residuals)
        normality_pass = jb_pvalue > 0.05
        tests_total += 1
        if normality_pass:
            tests_passed += 1
        
        # 2. Heteroskedasticity (Breusch-Pagan)
        try:
            bp_stat, bp_pvalue, _, _ = het_breuschpagan(residuals, X_const)
            bp_pass = bp_pvalue > 0.05
            bp_available = True
        except:
            bp_pass = None
            bp_available = False
        tests_total += 1
        if bp_pass:
            tests_passed += 1
        
        # 3. Heteroskedasticity (White)
        try:
            white_stat, white_pvalue, _, _ = het_white(residuals, X_const)
            white_pass = white_pvalue > 0.05
            white_available = True
        except:
            white_pass = None
            white_available = False
        tests_total += 1
        if white_pass:
            tests_passed += 1
        
        # 4. Autocorrelation (Durbin-Watson)
        dw_stat = durbin_watson(residuals)
        dw_pass = 1.5 < dw_stat < 2.5
        tests_total += 1
        if dw_pass:
            tests_passed += 1
        
        # 5. Autocorrelation (Ljung-Box)
        try:
            lb_test = acorr_ljungbox(residuals, lags=min(10, len(residuals)//5), return_df=True)
            lb_pass = (lb_test['lb_pvalue'] > 0.05).all()
            lb_available = True
        except:
            lb_pass = None
            lb_available = False
        tests_total += 1
        if lb_pass:
            tests_passed += 1
        
        # 6. Specification (RESET)
        try:
            reset_stat, reset_pvalue = linear_reset(model, power=2, use_f=True)
            reset_pass = reset_pvalue > 0.05
            reset_available = True
        except:
            reset_pass = None
            reset_available = False
        tests_total += 1
        if reset_pass:
            tests_passed += 1
        
        # 7. Multicollinearity (VIF)
        if len(X.columns) > 1:
            vif_data = pd.DataFrame()
            vif_data["Variable"] = X.columns
            vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
            vif_pass = (vif_data["VIF"] < 10).all()
            vif_available = True
        else:
            vif_pass = None
            vif_available = False
        tests_total += 1
        if vif_pass:
            tests_passed += 1
        
        # Dashboard summary
        if tests_passed == tests_total:
            status_color = "green"
            status_icon = "✅"
            status_text = "EXCELLENT"
        elif tests_passed >= tests_total * 0.7:
            status_color = "orange"
            status_icon = "⚠️"
            status_text = "CAUTION"
        else:
            status_color = "red"
            status_icon = "🚨"
            status_text = "WARNING"
        
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h3 style='color: white; margin: 0;'>{status_icon} Overall Status: {status_text}</h3>
            <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
                <b>{tests_passed}/{tests_total}</b> diagnostic tests passed
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if normality_pass:
                col1.success(f"✅ **Normality**\np={jb_pvalue:.4f}")
            else:
                col1.warning(f"⚠️ **Normality**\np={jb_pvalue:.4f}")
        
        with col2:
            if bp_available:
                if bp_pass:
                    col2.success(f"✅ **Homoskedasticity**\n(BP: p={bp_pvalue:.4f})")
                else:
                    col2.warning(f"⚠️ **Heteroskedasticity**\n(BP: p={bp_pvalue:.4f})")
            else:
                col2.info("BP test unavailable")
        
        with col3:
            if dw_pass:
                col3.success(f"✅ **No Autocorr**\nDW={dw_stat:.4f}")
            else:
                col3.warning(f"⚠️ **Autocorrelation**\nDW={dw_stat:.4f}")
        
        with col4:
            if vif_available:
                if vif_pass:
                    col4.success(f"✅ **No Multicollin**\nMax VIF={vif_data['VIF'].max():.2f}")
                else:
                    col4.warning(f"⚠️ **Multicollinearity**\nMax VIF={vif_data['VIF'].max():.2f}")
            else:
                col4.info("VIF: Single X")
        
        st.divider()
        
        # DETAILED DIAGNOSTIC TESTS
        st.markdown(f"### {txt['diagnostic_tests']}")
        
        # Normality Tests
        with st.expander("📊 **Normality Tests**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Jarque-Bera Test")
                st.metric("JB Statistic", f"{jb_stat:.4f}")
                st.metric("P-value", f"{jb_pvalue:.4f}")
                
                if jb_pvalue > 0.05:
                    st.success("✅ Residuals are normally distributed")
                else:
                    st.warning("⚠️ Residuals may not be normal")
                
                st.caption("""
                **H₀:** Residuals are normally distributed  
                **Decision:** Reject H₀ if p < 0.05
                """)
            
            with col2:
                st.markdown("#### What does this mean?")
                st.info("""
                **Normality** is required for:
                - Valid t-tests and F-tests
                - Accurate confidence intervals
                
                **If test fails:**
                - Check for outliers
                - Try transforming Y (log, sqrt)
                - Use robust standard errors
                - Bootstrap confidence intervals
                
                **Note:** With large samples (n>100), slight non-normality is often okay due to Central Limit Theorem.
                """)
        
        # Heteroskedasticity Tests
        with st.expander("📈 **Heteroskedasticity Tests**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Breusch-Pagan Test")
                if bp_available:
                    st.metric("BP Statistic", f"{bp_stat:.4f}")
                    st.metric("P-value", f"{bp_pvalue:.4f}")
                    
                    if bp_pvalue > 0.05:
                        st.success("✅ Homoskedastic (constant variance)")
                    else:
                        st.warning("⚠️ Heteroskedasticity detected")
                else:
                    st.info("Test unavailable")
                
                st.markdown("#### White Test")
                if white_available:
                    st.metric("White Statistic", f"{white_stat:.4f}")
                    st.metric("P-value", f"{white_pvalue:.4f}")
                    
                    if white_pvalue > 0.05:
                        st.success("✅ Homoskedastic")
                    else:
                        st.warning("⚠️ Heteroskedasticity detected")
                else:
                    st.info("Test unavailable")
            
            with col2:
                st.markdown("#### What does this mean?")
                st.info("""
                **Heteroskedasticity** means error variance is not constant.
                
                **Consequences:**
                - OLS estimates still unbiased
                - Standard errors are WRONG
                - t-tests and F-tests invalid
                
                **Solutions:**
                1. ✅ **Use Robust Standard Errors** (White/HC3)
                   - Check the box in Tab 1
                   - This fixes inference without changing estimates
                
                2. Try transformations (log Y)
                
                3. Weighted Least Squares (WLS)
                
                4. Add polynomial terms
                """)
                
                if not use_robust and (not bp_pass or not white_pass):
                    st.error("🚨 **Action Required:** Enable 'Use Robust Standard Errors' in Tab 1!")
        
        # Autocorrelation Tests
        with st.expander("🔄 **Autocorrelation Tests**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Durbin-Watson Test")
                st.metric("DW Statistic", f"{dw_stat:.4f}")
                
                if 1.5 < dw_stat < 2.5:
                    st.success("✅ No autocorrelation")
                elif dw_stat < 1.5:
                    st.warning("⚠️ Positive autocorrelation")
                else:
                    st.warning("⚠️ Negative autocorrelation")
                
                st.caption("DW ≈ 2 indicates no autocorrelation")
                
                st.markdown("#### Ljung-Box Test")
                if lb_available:
                    st.dataframe(lb_test[['lb_stat', 'lb_pvalue']].head(5), use_container_width=True)
                    
                    if lb_pass:
                        st.success("✅ No autocorrelation at any lag")
                    else:
                        st.warning("⚠️ Autocorrelation detected")
                else:
                    st.info("Test unavailable")
            
            with col2:
                st.markdown("#### What does this mean?")
                st.info("""
                **Autocorrelation** means errors are correlated over time.
                
                **Common in:**
                - Time series data
                - Panel data
                
                **Consequences:**
                - OLS estimates still unbiased
                - Standard errors are WRONG
                - Confidence intervals too narrow
                
                **Solutions:**
                1. Use HAC standard errors (Newey-West)
                
                2. Add lagged dependent variable
                
                3. Include time trend
                
                4. Check for omitted variables
                
                5. Use ARIMA or time series models
                """)
        
        # Specification Test
        with st.expander("🔧 **Specification Test (RESET)**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Ramsey RESET Test")
                if reset_available:
                    st.metric("F-statistic", f"{reset_stat:.4f}")
                    st.metric("P-value", f"{reset_pvalue:.4f}")
                    
                    if reset_pvalue > 0.05:
                        st.success("✅ Model specification appears correct")
                    else:
                        st.warning("⚠️ Possible specification error")
                else:
                    st.info("Test unavailable")
            
            with col2:
                st.markdown("#### What does this mean?")
                st.info("""
                **RESET Test** checks if your model is missing:
                - Non-linear terms (X², X³)
                - Interaction terms (X₁ × X₂)
                - Important variables
                
                **If test fails:**
                1. Add polynomial terms (X²)
                
                2. Try log transformation
                
                3. Add interaction terms
                
                4. Check for omitted variables
                
                5. Consider non-linear models
                """)
        
        # Multicollinearity
        with st.expander("🔗 **Multicollinearity (VIF)**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Variance Inflation Factor")
                if vif_available:
                    st.dataframe(vif_data.style.format({'VIF': '{:.2f}'}), 
                               use_container_width=True, hide_index=True)
                    
                    if (vif_data["VIF"] > 10).any():
                        st.warning("⚠️ High multicollinearity (VIF > 10)")
                    elif (vif_data["VIF"] > 5).any():
                        st.info("ℹ️ Moderate multicollinearity (VIF 5-10)")
                    else:
                        st.success("✅ No severe multicollinearity (VIF < 5)")
                else:
                    st.info("VIF requires multiple independent variables")
            
            with col2:
                st.markdown("#### What does this mean?")
                st.info("""
                **Multicollinearity** means X variables are highly correlated.
                
                **VIF Interpretation:**
                - VIF < 5: No problem ✅
                - VIF 5-10: Moderate concern ⚠️
                - VIF > 10: Severe problem 🚨
                
                **Consequences:**
                - Estimates still unbiased
                - Standard errors inflated
                - Coefficients unstable
                - Hard to isolate individual effects
                
                **Solutions:**
                1. Drop one of the correlated variables
                
                2. Combine correlated variables (PCA)
                
                3. Collect more data
                
                4. Accept it (if prediction is the goal)
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
        influence = model.get_influence()
        standardized_resid = influence.resid_studentized_internal
        
        # Create enhanced subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Residuals vs Fitted",
                "Q-Q Plot (Normality)",
                "Scale-Location (Homoskedasticity)",
                "Residuals Histogram"
            )
        )
        
        # 1. Residuals vs Fitted
        fig.add_trace(go.Scatter(
            x=fitted, 
            y=residuals, 
            mode='markers',
            name='Residuals',
            marker=dict(size=6, opacity=0.6, color='darkblue')
        ), row=1, col=1)
        fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=1)
        
        # Add LOWESS smoothing
        from scipy.signal import savgol_filter
        if len(fitted) > 10:
            sorted_idx = fitted.argsort()
            fitted_sorted = fitted.iloc[sorted_idx]
            resid_sorted = residuals.iloc[sorted_idx]
            try:
                smoothed = savgol_filter(resid_sorted, window_length=min(51, len(fitted)//3*2+1), polyorder=3)
                fig.add_trace(go.Scatter(
                    x=fitted_sorted,
                    y=smoothed,
                    mode='lines',
                    name='Trend',
                    line=dict(color='orange', width=2)
                ), row=1, col=1)
            except:
                pass
        
        # 2. Q-Q Plot
        qq = stats.probplot(residuals, dist="norm")
        fig.add_trace(go.Scatter(
            x=qq[0][0], 
            y=qq[0][1], 
            mode='markers',
            name='Q-Q',
            marker=dict(size=6, opacity=0.6, color='darkblue')
        ), row=1, col=2)
        fig.add_trace(go.Scatter(
            x=qq[0][0], 
            y=qq[1][1] + qq[1][0]*qq[0][0],
            mode='lines',
            name='Normal',
            line=dict(color='red', width=2)
        ), row=1, col=2)
        
        # 3. Scale-Location (sqrt of standardized residuals)
        sqrt_abs_std_resid = np.sqrt(np.abs(standardized_resid))
        fig.add_trace(go.Scatter(
            x=fitted,
            y=sqrt_abs_std_resid,
            mode='markers',
            name='Scale-Location',
            marker=dict(size=6, opacity=0.6, color='darkblue')
        ), row=2, col=1)
        
        # Add trend line
        if len(fitted) > 10:
            try:
                sorted_idx = fitted.argsort()
                fitted_sorted = fitted.iloc[sorted_idx]
                sqrt_sorted = sqrt_abs_std_resid.iloc[sorted_idx]
                smoothed = savgol_filter(sqrt_sorted, window_length=min(51, len(fitted)//3*2+1), polyorder=3)
                fig.add_trace(go.Scatter(
                    x=fitted_sorted,
                    y=smoothed,
                    mode='lines',
                    name='Trend',
                    line=dict(color='orange', width=2)
                ), row=2, col=1)
            except:
                pass
        
        # 4. Histogram
        fig.add_trace(go.Histogram(
            x=residuals,
            name='Histogram',
            nbinsx=30,
            marker=dict(color='darkblue', opacity=0.7)
        ), row=2, col=2)
        
        # Add normal curve overlay
        x_range = np.linspace(residuals.min(), residuals.max(), 100)
        normal_curve = stats.norm.pdf(x_range, residuals.mean(), residuals.std())
        # Scale to match histogram
        normal_curve = normal_curve * len(residuals) * (residuals.max() - residuals.min()) / 30
        fig.add_trace(go.Scatter(
            x=x_range,
            y=normal_curve,
            mode='lines',
            name='Normal',
            line=dict(color='red', width=2)
        ), row=2, col=2)
        
        # Update axes
        fig.update_xaxes(title_text="Fitted Values", row=1, col=1)
        fig.update_yaxes(title_text="Residuals", row=1, col=1)
        fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=2)
        fig.update_yaxes(title_text="Sample Quantiles", row=1, col=2)
        fig.update_xaxes(title_text="Fitted Values", row=2, col=1)
        fig.update_yaxes(title_text="√|Standardized Residuals|", row=2, col=1)
        fig.update_xaxes(title_text="Residuals", row=2, col=2)
        fig.update_yaxes(title_text="Frequency", row=2, col=2)
        
        fig.update_layout(height=800, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation guide
        with st.expander("📚 How to Interpret These Plots"):
            st.markdown("""
            ### 1. Residuals vs Fitted
            **What to look for:**
            - Random scatter around zero ✅
            - No patterns (U-shape, funnel) ⚠️
            
            **If you see:**
            - **Funnel shape:** Heteroskedasticity → Use robust SE
            - **U-shape:** Non-linearity → Add polynomial terms
            - **Outliers:** Check influential points in Tab 4
            
            ### 2. Q-Q Plot
            **What to look for:**
            - Points follow the red line ✅
            - Deviations at tails are common
            
            **If you see:**
            - **S-curve:** Heavy tails → Consider robust regression
            - **Systematic deviation:** Non-normality → Transform Y
            
            ### 3. Scale-Location
            **What to look for:**
            - Horizontal line ✅
            - Equal spread across fitted values
            
            **If you see:**
            - **Upward/downward trend:** Heteroskedasticity
            - **Funnel:** Variance increases with fitted values
            
            ### 4. Histogram
            **What to look for:**
            - Bell-shaped curve ✅
            - Matches red normal curve
            
            **If you see:**
            - **Skewed:** Transform Y (log, sqrt)
            - **Bimodal:** Missing categorical variable
            """)
        
        # Residual statistics
        st.markdown("### Residual Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Mean", f"{residuals.mean():.6f}",
                   help="Should be close to zero")
        col2.metric("Std Dev", f"{residuals.std():.4f}",
                   help="Measure of model error")
        col3.metric("Min", f"{residuals.min():.4f}")
        col4.metric("Max", f"{residuals.max():.4f}")
        col5.metric("Range", f"{residuals.max() - residuals.min():.4f}")
    
    else:
        st.info("Run regression first to see residual analysis.")

# ========== TAB 4: INFLUENCE & OUTLIERS ==========
with tab4:
    if 'model' in st.session_state:
        model = st.session_state['model']
        Y = st.session_state['Y']
        X = st.session_state['X']
        
        st.markdown(f"### {txt['influence_plots']}")
        
        influence = model.get_influence()
        
        # Cook's Distance
        cooks_d = influence.cooks_distance[0]
        leverage = influence.hat_matrix_diag
        standardized_resid = influence.resid_studentized_internal
        
        # Thresholds
        cooks_threshold = 4 / len(X)
        leverage_threshold = 2 * (len(X.columns) + 1) / len(X)
        
        # Identify influential points
        influential_cooks = cooks_d > cooks_threshold
        high_leverage = leverage > leverage_threshold
        outliers = np.abs(standardized_resid) > 2
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Influential Points", f"{influential_cooks.sum()}",
                   help=f"Cook's D > {cooks_threshold:.4f}")
        col2.metric("High Leverage", f"{high_leverage.sum()}",
                   help=f"Leverage > {leverage_threshold:.4f}")
        col3.metric("Outliers", f"{outliers.sum()}",
                   help="|Std Residual| > 2")
        col4.metric("Problematic", f"{(influential_cooks & high_leverage).sum()}",
                   help="Both influential AND high leverage")
        
        st.divider()
        
        # Create influence plots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Cook's Distance", "Leverage vs Standardized Residuals")
        )
        
        # 1. Cook's Distance
        colors = ['red' if x else 'blue' for x in influential_cooks]
        fig.add_trace(go.Bar(
            x=list(range(len(cooks_d))),
            y=cooks_d,
            name="Cook's D",
            marker=dict(color=colors, opacity=0.7)
        ), row=1, col=1)
        fig.add_hline(y=cooks_threshold, line_dash="dash", line_color="red", 
                     annotation_text=f"Threshold ({cooks_threshold:.4f})", row=1, col=1)
        
        # 2. Leverage vs Residuals
        colors = []
        for i in range(len(leverage)):
            if influential_cooks[i] and high_leverage[i]:
                colors.append('red')  # Most problematic
            elif high_leverage[i]:
                colors.append('orange')  # High leverage
            elif outliers[i]:
                colors.append('yellow')  # Outlier
            else:
                colors.append('blue')  # Normal
        
        fig.add_trace(go.Scatter(
            x=leverage,
            y=standardized_resid,
            mode='markers',
            name='Observations',
            marker=dict(size=8, color=colors, opacity=0.7),
            text=[f"Obs {i}" for i in range(len(leverage))],
            hovertemplate='<b>%{text}</b><br>Leverage: %{x:.4f}<br>Std Residual: %{y:.4f}'
        ), row=1, col=2)
        
        # Add threshold lines
        fig.add_hline(y=2, line_dash="dash", line_color="red", row=1, col=2)
        fig.add_hline(y=-2, line_dash="dash", line_color="red", row=1, col=2)
        fig.add_vline(x=leverage_threshold, line_dash="dash", line_color="red", row=1, col=2)
        
        # Update axes
        fig.update_xaxes(title_text="Observation Index", row=1, col=1)
        fig.update_yaxes(title_text="Cook's Distance", row=1, col=1)
        fig.update_xaxes(title_text="Leverage", row=1, col=2)
        fig.update_yaxes(title_text="Standardized Residuals", row=1, col=2)
        
        fig.update_layout(height=500, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation
        with st.expander("📚 Understanding Influence Diagnostics"):
            st.markdown("""
            ### Cook's Distance
            **Measures:** How much fitted values change if observation is removed
            
            **Threshold:** 4/n = {:.4f}
            
            **Interpretation:**
            - **High Cook's D:** Observation is influential
            - **Action:** Investigate why (data error? genuine outlier?)
            
            ### Leverage
            **Measures:** How far X values are from mean
            
            **Threshold:** 2(k+1)/n = {:.4f}
            
            **Interpretation:**
            - **High leverage:** Unusual X values
            - **Not necessarily bad** if residual is small
            
            ### Quadrant Analysis (Right Plot)
            - **Top-right (RED):** 🚨 Most problematic - High leverage + outlier
            - **Top-left (YELLOW):** Outlier but low leverage
            - **Bottom-right (ORANGE):** High leverage but not outlier
            - **Bottom-left (BLUE):** Normal observations
            
            ### What to Do?
            1. **Investigate red points** - Check for data entry errors
            2. **Re-run without influential points** - See if results change
            3. **Report sensitivity** - "Results robust to outlier removal"
            4. **Consider robust regression** - Less sensitive to outliers
            """.format(cooks_threshold, leverage_threshold))
        
        # List of influential observations
        if influential_cooks.sum() > 0:
            st.markdown("### Influential Observations")
            
            influential_df = pd.DataFrame({
                'Index': np.where(influential_cooks)[0],
                "Cook's D": cooks_d[influential_cooks],
                'Leverage': leverage[influential_cooks],
                'Std Residual': standardized_resid[influential_cooks]
            }).sort_values("Cook's D", ascending=False)
            
            st.dataframe(influential_df.style.format({
                "Cook's D": '{:.4f}',
                'Leverage': '{:.4f}',
                'Std Residual': '{:.4f}'
            }), use_container_width=True, hide_index=True)
            
            st.warning("""
            ⚠️ **Recommendation:** Investigate these observations:
            1. Check for data entry errors
            2. Verify if they represent genuine outliers
            3. Re-run regression without them to check sensitivity
            4. Consider using robust regression methods
            """)
    
    else:
        st.info("Run regression first to see influence diagnostics.")

# Footer
st.divider()
st.caption("🧪 **Professional Econometrics Lab** - Built with statsmodels, scipy, and plotly")
st.caption("💡 **Tip:** Use robust standard errors when heteroskedasticity is detected for valid inference!")
