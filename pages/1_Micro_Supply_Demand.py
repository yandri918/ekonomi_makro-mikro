import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Supply & Demand", page_icon="⚖️", layout="wide")

st.title("⚖️ Microeconomics: Supply, Demand & Elasticity")

tab1, tab2 = st.tabs(["📉 Supply & Demand Simulation", "🧮 Elasticity Calculator"])

# --- TAB 1: SUPPLY & DEMAND ---
with tab1:
    st.markdown("### 1. Market Equilibrium Simulator")
    st.markdown("Adjust the slopes and intercepts to see how **Supply** and **Demand** shifts affect the equilibrium price ($P^*$) and quantity ($Q^*$).")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ Parameters")
        
        st.markdown("**Demand Function:** $Q_d = a - bP$")
        a = st.slider("Demand Intercept (a) - Shift Demand", 50, 200, 100, help="Changes consumer willingness to buy (Income, Tastes)")
        b = st.slider("Demand Slope (b) - Elasticity", 0.5, 5.0, 1.0, step=0.1, help="Responsiveness of consumers to price changes")
        
        st.markdown("---")
        
        st.markdown("**Supply Function:** $Q_s = c + dP$")
        c = st.slider("Supply Intercept (c) - Shift Supply", 0, 100, 20, help="Changes production costs/technology")
        d = st.slider("Supply Slope (d) - Elasticity", 0.5, 5.0, 1.0, step=0.1, help="Responsiveness of producers to price changes")

    with col2:
        # 1. Calculate Equilibrium
        if c >= a:
            st.error("Supply Intercept must be lower than Demand Intercept for a valid market!")
            P_eq = 0
            Q_eq = 0
        else:
            P_eq = (a - c) / (b + d)
            Q_eq = a - b * P_eq

        # 2. Generate Data for Plotting
        # Create a price range around the equilibrium
        P_max = (a / b) if b > 0 else 100
        prices = np.linspace(0, max(P_max, P_eq * 1.5), 100)
        
        df = pd.DataFrame({'Price': prices})
        df['Demand'] = a - b * df['Price']
        df['Supply'] = c + d * df['Price']
        
        # Filter negative quantities
        df = df[(df['Demand'] >= 0) & (df['Supply'] >= 0)]
        
        # Melt for Altair
        df_melted = df.melt('Price', var_name='Type', value_name='Quantity')

        # 3. Plotting
        base = alt.Chart(df_melted).encode(
            x=alt.X('Quantity', title='Quantity (Q)'),
            y=alt.Y('Price', title='Price (P)')
        )
        
        lines = base.mark_line(size=3).encode(
            color=alt.Color('Type', scale=alt.Scale(domain=['Demand', 'Supply'], range=['#FF4B4B', '#1C83E1']))
        )
        
        # Equilibrium Point
        eq_point = alt.Chart(pd.DataFrame({'Price': [P_eq], 'Quantity': [Q_eq]})).mark_point(
            size=200, fill='black', color='black'
        ).encode(
            x='Quantity', y='Price',
            tooltip=[alt.Tooltip('Price', format=',.2f'), alt.Tooltip('Quantity', format=',.2f')]
        )
        
        # Text labels for Equilibrium
        eq_text = eq_point.mark_text(
            align='left', baseline='bottom', dx=7, dy=-7, fontSize=14
        ).encode(
            text=alt.value(f"E ({Q_eq:.1f}, {P_eq:.1f})")
        )

        st.altair_chart((lines + eq_point + eq_text).interactive(), use_container_width=True)

        st.info(f"""
        **Market Equilibrium:**
        - **Price ($P^*$):** {P_eq:.2f}
        - **Quantity ($Q^*$):** {Q_eq:.2f}
        """)

# --- TAB 2: ELASTICITY ---
with tab2:
    st.markdown("### 2. Elasticity Calculator")
    st.markdown("Calculate **Price Elasticity of Demand (PED)** using the Midpoint Method.")
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        P1 = st.number_input("Initial Price (P1)", value=10.0)
        P2 = st.number_input("New Price (P2)", value=12.0)
        
    with col_e2:
        Q1 = st.number_input("Initial Quantity (Q1)", value=100.0)
        Q2 = st.number_input("New Quantity (Q2)", value=80.0)
        
    if st.button("Calculate Elasticity"):
        # Midpoint Formula
        delta_Q = Q2 - Q1
        avg_Q = (Q2 + Q1) / 2
        pct_change_Q = delta_Q / avg_Q
        
        delta_P = P2 - P1
        avg_P = (P2 + P1) / 2
        pct_change_P = delta_P / avg_P
        
        if pct_change_P == 0:
            st.error("Price change cannot be zero.")
        else:
            PED = abs(pct_change_Q / pct_change_P)
            
            st.metric("Price Elasticity of Demand (|Ed|)", f"{PED:.2f}")
            
            if PED > 1:
                st.success("Result: **ELASTIC** (Consumers are sensitive to price changes)")
            elif PED < 1:
                st.warning("Result: **INELASTIC** (Consumers are not very sensitive)")
            else:
                st.info("Result: **UNITARY ELASTIC**")
                
            st.latex(r"E_d = \left| \frac{\% \Delta Q}{\% \Delta P} \right| = \left| \frac{(Q_2 - Q_1) / [(Q_2 + Q_1)/2]}{(P_2 - P_1) / [(P_2 + P_1)/2]} \right|")

