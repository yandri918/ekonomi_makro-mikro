import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Public Policy", page_icon="🏛️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🏛️ Public Policy Impact Analyzer",
        'subtitle': "Comprehensive analysis of government interventions on market equilibrium, welfare, and income distribution.",
        'tab1': "📊 Policy Simulation",
        'tab2': "💰 Welfare Analysis",
        'tab3': "📋 Policy Recommendations",
        'select_policy': "Select Policy Type",
        'none': "No Intervention (Free Market)",
        'tax': "Excise Tax (Per Unit)",
        'subsidy': "Subsidy (Per Unit)",
        'floor': "Price Floor (Minimum Wage)",
        'ceiling': "Price Ceiling (Rent Control)",
        'quota': "Production Quota",
        'params': "⚙️ Market Parameters",
        'demand_int': "Demand Intercept (a)",
        'demand_slope': "Demand Slope (b)",
        'supply_int': "Supply Intercept (c)",
        'supply_slope': "Supply Slope (d)",
        'policy_params': "⚙️ Policy Parameters",
        'tax_amt': "Tax Amount (Rp/unit)",
        'sub_amt': "Subsidy Amount (Rp/unit)",
        'floor_price': "Price Floor (Rp)",
        'ceiling_price': "Price Ceiling (Rp)",
        'quota_qty': "Production Quota (units)",
        'eq_res': "Initial Equilibrium (Free Market)",
        'eq_p': "Equilibrium Price",
        'eq_q': "Equilibrium Quantity",
        'policy_impact': "Policy Impact Summary",
        'cons_price': "Consumer Price",
        'prod_price': "Producer Price",
        'new_q': "New Quantity",
        'dwl': "Deadweight Loss",
        'gov_rev': "Government Revenue",
        'gov_cost': "Government Cost",
        'surplus': "Surplus (Excess Supply)",
        'shortage': "Shortage (Excess Demand)",
        'welfare_title': "Welfare Analysis",
        'consumer_surplus': "Consumer Surplus",
        'producer_surplus': "Producer Surplus",
        'total_surplus': "Total Surplus",
        'change_cs': "Change in CS",
        'change_ps': "Change in PS",
        'change_ts': "Change in TS",
        'efficiency_loss': "Efficiency Loss (%)",
        'distributional': "Distributional Effects",
        'winners': "Winners",
        'losers': "Losers",
        'recommendations': "Policy Recommendations",
        'effectiveness': "Policy Effectiveness Score",
        'trade_offs': "Key Trade-offs",
        'alternatives': "Alternative Policies to Consider",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nComprehensive tool for analyzing government policy impacts on markets, including welfare effects and distributional consequences.",
        'story_insight': "**Key Insight:**\nEvery policy creates winners and losers. Understanding these trade-offs is essential for evidence-based policymaking.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Policy Makers:** Evaluate policy options before implementation.",
        'use_analyst': "📈 **Economic Analysts:** Assess welfare impacts and distributional effects.",
        'use_academic': "🎓 **Researchers:** Study market interventions and their consequences."
    },
    'ID': {
        'title': "🏛️ Analisis Dampak Kebijakan Publik",
        'subtitle': "Analisis komprehensif intervensi pemerintah terhadap keseimbangan pasar, kesejahteraan, dan distribusi pendapatan.",
        'tab1': "📊 Simulasi Kebijakan",
        'tab2': "💰 Analisis Kesejahteraan",
        'tab3': "📋 Rekomendasi Kebijakan",
        'select_policy': "Pilih Jenis Kebijakan",
        'none': "Tanpa Intervensi (Pasar Bebas)",
        'tax': "Pajak Cukai (Per Unit)",
        'subsidy': "Subsidi (Per Unit)",
        'floor': "Harga Dasar (Upah Minimum)",
        'ceiling': "Harga Tertinggi (Kontrol Sewa)",
        'quota': "Kuota Produksi",
        'params': "⚙️ Parameter Pasar",
        'demand_int': "Intersep Permintaan (a)",
        'demand_slope': "Kemiringan Permintaan (b)",
        'supply_int': "Intersep Penawaran (c)",
        'supply_slope': "Kemiringan Penawaran (d)",
        'policy_params': "⚙️ Parameter Kebijakan",
        'tax_amt': "Besaran Pajak (Rp/unit)",
        'sub_amt': "Besaran Subsidi (Rp/unit)",
        'floor_price': "Harga Dasar (Rp)",
        'ceiling_price': "Harga Tertinggi (Rp)",
        'quota_qty': "Kuota Produksi (unit)",
        'eq_res': "Keseimbangan Awal (Pasar Bebas)",
        'eq_p': "Harga Keseimbangan",
        'eq_q': "Kuantitas Keseimbangan",
        'policy_impact': "Ringkasan Dampak Kebijakan",
        'cons_price': "Harga Konsumen",
        'prod_price': "Harga Produsen",
        'new_q': "Kuantitas Baru",
        'dwl': "Deadweight Loss",
        'gov_rev': "Pendapatan Pemerintah",
        'gov_cost': "Biaya Pemerintah",
        'surplus': "Surplus (Kelebihan Penawaran)",
        'shortage': "Kelangkaan (Kelebihan Permintaan)",
        'welfare_title': "Analisis Kesejahteraan",
        'consumer_surplus': "Surplus Konsumen",
        'producer_surplus': "Surplus Produsen",
        'total_surplus': "Total Surplus",
        'change_cs': "Perubahan SK",
        'change_ps': "Perubahan SP",
        'change_ts': "Perubahan TS",
        'efficiency_loss': "Kehilangan Efisiensi (%)",
        'distributional': "Efek Distribusi",
        'winners': "Pihak yang Diuntungkan",
        'losers': "Pihak yang Dirugikan",
        'recommendations': "Rekomendasi Kebijakan",
        'effectiveness': "Skor Efektivitas Kebijakan",
        'trade_offs': "Trade-off Utama",
        'alternatives': "Kebijakan Alternatif yang Dipertimbangkan",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nAlat komprehensif untuk menganalisis dampak kebijakan pemerintah terhadap pasar, termasuk efek kesejahteraan dan konsekuensi distribusi.",
        'story_insight': "**Wawasan Utama:**\nSetiap kebijakan menciptakan pihak yang diuntungkan dan dirugikan. Memahami trade-off ini penting untuk pembuatan kebijakan berbasis bukti.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Pembuat Kebijakan:** Evaluasi opsi kebijakan sebelum implementasi.",
        'use_analyst': "📈 **Analis Ekonomi:** Menilai dampak kesejahteraan dan efek distribusi.",
        'use_academic': "🎓 **Peneliti:** Mempelajari intervensi pasar dan konsekuensinya."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# Sidebar for parameters
with st.sidebar:
    st.markdown(f"### {txt['params']}")
    st.caption("Demand: $Q_d = a - bP$")
    st.caption("Supply: $Q_s = c + dP$")
    
    a = st.slider(txt['demand_int'], 50, 200, 100)
    b = st.slider(txt['demand_slope'], 0.5, 3.0, 1.0, 0.1)
    c = st.slider(txt['supply_int'], 0, 50, 20)
    d = st.slider(txt['supply_slope'], 0.5, 3.0, 1.0, 0.1)

# Calculate base equilibrium
P_eq = (a - c) / (b + d) if (b + d) != 0 else 0
Q_eq = a - b * P_eq if b != 0 else 0

# Consumer and Producer Surplus (Free Market)
CS_free = 0.5 * Q_eq * ((a/b) - P_eq) if b != 0 else 0
PS_free = 0.5 * Q_eq * (P_eq - (c/d)) if d != 0 else 0
TS_free = CS_free + PS_free

# Policy selection
policy = st.selectbox(txt['select_policy'], [txt['none'], txt['tax'], txt['subsidy'], txt['floor'], txt['ceiling'], txt['quota']])

# Policy parameters
magnitude = 0
if policy == txt['tax']:
    magnitude = st.slider(txt['tax_amt'], 0, 50, 10)
elif policy == txt['subsidy']:
    magnitude = st.slider(txt['sub_amt'], 0, 50, 10)
elif policy == txt['floor']:
    magnitude = st.slider(txt['floor_price'], 0, int(P_eq*2), int(P_eq*1.2))
elif policy == txt['ceiling']:
    magnitude = st.slider(txt['ceiling_price'], 0, int(P_eq*2), int(P_eq*0.8))
elif policy == txt['quota']:
    magnitude = st.slider(txt['quota_qty'], 0, int(Q_eq*2), int(Q_eq*0.7))

# TABS
tab1, tab2, tab3 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3']])

# Calculate policy effects
DWL = 0
Gov_Rev = 0
Gov_Cost = 0
Q_new = Q_eq
P_cons = P_eq
P_prod = P_eq
CS_new = CS_free
PS_new = PS_free
TS_new = TS_free

if policy == txt['tax']:
    P_prod = (a - c - b * magnitude) / (b + d)
    Q_new = c + d * P_prod
    P_cons = P_prod + magnitude
    DWL = 0.5 * (Q_eq - Q_new) * magnitude
    Gov_Rev = magnitude * Q_new
    CS_new = 0.5 * Q_new * ((a/b) - P_cons)
    PS_new = 0.5 * Q_new * (P_prod - (c/d))
    TS_new = CS_new + PS_new + Gov_Rev

elif policy == txt['subsidy']:
    P_cons = (a - c - d * magnitude) / (b + d)
    Q_new = a - b * P_cons
    P_prod = P_cons + magnitude
    DWL = 0.5 * (Q_new - Q_eq) * magnitude
    Gov_Cost = magnitude * Q_new
    CS_new = 0.5 * Q_new * ((a/b) - P_cons)
    PS_new = 0.5 * Q_new * (P_prod - (c/d))
    TS_new = CS_new + PS_new - Gov_Cost

elif policy == txt['floor']:
    if magnitude > P_eq:
        Q_d = a - b * magnitude
        Q_s = c + d * magnitude
        Q_new = min(Q_d, Q_s)
        P_cons = magnitude
        P_prod = magnitude
        CS_new = 0.5 * Q_new * ((a/b) - magnitude)
        PS_new = 0.5 * Q_new * (magnitude - (c/d)) + Q_new * (magnitude - P_eq)
        TS_new = CS_new + PS_new
        DWL = TS_free - TS_new

elif policy == txt['ceiling']:
    if magnitude < P_eq:
        Q_d = a - b * magnitude
        Q_s = c + d * magnitude
        Q_new = min(Q_d, Q_s)
        P_cons = magnitude
        P_prod = magnitude
        CS_new = 0.5 * Q_new * ((a/b) - magnitude) + Q_new * (P_eq - magnitude)
        PS_new = 0.5 * Q_new * (magnitude - (c/d))
        TS_new = CS_new + PS_new
        DWL = TS_free - TS_new

elif policy == txt['quota']:
    if magnitude < Q_eq:
        Q_new = magnitude
        P_cons = (a - Q_new) / b
        P_prod = (Q_new - c) / d
        CS_new = 0.5 * Q_new * ((a/b) - P_cons)
        PS_new = 0.5 * Q_new * (P_prod - (c/d)) + Q_new * (P_cons - P_prod)
        TS_new = CS_new + PS_new
        DWL = TS_free - TS_new

# ========== TAB 1: POLICY SIMULATION ==========
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"### {txt['eq_res']}")
        m1, m2 = st.columns(2)
        m1.metric(txt['eq_p'], f"Rp {P_eq:.2f}")
        m2.metric(txt['eq_q'], f"{Q_eq:.2f} units")
        
        if policy != txt['none']:
            st.markdown(f"### {txt['policy_impact']}")
            
            p1, p2, p3 = st.columns(3)
            p1.metric(txt['cons_price'], f"Rp {P_cons:.2f}", delta=f"{P_cons-P_eq:.2f}")
            p2.metric(txt['prod_price'], f"Rp {P_prod:.2f}", delta=f"{P_prod-P_eq:.2f}")
            p3.metric(txt['new_q'], f"{Q_new:.2f}", delta=f"{Q_new-Q_eq:.2f}")
            
            st.markdown("---")
            
            w1, w2 = st.columns(2)
            w1.metric(txt['dwl'], f"Rp {DWL:.2f}", delta_color="inverse")
            
            if Gov_Rev > 0:
                w2.metric(txt['gov_rev'], f"Rp {Gov_Rev:.2f}")
            elif Gov_Cost > 0:
                w2.metric(txt['gov_cost'], f"Rp {Gov_Cost:.2f}", delta_color="inverse")
    
    with col2:
        # Visualization
        prices = np.linspace(0, (a/b)*1.2, 100)
        Q_demand = a - b * prices
        Q_supply = c + d * prices
        
        fig = go.Figure()
        
        # Demand and Supply
        fig.add_trace(go.Scatter(x=Q_demand, y=prices, mode='lines', name='Demand', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=Q_supply, y=prices, mode='lines', name='Supply', line=dict(color='red', width=3)))
        
        # Equilibrium point
        fig.add_trace(go.Scatter(x=[Q_eq], y=[P_eq], mode='markers', name='Free Market Eq', marker=dict(size=12, color='green')))
        
        # Policy effects
        if policy != txt['none']:
            fig.add_trace(go.Scatter(x=[Q_new], y=[P_cons], mode='markers', name='New Equilibrium', marker=dict(size=12, color='orange')))
            
            # DWL area
            if DWL > 0:
                fig.add_shape(type="rect", x0=Q_new, y0=min(P_cons, P_prod), x1=Q_eq, y1=max(P_cons, P_prod),
                             fillcolor="gray", opacity=0.3, line_width=0)
        
        fig.update_layout(
            title="Market Equilibrium Analysis",
            xaxis_title="Quantity",
            yaxis_title="Price (Rp)",
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ========== TAB 2: WELFARE ANALYSIS ==========
with tab2:
    st.markdown(f"### {txt['welfare_title']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Welfare metrics
        st.markdown("**Before Policy (Free Market)**")
        b1, b2, b3 = st.columns(3)
        b1.metric(txt['consumer_surplus'], f"Rp {CS_free:.2f}")
        b2.metric(txt['producer_surplus'], f"Rp {PS_free:.2f}")
        b3.metric(txt['total_surplus'], f"Rp {TS_free:.2f}")
        
        if policy != txt['none']:
            st.markdown("**After Policy**")
            a1, a2, a3 = st.columns(3)
            a1.metric(txt['consumer_surplus'], f"Rp {CS_new:.2f}", delta=f"{CS_new-CS_free:.2f}")
            a2.metric(txt['producer_surplus'], f"Rp {PS_new:.2f}", delta=f"{PS_new-PS_free:.2f}")
            a3.metric(txt['total_surplus'], f"Rp {TS_new:.2f}", delta=f"{TS_new-TS_free:.2f}")
            
            efficiency_loss = (DWL / TS_free * 100) if TS_free > 0 else 0
            st.error(f"**{txt['efficiency_loss']}**: {efficiency_loss:.1f}%")
    
    with col2:
        if policy != txt['none']:
            # Distributional effects
            st.markdown(f"### {txt['distributional']}")
            
            change_cs = CS_new - CS_free
            change_ps = PS_new - PS_free
            
            if change_cs > 0:
                st.success(f"✅ **{txt['winners']}**: Consumers (gain Rp {change_cs:.2f})")
            else:
                st.error(f"❌ **{txt['losers']}**: Consumers (lose Rp {abs(change_cs):.2f})")
            
            if change_ps > 0:
                st.success(f"✅ **{txt['winners']}**: Producers (gain Rp {change_ps:.2f})")
            else:
                st.error(f"❌ **{txt['losers']}**: Producers (lose Rp {abs(change_ps):.2f})")
            
            if Gov_Rev > 0:
                st.success(f"✅ **{txt['winners']}**: Government (revenue Rp {Gov_Rev:.2f})")
            elif Gov_Cost > 0:
                st.error(f"❌ **{txt['losers']}**: Government (cost Rp {Gov_Cost:.2f})")
            
            # Pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Consumer Surplus', 'Producer Surplus', 'Deadweight Loss', 'Gov Revenue/Cost'],
                values=[max(CS_new, 0), max(PS_new, 0), max(DWL, 0), max(Gov_Rev - Gov_Cost, 0)],
                hole=.3
            )])
            fig_pie.update_layout(title="Welfare Distribution", height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

# ========== TAB 3: POLICY RECOMMENDATIONS ==========
with tab3:
    st.markdown(f"### {txt['recommendations']}")
    
    if policy != txt['none']:
        # Effectiveness score
        effectiveness = max(0, 100 - efficiency_loss)
        st.metric(txt['effectiveness'], f"{effectiveness:.1f}/100")
        
        if effectiveness > 80:
            st.success("🟢 **High Effectiveness** - Policy achieves goals with minimal efficiency loss")
        elif effectiveness > 50:
            st.warning("🟡 **Moderate Effectiveness** - Significant trade-offs exist")
        else:
            st.error("🔴 **Low Effectiveness** - High deadweight loss, consider alternatives")
        
        # Trade-offs
        st.markdown(f"### {txt['trade_offs']}")
        if policy == txt['tax']:
            st.info("📊 **Tax generates revenue but reduces market activity**\n- Government gains revenue\n- Both consumers and producers lose\n- Market becomes less efficient")
        elif policy == txt['subsidy']:
            st.info("📊 **Subsidy increases consumption but costs government**\n- Consumers benefit from lower prices\n- Producers benefit from higher revenue\n- Taxpayers bear the cost")
        elif policy == txt['floor']:
            st.info("📊 **Price floor protects producers but creates surplus**\n- Producers gain if they can sell\n- Consumers pay more\n- Excess supply may require government intervention")
        elif policy == txt['ceiling']:
            st.info("📊 **Price ceiling helps consumers but creates shortage**\n- Consumers pay less if they can buy\n- Producers lose revenue\n- Shortage leads to rationing/black markets")
        
        # Alternatives
        st.markdown(f"### {txt['alternatives']}")
        if policy == txt['tax']:
            st.write("- **Lump-sum tax** (less distortionary)")
            st.write("- **Pigouvian tax** (if externality exists)")
            st.write("- **Progressive income tax** (better redistribution)")
        elif policy == txt['subsidy']:
            st.write("- **Direct cash transfer** (more efficient)")
            st.write("- **Voucher system** (targeted support)")
            st.write("- **Tax credit** (less administrative cost)")
        elif policy == txt['floor']:
            st.write("- **Earned Income Tax Credit** (no surplus)")
            st.write("- **Training programs** (increase productivity)")
            st.write("- **Negative income tax** (better targeting)")
        elif policy == txt['ceiling']:
            st.write("- **Housing vouchers** (no shortage)")
            st.write("- **Supply-side subsidies** (increase supply)")
            st.write("- **Zoning reform** (address root cause)")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_govt'])
        st.write(txt['use_analyst'])
        st.write(txt['use_academic'])
