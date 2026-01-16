import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Market Structures", page_icon="🏭", layout="wide")

st.title("🏭 Market Structures & Production Theory")
st.markdown("Compare how firms maximize profit under **Perfect Competition** vs **Monopoly**.")

structure_type = st.radio("Select Market Structure:", ["Perfect Competition", "Monopoly"], horizontal=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ Cost Parameters")
    # Total Cost = FC + VC*Q + alpha*Q^2 + beta*Q^3 (Cubic Cost Function for U-shaped MC/AC)
    fc = st.slider("Fixed Cost (FC)", 10, 100, 50)
    vc_linear = st.slider("Variable Cost Linear (VC)", 1, 10, 2)
    alpha = 0.5 # Quadratic term
    
    st.markdown("---")
    st.markdown("### 💰 Demand Parameters")
    
    if structure_type == "Perfect Competition":
        market_price = st.slider("Market Price (P)", 10, 50, 20)
        st.info("In Perfect Competition, Price is determined by the market. The firm is a price taker ($P = MR = AR$).")
        quantity_max = 50
    else: # Monopoly
        intercept = st.slider("Demand Intercept", 30, 100, 60)
        slope = st.slider("Demand Slope", 0.5, 2.0, 1.0)
        st.info("A Monopolist faces the entire market demand. Marginal Revenue (MR) falls twice as fast as Price.")
        quantity_max = int(intercept / slope) if slope > 0 else 50

with col2:
    # Generate Data
    Q_range = np.linspace(0.1, quantity_max, 100) # Start from 0.1 to avoid division by zero for AC
    
    # Cost Functions
    # TC = FC + VC*Q + 0.1*Q^2 (Simpler Quadratic TC -> Linear MC for visualization clarity)
    # Actually let's use Quadratic TC -> Linear MC, or Cubic TC -> U-shaped MC.
    # Let's stick to Quadratic MC (from Cubic TC) for the classic U-shape.
    # TC = FC + aQ + bQ^2 + cQ^3
    # Let's keep it simple: TC = FC + vc_linear * Q + 0.05 * Q^2
    # MC = dTC/dQ = vc_linear + 0.1 * Q
    
    # Let's try to make U-shaped AC and rising MC.
    # TC = FC + 2Q + 0.5Q^2
    # MC = 2 + Q
    # AC = FC/Q + 2 + 0.5Q
    
    tc = fc + vc_linear * Q_range + 0.1 * (Q_range**2)
    mc = vc_linear + 0.2 * Q_range
    atc = tc / Q_range
    
    # Revenue Functions
    if structure_type == "Perfect Competition":
        price = np.full_like(Q_range, market_price)
        tr = market_price * Q_range
        mr = price # MR = P
        ar = price # AR = P
        
        # Find Equilibrium: MC = MR => vc + 0.2Q = P => 0.2Q = P - vc => Q = (P - vc) / 0.2
        if market_price > vc_linear:
            q_star = (market_price - vc_linear) / 0.2
            p_star = market_price
        else:
            q_star = 0
            p_star = market_price
            
    else: # Monopoly
        # P = Intercept - Slope*Q
        price = intercept - slope * Q_range
        tr = price * Q_range
        # MR = Intercept - 2*Slope*Q
        mr = intercept - 2 * slope * Q_range
        ar = price
        
        # Find Equilibrium: MC = MR
        # vc + 0.2Q = int - 2*slope*Q
        # (0.2 + 2*slope)Q = int - vc
        if intercept > vc_linear:
            q_star = (intercept - vc_linear) / (0.2 + 2 * slope)
            p_star = intercept - slope * q_star
        else:
            q_star = 0
            p_star = 0

    # DataFrame
    df = pd.DataFrame({
        'Quantity': Q_range,
        'MC': mc,
        'ATC': atc,
        'MR': mr,
        'Average Revenue (Demand)': ar
    })
    
    # Filter for plotting range
    df = df[df['Quantity'] <= quantity_max]
    
    # Melt
    df_melted_costs = df.melt('Quantity', value_vars=['MC', 'ATC'], var_name='Cost Curves', value_name='Price')
    df_melted_revenue = df.melt('Quantity', value_vars=['MR', 'Average Revenue (Demand)'], var_name='Revenue Curves', value_name='Price')
    
    # Combine
    chart_costs = alt.Chart(df_melted_costs).mark_line().encode(
        x='Quantity', 
        y=alt.Y('Price', scale=alt.Scale(domain=[0, max(p_star*2, 100)])),
        color=alt.Color('Cost Curves', scale=alt.Scale(domain=['MC', 'ATC'], range=['red', 'orange']))
    )
    
    chart_rev = alt.Chart(df_melted_revenue).mark_line(strokeDash=[5,5]).encode(
        x='Quantity',
        y='Price',
        color=alt.Color('Revenue Curves', scale=alt.Scale(domain=['MR', 'Average Revenue (Demand)'], range=['green', 'blue']))
    )
    
    # Equilibrium Point
    eq_df = pd.DataFrame({'Quantity': [q_star], 'Price': [p_star]})
    point = alt.Chart(eq_df).mark_point(size=200, color='black').encode(x='Quantity', y='Price')
    text = point.mark_text(dx=10, dy=-10, text=f"Q*={q_star:.1f}, P*={p_star:.1f}").encode()
    
    st.altair_chart((chart_costs + chart_rev + point + text).interactive(), use_container_width=True)
    
    # Profit Calculation
    atc_at_qstar = (fc + vc_linear * q_star + 0.1 * (q_star**2)) / q_star if q_star > 0 else 0
    profit = (p_star - atc_at_qstar) * q_star
    
    st.markdown(f"**Profit Maximization Analysis:**")
    st.write(f"- Optimal Quantity ($Q^*$): **{q_star:.2f}** (where $MR = MC$)")
    st.write(f"- Optimal Price ($P^*$): **{p_star:.2f}**")
    st.write(f"- Average Total Cost at $Q^*$: **{atc_at_qstar:.2f}**")
    
    if profit > 0:
        st.success(f"📈 Supernormal Profit: **${profit:.2f}**")
    elif profit < 0:
        st.error(f"📉 Loss: **${profit:.2f}**")
    else:
        st.info("⚖️ Normal Profit (Break-even)")

