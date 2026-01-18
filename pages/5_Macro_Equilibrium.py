import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Macroeconomic Equilibrium", page_icon="⚖️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "⚖️ Macroeconomic Equilibrium: IS-LM & AD-AS Models",
        'subtitle': "Interactive visualization of short-run and long-run macroeconomic equilibrium with easy-to-understand explanations.",
        'tab1': "📉 IS-LM Model",
        'tab2': "📈 AD-AS Model",
        'tab3': "🎯 Policy Experiments",
        'tab4': "📚 Learn the Basics",
        # Tab 1: IS-LM
        'islm_title': "IS-LM Model: Goods & Money Market Equilibrium",
        'what_is_islm': "**What is IS-LM?**",
        'islm_explain': """
The IS-LM model shows how the **Goods Market** (IS curve) and **Money Market** (LM curve) interact to determine:
- **Output (Y)** - How much the economy produces
- **Interest Rate (r)** - The cost of borrowing money

Think of it like this:
- **IS Curve** = "Investment-Savings" - Shows all combinations of Y and r where spending equals production
- **LM Curve** = "Liquidity-Money" - Shows all combinations of Y and r where money supply equals money demand
        """,
        'fiscal_policy': "🏛️ Fiscal Policy (Government)",
        'govt_spending': "Government Spending (G) - Trillion Rp",
        'taxes': "Taxes (T) - Trillion Rp",
        'mpc': "MPC (How much people spend from extra income)",
        'mpc_help': "0.75 means if you get Rp 100, you spend Rp 75",
        'monetary_policy': "🏦 Monetary Policy (Central Bank)",
        'money_supply': "Money Supply (M) - Trillion Rp",
        'price_level': "Price Level (P)",
        'money_demand_y': "Money Demand Sensitivity to Income (k)",
        'money_demand_r': "Money Demand Sensitivity to Interest Rate (h)",
        'equilibrium': "Equilibrium Results",
        'output': "Output (Y*)",
        'interest_rate': "Interest Rate (r*)",
        'is_curve': "IS Curve (Goods Market)",
        'lm_curve': "LM Curve (Money Market)",
        'equilibrium_point': "Equilibrium",
        # Tab 2: AD-AS
        'adas_title': "AD-AS Model: Price Level & Output Determination",
        'what_is_adas': "**What is AD-AS?**",
        'adas_explain': """
The AD-AS model shows how **Aggregate Demand** and **Aggregate Supply** determine:
- **Price Level (P)** - Average price of all goods
- **Output (Y)** - Total production in the economy

Think of it like this:
- **AD Curve** = Total spending in economy (C + I + G + NX)
- **SRAS Curve** = What firms can produce in short run
- **LRAS Curve** = Maximum sustainable production (full employment)
        """,
        'shock_type': "Economic Shock Type",
        'no_shock': "No Shock (Baseline)",
        'demand_shock_pos': "Positive Demand Shock (+10%)",
        'demand_shock_neg': "Negative Demand Shock (-10%)",
        'supply_shock_pos': "Positive Supply Shock (+10%)",
        'supply_shock_neg': "Negative Supply Shock (-10%)",
        'results': "Results",
        'price_level': "Price Level (P*)",
        'output_gap': "Output Gap",
        'gap_explain': "Distance from full employment",
        'recession_gap': "🔴 Recession (below potential)",
        'inflation_gap': "🔴 Overheating (above potential)",
        'full_employment': "🟢 Full Employment",
        # Tab 3: Policy
        'policy_title': "Policy Experiments: Test Different Policies",
        'experiment': "Choose Policy Experiment",
        'exp_fiscal_expansion': "Fiscal Expansion (↑G or ↓T)",
        'exp_fiscal_contraction': "Fiscal Contraction (↓G or ↑T)",
        'exp_monetary_expansion': "Monetary Expansion (↑M)",
        'exp_monetary_contraction': "Monetary Contraction (↓M)",
        'exp_combined': "Combined Policy",
        'policy_change': "Policy Change Amount",
        'run_experiment': "Run Experiment",
        'before_after': "Before vs After Policy",
        'impact': "Policy Impact",
        # Tab 4: Learn
        'learn_title': "📚 Learn the Basics: Step-by-Step Guide",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nInteractive macroeconomic equilibrium models showing how fiscal and monetary policy affect the economy.",
        'story_insight': "**Key Insight:**\nIS-LM shows short-run equilibrium. AD-AS shows how prices adjust. Together they explain business cycles and policy effectiveness.",
        'story_users': "**Who needs this?**",
        'use_students': "🎓 **Students:** Understand macro theory visually",
        'use_policymakers': "🏛️ **Policymakers:** Analyze policy effects",
        'use_analysts': "📊 **Analysts:** Forecast economic outcomes"
    },
    'ID': {
        'title': "⚖️ Keseimbangan Makroekonomi: Model IS-LM & AD-AS",
        'subtitle': "Visualisasi interaktif keseimbangan makroekonomi jangka pendek dan panjang dengan penjelasan yang mudah dipahami.",
        'tab1': "📉 Model IS-LM",
        'tab2': "📈 Model AD-AS",
        'tab3': "🎯 Eksperimen Kebijakan",
        'tab4': "📚 Pelajari Dasar-dasar",
        # Tab 1: IS-LM
        'islm_title': "Model IS-LM: Keseimbangan Pasar Barang & Uang",
        'what_is_islm': "**Apa itu IS-LM?**",
        'islm_explain': """
Model IS-LM menunjukkan bagaimana **Pasar Barang** (kurva IS) dan **Pasar Uang** (kurva LM) berinteraksi untuk menentukan:
- **Output (Y)** - Berapa banyak ekonomi memproduksi
- **Suku Bunga (r)** - Biaya meminjam uang

Bayangkan seperti ini:
- **Kurva IS** = "Investment-Savings" - Menunjukkan semua kombinasi Y dan r dimana pengeluaran = produksi
- **Kurva LM** = "Liquidity-Money" - Menunjukkan semua kombinasi Y dan r dimana jumlah uang beredar = permintaan uang
        """,
        'fiscal_policy': "🏛️ Kebijakan Fiskal (Pemerintah)",
        'govt_spending': "Belanja Pemerintah (G) - Triliun Rp",
        'taxes': "Pajak (T) - Triliun Rp",
        'mpc': "MPC (Berapa banyak orang belanja dari pendapatan tambahan)",
        'mpc_help': "0.75 artinya jika dapat Rp 100, Anda belanja Rp 75",
        'monetary_policy': "🏦 Kebijakan Moneter (Bank Sentral)",
        'money_supply': "Jumlah Uang Beredar (M) - Triliun Rp",
        'price_level': "Tingkat Harga (P)",
        'money_demand_y': "Sensitivitas Permintaan Uang thd Pendapatan (k)",
        'money_demand_r': "Sensitivitas Permintaan Uang thd Suku Bunga (h)",
        'equilibrium': "Hasil Keseimbangan",
        'output': "Output (Y*)",
        'interest_rate': "Suku Bunga (r*)",
        'is_curve': "Kurva IS (Pasar Barang)",
        'lm_curve': "Kurva LM (Pasar Uang)",
        'equilibrium_point': "Keseimbangan",
        # Tab 2: AD-AS
        'adas_title': "Model AD-AS: Penentuan Tingkat Harga & Output",
        'what_is_adas': "**Apa itu AD-AS?**",
        'adas_explain': """
Model AD-AS menunjukkan bagaimana **Permintaan Agregat** dan **Penawaran Agregat** menentukan:
- **Tingkat Harga (P)** - Harga rata-rata semua barang
- **Output (Y)** - Total produksi dalam ekonomi

Bayangkan seperti ini:
- **Kurva AD** = Total pengeluaran dalam ekonomi (C + I + G + NX)
- **Kurva SRAS** = Apa yang bisa diproduksi perusahaan dalam jangka pendek
- **Kurva LRAS** = Produksi maksimum berkelanjutan (kesempatan kerja penuh)
        """,
        'shock_type': "Jenis Guncangan Ekonomi",
        'no_shock': "Tanpa Guncangan (Baseline)",
        'demand_shock_pos': "Guncangan Permintaan Positif (+10%)",
        'demand_shock_neg': "Guncangan Permintaan Negatif (-10%)",
        'supply_shock_pos': "Guncangan Penawaran Positif (+10%)",
        'supply_shock_neg': "Guncangan Penawaran Negatif (-10%)",
        'results': "Hasil",
        'price_level': "Tingkat Harga (P*)",
        'output_gap': "Celah Output",
        'gap_explain': "Jarak dari kesempatan kerja penuh",
        'recession_gap': "🔴 Resesi (di bawah potensial)",
        'inflation_gap': "🔴 Overheating (di atas potensial)",
        'full_employment': "🟢 Kesempatan Kerja Penuh",
        # Tab 3: Policy
        'policy_title': "Eksperimen Kebijakan: Uji Berbagai Kebijakan",
        'experiment': "Pilih Eksperimen Kebijakan",
        'exp_fiscal_expansion': "Ekspansi Fiskal (↑G atau ↓T)",
        'exp_fiscal_contraction': "Kontraksi Fiskal (↓G atau ↑T)",
        'exp_monetary_expansion': "Ekspansi Moneter (↑M)",
        'exp_monetary_contraction': "Kontraksi Moneter (↓M)",
        'exp_combined': "Kebijakan Kombinasi",
        'policy_change': "Jumlah Perubahan Kebijakan",
        'run_experiment': "Jalankan Eksperimen",
        'before_after': "Sebelum vs Sesudah Kebijakan",
        'impact': "Dampak Kebijakan",
        # Tab 4: Learn
        'learn_title': "📚 Pelajari Dasar-dasar: Panduan Langkah demi Langkah",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nModel keseimbangan makroekonomi interaktif yang menunjukkan bagaimana kebijakan fiskal dan moneter mempengaruhi ekonomi.",
        'story_insight': "**Wawasan Utama:**\nIS-LM menunjukkan keseimbangan jangka pendek. AD-AS menunjukkan bagaimana harga menyesuaikan. Bersama-sama mereka menjelaskan siklus bisnis dan efektivitas kebijakan.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_students': "🎓 **Mahasiswa:** Memahami teori makro secara visual",
        'use_policymakers': "🏛️ **Pembuat Kebijakan:** Menganalisis efek kebijakan",
        'use_analysts': "📊 **Analis:** Meramalkan hasil ekonomi"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ========== TAB 1: IS-LM MODEL ==========
with tab1:
    st.markdown(f"### {txt['islm_title']}")
    
    with st.expander(txt['what_is_islm'], expanded=False):
        st.markdown(txt['islm_explain'])
        st.latex(r"IS: Y = C + I(r) + G")
        st.latex(r"LM: \frac{M}{P} = L(Y, r)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['fiscal_policy']}")
        
        G = st.number_input(txt['govt_spending'], min_value=0.0, max_value=10000.0, value=150.0, step=10.0)
        T = st.number_input(txt['taxes'], min_value=0.0, max_value=10000.0, value=100.0, step=10.0)
        MPC = st.slider(txt['mpc'], 0.1, 0.9, 0.75, 0.05, help=txt['mpc_help'])
        
        st.markdown(f"#### {txt['monetary_policy']}")
        
        M = st.number_input(txt['money_supply'], min_value=0.0, max_value=50000.0, value=400.0, step=50.0)
        P = st.slider(txt['price_level'], 0.5, 3.0, 1.0, 0.1)
        k = st.slider(txt['money_demand_y'], 0.1, 1.0, 0.5, 0.05)
        h = st.slider(txt['money_demand_r'], 10, 200, 100, 10)
    
    with col2:
        # IS Curve calculation
        # Y = C + I + G, where C = a + MPC(Y-T), I = I0 - b*r
        # Solving for r: r = (a + I0 + G - MPC*T)/(b) - (1-MPC)/b * Y
        
        a = 100  # Autonomous consumption
        I0 = 200  # Autonomous investment
        b = 50   # Investment sensitivity to interest rate
        
        # IS parameters
        IS_intercept = (a + I0 + G - MPC * T) / b
        IS_slope = (1 - MPC) / b
        
        # LM Curve calculation
        # M/P = kY - hr
        # Solving for r: r = (k/h)Y - (1/h)(M/P)
        
        real_money = M / P
        LM_slope = k / h
        LM_intercept = -real_money / h
        
        # Equilibrium
        # IS: r = IS_intercept - IS_slope * Y
        # LM: r = LM_slope * Y + LM_intercept
        # Set equal: IS_intercept - IS_slope * Y = LM_slope * Y + LM_intercept
        
        Y_eq = (IS_intercept - LM_intercept) / (IS_slope + LM_slope)
        r_eq = IS_intercept - IS_slope * Y_eq
        
        # Display results
        st.markdown(f"### {txt['equilibrium']}")
        
        m1, m2 = st.columns(2)
        m1.metric(txt['output'], f"Rp {Y_eq:,.0f}T")
        m2.metric(txt['interest_rate'], f"{r_eq:.2f}%")
        
        # Plot IS-LM
        Y_range = np.linspace(0, 1000, 100)
        IS_curve = IS_intercept - IS_slope * Y_range
        LM_curve = LM_slope * Y_range + LM_intercept
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=Y_range, y=IS_curve, mode='lines',
                                name=txt['is_curve'], line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=Y_range, y=LM_curve, mode='lines',
                                name=txt['lm_curve'], line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=[Y_eq], y=[r_eq], mode='markers',
                                name=txt['equilibrium_point'],
                                marker=dict(size=15, color='green', symbol='star')))
        
        fig.update_layout(
            title="IS-LM Equilibrium",
            xaxis_title="Output (Y) - Trillion Rp",
            yaxis_title="Interest Rate (r) - %",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Explanation
        st.info(f"""
        **💡 Interpretation:**
        - At equilibrium Y* = {Y_eq:.0f}T and r* = {r_eq:.2f}%
        - **IS Curve**: Higher interest rates → Lower investment → Lower output
        - **LM Curve**: Higher output → More money demand → Higher interest rates
        - **Equilibrium**: Where both markets clear simultaneously
        """)

# ========== TAB 2: AD-AS MODEL ==========
with tab2:
    st.markdown(f"### {txt['adas_title']}")
    
    with st.expander(txt['what_is_adas'], expanded=False):
        st.markdown(txt['adas_explain'])
        st.latex(r"AD: Y = C + I + G + NX")
        st.latex(r"SRAS: P = P_e + \alpha(Y - Y_n)")
        st.latex(r"LRAS: Y = Y_n \text{ (vertical)}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['shock_type']}")
        
        shock = st.selectbox("", [
            txt['no_shock'],
            txt['demand_shock_pos'],
            txt['demand_shock_neg'],
            txt['supply_shock_pos'],
            txt['supply_shock_neg']
        ])
    
    with col2:
        # AD-AS Model
        Y_potential = 500  # Full employment output
        P_base = 100  # Base price level
        
        # AD Curve: P = a - b*Y (downward sloping)
        AD_intercept = 200
        AD_slope = 0.2
        
        # SRAS Curve: P = c + d*Y (upward sloping)
        SRAS_intercept = 50
        SRAS_slope = 0.1
        
        # Apply shocks
        if shock == txt['demand_shock_pos']:
            AD_intercept += 20
        elif shock == txt['demand_shock_neg']:
            AD_intercept -= 20
        elif shock == txt['supply_shock_pos']:
            SRAS_intercept -= 10
        elif shock == txt['supply_shock_neg']:
            SRAS_intercept += 10
        
        # Equilibrium
        Y_eq_ad = (AD_intercept - SRAS_intercept) / (AD_slope + SRAS_slope)
        P_eq_ad = AD_intercept - AD_slope * Y_eq_ad
        
        # Output gap
        output_gap = Y_eq_ad - Y_potential
        
        # Display results
        st.markdown(f"### {txt['results']}")
        
        r1, r2 = st.columns(2)
        r1.metric(txt['price_level'], f"{P_eq_ad:.1f}")
        r2.metric(txt['output'], f"Rp {Y_eq_ad:.0f}T")
        
        # Gap analysis
        if abs(output_gap) < 10:
            gap_status = txt['full_employment']
            gap_color = "success"
        elif output_gap < 0:
            gap_status = txt['recession_gap']
            gap_color = "error"
        else:
            gap_status = txt['inflation_gap']
            gap_color = "warning"
        
        st.metric(txt['output_gap'], f"{output_gap:+.1f}T", help=txt['gap_explain'])
        
        if gap_color == "success":
            st.success(gap_status)
        elif gap_color == "error":
            st.error(gap_status)
        else:
            st.warning(gap_status)
        
        # Plot AD-AS
        Y_range = np.linspace(200, 800, 100)
        AD_curve = AD_intercept - AD_slope * Y_range
        SRAS_curve = SRAS_intercept + SRAS_slope * Y_range
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=Y_range, y=AD_curve, mode='lines',
                                name='AD', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=Y_range, y=SRAS_curve, mode='lines',
                                name='SRAS', line=dict(color='red', width=3)))
        fig.add_vline(x=Y_potential, line_dash="dash", line_color="gray",
                     annotation_text="LRAS (Full Employment)")
        fig.add_trace(go.Scatter(x=[Y_eq_ad], y=[P_eq_ad], mode='markers',
                                name=txt['equilibrium_point'],
                                marker=dict(size=15, color='green', symbol='star')))
        
        fig.update_layout(
            title="AD-AS Equilibrium",
            xaxis_title="Output (Y) - Trillion Rp",
            yaxis_title="Price Level (P)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Explanation
        st.info(f"""
        **💡 Interpretation:**
        - Equilibrium at P* = {P_eq_ad:.1f}, Y* = {Y_eq_ad:.0f}T
        - **AD Curve**: Higher prices → Lower real money → Lower spending
        - **SRAS Curve**: Higher output → Higher costs → Higher prices
        - **LRAS**: Long-run potential at Y = {Y_potential}T (full employment)
        - **Output Gap**: {output_gap:+.1f}T - {gap_status}
        """)

# ========== TAB 3: POLICY EXPERIMENTS ==========
with tab3:
    st.markdown(f"### {txt['policy_title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        experiment = st.selectbox(txt['experiment'], [
            txt['exp_fiscal_expansion'],
            txt['exp_fiscal_contraction'],
            txt['exp_monetary_expansion'],
            txt['exp_monetary_contraction'],
            txt['exp_combined']
        ])
        
        policy_change = st.slider(txt['policy_change'], -100, 100, 50, 10)
        
        if st.button(txt['run_experiment'], type='primary'):
            # Baseline
            G_base = 150
            M_base = 400
            
            # Apply policy
            if experiment == txt['exp_fiscal_expansion']:
                G_new = G_base + policy_change
                M_new = M_base
            elif experiment == txt['exp_fiscal_contraction']:
                G_new = G_base - policy_change
                M_new = M_base
            elif experiment == txt['exp_monetary_expansion']:
                G_new = G_base
                M_new = M_base + policy_change
            elif experiment == txt['exp_monetary_contraction']:
                G_new = G_base
                M_new = M_base - policy_change
            else:  # Combined
                G_new = G_base + policy_change
                M_new = M_base + policy_change
            
            # Calculate new equilibrium (simplified)
            Y_base = 500
            r_base = 5.0
            
            # Fiscal multiplier
            fiscal_mult = MPC / (1 - MPC)
            delta_Y_fiscal = fiscal_mult * (G_new - G_base)
            
            # Monetary effect
            delta_Y_monetary = 0.5 * (M_new - M_base)
            
            Y_new = Y_base + delta_Y_fiscal + delta_Y_monetary
            r_new = r_base + 0.01 * (G_new - G_base) - 0.005 * (M_new - M_base)
            
            st.session_state['experiment_results'] = {
                'Y_base': Y_base,
                'r_base': r_base,
                'Y_new': Y_new,
                'r_new': r_new,
                'G_base': G_base,
                'G_new': G_new,
                'M_base': M_base,
                'M_new': M_new
            }
    
    with col2:
        if 'experiment_results' in st.session_state:
            res = st.session_state['experiment_results']
            
            st.markdown(f"### {txt['before_after']}")
            
            # Metrics
            col_a, col_b = st.columns(2)
            col_a.metric("Output Before", f"Rp {res['Y_base']:.0f}T")
            col_b.metric("Output After", f"Rp {res['Y_new']:.0f}T",
                        delta=f"{res['Y_new'] - res['Y_base']:+.0f}T")
            
            col_c, col_d = st.columns(2)
            col_c.metric("Interest Rate Before", f"{res['r_base']:.2f}%")
            col_d.metric("Interest Rate After", f"{res['r_new']:.2f}%",
                        delta=f"{res['r_new'] - res['r_base']:+.2f}%")
            
            # Comparison chart
            fig = go.Figure()
            
            categories = ['Output (Y)', 'Interest Rate (r)', 'Govt Spending (G)', 'Money Supply (M)']
            before = [res['Y_base'], res['r_base'], res['G_base'], res['M_base']]
            after = [res['Y_new'], res['r_new'], res['G_new'], res['M_new']]
            
            fig.add_trace(go.Bar(name='Before', x=categories, y=before, marker_color='lightblue'))
            fig.add_trace(go.Bar(name='After', x=categories, y=after, marker_color='darkblue'))
            
            fig.update_layout(
                title=txt['impact'],
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 4: LEARN THE BASICS ==========
with tab4:
    st.markdown(f"### {txt['learn_title']}")
    
    st.markdown("""
    ## 📖 Step 1: Understanding IS-LM
    
    **The IS Curve (Investment-Savings)**
    - Shows equilibrium in the **goods market**
    - When interest rates ↑ → Investment ↓ → Output ↓
    - **Slopes downward** (negative relationship between r and Y)
    
    **The LM Curve (Liquidity-Money)**
    - Shows equilibrium in the **money market**
    - When output ↑ → Money demand ↑ → Interest rates ↑
    - **Slopes upward** (positive relationship between r and Y)
    
    **Equilibrium**
    - Where IS and LM intersect
    - Both markets clear simultaneously
    
    ---
    
    ## 📖 Step 2: Understanding AD-AS
    
    **Aggregate Demand (AD)**
    - Total spending: C + I + G + NX
    - **Slopes downward** (higher prices → lower real money → less spending)
    
    **Short-Run Aggregate Supply (SRAS)**
    - What firms can produce given current prices and wages
    - **Slopes upward** (higher output → higher costs → higher prices)
    
    **Long-Run Aggregate Supply (LRAS)**
    - Maximum sustainable output (full employment)
    - **Vertical** (independent of price level)
    
    ---
    
    ## 📖 Step 3: Policy Effects
    
    **Fiscal Policy (Government Spending/Taxes)**
    - ↑G or ↓T → IS shifts right → ↑Y, ↑r
    - ↓G or ↑T → IS shifts left → ↓Y, ↓r
    
    **Monetary Policy (Money Supply)**
    - ↑M → LM shifts right → ↑Y, ↓r
    - ↓M → LM shifts left → ↓Y, ↑r
    
    **Demand Shocks**
    - Positive: AD shifts right → ↑P, ↑Y
    - Negative: AD shifts left → ↓P, ↓Y
    
    **Supply Shocks**
    - Positive: SRAS shifts right → ↓P, ↑Y
    - Negative: SRAS shifts left → ↑P, ↓Y
    """)

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_students'])
        st.write(txt['use_policymakers'])
        st.write(txt['use_analysts'])
