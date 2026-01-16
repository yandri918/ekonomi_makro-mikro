import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import statsmodels.api as sm

st.set_page_config(page_title="Econometrics Lab", page_icon="🧪", layout="wide")

st.title("🧪 Econometrics Lab: Regression Analysis")
st.markdown("Estimate economic relationships using **Ordinary Least Squares (OLS)** regression.")

# Helper to generate data
def generate_data(type_data):
    np.random.seed(42)
    n = 50
    if type_data == "Demand Function (Q vs P)":
        X = np.random.uniform(10, 50, n) # Price
        # Q = 100 - 2P + error
        Y = 100 - 1.5 * X + np.random.normal(0, 5, n)
        return pd.DataFrame({'Price (P)': X, 'Quantity (Q)': Y})
    elif type_data == "Consumption Function (C vs Y)":
        X = np.random.uniform(2000, 5000, n) # Income
        # C = 500 + 0.8Y + error
        Y = 500 + 0.8 * X + np.random.normal(0, 100, n)
        return pd.DataFrame({'Income (Y)': X, 'Consumption (C)': Y})
    elif type_data == "Phillips Curve (Inf vs Unemp)":
        X = np.random.uniform(3, 8, n) # Unemployment
        # Inf = 5 - 0.5 * U + error
        Y = 8 - 0.8 * X + np.random.normal(0, 0.5, n)
        return pd.DataFrame({'Unemployment (%)': X, 'Inflation (%)': Y})
    else:
        return pd.DataFrame({'X': range(10), 'Y': range(10)})

# Main Interface
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Data Selection")
    model_type = st.selectbox("Choose Economic Model", ["Demand Function (Q vs P)", "Consumption Function (C vs Y)", "Phillips Curve (Inf vs Unemp)"])
    
    if st.button("🔄 Generate New Sample Data"):
        # Just clears cache implicitly by rerunning
        st.cache_data.clear()
        
    df = generate_data(model_type)
    
    st.markdown("### 2. Edit Data")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

with col2:
    st.subheader("3. Regression Results")
    
    if not edited_df.empty and len(edited_df) > 2:
        # Identify X and Y
        cols = edited_df.columns
        X_col = cols[0]
        Y_col = cols[1]
        
        X = edited_df[X_col]
        Y = edited_df[Y_col]
        
        # Add constant
        X_const = sm.add_constant(X)
        
        # Fit OLS
        model = sm.OLS(Y, X_const).fit()
        predictions = model.predict(X_const)
        
        # Add predictions to df for plotting
        plot_df = edited_df.copy()
        plot_df['Fitted'] = predictions
        
        # Display Equation
        intercept = model.params['const']
        slope = model.params[X_col]
        r_squared = model.rsquared
        
        st.success(f"**Estimated Equation:** ${Y_col.split(' ')[0]} = {intercept:.2f} + {slope:.2f} ({X_col.split(' ')[0]})$")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Intercept (α)", f"{intercept:.4f}")
        m2.metric("Slope (β)", f"{slope:.4f}")
        m3.metric("R-squared", f"{r_squared:.4f}")
        
        # Altair Plot
        base = alt.Chart(plot_df).encode(x=X_col)
        
        scatter = base.mark_circle(size=60, color='steelblue', opacity=0.6).encode(
            y=Y_col,
            tooltip=[X_col, Y_col]
        )
        
        line = base.mark_line(color='red', size=3).encode(
            y='Fitted'
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

