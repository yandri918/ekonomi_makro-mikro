import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from scipy.integrate import quad

st.set_page_config(page_title="Supply & Demand", page_icon="⚖️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

# ==================== TRANSLATIONS ====================
T = {
    'EN': {
        'title': "⚖️ Advanced Microeconomics: Supply, Demand & Market Analysis",
        'tab1': "📉 Market Equilibrium Simulator",
        'tab2': "🏛️ Government Interventions",
        'tab3': "💰 Welfare Analysis",
        'tab4': "🧮 Elasticity Calculator",
        
        # Tab 1
        'simulator_title': "Interactive Market Equilibrium Simulator",
        'simulator_intro': "Adjust supply and demand parameters to analyze market equilibrium, consumer/producer surplus, and comparative statics.",
        'params': "⚙️ Market Parameters",
        'dem_func': "**Demand Function:** $Q_d = a - bP$",
        'sup_func': "**Supply Function:** $Q_s = c + dP$",
        'a_label': "Demand Intercept (a)",
        'b_label': "Demand Slope (b)",
        'c_label': "Supply Intercept (c)",
        'd_label': "Supply Slope (d)",
        'advanced_opts': "🔧 Advanced Options",
        'show_surplus': "Show Consumer & Producer Surplus",
        'show_comparative': "Show Comparative Statics",
        'market_scenarios': "📚 Market Scenarios",
        'select_scenario': "Select a pre-configured scenario",
        'custom': "Custom",
        'eq_result': "Market Equilibrium",
        'price': "Price (Rp)",
        'qty': "Quantity (Q)",
        'cs_label': "Consumer Surplus",
        'ps_label': "Producer Surplus",
        'ts_label': "Total Surplus",
        'ped_label': "Price Elasticity of Demand",
        'pes_label': "Price Elasticity of Supply",
        'elastic': "Elastic",
        'inelastic': "Inelastic",
        'unitary': "Unitary",
        
        # Tab 2
        'intervention_title': "Government Market Interventions",
        'intervention_intro': "Analyze the effects of taxes, subsidies, and price controls on market equilibrium.",
        'intervention_type': "Intervention Type",
        'no_intervention': "No Intervention",
        'per_unit_tax': "Per-Unit Tax",
        'ad_valorem_tax': "Ad Valorem Tax (%)",
        'subsidy': "Per-Unit Subsidy",
        'price_ceiling': "Price Ceiling",
        'price_floor': "Price Floor",
        'tax_amount': "Tax Amount (Rp per unit)",
        'tax_rate': "Tax Rate (%)",
        'subsidy_amount': "Subsidy Amount (Rp per unit)",
        'ceiling_price': "Ceiling Price (Rp)",
        'floor_price': "Floor Price (Rp)",
        'original_eq': "Original Equilibrium",
        'new_eq': "New Equilibrium (with intervention)",
        'tax_revenue': "Tax Revenue",
        'gov_expenditure': "Government Expenditure",
        'dwl': "Deadweight Loss",
        'shortage': "Shortage",
        'surplus': "Surplus",
        'buyer_price': "Price Paid by Buyers",
        'seller_price': "Price Received by Sellers",
        'tax_burden_consumers': "Tax Burden on Consumers",
        'tax_burden_producers': "Tax Burden on Producers",
        
        # Tab 3
        'welfare_title': "Welfare Economics Analysis",
        'welfare_intro': "Detailed analysis of consumer surplus, producer surplus, and total welfare.",
        
        # Tab 4
        'el_title': "Elasticity Calculator",
        'el_intro': "Calculate Price Elasticity of Demand (PED) using the Midpoint Method.",
        'p1': "Initial Price (Rp)",
        'p2': "New Price (Rp)",
        'q1': "Initial Quantity (Q1)",
        'q2': "New Quantity (Q2)",
        'calc_btn': "Calculate Elasticity",
        'zero_err': "Price change cannot be zero.",
        'elastic_result': "Result: **ELASTIC** (Consumers are sensitive to price changes)",
        'inelastic_result': "Result: **INELASTIC** (Consumers are not very sensitive)",
        'unitary_result': "Result: **UNITARY ELASTIC**"
    },
    'ID': {
        'title': "⚖️ Ekonomi Mikro Lanjutan: Analisis Pasar Permintaan & Penawaran",
        'tab1': "📉 Simulator Keseimbangan Pasar",
        'tab2': "🏛️ Intervensi Pemerintah",
        'tab3': "💰 Analisis Kesejahteraan",
        'tab4': "🧮 Kalkulator Elastisitas",
        
        # Tab 1
        'simulator_title': "Simulator Keseimbangan Pasar Interaktif",
        'simulator_intro': "Atur parameter penawaran dan permintaan untuk menganalisis keseimbangan pasar, surplus konsumen/produsen, dan statika komparatif.",
        'params': "⚙️ Parameter Pasar",
        'dem_func': "**Fungsi Permintaan:** $Q_d = a - bP$",
        'sup_func': "**Fungsi Penawaran:** $Q_s = c + dP$",
        'a_label': "Intersep Permintaan (a)",
        'b_label': "Kemiringan Permintaan (b)",
        'c_label': "Intersep Penawaran (c)",
        'd_label': "Kemiringan Penawaran (d)",
        'advanced_opts': "🔧 Opsi Lanjutan",
        'show_surplus': "Tampilkan Surplus Konsumen & Produsen",
        'show_comparative': "Tampilkan Statika Komparatif",
        'market_scenarios': "📚 Skenario Pasar",
        'select_scenario': "Pilih skenario yang sudah dikonfigurasi",
        'custom': "Kustom",
        'eq_result': "Keseimbangan Pasar",
        'price': "Harga (Rp)",
        'qty': "Kuantitas (Q)",
        'cs_label': "Surplus Konsumen",
        'ps_label': "Surplus Produsen",
        'ts_label': "Total Surplus",
        'ped_label': "Elastisitas Harga Permintaan",
        'pes_label': "Elastisitas Harga Penawaran",
        'elastic': "Elastis",
        'inelastic': "Inelastis",
        'unitary': "Uniter",
        
        # Tab 2
        'intervention_title': "Intervensi Pasar oleh Pemerintah",
        'intervention_intro': "Analisis efek pajak, subsidi, dan kontrol harga terhadap keseimbangan pasar.",
        'intervention_type': "Jenis Intervensi",
        'no_intervention': "Tanpa Intervensi",
        'per_unit_tax': "Pajak Per Unit",
        'ad_valorem_tax': "Pajak Ad Valorem (%)",
        'subsidy': "Subsidi Per Unit",
        'price_ceiling': "Harga Maksimum (Ceiling)",
        'price_floor': "Harga Minimum (Floor)",
        'tax_amount': "Jumlah Pajak (Rp per unit)",
        'tax_rate': "Tarif Pajak (%)",
        'subsidy_amount': "Jumlah Subsidi (Rp per unit)",
        'ceiling_price': "Harga Maksimum (Rp)",
        'floor_price': "Harga Minimum (Rp)",
        'original_eq': "Keseimbangan Awal",
        'new_eq': "Keseimbangan Baru (dengan intervensi)",
        'tax_revenue': "Pendapatan Pajak",
        'gov_expenditure': "Pengeluaran Pemerintah",
        'dwl': "Deadweight Loss",
        'shortage': "Kekurangan",
        'surplus': "Kelebihan",
        'buyer_price': "Harga Dibayar Pembeli",
        'seller_price': "Harga Diterima Penjual",
        'tax_burden_consumers': "Beban Pajak Konsumen",
        'tax_burden_producers': "Beban Pajak Produsen",
        
        # Tab 3
        'welfare_title': "Analisis Ekonomi Kesejahteraan",
        'welfare_intro': "Analisis detail surplus konsumen, surplus produsen, dan total kesejahteraan.",
        
        # Tab 4
        'el_title': "Kalkulator Elastisitas",
        'el_intro': "Hitung Elastisitas Harga Permintaan (PED) menggunakan Metode Titik Tengah.",
        'p1': "Harga Awal (Rp)",
        'p2': "Harga Baru (Rp)",
        'q1': "Kuantitas Awal (Q1)",
        'q2': "Kuantitas Baru (Q2)",
        'calc_btn': "Hitung Elastisitas",
        'zero_err': "Perubahan harga tidak boleh nol.",
        'elastic_result': "Hasil: **ELASTIS** (Konsumen peka terhadap perubahan harga)",
        'inelastic_result': "Hasil: **INELASTIS** (Konsumen tidak terlalu peka)",
        'unitary_result': "Hasil: **ELASTIS UNITER**"
    }
}

txt = T[lang]

# ==================== HELPER FUNCTIONS ====================

@st.cache_data
def calculate_equilibrium(a, b, c, d):
    """Calculate market equilibrium price and quantity"""
    if b + d == 0:
        return None, None
    P_eq = (a - c) / (b + d)
    Q_eq = a - b * P_eq
    return P_eq, Q_eq

@st.cache_data
def calculate_surplus(P_eq, Q_eq, a, b, c, d):
    """Calculate consumer and producer surplus"""
    # Consumer Surplus: Area of triangle above P_eq, below demand curve
    P_max = a / b if b > 0 else 0
    CS = 0.5 * (P_max - P_eq) * Q_eq
    
    # Producer Surplus: Area of triangle below P_eq, above supply curve
    P_min = -c / d if d > 0 else 0
    PS = 0.5 * (P_eq - P_min) * Q_eq
    
    TS = CS + PS
    return CS, PS, TS

@st.cache_data
def calculate_elasticity_at_point(P, Q, slope, is_demand=True):
    """Calculate price elasticity at a given point"""
    if Q == 0:
        return 0
    if is_demand:
        # For demand: Ed = (dQ/dP) * (P/Q) = -b * (P/Q)
        elasticity = abs(slope * (P / Q))
    else:
        # For supply: Es = (dQ/dP) * (P/Q) = d * (P/Q)
        elasticity = abs(slope * (P / Q))
    return elasticity

@st.cache_data
def apply_per_unit_tax(a, b, c, d, tax):
    """Calculate new equilibrium with per-unit tax"""
    # Tax shifts supply curve up by tax amount
    # New supply: Qs = c + d(P - tax) = (c - d*tax) + dP
    c_new = c - d * tax
    P_eq_new, Q_eq_new = calculate_equilibrium(a, b, c_new, d)
    
    # Price paid by buyers
    P_buyers = P_eq_new
    # Price received by sellers
    P_sellers = P_buyers - tax
    
    # Tax revenue
    tax_revenue = tax * Q_eq_new if Q_eq_new else 0
    
    # Deadweight loss (triangle area)
    P_eq_original, Q_eq_original = calculate_equilibrium(a, b, c, d)
    if Q_eq_original and Q_eq_new:
        DWL = 0.5 * tax * abs(Q_eq_original - Q_eq_new)
    else:
        DWL = 0
    
    return P_buyers, P_sellers, Q_eq_new, tax_revenue, DWL

@st.cache_data
def apply_subsidy(a, b, c, d, subsidy):
    """Calculate new equilibrium with per-unit subsidy"""
    # Subsidy shifts supply curve down
    c_new = c + d * subsidy
    P_eq_new, Q_eq_new = calculate_equilibrium(a, b, c_new, d)
    
    P_buyers = P_eq_new
    P_sellers = P_buyers + subsidy
    
    gov_expenditure = subsidy * Q_eq_new if Q_eq_new else 0
    
    return P_buyers, P_sellers, Q_eq_new, gov_expenditure

@st.cache_data
def apply_price_ceiling(a, b, c, d, P_ceiling):
    """Calculate effects of price ceiling"""
    P_eq, Q_eq = calculate_equilibrium(a, b, c, d)
    
    if P_ceiling >= P_eq:
        # Ceiling is not binding
        return P_eq, Q_eq, 0, False
    
    # Ceiling is binding
    Q_demanded = a - b * P_ceiling
    Q_supplied = c + d * P_ceiling
    shortage = Q_demanded - Q_supplied
    
    # Quantity traded is the minimum
    Q_traded = min(Q_demanded, Q_supplied)
    
    return P_ceiling, Q_traded, shortage, True

@st.cache_data
def apply_price_floor(a, b, c, d, P_floor):
    """Calculate effects of price floor"""
    P_eq, Q_eq = calculate_equilibrium(a, b, c, d)
    
    if P_floor <= P_eq:
        # Floor is not binding
        return P_eq, Q_eq, 0, False
    
    # Floor is binding
    Q_demanded = a - b * P_floor
    Q_supplied = c + d * P_floor
    surplus = Q_supplied - Q_demanded
    
    # Quantity traded is the minimum
    Q_traded = min(Q_demanded, Q_supplied)
    
    return P_floor, Q_traded, surplus, True

def get_market_scenarios():
    """Pre-configured market scenarios"""
    scenarios = {
        'Custom': {'a': 100, 'b': 1.0, 'c': 20, 'd': 1.0, 'desc': 'Custom parameters'},
        'Agricultural Market (Rice)': {
            'a': 150, 'b': 2.0, 'c': 30, 'd': 1.5,
            'desc': 'Inelastic demand (necessity), moderate supply elasticity'
        },
        'Technology Market (Smartphones)': {
            'a': 200, 'b': 3.0, 'c': 50, 'd': 2.5,
            'desc': 'Elastic demand (luxury), elastic supply'
        },
        'Energy Market (Gasoline)': {
            'a': 120, 'b': 0.8, 'c': 40, 'd': 0.6,
            'desc': 'Very inelastic demand and supply (short-run)'
        },
        'Housing Market': {
            'a': 180, 'b': 1.2, 'c': 60, 'd': 0.8,
            'desc': 'Inelastic supply (construction takes time)'
        },
        'Labor Market': {
            'a': 160, 'b': 1.5, 'c': 40, 'd': 1.8,
            'desc': 'Wage as price, workers as quantity'
        }
    }
    return scenarios

# ==================== MAIN UI ====================

st.title(txt['title'])

# Initialize session state for comparative statics
if 'prev_params' not in st.session_state:
    st.session_state.prev_params = None

tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ==================== TAB 1: MARKET EQUILIBRIUM SIMULATOR ====================
with tab1:
    st.markdown(f"### {txt['simulator_title']}")
    st.markdown(txt['simulator_intro'])
    
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader(txt['params'])
        
        # Market Scenarios
        with st.expander(txt['market_scenarios'], expanded=False):
            scenarios = get_market_scenarios()
            scenario_name = st.selectbox(
                txt['select_scenario'],
                list(scenarios.keys()),
                key='scenario_selector'
            )
            
            if scenario_name != 'Custom':
                st.info(scenarios[scenario_name]['desc'])
        
        # Get parameters from scenario or use sliders
        if scenario_name != 'Custom':
            params = scenarios[scenario_name]
            a = params['a']
            b = params['b']
            c = params['c']
            d = params['d']
            
            # Display values
            st.markdown(txt['dem_func'])
            st.write(f"a = {a}, b = {b}")
            st.markdown(txt['sup_func'])
            st.write(f"c = {c}, d = {d}")
        else:
            st.markdown(txt['dem_func'])
            a = st.slider(txt['a_label'], 50, 200, 100, key='a_slider')
            b = st.slider(txt['b_label'], 0.5, 5.0, 1.0, step=0.1, key='b_slider')
            
            st.markdown("---")
            
            st.markdown(txt['sup_func'])
            c = st.slider(txt['c_label'], 0, 100, 20, key='c_slider')
            d = st.slider(txt['d_label'], 0.5, 5.0, 1.0, step=0.1, key='d_slider')
        
        st.markdown("---")
        
        # Advanced Options
        with st.expander(txt['advanced_opts'], expanded=True):
            show_surplus = st.checkbox(txt['show_surplus'], value=True)
            show_comparative = st.checkbox(txt['show_comparative'], value=False)
    
    with col_right:
        # Calculate equilibrium
        P_eq, Q_eq = calculate_equilibrium(a, b, c, d)
        
        if P_eq is None or Q_eq is None or c >= a:
            st.error("Invalid market parameters! Supply intercept must be lower than demand intercept.")
        else:
            # Generate data for plotting
            P_max = (a / b) if b > 0 else 100
            prices = np.linspace(0, max(P_max, P_eq * 1.5), 200)
            
            df = pd.DataFrame({'Price': prices})
            df['Demand'] = a - b * df['Price']
            df['Supply'] = c + d * df['Price']
            
            # Filter negative quantities
            df = df[(df['Demand'] >= 0) & (df['Supply'] >= 0)]
            
            # Create visualization
            df_melted = df.melt('Price', var_name='Type', value_name='Quantity')
            
            # Base chart
            base = alt.Chart(df_melted).encode(
                x=alt.X('Quantity:Q', title=txt['qty'], scale=alt.Scale(domain=[0, max(df['Demand'].max(), df['Supply'].max()) * 1.1])),
                y=alt.Y('Price:Q', title=txt['price'])
            )
            
            # Supply and Demand lines
            lines = base.mark_line(size=3).encode(
                color=alt.Color('Type:N', 
                    scale=alt.Scale(domain=['Demand', 'Supply'], range=['#FF4B4B', '#1C83E1']),
                    legend=alt.Legend(title='Curve')
                )
            )
            
            # Equilibrium point
            eq_df = pd.DataFrame({'Price': [P_eq], 'Quantity': [Q_eq]})
            eq_point = alt.Chart(eq_df).mark_point(
                size=300, fill='gold', stroke='black', strokeWidth=2
            ).encode(
                x='Quantity:Q',
                y='Price:Q',
                tooltip=[
                    alt.Tooltip('Quantity:Q', format=',.2f', title=txt['qty']),
                    alt.Tooltip('Price:Q', format=',.2f', title=txt['price'])
                ]
            )
            
            # Equilibrium label
            eq_text = eq_point.mark_text(
                align='left', baseline='bottom', dx=10, dy=-10, fontSize=14, fontWeight='bold'
            ).encode(
                text=alt.value(f"E* ({Q_eq:.1f}, {P_eq:.1f})")
            )
            
            chart = lines + eq_point + eq_text
            
            # Add surplus shading if enabled
            if show_surplus:
                # Consumer Surplus (triangle above P_eq, below demand)
                P_max_demand = a / b
                cs_data = pd.DataFrame({
                    'Quantity': [0, Q_eq, 0],
                    'Price': [P_max_demand, P_eq, P_eq]
                })
                cs_area = alt.Chart(cs_data).mark_area(
                    opacity=0.3, color='blue'
                ).encode(
                    x='Quantity:Q',
                    y='Price:Q'
                )
                
                # Producer Surplus (triangle below P_eq, above supply)
                P_min_supply = -c / d if d > 0 else 0
                ps_data = pd.DataFrame({
                    'Quantity': [0, Q_eq, 0],
                    'Price': [P_min_supply, P_eq, P_eq]
                })
                ps_area = alt.Chart(ps_data).mark_area(
                    opacity=0.3, color='green'
                ).encode(
                    x='Quantity:Q',
                    y='Price:Q'
                )
                
                chart = chart + cs_area + ps_area
            
            st.altair_chart(chart.interactive(), use_container_width=True)
            
            # Display equilibrium results
            col_eq1, col_eq2, col_eq3 = st.columns(3)
            
            with col_eq1:
                st.metric(txt['price'] + " (P*)", f"Rp {P_eq:,.2f}")
            with col_eq2:
                st.metric(txt['qty'] + " (Q*)", f"{Q_eq:,.2f}")
            with col_eq3:
                # Calculate and display elasticities
                PED = calculate_elasticity_at_point(P_eq, Q_eq, b, is_demand=True)
                PES = calculate_elasticity_at_point(P_eq, Q_eq, d, is_demand=False)
                
                if PED > 1:
                    ped_type = txt['elastic']
                elif PED < 1:
                    ped_type = txt['inelastic']
                else:
                    ped_type = txt['unitary']
                
                st.metric(txt['ped_label'], f"{PED:.2f}", delta=ped_type)
            
            # Display surplus if enabled
            if show_surplus:
                CS, PS, TS = calculate_surplus(P_eq, Q_eq, a, b, c, d)
                
                st.markdown("---")
                st.markdown("### 💰 Welfare Analysis")
                
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    st.metric(txt['cs_label'], f"Rp {CS:,.2f}")
                with col_s2:
                    st.metric(txt['ps_label'], f"Rp {PS:,.2f}")
                with col_s3:
                    st.metric(txt['ts_label'], f"Rp {TS:,.2f}")

# ==================== TAB 2: GOVERNMENT INTERVENTIONS ====================
with tab2:
    st.markdown(f"### {txt['intervention_title']}")
    st.markdown(txt['intervention_intro'])
    
    col_int_left, col_int_right = st.columns([1, 2])
    
    with col_int_left:
        st.subheader(txt['intervention_type'])
        
        intervention = st.selectbox(
            "Select intervention:",
            [txt['no_intervention'], txt['per_unit_tax'], txt['ad_valorem_tax'], 
             txt['subsidy'], txt['price_ceiling'], txt['price_floor']]
        )
        
        # Use same base parameters from Tab 1
        st.markdown("---")
        st.markdown("**Base Market Parameters:**")
        st.write(f"Demand: Qd = {a} - {b}P")
        st.write(f"Supply: Qs = {c} + {d}P")
        
        # Original equilibrium
        P_eq_orig, Q_eq_orig = calculate_equilibrium(a, b, c, d)
        st.info(f"**{txt['original_eq']}:**\nP* = Rp {P_eq_orig:,.2f}\nQ* = {Q_eq_orig:,.2f}")
        
        st.markdown("---")
        
        # Intervention parameters
        if intervention == txt['per_unit_tax']:
            tax_amount = st.slider(txt['tax_amount'], 0.0, 50.0, 10.0, step=1.0)
            P_buyers, P_sellers, Q_new, tax_revenue, DWL = apply_per_unit_tax(a, b, c, d, tax_amount)
            
        elif intervention == txt['ad_valorem_tax']:
            tax_rate = st.slider(txt['tax_rate'], 0.0, 50.0, 10.0, step=1.0)
            # Ad valorem tax: tax = rate * P
            # This requires iterative solution, simplified here
            st.warning("Ad valorem tax requires iterative calculation (simplified version)")
            tax_amount = (tax_rate / 100) * P_eq_orig
            P_buyers, P_sellers, Q_new, tax_revenue, DWL = apply_per_unit_tax(a, b, c, d, tax_amount)
            
        elif intervention == txt['subsidy']:
            subsidy_amount = st.slider(txt['subsidy_amount'], 0.0, 50.0, 10.0, step=1.0)
            P_buyers, P_sellers, Q_new, gov_expenditure = apply_subsidy(a, b, c, d, subsidy_amount)
            
        elif intervention == txt['price_ceiling']:
            ceiling_price = st.slider(txt['ceiling_price'], 0.0, P_eq_orig * 1.5, P_eq_orig * 0.8, step=1.0)
            P_new, Q_new, shortage, is_binding = apply_price_ceiling(a, b, c, d, ceiling_price)
            
        elif intervention == txt['price_floor']:
            floor_price = st.slider(txt['floor_price'], 0.0, P_eq_orig * 2, P_eq_orig * 1.2, step=1.0)
            P_new, Q_new, surplus_qty, is_binding = apply_price_floor(a, b, c, d, floor_price)
    
    with col_int_right:
        if intervention == txt['no_intervention']:
            st.info("Select an intervention type to see the analysis.")
            
        elif intervention in [txt['per_unit_tax'], txt['ad_valorem_tax']]:
            # Display tax analysis
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                st.metric(txt['buyer_price'], f"Rp {P_buyers:,.2f}", delta=f"{P_buyers - P_eq_orig:+.2f}")
            with col_t2:
                st.metric(txt['seller_price'], f"Rp {P_sellers:,.2f}", delta=f"{P_sellers - P_eq_orig:+.2f}")
            with col_t3:
                st.metric(txt['qty'], f"{Q_new:,.2f}", delta=f"{Q_new - Q_eq_orig:+.2f}")
            
            st.markdown("---")
            
            col_t4, col_t5, col_t6 = st.columns(3)
            with col_t4:
                st.metric(txt['tax_revenue'], f"Rp {tax_revenue:,.2f}")
            with col_t5:
                st.metric(txt['dwl'], f"Rp {DWL:,.2f}")
            with col_t6:
                # Tax burden
                consumer_burden = P_buyers - P_eq_orig
                producer_burden = P_eq_orig - P_sellers
                st.metric(txt['tax_burden_consumers'], f"Rp {consumer_burden:,.2f}")
            
            # Visualization
            st.markdown("---")
            st.markdown("**Market with Tax:**")
            
            # Create visualization with tax
            prices = np.linspace(0, max(a/b, P_buyers * 1.3), 200)
            df_tax = pd.DataFrame({'Price': prices})
            df_tax['Demand'] = a - b * df_tax['Price']
            df_tax['Supply_Original'] = c + d * df_tax['Price']
            df_tax['Supply_With_Tax'] = (c - d * tax_amount) + d * df_tax['Price']
            
            df_tax = df_tax[(df_tax['Demand'] >= 0) & (df_tax['Supply_Original'] >= 0)]
            
            # Plot
            chart_tax = alt.Chart(df_tax).transform_fold(
                ['Demand', 'Supply_Original', 'Supply_With_Tax'],
                as_=['Type', 'Quantity']
            ).mark_line(size=2).encode(
                x=alt.X('Quantity:Q', title=txt['qty']),
                y=alt.Y('Price:Q', title=txt['price']),
                color=alt.Color('Type:N', scale=alt.Scale(
                    domain=['Demand', 'Supply_Original', 'Supply_With_Tax'],
                    range=['#FF4B4B', '#1C83E1', '#FFA500']
                )),
                strokeDash=alt.condition(
                    alt.datum.Type == 'Supply_With_Tax',
                    alt.value([5, 5]),
                    alt.value([0])
                )
            )
            
            # Add equilibrium points
            eq_points_df = pd.DataFrame({
                'Quantity': [Q_eq_orig, Q_new],
                'Price': [P_eq_orig, P_buyers],
                'Label': ['Original E', 'New E']
            })
            
            eq_points = alt.Chart(eq_points_df).mark_point(size=200, filled=True).encode(
                x='Quantity:Q',
                y='Price:Q',
                color=alt.Color('Label:N', scale=alt.Scale(domain=['Original E', 'New E'], range=['gold', 'red'])),
                tooltip=['Label', 'Quantity', 'Price']
            )
            
            st.altair_chart((chart_tax + eq_points).interactive(), use_container_width=True)
            
        elif intervention == txt['subsidy']:
            # Display subsidy analysis
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric(txt['buyer_price'], f"Rp {P_buyers:,.2f}", delta=f"{P_buyers - P_eq_orig:+.2f}")
            with col_s2:
                st.metric(txt['seller_price'], f"Rp {P_sellers:,.2f}", delta=f"{P_sellers - P_eq_orig:+.2f}")
            with col_s3:
                st.metric(txt['qty'], f"{Q_new:,.2f}", delta=f"{Q_new - Q_eq_orig:+.2f}")
            
            st.markdown("---")
            st.metric(txt['gov_expenditure'], f"Rp {gov_expenditure:,.2f}")
            
        elif intervention == txt['price_ceiling']:
            if not is_binding:
                st.warning(f"Price ceiling (Rp {ceiling_price:.2f}) is above equilibrium price (Rp {P_eq_orig:.2f}). Not binding!")
            else:
                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    st.metric(txt['price'], f"Rp {P_new:,.2f}")
                with col_c2:
                    st.metric(txt['qty'] + " Traded", f"{Q_new:,.2f}")
                with col_c3:
                    st.metric(txt['shortage'], f"{shortage:,.2f}", delta="Excess Demand")
                
                st.error(f"⚠️ Shortage of {shortage:.2f} units! Quantity demanded exceeds quantity supplied.")
                
        elif intervention == txt['price_floor']:
            if not is_binding:
                st.warning(f"Price floor (Rp {floor_price:.2f}) is below equilibrium price (Rp {P_eq_orig:.2f}). Not binding!")
            else:
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    st.metric(txt['price'], f"Rp {P_new:,.2f}")
                with col_f2:
                    st.metric(txt['qty'] + " Traded", f"{Q_new:,.2f}")
                with col_f3:
                    st.metric(txt['surplus'], f"{surplus_qty:,.2f}", delta="Excess Supply")
                
                st.error(f"⚠️ Surplus of {surplus_qty:.2f} units! Quantity supplied exceeds quantity demanded.")

# ==================== TAB 3: WELFARE ANALYSIS ====================
with tab3:
    st.markdown(f"### {txt['welfare_title']}")
    st.markdown(txt['welfare_intro'])
    
    # Calculate welfare for current equilibrium
    P_eq, Q_eq = calculate_equilibrium(a, b, c, d)
    
    if P_eq and Q_eq:
        CS, PS, TS = calculate_surplus(P_eq, Q_eq, a, b, c, d)
        
        col_w1, col_w2, col_w3 = st.columns(3)
        
        with col_w1:
            st.markdown("#### 🔵 Consumer Surplus")
            st.metric("CS", f"Rp {CS:,.2f}")
            st.latex(r"CS = \frac{1}{2} \times (P_{max} - P^*) \times Q^*")
            st.write(f"= 0.5 × ({a/b:.2f} - {P_eq:.2f}) × {Q_eq:.2f}")
            st.write(f"= Rp {CS:,.2f}")
            
        with col_w2:
            st.markdown("#### 🟢 Producer Surplus")
            st.metric("PS", f"Rp {PS:,.2f}")
            st.latex(r"PS = \frac{1}{2} \times (P^* - P_{min}) \times Q^*")
            P_min = -c/d if d > 0 else 0
            st.write(f"= 0.5 × ({P_eq:.2f} - {P_min:.2f}) × {Q_eq:.2f}")
            st.write(f"= Rp {PS:,.2f}")
            
        with col_w3:
            st.markdown("#### 💎 Total Surplus")
            st.metric("TS", f"Rp {TS:,.2f}")
            st.latex(r"TS = CS + PS")
            st.write(f"= {CS:.2f} + {PS:.2f}")
            st.write(f"= Rp {TS:,.2f}")
        
        st.markdown("---")
        
        # Welfare distribution visualization
        welfare_data = pd.DataFrame({
            'Type': ['Consumer Surplus', 'Producer Surplus'],
            'Value': [CS, PS]
        })
        
        welfare_chart = alt.Chart(welfare_data).mark_bar().encode(
            x=alt.X('Type:N', title=''),
            y=alt.Y('Value:Q', title='Surplus (Rp)'),
            color=alt.Color('Type:N', scale=alt.Scale(domain=['Consumer Surplus', 'Producer Surplus'], range=['#4169E1', '#32CD32'])),
            tooltip=['Type', alt.Tooltip('Value:Q', format=',.2f')]
        ).properties(height=300)
        
        st.altair_chart(welfare_chart, use_container_width=True)
        
        # Educational explanation
        with st.expander("📚 Understanding Surplus", expanded=False):
            st.markdown("""
            **Consumer Surplus (CS):**
            - Represents the benefit consumers receive from purchasing at market price
            - It's the difference between what consumers are willing to pay and what they actually pay
            - Graphically: Area below demand curve, above equilibrium price
            
            **Producer Surplus (PS):**
            - Represents the benefit producers receive from selling at market price
            - It's the difference between market price and the minimum price producers would accept
            - Graphically: Area above supply curve, below equilibrium price
            
            **Total Surplus (TS):**
            - Sum of consumer and producer surplus
            - Represents total welfare/benefit to society
            - Maximized at competitive equilibrium (no deadweight loss)
            """)

# ==================== TAB 4: ELASTICITY CALCULATOR ====================
with tab4:
    st.markdown(f"### {txt['el_title']}")
    st.markdown(txt['el_intro'])
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        P1 = st.number_input(txt['p1'], value=10.0, key='elas_p1')
        P2 = st.number_input(txt['p2'], value=12.0, key='elas_p2')
        
    with col_e2:
        Q1 = st.number_input(txt['q1'], value=100.0, key='elas_q1')
        Q2 = st.number_input(txt['q2'], value=80.0, key='elas_q2')
        
    if st.button(txt['calc_btn']):
        # Midpoint Formula
        delta_Q = Q2 - Q1
        avg_Q = (Q2 + Q1) / 2
        pct_change_Q = delta_Q / avg_Q
        
        delta_P = P2 - P1
        avg_P = (P2 + P1) / 2
        pct_change_P = delta_P / avg_P
        
        if pct_change_P == 0:
            st.error(txt['zero_err'])
        else:
            PED = abs(pct_change_Q / pct_change_P)
            
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                st.metric("% Change in Quantity", f"{pct_change_Q * 100:.2f}%")
            with col_r2:
                st.metric("% Change in Price", f"{pct_change_P * 100:.2f}%")
            with col_r3:
                st.metric("Price Elasticity (|Ed|)", f"{PED:.2f}")
            
            st.markdown("---")
            
            if PED > 1:
                st.success(txt['elastic_result'])
                st.info("💡 A 1% increase in price leads to more than 1% decrease in quantity demanded.")
            elif PED < 1:
                st.warning(txt['inelastic_result'])
                st.info("💡 A 1% increase in price leads to less than 1% decrease in quantity demanded.")
            else:
                st.info(txt['unitary_result'])
                st.info("💡 A 1% increase in price leads to exactly 1% decrease in quantity demanded.")
            
            st.markdown("---")
            st.markdown("**Formula (Midpoint Method):**")
            st.latex(r"E_d = \left| \frac{\% \Delta Q}{\% \Delta P} \right| = \left| \frac{(Q_2 - Q_1) / [(Q_2 + Q_1)/2]}{(P_2 - P_1) / [(P_2 + P_1)/2]} \right|")
            
            st.markdown("**Calculation:**")
            st.write(f"Ed = |({Q2} - {Q1}) / {avg_Q:.2f}| / |({P2} - {P1}) / {avg_P:.2f}|")
            st.write(f"Ed = |{pct_change_Q:.4f}| / |{pct_change_P:.4f}|")
            st.write(f"Ed = **{PED:.2f}**")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Advanced Microeconomics Simulator | Built with Streamlit & Altair</p>
    <p>📚 Educational tool for economics students and analysts</p>
</div>
""", unsafe_allow_html=True)
