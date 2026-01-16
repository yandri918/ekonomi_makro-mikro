import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import statsmodels.api as sm

st.set_page_config(page_title="Econometrics Lab", page_icon="🧪", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🧪 Econometrics Lab",
        'intro': "Generate synthetic data and perform **Ordinary Least Squares (OLS)** regression analysis.",
        'setup': "Step 1: Data Setup",
        'dataset': "Select Dataset Type:",
        'demand': "Demand Function (Q = a - bP + e)",
        'consumption': "Consumption Function (C = c0 + MPC*Y + e)",
        'phillips': "Phillips Curve (Inf = a - b*Unemp + e)",
        'n_samples': "Number of Samples (N)",
        'noise': "Noise Level (Error Variance)",
        'gen_btn': "Generate New Data",
        'data_prev': "Step 2: Data Preview & Edit",
        'analysis': "Step 3: Regression Analysis",
        'run_ols': "Run OLS Regression",
        'results': "Regression Results",
        'params': "Estimated Parameters:",
        'intercept': "Intercept (const):",
        'slope': "Slope (beta):",
        'r2': "R-squared:",
        'summ': "Detailed Summary",
        'viz': "Visualization",
        'scatter': "Scatter Plot with Regression Line",
        'x_axis': "Independent Variable (X)",
        'y_axis': "Dependent Variable (Y)"
    },
    'ID': {
        'title': "🧪 Lab Ekonometrika",
        'intro': "Hasilkan data sintetis dan lakukan analisis regresi **Ordinary Least Squares (OLS)**.",
        'setup': "Langkah 1: Pengaturan Data",
        'dataset': "Pilih Jenis Dataset:",
        'demand': "Fungsi Permintaan (Q = a - bP + e)",
        'consumption': "Fungsi Konsumsi (C = c0 + MPC*Y + e)",
        'phillips': "Kurva Phillips (Inf = a - b*Unemp + e)",
        'n_samples': "Jumlah Sampel (N)",
        'noise': "Tingkat Noise (Varians Error)",
        'gen_btn': "Hasilkan Data Baru",
        'data_prev': "Langkah 2: Pratinjau & Edit Data",
        'analysis': "Langkah 3: Analisis Regresi",
        'run_ols': "Jalankan Regresi OLS",
        'results': "Hasil Regresi",
        'params': "Parameter Terestimasi:",
        'intercept': "Intersep (const):",
        'slope': "Kemiringan (beta):",
        'r2': "R-squared (Koef. Determinasi):",
        'summ': "Ringkasan Detail",
        'viz': "Visualisasi",
        'scatter': "Scatter Plot dengan Garis Regresi",
        'x_axis': "Variabel Independen (X)",
        'y_axis': "Variabel Dependen (Y)"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['intro'])

# --- 1. Data Generation ---
st.header(txt['setup'])
col1, col2 = st.columns(2)

with col1:
    model_type = st.selectbox(txt['dataset'], [
        "Demand Function", 
        "Consumption Function", 
        "Phillips Curve"
    ])
    
    # Map selection to ID/EN text key if needed, or just keep english keys for logic
    # Let's keep logic keys English but display could be localized if we wanted complete localization of dropdowns.
    # For now, English keys in dropdown are acceptable or we map them.
    
    n_samples = st.slider(txt['n_samples'], 20, 500, 100)
    noise_level = st.slider(txt['noise'], 0.1, 5.0, 1.0)

with col2:
    if st.button(txt['gen_btn']):
        np.random.seed(42) # For reproducibility
        X = np.zeros(n_samples)
        Y = np.zeros(n_samples)
        
        if model_type == "Demand Function":
            # Q = 100 - 2P + e
            X = np.random.uniform(5, 40, n_samples) # Price
            error = np.random.normal(0, noise_level * 2, n_samples)
            Y = 100 - 2 * X + error # Quantity
            x_label, y_label = "Price", "Quantity"
            
        elif model_type == "Consumption Function":
            # C = 50 + 0.8Y + e
            X = np.random.uniform(100, 1000, n_samples) # Income
            error = np.random.normal(0, noise_level * 10, n_samples)
            Y = 50 + 0.8 * X + error # Consumption
            x_label, y_label = "Income", "Consumption"
            
        elif model_type == "Phillips Curve":
            # Inf = 5 - 0.5 * Unemp + e
            X = np.random.uniform(2, 10, n_samples) # Unemployment
            error = np.random.normal(0, noise_level * 0.5, n_samples)
            Y = 5 - 0.5 * X + error # Inflation
            x_label, y_label = "Unemployment Rate (%)", "Inflation Rate (%)"
            
        st.session_state['data'] = pd.DataFrame({x_label: X, y_label: Y})
        st.session_state['x_label'] = x_label
        st.session_state['y_label'] = y_label
        st.success("Data Generated!")

# --- 2. Data Preview ---
if 'data' in st.session_state:
    st.header(txt['data_prev'])
    df = st.session_state['data']
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    x_col = st.session_state['x_label']
    y_col = st.session_state['y_label']
    
    # --- 3. Analysis ---
    st.header(txt['analysis'])
    
    if st.button(txt['run_ols']):
        X = edited_df[x_col]
        Y = edited_df[y_col]
        
        # Add constant
        X_const = sm.add_constant(X)
        
        model = sm.OLS(Y, X_const).fit()
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.subheader(txt['results'])
            st.markdown(txt['params'])
            st.write(f"- {txt['intercept']} **{model.params['const']:.4f}**")
            st.write(f"- {txt['slope']} **{model.params[x_col]:.4f}**")
            st.write(f"- {txt['r2']} **{model.rsquared:.4f}**")
            
            with st.expander(txt['summ']):
                st.text(model.summary())
                
        with c2:
            st.subheader(txt['viz'])
            
            # Predict lines
            edited_df['Predicted'] = model.predict(X_const)
            
            base = alt.Chart(edited_df).encode(x=x_col)
            
            scatter = base.mark_point().encode(
                y=y_col, tooltip=[x_col, y_col]
            ).properties(title=txt['scatter'])
            
            line = base.mark_line(color='red').encode(
                y='Predicted'
            )
            
            st.altair_chart((scatter + line).interactive(), use_container_width=True)

        
        with st.expander("Show Detailed Summary"):
            st.text(model.summary())
            
            st.warning("""
            **Note:** This is a simplified OLS regression.
            - **R-squared**: Explains the variability of the dependent variable.
            - **P-values**: Check the detailed summary to see if the relationship is statistically significant (P < 0.05).
            """)
    else:
        st.warning("Not enough data to run regression.")

