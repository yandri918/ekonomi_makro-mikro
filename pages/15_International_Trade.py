import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="International Trade", page_icon="🌐", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "🌐 International Trade & Policy",
        'subtitle': "Analyze **Comparative Advantage** and **Tariff Impacts** for trade policy decisions.",
        'tab1': "📊 Comparative Advantage",
        'tab2': "💰 Tariff Impact Simulator",
        # Tab 1
        'ca_theory': "**Theory**: Ricardo's Comparative Advantage - Countries should specialize in goods where they have the lowest opportunity cost.",
        'country_a': "Country A Name",
        'country_b': "Country B Name",
        'product_1': "Product 1 Name",
        'product_2': "Product 2 Name",
        'labor_matrix': "Labor Hours Required (per unit)",
        'country': "Country",
        'calc_btn': "🔍 Calculate Advantage",
        'results': "📋 Analysis Results",
        'opp_cost': "Opportunity Cost Analysis",
        'opp_cost_exp': "**{country}** to produce 1 unit of **{prod}**, must give up **{oc:.2f}** units of **{other}**.",
        'advantage': "✅ **Comparative Advantage**:",
        'adv_result': "**{country}** should specialize in **{prod}** (Lower opportunity cost: {oc:.2f})",
        'trade_gains': "🤝 Gains from Trade",
        'trade_insight': "If both countries specialize and trade, total world production increases. Both countries can consume beyond their individual PPF!",
        'ppf_title': "Production Possibilities Frontier (PPF)",
        # Tab 2
        'tariff_theory': "**Theory**: Tariffs protect domestic producers but create deadweight loss and hurt consumers.",
        'demand_params': "📉 Domestic Demand",
        'supply_params': "📈 Domestic Supply",
        'trade_params': "🌍 World Trade",
        'demand_int': "Demand Intercept (Max Price)",
        'demand_slope': "Demand Slope",
        'supply_int': "Supply Intercept (Min Price)",
        'supply_slope': "Supply Slope",
        'world_price': "World Price (Free Trade)",
        'tariff_rate': "Tariff Rate (%)",
        'analyze_btn': "📊 Analyze Tariff Impact",
        'welfare_analysis': "💵 Welfare Analysis",
        'free_trade': "Free Trade",
        'with_tariff': "With Tariff",
        'consumer_surplus': "Consumer Surplus",
        'producer_surplus': "Producer Surplus",
        'govt_revenue': "Government Revenue (Tariff)",
        'total_surplus': "Total Surplus",
        'dwl': "Deadweight Loss (DWL)",
        'tariff_insight': "**Impact Summary**: Tariff increases producer surplus by **Rp {ps_gain:,.0f}** but decreases consumer surplus by **Rp {cs_loss:,.0f}**. Government collects **Rp {rev:,.0f}** in tariff revenue. Net welfare loss (DWL): **Rp {dwl:,.0f}**.",
        'chart_title': "Supply, Demand & Tariff Impact",
        # Story
        'story_title': "📚 Story & Use Cases: International Trade",
        'story_meaning': "**What is this?**\nThis module analyzes trade policy using Comparative Advantage (who should produce what) and Tariff Impact (costs of protectionism).",
        'story_insight': "**Key Insight:**\nFree trade based on comparative advantage maximizes global welfare. Tariffs help specific industries but create net losses for the economy.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Trade Ministry:** To evaluate FTA (Free Trade Agreement) benefits and tariff policy impacts.",
        'use_corp': "🏢 **Export Companies:** To identify which products have competitive advantage in international markets.",
        'use_analyst': "📈 **Policy Analysts:** To quantify the welfare costs of protectionist policies."
    },
    'ID': {
        'title': "🌐 Perdagangan Internasional & Kebijakan",
        'subtitle': "Analisis **Keunggulan Komparatif** dan **Dampak Tarif** untuk keputusan kebijakan perdagangan.",
        'tab1': "📊 Keunggulan Komparatif",
        'tab2': "💰 Simulator Dampak Tarif",
        # Tab 1
        'ca_theory': "**Teori**: Keunggulan Komparatif Ricardo - Negara harus spesialisasi pada barang dengan biaya peluang terendah.",
        'country_a': "Nama Negara A",
        'country_b': "Nama Negara B",
        'product_1': "Nama Produk 1",
        'product_2': "Nama Produk 2",
        'labor_matrix': "Jam Kerja Dibutuhkan (per unit)",
        'country': "Negara",
        'calc_btn': "🔍 Hitung Keunggulan",
        'results': "📋 Hasil Analisis",
        'opp_cost': "Analisis Biaya Peluang",
        'opp_cost_exp': "**{country}** untuk memproduksi 1 unit **{prod}**, harus mengorbankan **{oc:.2f}** unit **{other}**.",
        'advantage': "✅ **Keunggulan Komparatif**:",
        'adv_result': "**{country}** sebaiknya spesialisasi di **{prod}** (Biaya peluang lebih rendah: {oc:.2f})",
        'trade_gains': "🤝 Keuntungan dari Perdagangan",
        'trade_insight': "Jika kedua negara spesialisasi dan berdagang, total produksi dunia meningkat. Kedua negara bisa konsumsi melebihi PPF individu mereka!",
        'ppf_title': "Kurva Kemungkinan Produksi (PPF)",
        # Tab 2
        'tariff_theory': "**Teori**: Tarif melindungi produsen domestik tapi menciptakan kerugian deadweight dan merugikan konsumen.",
        'demand_params': "📉 Permintaan Domestik",
        'supply_params': "📈 Penawaran Domestik",
        'trade_params': "🌍 Perdagangan Dunia",
        'demand_int': "Intersep Permintaan (Harga Maks)",
        'demand_slope': "Kemiringan Permintaan",
        'supply_int': "Intersep Penawaran (Harga Min)",
        'supply_slope': "Kemiringan Penawaran",
        'world_price': "Harga Dunia (Perdagangan Bebas)",
        'tariff_rate': "Tarif (%)",
        'analyze_btn': "📊 Analisis Dampak Tarif",
        'welfare_analysis': "💵 Analisis Kesejahteraan",
        'free_trade': "Perdagangan Bebas",
        'with_tariff': "Dengan Tarif",
        'consumer_surplus': "Surplus Konsumen",
        'producer_surplus': "Surplus Produsen",
        'govt_revenue': "Pendapatan Pemerintah (Tarif)",
        'total_surplus': "Total Surplus",
        'dwl': "Deadweight Loss (DWL)",
        'tariff_insight': "**Ringkasan Dampak**: Tarif meningkatkan surplus produsen sebesar **Rp {ps_gain:,.0f}** tapi menurunkan surplus konsumen sebesar **Rp {cs_loss:,.0f}**. Pemerintah mengumpulkan **Rp {rev:,.0f}** dari tarif. Kerugian kesejahteraan bersih (DWL): **Rp {dwl:,.0f}**.",
        'chart_title': "Penawaran, Permintaan & Dampak Tarif",
        # Story
        'story_title': "📚 Cerita & Kasus Penggunaan: Perdagangan Internasional",
        'story_meaning': "**Apa artinya ini?**\nModul ini menganalisis kebijakan perdagangan menggunakan Keunggulan Komparatif (siapa produksi apa) dan Dampak Tarif (biaya proteksionisme).",
        'story_insight': "**Wawasan Utama:**\nPerdagangan bebas berdasarkan keunggulan komparatif memaksimalkan kesejahteraan global. Tarif membantu industri tertentu tapi menciptakan kerugian bersih bagi ekonomi.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Kementerian Perdagangan:** Untuk mengevaluasi manfaat FTA dan dampak kebijakan tarif.",
        'use_corp': "🏢 **Perusahaan Eksportir:** Untuk mengidentifikasi produk mana yang punya keunggulan kompetitif di pasar internasional.",
        'use_analyst': "📈 **Analis Kebijakan:** Untuk mengukur biaya kesejahteraan dari kebijakan proteksionis."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- TABS ---
tab1, tab2 = st.tabs([txt['tab1'], txt['tab2']])

# ========== TAB 1: COMPARATIVE ADVANTAGE ==========
with tab1:
    st.info(txt['ca_theory'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🌍 " + txt['labor_matrix'])
        
        country_a = st.text_input(txt['country_a'], value="Indonesia")
        country_b = st.text_input(txt['country_b'], value="Vietnam")
        product_1 = st.text_input(txt['product_1'], value="Rice")
        product_2 = st.text_input(txt['product_2'], value="Textiles")
        
        st.markdown("---")
        
        # Labor Matrix
        st.markdown(f"**{country_a}**")
        a_p1 = st.number_input(f"{product_1} (hours)", value=2.0, step=0.5, key='a_p1')
        a_p2 = st.number_input(f"{product_2} (hours)", value=4.0, step=0.5, key='a_p2')
        
        st.markdown(f"**{country_b}**")
        b_p1 = st.number_input(f"{product_1} (hours)", value=3.0, step=0.5, key='b_p1')
        b_p2 = st.number_input(f"{product_2} (hours)", value=3.0, step=0.5, key='b_p2')
        
        calc_btn = st.button(txt['calc_btn'], type='primary')
    
    with col2:
        if calc_btn:
            st.subheader(txt['results'])
            
            # Opportunity Cost Calculation
            # OC of P1 in Country A = How much P2 must be given up to produce 1 unit of P1
            # OC(P1_A) = Labor(P1_A) / Labor(P2_A)
            oc_a_p1 = a_p1 / a_p2  # To produce 1 P1, give up this much P2
            oc_a_p2 = a_p2 / a_p1  # To produce 1 P2, give up this much P1
            
            oc_b_p1 = b_p1 / b_p2
            oc_b_p2 = b_p2 / b_p1
            
            st.markdown(f"### {txt['opp_cost']}")
            st.write(txt['opp_cost_exp'].format(country=country_a, prod=product_1, oc=oc_a_p1, other=product_2))
            st.write(txt['opp_cost_exp'].format(country=country_a, prod=product_2, oc=oc_a_p2, other=product_1))
            st.write(txt['opp_cost_exp'].format(country=country_b, prod=product_1, oc=oc_b_p1, other=product_2))
            st.write(txt['opp_cost_exp'].format(country=country_b, prod=product_2, oc=oc_b_p2, other=product_1))
            
            st.markdown("---")
            st.markdown(f"### {txt['advantage']}")
            
            # Determine Comparative Advantage
            if oc_a_p1 < oc_b_p1:
                st.success(txt['adv_result'].format(country=country_a, prod=product_1, oc=oc_a_p1))
                st.success(txt['adv_result'].format(country=country_b, prod=product_2, oc=oc_b_p2))
            else:
                st.success(txt['adv_result'].format(country=country_b, prod=product_1, oc=oc_b_p1))
                st.success(txt['adv_result'].format(country=country_a, prod=product_2, oc=oc_a_p2))
            
            st.info(txt['trade_gains'])
            st.write(txt['trade_insight'])
            
            # PPF Visualization
            # Assume 100 hours of labor available
            total_hours = 100
            
            # Country A PPF: If all labor to P1 -> 100/a_p1, If all to P2 -> 100/a_p2
            a_max_p1 = total_hours / a_p1
            a_max_p2 = total_hours / a_p2
            
            b_max_p1 = total_hours / b_p1
            b_max_p2 = total_hours / b_p2
            
            # PPF is linear: P1 + (a_p1/a_p2)*P2 = a_max_p1
            df_ppf = pd.DataFrame({
                'Product 1': [0, a_max_p1, 0, b_max_p1],
                'Product 2': [a_max_p2, 0, b_max_p2, 0],
                'Country': [country_a, country_a, country_b, country_b]
            })
            
            chart = alt.Chart(df_ppf).mark_line(point=True).encode(
                x=alt.X('Product 1', title=product_1),
                y=alt.Y('Product 2', title=product_2),
                color='Country',
                tooltip=['Country', 'Product 1', 'Product 2']
            ).properties(title=txt['ppf_title'], height=400)
            
            st.altair_chart(chart, use_container_width=True)

# ========== TAB 2: TARIFF IMPACT ==========
with tab2:
    st.info(txt['tariff_theory'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['demand_params'])
        d_int = st.number_input(txt['demand_int'], value=100.0, step=5.0)
        d_slope = st.number_input(txt['demand_slope'], value=2.0, step=0.1)
        
        st.subheader(txt['supply_params'])
        s_int = st.number_input(txt['supply_int'], value=20.0, step=5.0)
        s_slope = st.number_input(txt['supply_slope'], value=1.5, step=0.1)
        
        st.subheader(txt['trade_params'])
        p_world = st.number_input(txt['world_price'], value=40.0, step=5.0)
        tariff_pct = st.number_input(txt['tariff_rate'], value=25.0, step=5.0)
        
        analyze_btn = st.button(txt['analyze_btn'], type='primary')
    
    with col2:
        if analyze_btn:
            # Demand: P = d_int - d_slope * Q -> Q_d = (d_int - P) / d_slope
            # Supply: P = s_int + s_slope * Q -> Q_s = (P - s_int) / s_slope
            
            # Free Trade Equilibrium
            p_free = p_world
            q_d_free = (d_int - p_free) / d_slope
            q_s_free = (p_free - s_int) / s_slope
            imports_free = q_d_free - q_s_free
            
            # With Tariff
            p_tariff = p_world * (1 + tariff_pct / 100)
            q_d_tariff = (d_int - p_tariff) / d_slope
            q_s_tariff = (p_tariff - s_int) / s_slope
            imports_tariff = q_d_tariff - q_s_tariff
            
            # Welfare Calculations
            # Consumer Surplus = 0.5 * (d_int - P) * Q_d
            cs_free = 0.5 * (d_int - p_free) * q_d_free
            cs_tariff = 0.5 * (d_int - p_tariff) * q_d_tariff
            cs_loss = cs_free - cs_tariff
            
            # Producer Surplus = 0.5 * (P - s_int) * Q_s
            ps_free = 0.5 * (p_free - s_int) * q_s_free
            ps_tariff = 0.5 * (p_tariff - s_int) * q_s_tariff
            ps_gain = ps_tariff - ps_free
            
            # Government Revenue = Tariff * Imports
            tariff_per_unit = p_tariff - p_world
            govt_rev = tariff_per_unit * imports_tariff
            
            # Total Surplus
            ts_free = cs_free + ps_free
            ts_tariff = cs_tariff + ps_tariff + govt_rev
            
            # Deadweight Loss
            dwl = ts_free - ts_tariff
            
            # Display Results
            st.subheader(txt['welfare_analysis'])
            
            df_welfare = pd.DataFrame({
                txt['free_trade']: [f"Rp {cs_free:,.0f}", f"Rp {ps_free:,.0f}", "Rp 0", f"Rp {ts_free:,.0f}", "-"],
                txt['with_tariff']: [f"Rp {cs_tariff:,.0f}", f"Rp {ps_tariff:,.0f}", f"Rp {govt_rev:,.0f}", f"Rp {ts_tariff:,.0f}", f"Rp {dwl:,.0f}"]
            }, index=[txt['consumer_surplus'], txt['producer_surplus'], txt['govt_revenue'], txt['total_surplus'], txt['dwl']])
            
            st.dataframe(df_welfare, use_container_width=True)
            
            st.warning(txt['tariff_insight'].format(ps_gain=ps_gain, cs_loss=cs_loss, rev=govt_rev, dwl=dwl))
            
            # Visualization
            Q_range = np.linspace(0, 60, 200)
            P_demand = d_int - d_slope * Q_range
            P_supply = s_int + s_slope * Q_range
            
            df_chart = pd.DataFrame({
                'Quantity': np.concatenate([Q_range, Q_range]),
                'Price': np.concatenate([P_demand, P_supply]),
                'Curve': ['Demand'] * len(Q_range) + ['Supply'] * len(Q_range)
            })
            
            # Filter valid range
            df_chart = df_chart[df_chart['Price'] >= 0]
            
            base_chart = alt.Chart(df_chart).mark_line().encode(
                x='Quantity',
                y=alt.Y('Price', scale=alt.Scale(domain=[0, d_int])),
                color='Curve'
            )
            
            # World Price Line
            world_line = alt.Chart(pd.DataFrame({'P': [p_world]})).mark_rule(color='green', strokeDash=[5,5]).encode(y='P')
            tariff_line = alt.Chart(pd.DataFrame({'P': [p_tariff]})).mark_rule(color='red', strokeDash=[5,5]).encode(y='P')
            
            final_chart = (base_chart + world_line + tariff_line).properties(title=txt['chart_title'], height=400)
            st.altair_chart(final_chart, use_container_width=True)

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_govt'])
        st.write(txt['use_corp'])
        st.write(txt['use_analyst'])
