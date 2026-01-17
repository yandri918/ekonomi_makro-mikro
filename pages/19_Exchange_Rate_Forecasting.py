import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Exchange Rate Forecasting", page_icon="💱", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "💱 Exchange Rate Forecasting",
        'subtitle': "Forecast exchange rates using **PPP (Big Mac Index)** and **Interest Rate Parity** for hedging decisions.",
        'tab1': "🍔 PPP Calculator (Big Mac Index)",
        'tab2': "📈 Interest Rate Parity",
        'tab3': "🛡️ Hedging Decision Tool",
        # Tab 1: PPP
        'ppp_theory': "**Purchasing Power Parity (PPP)**: Exchange rates should adjust so identical goods cost the same in different countries.",
        'ppp_example': "**Big Mac Index**: If a Big Mac costs Rp 35,000 in Indonesia and $5.50 in USA, the implied exchange rate is 35,000 / 5.50 ≈ 6,364 IDR/USD.",
        'ppp_inputs': "🍔 Product Price Comparison",
        'product_name': "Product Name",
        'country_a': "Country A (Indonesia)",
        'country_b': "Country B (USA)",
        'price_a': "Price in IDR (Rp)",
        'price_b': "Price in USD ($)",
        'current_rate': "Current Exchange Rate (IDR/USD)",
        'calc_ppp': "📊 Calculate PPP",
        'ppp_results': "📋 PPP Analysis Results",
        'implied_rate': "Implied Exchange Rate (PPP)",
        'actual_rate': "Actual Exchange Rate",
        'valuation': "Currency Valuation",
        'overvalued': "🔴 OVERVALUED",
        'undervalued': "🟢 UNDERVALUED",
        'fair': "🟡 FAIRLY VALUED",
        'valuation_pct': "Valuation: {val:.1f}%",
        'prediction': "💡 Prediction",
        'pred_appreciate': "IDR likely to **APPRECIATE** (strengthen) toward {rate:,.0f}",
        'pred_depreciate': "IDR likely to **DEPRECIATE** (weaken) toward {rate:,.0f}",
        'pred_stable': "IDR is **FAIRLY VALUED** - expect stability around {rate:,.0f}",
        # Tab 2: IRP
        'irp_theory': "**Interest Rate Parity (IRP)**: Forward rate = Spot rate × (1 + domestic rate) / (1 + foreign rate)",
        'irp_formula': "**Formula**: F = S × (1 + r_d) / (1 + r_f)",
        'irp_inputs': "📊 Interest Rate Parity Parameters",
        'spot_rate': "Spot Exchange Rate (IDR/USD)",
        'domestic_rate': "Domestic Interest Rate (BI Rate %)",
        'foreign_rate': "Foreign Interest Rate (Fed Rate %)",
        'time_period': "Time Period (Months)",
        'calc_irp': "📈 Calculate Forward Rate",
        'irp_results': "📋 IRP Analysis Results",
        'forward_rate': "Forward Exchange Rate",
        'rate_diff': "Interest Rate Differential",
        'arbitrage': "Arbitrage Opportunity",
        'no_arbitrage': "✅ No arbitrage - Market is efficient",
        'arbitrage_exists': "⚠️ Potential arbitrage opportunity exists",
        'hedging_rec': "💡 Hedging Recommendation",
        'hedge_forward': "Use **Forward Contract** at {rate:,.0f} to lock in rate",
        'hedge_wait': "Consider **waiting** - rates may improve",
        # Tab 3: Hedging
        'hedging_theory': "**Hedging**: Protect against exchange rate risk for future transactions.",
        'hedging_inputs': "🛡️ Transaction Details",
        'transaction_amount': "Transaction Amount (USD)",
        'transaction_date': "Transaction Date (Future)",
        'forward_quote': "Forward Rate Quote from Bank (IDR/USD)",
        'calc_hedge': "🎯 Analyze Hedging Options",
        'hedging_results': "📋 Hedging Analysis",
        'unhedged_value': "Unhedged Value (at current spot)",
        'hedged_value': "Hedged Value (at forward rate)",
        'hedging_cost': "Hedging Cost/Benefit",
        'recommendation': "Recommendation",
        'rec_hedge': "✅ **HEDGE** - Lock in forward rate to avoid risk",
        'rec_no_hedge': "❌ **DON'T HEDGE** - Forward rate is unfavorable",
        'rec_partial': "🟡 **PARTIAL HEDGE** - Hedge 50-70% of exposure",
        # Story
        'story_title': "📚 Story & Use Cases: Exchange Rate Forecasting",
        'story_meaning': "**What is this?**\nThis tool helps exporters/importers forecast exchange rates and make hedging decisions to protect against currency risk.",
        'story_insight': "**Key Insight:**\nPPP shows long-term currency trends. IRP shows short-term forward rates. Hedging protects your profit margins.",
        'story_users': "**Who needs this?**",
        'use_exporter': "📦 **Exporters:** To decide when to convert USD revenue to IDR and whether to use forward contracts.",
        'use_importer': "🛒 **Importers:** To lock in favorable rates for future USD payments and avoid currency losses.",
        'use_treasury': "🏦 **Corporate Treasury:** To manage FX exposure and optimize hedging strategies."
    },
    'ID': {
        'title': "💱 Peramalan Kurs Mata Uang",
        'subtitle': "Ramalkan kurs menggunakan **PPP (Indeks Big Mac)** dan **Paritas Suku Bunga** untuk keputusan hedging.",
        'tab1': "🍔 Kalkulator PPP (Indeks Big Mac)",
        'tab2': "📈 Paritas Suku Bunga",
        'tab3': "🛡️ Alat Keputusan Hedging",
        # Tab 1: PPP
        'ppp_theory': "**Purchasing Power Parity (PPP)**: Kurs harus menyesuaikan agar barang identik berharga sama di berbagai negara.",
        'ppp_example': "**Indeks Big Mac**: Jika Big Mac Rp 35,000 di Indonesia dan $5.50 di USA, kurs tersirat adalah 35,000 / 5.50 ≈ 6,364 IDR/USD.",
        'ppp_inputs': "🍔 Perbandingan Harga Produk",
        'product_name': "Nama Produk",
        'country_a': "Negara A (Indonesia)",
        'country_b': "Negara B (USA)",
        'price_a': "Harga dalam IDR (Rp)",
        'price_b': "Harga dalam USD ($)",
        'current_rate': "Kurs Saat Ini (IDR/USD)",
        'calc_ppp': "📊 Hitung PPP",
        'ppp_results': "📋 Hasil Analisis PPP",
        'implied_rate': "Kurs Tersirat (PPP)",
        'actual_rate': "Kurs Aktual",
        'valuation': "Valuasi Mata Uang",
        'overvalued': "🔴 OVERVALUED (Terlalu Kuat)",
        'undervalued': "🟢 UNDERVALUED (Terlalu Lemah)",
        'fair': "🟡 WAJAR",
        'valuation_pct': "Valuasi: {val:.1f}%",
        'prediction': "💡 Prediksi",
        'pred_appreciate': "IDR kemungkinan **MENGUAT** menuju {rate:,.0f}",
        'pred_depreciate': "IDR kemungkinan **MELEMAH** menuju {rate:,.0f}",
        'pred_stable': "IDR **WAJAR** - ekspektasi stabil di sekitar {rate:,.0f}",
        # Tab 2: IRP
        'irp_theory': "**Interest Rate Parity (IRP)**: Kurs forward = Kurs spot × (1 + suku bunga domestik) / (1 + suku bunga asing)",
        'irp_formula': "**Rumus**: F = S × (1 + r_d) / (1 + r_f)",
        'irp_inputs': "📊 Parameter Paritas Suku Bunga",
        'spot_rate': "Kurs Spot (IDR/USD)",
        'domestic_rate': "Suku Bunga Domestik (BI Rate %)",
        'foreign_rate': "Suku Bunga Asing (Fed Rate %)",
        'time_period': "Periode Waktu (Bulan)",
        'calc_irp': "📈 Hitung Kurs Forward",
        'irp_results': "📋 Hasil Analisis IRP",
        'forward_rate': "Kurs Forward",
        'rate_diff': "Diferensial Suku Bunga",
        'arbitrage': "Peluang Arbitrase",
        'no_arbitrage': "✅ Tidak ada arbitrase - Pasar efisien",
        'arbitrage_exists': "⚠️ Potensi peluang arbitrase ada",
        'hedging_rec': "💡 Rekomendasi Hedging",
        'hedge_forward': "Gunakan **Kontrak Forward** di {rate:,.0f} untuk mengunci kurs",
        'hedge_wait': "Pertimbangkan **menunggu** - kurs mungkin membaik",
        # Tab 3: Hedging
        'hedging_theory': "**Hedging**: Lindungi dari risiko kurs untuk transaksi masa depan.",
        'hedging_inputs': "🛡️ Detail Transaksi",
        'transaction_amount': "Jumlah Transaksi (USD)",
        'transaction_date': "Tanggal Transaksi (Masa Depan)",
        'forward_quote': "Kurs Forward dari Bank (IDR/USD)",
        'calc_hedge': "🎯 Analisis Opsi Hedging",
        'hedging_results': "📋 Analisis Hedging",
        'unhedged_value': "Nilai Tanpa Hedging (kurs spot)",
        'hedged_value': "Nilai Dengan Hedging (kurs forward)",
        'hedging_cost': "Biaya/Manfaat Hedging",
        'recommendation': "Rekomendasi",
        'rec_hedge': "✅ **HEDGING** - Kunci kurs forward untuk hindari risiko",
        'rec_no_hedge': "❌ **JANGAN HEDGING** - Kurs forward tidak menguntungkan",
        'rec_partial': "🟡 **HEDGING PARSIAL** - Hedging 50-70% dari eksposur",
        # Story
        'story_title': "📚 Cerita & Kasus Penggunaan: Peramalan Kurs",
        'story_meaning': "**Apa artinya ini?**\nAlat ini membantu eksportir/importir meramalkan kurs dan membuat keputusan hedging untuk melindungi dari risiko mata uang.",
        'story_insight': "**Wawasan Utama:**\nPPP menunjukkan tren kurs jangka panjang. IRP menunjukkan kurs forward jangka pendek. Hedging melindungi margin keuntungan Anda.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_exporter': "📦 **Eksportir:** Untuk memutuskan kapan mengkonversi pendapatan USD ke IDR dan apakah menggunakan kontrak forward.",
        'use_importer': "🛒 **Importir:** Untuk mengunci kurs yang menguntungkan untuk pembayaran USD masa depan dan menghindari kerugian mata uang.",
        'use_treasury': "🏦 **Treasury Korporat:** Untuk mengelola eksposur FX dan mengoptimalkan strategi hedging."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# --- TABS ---
tab1, tab2, tab3 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3']])

# ========== TAB 1: PPP CALCULATOR ==========
with tab1:
    st.info(txt['ppp_theory'])
    st.caption(txt['ppp_example'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['ppp_inputs'])
        product_name = st.text_input(txt['product_name'], value="Big Mac")
        
        st.markdown(f"**{txt['country_a']}**")
        price_idr = st.number_input(txt['price_a'], value=35000.0, step=1000.0)
        
        st.markdown(f"**{txt['country_b']}**")
        price_usd = st.number_input(txt['price_b'], value=5.50, step=0.10)
        
        current_rate = st.number_input(txt['current_rate'], value=15500.0, step=100.0)
        
        calc_ppp_btn = st.button(txt['calc_ppp'], type='primary')
    
    with col2:
        if calc_ppp_btn:
            # Calculate implied exchange rate (PPP)
            implied_rate = price_idr / price_usd
            
            # Calculate over/under valuation
            valuation_pct = ((current_rate - implied_rate) / implied_rate) * 100
            
            st.subheader(txt['ppp_results'])
            
            m1, m2 = st.columns(2)
            m1.metric(txt['implied_rate'], f"{implied_rate:,.0f} IDR/USD")
            m2.metric(txt['actual_rate'], f"{current_rate:,.0f} IDR/USD")
            
            # Valuation status
            st.markdown("---")
            st.subheader(txt['valuation'])
            
            if abs(valuation_pct) < 5:
                st.success(txt['fair'])
                st.info(txt['valuation_pct'].format(val=valuation_pct))
            elif valuation_pct > 0:
                st.error(txt['overvalued'])
                st.warning(txt['valuation_pct'].format(val=valuation_pct))
            else:
                st.success(txt['undervalued'])
                st.info(txt['valuation_pct'].format(val=abs(valuation_pct)))
            
            # Prediction
            st.markdown("---")
            st.subheader(txt['prediction'])
            
            if abs(valuation_pct) < 5:
                st.info(txt['pred_stable'].format(rate=current_rate))
            elif valuation_pct > 0:
                # Overvalued -> IDR will depreciate (weaken)
                st.warning(txt['pred_depreciate'].format(rate=implied_rate))
            else:
                # Undervalued -> IDR will appreciate (strengthen)
                st.success(txt['pred_appreciate'].format(rate=implied_rate))
            
            # Visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Implied Rate (PPP)', 'Actual Rate'],
                y=[implied_rate, current_rate],
                marker_color=['blue', 'red' if valuation_pct > 0 else 'green'],
                text=[f"{implied_rate:,.0f}", f"{current_rate:,.0f}"],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="PPP vs Actual Exchange Rate",
                yaxis_title="IDR/USD",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 2: INTEREST RATE PARITY ==========
with tab2:
    st.info(txt['irp_theory'])
    st.caption(txt['irp_formula'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['irp_inputs'])
        spot_rate = st.number_input(txt['spot_rate'], value=15500.0, step=100.0)
        domestic_rate = st.number_input(txt['domestic_rate'], value=6.0, step=0.25)
        foreign_rate = st.number_input(txt['foreign_rate'], value=5.0, step=0.25)
        time_months = st.slider(txt['time_period'], 1, 12, 6)
        
        calc_irp_btn = st.button(txt['calc_irp'], type='primary')
    
    with col2:
        if calc_irp_btn:
            # Convert annual rates to period rates
            time_years = time_months / 12
            r_d = (domestic_rate / 100) * time_years
            r_f = (foreign_rate / 100) * time_years
            
            # Calculate forward rate using IRP
            forward_rate = spot_rate * (1 + r_d) / (1 + r_f)
            
            # Interest rate differential
            rate_diff = domestic_rate - foreign_rate
            
            st.subheader(txt['irp_results'])
            
            m1, m2, m3 = st.columns(3)
            m1.metric(txt['spot_rate'], f"{spot_rate:,.0f}")
            m2.metric(txt['forward_rate'], f"{forward_rate:,.0f}")
            m3.metric(txt['rate_diff'], f"{rate_diff:.2f}%")
            
            # Arbitrage check
            st.markdown("---")
            st.subheader(txt['arbitrage'])
            
            # In practice, if actual forward rate differs significantly from theoretical, arbitrage exists
            st.success(txt['no_arbitrage'])
            
            # Hedging recommendation
            st.markdown("---")
            st.subheader(txt['hedging_rec'])
            
            if forward_rate > spot_rate:
                st.warning(txt['hedge_forward'].format(rate=forward_rate))
            else:
                st.info(txt['hedge_wait'])
            
            # Visualization
            fig = go.Figure()
            
            # Timeline
            months = list(range(0, time_months + 1))
            rates = [spot_rate + (forward_rate - spot_rate) * (m / time_months) for m in months]
            
            fig.add_trace(go.Scatter(
                x=months,
                y=rates,
                mode='lines+markers',
                name='Projected Rate',
                line=dict(color='blue', width=3)
            ))
            
            fig.add_hline(y=spot_rate, line_dash="dash", line_color="green", annotation_text=f"Spot: {spot_rate:,.0f}")
            fig.add_hline(y=forward_rate, line_dash="dash", line_color="red", annotation_text=f"Forward: {forward_rate:,.0f}")
            
            fig.update_layout(
                title="Exchange Rate Projection (IRP)",
                xaxis_title="Months",
                yaxis_title="IDR/USD",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 3: HEDGING DECISION TOOL ==========
with tab3:
    st.info(txt['hedging_theory'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(txt['hedging_inputs'])
        transaction_amount = st.number_input(txt['transaction_amount'], value=100000.0, step=10000.0)
        
        # Transaction date
        min_date = datetime.now() + timedelta(days=30)
        transaction_date = st.date_input(txt['transaction_date'], value=min_date, min_value=min_date)
        
        # Current spot and forward quote
        spot_hedge = st.number_input(txt['spot_rate'], value=15500.0, step=100.0, key='spot_hedge')
        forward_quote = st.number_input(txt['forward_quote'], value=15700.0, step=100.0)
        
        calc_hedge_btn = st.button(txt['calc_hedge'], type='primary')
    
    with col2:
        if calc_hedge_btn:
            # Calculate values
            unhedged_value_idr = transaction_amount * spot_hedge
            hedged_value_idr = transaction_amount * forward_quote
            hedging_cost = hedged_value_idr - unhedged_value_idr
            hedging_cost_pct = (hedging_cost / unhedged_value_idr) * 100
            
            st.subheader(txt['hedging_results'])
            
            m1, m2, m3 = st.columns(3)
            m1.metric(txt['unhedged_value'], f"Rp {unhedged_value_idr:,.0f}")
            m2.metric(txt['hedged_value'], f"Rp {hedged_value_idr:,.0f}")
            m3.metric(txt['hedging_cost'], f"Rp {hedging_cost:,.0f}", delta=f"{hedging_cost_pct:.2f}%")
            
            # Recommendation
            st.markdown("---")
            st.subheader(txt['recommendation'])
            
            if abs(hedging_cost_pct) < 2:
                st.success(txt['rec_hedge'])
                st.info("Forward rate is close to spot - minimal cost to hedge")
            elif hedging_cost_pct > 5:
                st.error(txt['rec_no_hedge'])
                st.warning("Forward rate is significantly worse than spot - expensive to hedge")
            else:
                st.warning(txt['rec_partial'])
                st.info("Consider hedging 50-70% to balance risk and cost")
            
            # Visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Unhedged (Spot)', 'Hedged (Forward)'],
                y=[unhedged_value_idr, hedged_value_idr],
                marker_color=['blue', 'green' if hedging_cost < 0 else 'red'],
                text=[f"Rp {unhedged_value_idr:,.0f}", f"Rp {hedged_value_idr:,.0f}"],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Hedging Cost-Benefit Analysis",
                yaxis_title="Value (IDR)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_exporter'])
        st.write(txt['use_importer'])
        st.write(txt['use_treasury'])
