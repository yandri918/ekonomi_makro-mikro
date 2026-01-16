import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Public Policy", page_icon="🏛️", layout="wide")

st.title("🏛️ Public Policy & Welfare Analysis")
st.markdown("Simulate the effects of government intervention: **Taxes, Subsidies,** and **Price Controls** on Market Welfare.")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🛠️ Policy Settings")
    policy = st.selectbox("Select Policy Type", ["None", "Tax (Per Unit)", "Subsidy (Per Unit)", "Price Floor (Min Wage)", "Price Ceiling"])
    
    st.markdown("---")
    st.markdown("**Market Parameters**")
    a = st.number_input("Demand Intercept (a)", value=100)
    b = st.number_input("Demand Slope (b)", value=1.0)
    c = st.number_input("Supply Intercept (c)", value=10)
    d = st.number_input("Supply Slope (d)", value=1.0)
    
    magnitude = 0.0
    if policy == "Tax (Per Unit)":
        magnitude = st.slider("Tax Amount", 0, 50, 10)
    elif policy == "Subsidy (Per Unit)":
        magnitude = st.slider("Subsidy Amount", 0, 50, 10)
    elif policy == "Price Floor (Min Wage)":
        magnitude = st.slider("Price Floor Level", 0, 100, 60)
    elif policy == "Price Ceiling":
        magnitude = st.slider("Price Ceiling Level", 0, 100, 40)

