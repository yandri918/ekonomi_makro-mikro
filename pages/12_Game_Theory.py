import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Game Theory Simulator", page_icon="♟️", layout="wide")

if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'
lang = st.session_state['language']

T = {
    'EN': {
        'title': "♟️ Game Theory: Oligopoly Strategy",
        'subtitle': "Experience the **Prisoner's Dilemma** in a Price War scenario.",
        'scenario': "**Scenario:** You and a Competitor (AI) dominate the market.",
        'choice': "Make your Move:",
        'high': "Maintain High Price (Cooperate)",
        'low': "Cut Price (Defect/War)",
        'matrix_title': "📊 Payoff Matrix (You vs AI)",
        'result_title': "Game Result",
        'you_chose': "You Chose:",
        'ai_chose': "AI Chose:",
        'payoff': "Your Profit:",
        'ai_payoff': "AI Profit:",
        'nash': "🔔 **Nash Equilibrium:** Both choose 'Low Price'. Why? Because regardless of what the other does, cutting price is the dominant strategy to avoid losing market share.",
        'collusion': "🤝 **Collusion Success:** Both maintained High Price. Maximum joint profit!",
        'betrayal': "😈 **You Betrayed!** You cut price while AI stayed high. You stole the market!",
        'sucker': "😓 **You got Played!** AI cut price while you stayed high. You lost market share.",
        'score_you': "You",
        'score_ai': "AI",
        'story_title': "📚 Story & Use Cases: Game Theory",
        'story_meaning': "**What is this?**\nGame Theory analyzes strategic interactions where your outcome depends on your rival's move.",
        'story_insight': "**Key Insight:**\nRational behavior (Self-Interest) often leads to a worse outcome for everyone (Nash Equilibrium). Cooperation requires trust or binding contracts.",
        'story_users': "**Who needs this?**",
        'use_govt': "🏛️ **Diplomats:** For Arms Races or Climate Treaties. 'If I cut emissions but you don't, I lose economic growth.'",
        'use_corp': "🏢 **CEOs:** For Price Wars. 'If I cut price, I gain share temporarily, but if rival follows, we both lose margin.'",
        'use_analyst': "📈 **Auction Bidders:** To determine the optimal bid strategy without overpaying (Winner's Curse)."
    },
    'ID': {
        'title': "♟️ Teori Permainan: Strategi Oligopoli",
        'subtitle': "Rasakan simulasi **Dilema Tahanan (Prisoner's Dilemma)** dalam skenario Perang Harga.",
        'scenario': "**Skenario:** Anda dan Pesaing (AI) menguasai pasar.",
        'choice': "Tentukan Langkah Anda:",
        'high': "Pertahankan Harga Tinggi (Kooperasi)",
        'low': "Banting Harga (Defect/Perang)",
        'matrix_title': "📊 Matriks Imbalan (Anda vs AI)",
        'result_title': "Hasil Permainan",
        'you_chose': "Anda Memilih:",
        'ai_chose': "AI Memilih:",
        'payoff': "Profit Anda:",
        'ai_payoff': "Profit AI:",
        'nash': "🔔 **Nash Equilibrium:** Keduanya memiilih 'Banting Harga'. Kenapa? Karena apapun yang lawan lakukan, banting harga adalah strategi dominan agar tidak kehilangan pasar.",
        'collusion': "🤝 **Kolusi Berhasil:** Keduanya Harga Tinggi. Keuntungan bersama maksimal!",
        'betrayal': "😈 **Anda Berkhianat!** Anda banting harga saat AI bertahan. Anda merebut pasar!",
        'sucker': "😓 **Anda Tertipu!** AI banting harga saat Anda bertahan. Anda kehilangan pasar.",
        'score_you': "Anda",
        'score_ai': "AI",
        'story_title': "📚 Cerita & Kasus Penggunaan: Teori Permainan",
        'story_meaning': "**Apa artinya ini?**\nTeori Permainan menganalisis interaksi strategis di mana hasil Anda bergantung pada langkah lawan.",
        'story_insight': "**Wawasan Utama:**\nPerilaku rasional (mementingkan diri sendiri) seringkali berujung pada hasil yang lebih buruk bagi semua pihak (Nash Equilibrium). Kerjasama butuh kepercayaan atau kontrak mengikat.",
        'story_users': "**Siapa yang butuh ini?**",
        'use_govt': "🏛️ **Diplomat:** Untuk Perjanjian Iklim. 'Kalau saya kurangi emisi tapi negara lain tidak, ekonomi saya melambat sendirian.'",
        'use_corp': "🏢 **CEO:** Untuk Perang Harga. 'Kalau saya banting harga, saya dapat pasar sebentar, tapi kalau lawan ikut, margin kami berdua hancur.'",
        'use_analyst': "📈 **Peserta Lelang:** Untuk menentukan strategi penawaran (bidding) optimal tanpa membayar kemahalan."
    }
}

