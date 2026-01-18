import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

st.set_page_config(page_title="Exchange Rate Forecasting", page_icon="💱", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "💱 Advanced Exchange Rate Forecasting & Hedging",
        'subtitle': "Comprehensive FX analysis using PPP, Interest Rate Parity, and advanced hedging strategies for policy and business decisions.",
        'tab1': "🍔 PPP Analysis",
        'tab2': "📈 Interest Rate Parity",
        'tab3': "🛡️ Hedging Strategy",
        'tab4': "📊 Multi-Method Forecast",
        # Tab 1
        'ppp_title': "Purchasing Power Parity (PPP) Analysis",
        'what_is_ppp': "**What is PPP?**",
        'ppp_explain': """
PPP theory states that exchange rates should adjust so that identical goods cost the same across countries.

**Big Mac Index Example:**
- Big Mac in Indonesia: Rp 35,000
- Big Mac in USA: $5.50
- **Implied Rate**: 35,000 / 5.50 = 6,364 IDR/USD
- If actual rate is 15,500 → IDR is **undervalued** by 59%
        """,
        'product_comparison': "Product Price Comparison",
        'product_name': "Product Name",
        'price_idr': "Price in Indonesia (Rp)",
        'price_usd': "Price in USA ($)",
        'current_rate': "Current Exchange Rate (IDR/USD)",
        'calculate': "Calculate PPP",
        'results': "PPP Analysis Results",
        'implied_rate': "Implied Exchange Rate (PPP)",
        'actual_rate': "Actual Market Rate",
        'valuation': "Currency Valuation",
        'valuation_pct': "Valuation Gap",
        'forecast': "Long-term Forecast",
        # Tab 2
        'irp_title': "Interest Rate Parity (IRP) Analysis",
        'what_is_irp': "**What is IRP?**",
        'irp_explain': """
IRP states that the difference between forward and spot rates equals the interest rate differential.

**Formula:** F = S × (1 + r_domestic) / (1 + r_foreign)

**Example:**
- Spot Rate: 15,500 IDR/USD
- BI Rate: 6%, Fed Rate: 5%
- **Forward Rate (1 year)**: 15,500 × 1.06 / 1.05 = 15,643 IDR/USD
        """,
        'irp_inputs': "IRP Parameters",
        'spot_rate': "Spot Rate (IDR/USD)",
        'bi_rate': "BI Rate (%)",
        'fed_rate': "Fed Rate (%)",
        'time_horizon': "Time Horizon (months)",
        'forward_rate': "Forward Rate",
        'rate_differential': "Interest Rate Differential",
        'expected_change': "Expected Exchange Rate Change",
        # Tab 3
        'hedging_title': "Hedging Strategy Optimizer",
        'what_is_hedging': "**What is Hedging?**",
        'hedging_explain': """
Hedging protects against FX risk by locking in future exchange rates.

**Hedging Tools:**
1. **Forward Contracts** - Lock in rate for future date
2. **Options** - Right (not obligation) to exchange at set rate
3. **Natural Hedge** - Match foreign currency revenues with expenses
        """,
        'transaction_details': "Transaction Details",
        'transaction_type': "Transaction Type",
        'export': "Export (Receiving USD)",
        'import': "Import (Paying USD)",
        'amount_usd': "Amount (USD)",
        'payment_date': "Payment/Receipt Date",
        'forward_quote': "Forward Rate Quote from Bank",
        'hedging_options': "Hedging Options Analysis",
        'option1': "Option 1: No Hedge (Spot at maturity)",
        'option2': "Option 2: Forward Contract",
        'option3': "Option 3: Partial Hedge (70%)",
        'recommendation': "Recommendation",
        # Tab 4
        'multi_title': "Multi-Method Forecast Consensus",
        'consensus_explain': """
Combines multiple forecasting methods for robust predictions:
1. **PPP** - Long-term fundamental value
2. **IRP** - Short-term interest rate effect
3. **Trend** - Historical momentum
4. **Consensus** - Weighted average of all methods
        """,
        'forecast_horizon': "Forecast Horizon (months)",
        'run_forecast': "Run Multi-Method Forecast",
        'consensus_forecast': "Consensus Forecast",
        'confidence_interval': "Confidence Interval",
        'policy_implications': "Policy Implications",
        'story_title': "📚 Story & Use Cases",
        'story_meaning': "**What is this?**\nComprehensive FX forecasting and hedging tool for exporters, importers, and policymakers.",
        'story_insight': "**Key Insight:**\nCombining PPP (long-term), IRP (short-term), and hedging strategies provides complete FX risk management framework.",
        'story_users': "**Who needs this?**",
        'use_exporter': "📦 **Exporters:** Optimize USD→IDR conversion timing",
        'use_importer': "🛒 **Importers:** Lock in favorable rates for USD payments",
        'use_central_bank': "🏦 **Central Bank:** Monitor currency valuation and intervention needs"
    },
    'ID': {
        'title': "💱 Peramalan Kurs & Hedging Lanjutan",
        'subtitle': "Analisis FX komprehensif menggunakan PPP, Paritas Suku Bunga, dan strategi hedging lanjutan untuk kebijakan dan keputusan bisnis.",
        'tab1': "🍔 Analisis PPP",
        'tab2': "📈 Paritas Suku Bunga",
        'tab3': "🛡️ Strategi Hedging",
        'tab4': "📊 Peramalan Multi-Metode",
        # Tab 1
        'ppp_title': "Analisis Purchasing Power Parity (PPP)",
        'what_is_ppp': "**Apa itu PPP?**",
        'ppp_explain': """
Teori PPP menyatakan bahwa kurs harus menyesuaikan agar barang identik berharga sama di berbagai negara.

**Contoh Indeks Big Mac:**
- Big Mac di Indonesia: Rp 35,000
- Big Mac di USA: $5.50
- **Kurs Tersirat**: 35,000 / 5.50 = 6,364 IDR/USD
- Jika kurs aktual 15,500 → IDR **undervalued** 59%
        """,
        'product_comparison': "Perbandingan Harga Produk",
        'product_name': "Nama Produk",
        'price_idr': "Harga di Indonesia (Rp)",
        'price_usd': "Harga di USA ($)",
        'current_rate': "Kurs Saat Ini (IDR/USD)",
        'calculate': "Hitung PPP",
        'results': "Hasil Analisis PPP",
        'implied_rate': "Kurs Tersirat (PPP)",
        'actual_rate': "Kurs Pasar Aktual",
        'valuation': "Valuasi Mata Uang",
        'valuation_pct': "Selisih Valuasi",
        'forecast': "Peramalan Jangka Panjang",
        # Tab 2
        'irp_title': "Analisis Interest Rate Parity (IRP)",
        'what_is_irp': "**Apa itu IRP?**",
        'irp_explain': """
IRP menyatakan bahwa perbedaan antara kurs forward dan spot sama dengan diferensial suku bunga.

**Rumus:** F = S × (1 + r_domestik) / (1 + r_asing)

**Contoh:**
- Kurs Spot: 15,500 IDR/USD
- BI Rate: 6%, Fed Rate: 5%
- **Kurs Forward (1 tahun)**: 15,500 × 1.06 / 1.05 = 15,643 IDR/USD
        """,
        'irp_inputs': "Parameter IRP",
        'spot_rate': "Kurs Spot (IDR/USD)",
        'bi_rate': "BI Rate (%)",
        'fed_rate': "Fed Rate (%)",
        'time_horizon': "Horizon Waktu (bulan)",
        'forward_rate': "Kurs Forward",
        'rate_differential': "Diferensial Suku Bunga",
        'expected_change': "Perubahan Kurs yang Diharapkan",
        # Tab 3
        'hedging_title': "Pengoptimal Strategi Hedging",
        'what_is_hedging': "**Apa itu Hedging?**",
        'hedging_explain': """
Hedging melindungi dari risiko FX dengan mengunci kurs masa depan.

**Alat Hedging:**
1. **Kontrak Forward** - Kunci kurs untuk tanggal masa depan
2. **Opsi** - Hak (bukan kewajiban) untuk menukar di kurs tertentu
3. **Natural Hedge** - Cocokkan pendapatan mata uang asing dengan pengeluaran
        """,
        'transaction_details': "Detail Transaksi",
        'transaction_type': "Jenis Transaksi",
        'export': "Ekspor (Menerima USD)",
        'import': "Impor (Membayar USD)",
        'amount_usd': "Jumlah (USD)",
        'payment_date': "Tanggal Pembayaran/Penerimaan",
        'forward_quote': "Kurs Forward dari Bank",
        'hedging_options': "Analisis Opsi Hedging",
        'option1': "Opsi 1: Tanpa Hedge (Spot saat jatuh tempo)",
        'option2': "Opsi 2: Kontrak Forward",
        'option3': "Opsi 3: Hedge Parsial (70%)",
        'recommendation': "Rekomendasi",
        # Tab 4
        'multi_title': "Konsensus Peramalan Multi-Metode",
        'consensus_explain': """
Menggabungkan beberapa metode peramalan untuk prediksi yang robust:
1. **PPP** - Nilai fundamental jangka panjang
2. **IRP** - Efek suku bunga jangka pendek
3. **Trend** - Momentum historis
4. **Konsensus** - Rata-rata tertimbang semua metode
        """,
        'forecast_horizon': "Horizon Peramalan (bulan)",
        'run_forecast': "Jalankan Peramalan Multi-Metode",
        'consensus_forecast': "Peramalan Konsensus",
        'confidence_interval': "Interval Kepercayaan",
        'policy_implications': "Implikasi Kebijakan",
        'story_title': "📚 Cerita & Kasus Penggunaan",
        'story_meaning': "**Apa artinya ini?**\nAlat peramalan FX dan hedging komprehensif untuk eksportir, importir, dan pembuat kebijakan.",
        'story_insight': "**Wawasan Utama:**\nMenggabungkan PPP (jangka panjang), IRP (jangka pendek), dan strategi hedging memberikan kerangka manajemen risiko FX yang lengkap.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_exporter': "📦 **Eksportir:** Optimalkan waktu konversi USD→IDR",
        'use_importer': "🛒 **Importir:** Kunci kurs menguntungkan untuk pembayaran USD",
        'use_central_bank': "🏦 **Bank Sentral:** Monitor valuasi mata uang dan kebutuhan intervensi"
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

# TABS
tab1, tab2, tab3, tab4 = st.tabs([txt['tab1'], txt['tab2'], txt['tab3'], txt['tab4']])

# ========== TAB 1: PPP ANALYSIS ==========
with tab1:
    st.markdown(f"### {txt['ppp_title']}")
    
    with st.expander(txt['what_is_ppp'], expanded=False):
        st.markdown(txt['ppp_explain'])
        st.latex(r"E_{PPP} = \frac{P_{domestic}}{P_{foreign}}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['product_comparison']}")
        
        product = st.text_input(txt['product_name'], value="Big Mac")
        price_idr = st.number_input(txt['price_idr'], min_value=0.0, value=35000.0, step=1000.0)
        price_usd = st.number_input(txt['price_usd'], min_value=0.01, value=5.50, step=0.10)
        current_rate = st.number_input(txt['current_rate'], min_value=0.0, value=15500.0, step=100.0)
        
        if st.button(txt['calculate'], type='primary', key='ppp_calc'):
            implied_rate = price_idr / price_usd
            valuation_pct = ((current_rate - implied_rate) / implied_rate) * 100
            
            st.session_state['ppp_results'] = {
                'implied': implied_rate,
                'actual': current_rate,
                'valuation': valuation_pct,
                'product': product
            }
    
    with col2:
        if 'ppp_results' in st.session_state:
            res = st.session_state['ppp_results']
            
            st.markdown(f"### {txt['results']}")
            
            r1, r2, r3 = st.columns(3)
            r1.metric(txt['implied_rate'], f"{res['implied']:,.0f} IDR/USD")
            r2.metric(txt['actual_rate'], f"{res['actual']:,.0f} IDR/USD")
            r3.metric(txt['valuation_pct'], f"{res['valuation']:+.1f}%")
            
            # Valuation analysis
            st.markdown(f"### {txt['valuation']}")
            
            if abs(res['valuation']) < 5:
                st.success("🟢 **FAIRLY VALUED** - IDR is at equilibrium")
                color = "green"
            elif res['valuation'] > 0:
                st.error(f"🔴 **OVERVALUED** - IDR is {res['valuation']:.1f}% too strong")
                st.warning("💡 Expect IDR to **WEAKEN** (depreciate) toward PPP level")
                color = "red"
            else:
                st.success(f"🟢 **UNDERVALUED** - IDR is {abs(res['valuation']):.1f}% too weak")
                st.info("💡 Expect IDR to **STRENGTHEN** (appreciate) toward PPP level")
                color = "blue"
            
            # Chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['PPP Implied', 'Actual Market'],
                y=[res['implied'], res['actual']],
                marker_color=['blue', color],
                text=[f"{res['implied']:,.0f}", f"{res['actual']:,.0f}"],
                textposition='outside'
            ))
            
            fig.update_layout(
                title=f"PPP Analysis: {res['product']}",
                yaxis_title="Exchange Rate (IDR/USD)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Long-term forecast
            st.markdown(f"### {txt['forecast']}")
            
            # Assume 50% adjustment over 2 years
            months = np.arange(0, 25)
            forecast = res['actual'] + (res['implied'] - res['actual']) * (1 - np.exp(-months/12))
            
            fig2 = go.Figure()
            
            fig2.add_trace(go.Scatter(x=months, y=forecast, mode='lines',
                                     name='PPP Forecast', line=dict(color='blue', width=3)))
            fig2.add_hline(y=res['implied'], line_dash="dash", line_color="green",
                          annotation_text=f"PPP Target: {res['implied']:,.0f}")
            fig2.add_hline(y=res['actual'], line_dash="dash", line_color="red",
                          annotation_text=f"Current: {res['actual']:,.0f}")
            
            fig2.update_layout(
                title="Long-term PPP Convergence Forecast",
                xaxis_title="Months",
                yaxis_title="IDR/USD",
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)

# ========== TAB 2: INTEREST RATE PARITY ==========
with tab2:
    st.markdown(f"### {txt['irp_title']}")
    
    with st.expander(txt['what_is_irp'], expanded=False):
        st.markdown(txt['irp_explain'])
        st.latex(r"F = S \times \frac{1 + r_d}{1 + r_f}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['irp_inputs']}")
        
        spot = st.number_input(txt['spot_rate'], min_value=0.0, value=15500.0, step=100.0)
        bi_rate = st.number_input(txt['bi_rate'], min_value=0.0, value=6.0, step=0.25)
        fed_rate = st.number_input(txt['fed_rate'], min_value=0.0, value=5.0, step=0.25)
        months = st.slider(txt['time_horizon'], 1, 24, 12)
        
        if st.button(txt['calculate'], type='primary', key='irp_calc'):
            # Convert to period rates
            years = months / 12
            r_d = (bi_rate / 100) * years
            r_f = (fed_rate / 100) * years
            
            forward = spot * (1 + r_d) / (1 + r_f)
            rate_diff = bi_rate - fed_rate
            expected_change = ((forward - spot) / spot) * 100
            
            st.session_state['irp_results'] = {
                'spot': spot,
                'forward': forward,
                'rate_diff': rate_diff,
                'change': expected_change,
                'months': months
            }
    
    with col2:
        if 'irp_results' in st.session_state:
            res = st.session_state['irp_results']
            
            st.markdown(f"### {txt['results']}")
            
            i1, i2, i3 = st.columns(3)
            i1.metric(txt['spot_rate'], f"{res['spot']:,.0f}")
            i2.metric(txt['forward_rate'], f"{res['forward']:,.0f}",
                     delta=f"{res['forward'] - res['spot']:+,.0f}")
            i3.metric(txt['rate_differential'], f"{res['rate_diff']:+.2f}%")
            
            st.metric(txt['expected_change'], f"{res['change']:+.2f}%")
            
            # Interpretation
            if res['change'] > 0:
                st.warning(f"⚠️ IDR expected to **WEAKEN** by {res['change']:.2f}% over {res['months']} months")
                st.info("💡 Higher domestic rates → Capital inflow → But forward premium offsets")
            else:
                st.success(f"✅ IDR expected to **STRENGTHEN** by {abs(res['change']):.2f}% over {res['months']} months")
            
            # Timeline chart
            time_range = np.linspace(0, res['months'], 50)
            rate_path = res['spot'] + (res['forward'] - res['spot']) * (time_range / res['months'])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=time_range, y=rate_path, mode='lines',
                                    name='IRP Forecast', line=dict(color='purple', width=3)))
            fig.add_scatter(x=[0, res['months']], y=[res['spot'], res['forward']],
                           mode='markers', name='Spot & Forward',
                           marker=dict(size=12, color=['green', 'red']))
            
            fig.update_layout(
                title="Interest Rate Parity Forecast",
                xaxis_title="Months",
                yaxis_title="IDR/USD",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 3: HEDGING STRATEGY ==========
with tab3:
    st.markdown(f"### {txt['hedging_title']}")
    
    with st.expander(txt['what_is_hedging'], expanded=False):
        st.markdown(txt['hedging_explain'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"#### {txt['transaction_details']}")
        
        trans_type = st.radio(txt['transaction_type'], [txt['export'], txt['import']])
        amount = st.number_input(txt['amount_usd'], min_value=0.0, value=100000.0, step=10000.0)
        
        min_date = datetime.now() + timedelta(days=30)
        payment_date = st.date_input(txt['payment_date'], value=min_date, min_value=min_date)
        
        spot_h = st.number_input(txt['spot_rate'], min_value=0.0, value=15500.0, step=100.0, key='spot_h')
        forward_h = st.number_input(txt['forward_quote'], min_value=0.0, value=15700.0, step=100.0)
        
        if st.button(txt['calculate'], type='primary', key='hedge_calc'):
            # Calculate scenarios
            unhedged = amount * spot_h
            hedged = amount * forward_h
            partial = amount * (0.7 * forward_h + 0.3 * spot_h)
            
            st.session_state['hedge_results'] = {
                'type': trans_type,
                'amount': amount,
                'unhedged': unhedged,
                'hedged': hedged,
                'partial': partial,
                'spot': spot_h,
                'forward': forward_h
            }
    
    with col2:
        if 'hedge_results' in st.session_state:
            res = st.session_state['hedge_results']
            
            st.markdown(f"### {txt['hedging_options']}")
            
            # Create comparison table
            df = pd.DataFrame({
                'Strategy': [txt['option1'], txt['option2'], txt['option3']],
                'Rate': [res['spot'], res['forward'], (0.7*res['forward'] + 0.3*res['spot'])],
                'IDR Value': [res['unhedged'], res['hedged'], res['partial']],
                'Cost vs Spot': [0, res['hedged']-res['unhedged'], res['partial']-res['unhedged']]
            })
            
            st.dataframe(df.style.format({
                'Rate': '{:,.0f}',
                'IDR Value': 'Rp {:,.0f}',
                'Cost vs Spot': 'Rp {:+,.0f}'
            }).highlight_max(subset=['IDR Value'], color='lightgreen' if res['type'] == txt['export'] else 'lightcoral')
            .highlight_min(subset=['IDR Value'], color='lightcoral' if res['type'] == txt['export'] else 'lightgreen'),
            use_container_width=True, hide_index=True)
            
            # Recommendation
            st.markdown(f"### {txt['recommendation']}")
            
            cost_pct = abs((res['hedged'] - res['unhedged']) / res['unhedged'] * 100)
            
            if cost_pct < 1:
                st.success("✅ **FULL HEDGE RECOMMENDED** - Forward rate is very close to spot")
            elif cost_pct > 3:
                st.warning("⚠️ **PARTIAL HEDGE RECOMMENDED** - Forward premium is high, hedge 50-70%")
            else:
                st.info("💡 **MODERATE HEDGE** - Consider hedging based on risk tolerance")
            
            # Visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['No Hedge', 'Full Hedge', 'Partial (70%)'],
                y=[res['unhedged'], res['hedged'], res['partial']],
                marker_color=['blue', 'green', 'orange'],
                text=[f"Rp {res['unhedged']:,.0f}", f"Rp {res['hedged']:,.0f}", f"Rp {res['partial']:,.0f}"],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Hedging Strategy Comparison",
                yaxis_title="IDR Value",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ========== TAB 4: MULTI-METHOD FORECAST ==========
with tab4:
    st.markdown(f"### {txt['multi_title']}")
    
    with st.expander("📚 Methodology", expanded=False):
        st.markdown(txt['consensus_explain'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        horizon = st.slider(txt['forecast_horizon'], 3, 24, 12)
        
        # Inputs for all methods
        st.markdown("#### Current Data")
        spot_m = st.number_input("Spot Rate", min_value=0.0, value=15500.0, step=100.0, key='spot_m')
        ppp_implied = st.number_input("PPP Implied Rate", min_value=0.0, value=6364.0, step=100.0)
        bi_m = st.number_input("BI Rate", min_value=0.0, value=6.0, step=0.25, key='bi_m')
        fed_m = st.number_input("Fed Rate", min_value=0.0, value=5.0, step=0.25, key='fed_m')
        
        if st.button(txt['run_forecast'], type='primary'):
            # Method 1: PPP (50% adjustment over time)
            months_range = np.arange(0, horizon + 1)
            ppp_forecast = spot_m + (ppp_implied - spot_m) * (1 - np.exp(-months_range/12))
            
            # Method 2: IRP
            years = months_range / 12
            r_d = (bi_m / 100) * years
            r_f = (fed_m / 100) * years
            irp_forecast = spot_m * (1 + r_d) / (1 + r_f)
            
            # Method 3: Trend (simple momentum)
            trend_rate = 0.003  # 0.3% per month depreciation (historical avg)
            trend_forecast = spot_m * (1 + trend_rate) ** months_range
            
            # Consensus (weighted average)
            consensus = 0.3 * ppp_forecast + 0.4 * irp_forecast + 0.3 * trend_forecast
            
            # Confidence interval (±5%)
            ci_upper = consensus * 1.05
            ci_lower = consensus * 0.95
            
            st.session_state['multi_forecast'] = {
                'months': months_range,
                'ppp': ppp_forecast,
                'irp': irp_forecast,
                'trend': trend_forecast,
                'consensus': consensus,
                'ci_upper': ci_upper,
                'ci_lower': ci_lower,
                'horizon': horizon
            }
    
    with col2:
        if 'multi_forecast' in st.session_state:
            res = st.session_state['multi_forecast']
            
            st.markdown(f"### {txt['consensus_forecast']}")
            
            # Final forecast
            final_rate = res['consensus'][-1]
            change_pct = ((final_rate - spot_m) / spot_m) * 100
            
            f1, f2 = st.columns(2)
            f1.metric(f"Forecast ({res['horizon']} months)", f"{final_rate:,.0f} IDR/USD")
            f2.metric("Expected Change", f"{change_pct:+.2f}%")
            
            # Multi-method chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=res['months'], y=res['ppp'], mode='lines',
                                    name='PPP Method', line=dict(dash='dash', color='blue')))
            fig.add_trace(go.Scatter(x=res['months'], y=res['irp'], mode='lines',
                                    name='IRP Method', line=dict(dash='dash', color='red')))
            fig.add_trace(go.Scatter(x=res['months'], y=res['trend'], mode='lines',
                                    name='Trend Method', line=dict(dash='dash', color='green')))
            fig.add_trace(go.Scatter(x=res['months'], y=res['consensus'], mode='lines',
                                    name='CONSENSUS', line=dict(color='purple', width=4)))
            
            # Confidence interval
            fig.add_trace(go.Scatter(x=res['months'], y=res['ci_upper'], mode='lines',
                                    line=dict(width=0), showlegend=False))
            fig.add_trace(go.Scatter(x=res['months'], y=res['ci_lower'], mode='lines',
                                    fill='tonexty', fillcolor='rgba(128,0,128,0.2)',
                                    line=dict(width=0), name='95% CI'))
            
            fig.update_layout(
                title="Multi-Method Consensus Forecast",
                xaxis_title="Months",
                yaxis_title="IDR/USD",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Policy implications
            st.markdown(f"### {txt['policy_implications']}")
            
            if change_pct > 5:
                st.error(f"🔴 **DEPRECIATION PRESSURE** - IDR expected to weaken {change_pct:.1f}%")
                st.warning("""
                **Policy Recommendations:**
                - Central bank may need to raise rates to defend currency
                - Exporters: Good time to lock in forward contracts
                - Importers: Hedge immediately to avoid higher costs
                """)
            elif change_pct < -5:
                st.success(f"🟢 **APPRECIATION PRESSURE** - IDR expected to strengthen {abs(change_pct):.1f}%")
                st.info("""
                **Policy Recommendations:**
                - Central bank may consider rate cuts
                - Exporters: Wait for better rates before converting
                - Importers: Can delay hedging
                """)
            else:
                st.info("🟡 **STABLE OUTLOOK** - IDR expected to remain relatively stable")

# --- STORY & USE CASES ---
if 'story_title' in txt:
    st.divider()
    with st.expander(txt['story_title']):
        st.markdown(txt['story_meaning'])
        st.info(txt['story_insight'])
        st.markdown(txt['story_users'])
        st.write(txt['use_exporter'])
        st.write(txt['use_importer'])
        st.write(txt['use_central_bank'])