with col2:
    # 1. Base Equilibrium
    if b+d == 0:
        P_eq, Q_eq = 0, 0
    else:
        P_eq = (a - c) / (b + d)
        Q_eq = a - b * P_eq

    # 2. Policy Impact
    Q_new, P_cons, P_prod, DWL, Gov_Rev_Cost = 0, 0, 0, 0, 0
    type_label = "Base"
    
    if policy == "None":
        Q_new = Q_eq
        P_cons = P_eq
        P_prod = P_eq
        
    elif policy == "Tax (Per Unit)":
        # Supply shifts up by Tax: P = (c+Tax)/d + (1/d)Q ... careful with inv supply P = (Q-c)/d
        # Qs = c + d(P - Tax) -> P_supply_curve_effective = P_market - Tax
        # Easier: Pd = Ps + Tax
        # Q = a - b(Ps + Tax) = c + dPs
        # a - bPs - bTax = c + dPs
        # Ps(b+d) = a - bTax - c
        P_prod = (a - c - b*magnitude) / (b + d)
        Q_new = c + d * P_prod
        P_cons = P_prod + magnitude
        type_label = "Tax"
        
        DWL = 0.5 * (Q_eq - Q_new) * magnitude
        Gov_Rev_Cost = magnitude * Q_new
        
    elif policy == "Subsidy (Per Unit)":
        # Ps = Pd + Subsidy
        # Q = a - bPd = c + d(Pd + Subsidy)
        # a - bPd = c + dPd + dSub
        # Pd(b+d) = a - c - dSub
        P_cons = (a - c - d*magnitude) / (b + d)
        Q_new = a - b * P_cons
        P_prod = P_cons + magnitude
        type_label = "Subsidy"
        
        DWL = 0.5 * (Q_new - Q_eq) * magnitude 
        Gov_Rev_Cost = -magnitude * Q_new # Cost to Gov
        
    elif policy == "Price Floor (Min Wage)":
        # Price cannot go below magnitude
        if magnitude > P_eq: # Binding
            P_cons = magnitude
            Q_demanded = a - b * P_cons
            Q_supplied = c + d * P_cons
            Q_new = min(Q_demanded, Q_supplied)
            # DWL is area between Q_new and Q_eq under Demand and Supply
            # Triangle approximation? Trapezoid.
            # DWL = Integral from Q_new to Q_eq of (Pd - Ps) dQ
            # Pd(q) = (a-q)/b, Ps(q) = (q-c)/d
            # Intercepts at Q_new:
            Pd_at_Qnew = (a - Q_new)/b
            Ps_at_Qnew = (Q_new - c)/d
            DWL = 0.5 * (Pd_at_Qnew - Ps_at_Qnew) * (Q_eq - Q_new)
        else:
            Q_new, P_cons, P_prod = Q_eq, P_eq, P_eq
            DWL = 0

    elif policy == "Price Ceiling":
        if magnitude < P_eq: # Binding
            P_cons = magnitude
            Q_demanded = a - b * P_cons
            Q_supplied = c + d * P_cons
            Q_new = min(Q_demanded, Q_supplied)
            
            Pd_at_Qnew = (a - Q_new)/b
            Ps_at_Qnew = (Q_new - c)/d
            DWL = 0.5 * (Pd_at_Qnew - Ps_at_Qnew) * (Q_eq - Q_new)
        else:
            Q_new, P_cons, P_prod = Q_eq, P_eq, P_eq
            DWL = 0

    # 3. Visualization
    # Create Lines
    prices = np.linspace(0, max(a/b, (Q_new/d + c + 10)), 100)
    df = pd.DataFrame({'Price': prices})
    df['Demand'] = a - b * df['Price']
    df['Supply'] = c + d * df['Price']
    if policy == "Tax (Per Unit)":
        df['Supply + Tax'] = c + d * (df['Price'] - magnitude) # Q = c + d(P - t) -> P_sup = P -t
    elif policy == "Subsidy (Per Unit)":
        df['Supply + Subsidy'] = c + d * (df['Price'] + magnitude)
        
    df = df[(df['Demand'] >= 0) & (df['Supply'] >= 0)]
    df_melted = df.melt('Price', var_name='Type', value_name='Quantity')
    
    base_chart = alt.Chart(df_melted).mark_line().encode(
        x='Quantity', y='Price', color='Type'
    )
    
    # Shade DWL if applicable
    # Create polygon for DWL
    if DWL > 0 and policy in ["Tax (Per Unit)", "Subsidy (Per Unit)"]:
        # Polygon points: (Q_new, P_cons), (Q_new, P_prod), (Q_eq, P_eq)
        dwl_df = pd.DataFrame([
            {'Quantity': Q_new, 'Price': P_cons},
            {'Quantity': Q_new, 'Price': P_prod},
            {'Quantity': Q_eq, 'Price': P_eq}
        ])
        dwl_area = alt.Chart(dwl_df).mark_area(opacity=0.3, color='gray').encode(
            x='Quantity', y='Price'
        )
        base_chart += dwl_area
    elif DWL > 0: # Price controls
         # (Q_new, Pd_at_Qnew), (Q_new, Ps_at_Qnew), (Q_eq, P_eq)
         Pd_at_Qnew = (a - Q_new)/b
         Ps_at_Qnew = (Q_new - c)/d
         dwl_df = pd.DataFrame([
            {'Quantity': Q_new, 'Price': Pd_at_Qnew},
            {'Quantity': Q_new, 'Price': Ps_at_Qnew},
            {'Quantity': Q_eq, 'Price': P_eq}
        ])
         dwl_area = alt.Chart(dwl_df).mark_area(opacity=0.3, color='gray').encode(
            x='Quantity', y='Price'
        )
         base_chart += dwl_area

    st.altair_chart(base_chart.interactive(), use_container_width=True)
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("New Quantity", f"{Q_new:.2f}", delta=f"{Q_new - Q_eq:.2f}")
    m2.metric("Deadweight Loss", f"{DWL:.2f}", delta_color="inverse")
    if policy == "Tax (Per Unit)":
        m3.metric("Gov Revenue", f"{Gov_Rev_Cost:.2f}")
    elif policy == "Subsidy (Per Unit)":
        m3.metric("Gov Cost", f"{abs(Gov_Rev_Cost):.2f}", delta_color="inverse")
        
    st.info("The Gray shaded area represents the **Deadweight Loss (DWL)**: the loss of economic efficiency when the equilibrium outcome is not achievable or not achieved.")