txt = T[lang]

st.title(txt['title'])
st.markdown(txt['subtitle'])

col1, col2 = st.columns([1, 1.5])

# --- Game Logic ---
# Payoff Matrix Structure: (User Payoff, AI Payoff)
#               AI High      AI Low
# User High    (100, 100)   (0, 150)
# User Low     (150, 0)     (50, 50)

payoff_map = {
    ('High', 'High'): (100, 100),
    ('High', 'Low'): (0, 150),
    ('Low', 'High'): (150, 0),
    ('Low', 'Low'): (50, 50)
}

with col1:
    st.info(txt['scenario'])
    
    user_action = st.radio(txt['choice'], 
                           ['High', 'Low'], 
                           format_func=lambda x: txt['high'] if x == 'High' else txt['low'])
    
    solve_btn = st.button("🏁 Submit Decision", type='primary')
    
    if solve_btn:
        # Simple AI: Random but slightly biased towards betrayal (Rational) or Tit-for-Tat if implemented fully
        # For this demo, let's make AI rational (mostly chooses Low) but sometimes cooperative to tempt user.
        ai_action = np.random.choice(['High', 'Low'], p=[0.3, 0.7]) 
        
        user_score, ai_score = payoff_map[(user_action, ai_action)]
        
        st.divider()
        st.subheader(txt['result_title'])
        st.write(f"🧑 **{txt['you_chose']}** {txt['high' if user_action=='High' else 'low']}")
        st.write(f"🤖 **{txt['ai_chose']}** {txt['high' if ai_action=='High' else 'low']}")
        
        if user_score == 100:
            st.success(txt['collusion'])
            st.metric(txt['payoff'], f"Rp {user_score}", delta="Max Joint")
        elif user_score == 150:
            st.success(txt['betrayal'])
            st.metric(txt['payoff'], f"Rp {user_score}", delta="You Win Big")
        elif user_score == 0:
            st.error(txt['sucker'])
            st.metric(txt['payoff'], f"Rp {user_score}", delta="-Loss")
        else: # 50, 50
            st.warning(txt['nash'])
            st.metric(txt['payoff'], f"Rp {user_score}", delta="Nash Eq")


with col2:
    st.subheader(txt['matrix_title'])
    
    # Visualizing Payoff Matrix using HTML/Markdown Table or Plotly Heatmap
    # A custom Heatmap is cooler.
    
    # Coordinates
    x = [txt['score_ai'] + " High", txt['score_ai'] + " Low"]
    y = [txt['score_you'] + " Low", txt['score_you'] + " High"] # Reversed for plot y-axis
    
    # Z values (User Payoff for coloring)
    z = [[50, 150], [0, 100]] 
    
    # Text Annotation
    text = [
        [f"User: 50<br>AI: 50<br>(Nash)", f"User: 150<br>AI: 0<br>(You Win)"],
        [f"User: 0<br>AI: 150<br>(AI Wins)", f"User: 100<br>AI: 100<br>(Coop)"]
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        text=text,
        texttemplate="%{text}",
        textfont={"size": 14},
        colorscale='RdBu',
        showscale=False
    ))
    
    fig.update_layout(
        title="Payoff Heatmap (User Profit View)",
        xaxis_title="AI Strategy",
        yaxis_title="User Strategy",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("""
    - **Top Left (100, 100)**: Reward for Cooperation.
    - **Bottom Right (50, 50)**: Punishment for Mutual Defection (Nash Equilibrium).
    - **Off-Diagonals**: Temptation vs Sucker's Payoff.
    """)

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
