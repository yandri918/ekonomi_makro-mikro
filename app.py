
import streamlit as st
import sys
import os

# Add parent dir to path to find utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.language import get_text

st.set_page_config(
    page_title="Economics & Data Science Portfolio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Language Toggle in Sidebar
if 'language' not in st.session_state:
    st.session_state['language'] = 'ID'

with st.sidebar:
    st.header(get_text('sidebar_title', st.session_state['language']))
    lang_choice = st.radio(get_text('select_language', st.session_state['language']), ["Bahasa Indonesia", "English"])
    if lang_choice == "Bahasa Indonesia":
        st.session_state['language'] = 'ID'
    else:
        st.session_state['language'] = 'EN'
        
    st.markdown("---")

lang = st.session_state['language']

st.title(f"📊 {get_text('welcome_title', lang)}")
st.markdown(f"""
### {get_text('welcome_subtitle', lang)}

{get_text('intro_text', lang)}
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"#### 🧠 {get_text('micro', lang)}")
    st.write(f"- 1. **{get_text('supply_demand', lang)}**: {get_text('supply_demand_desc', lang)}")
    st.write(f"- 2. **{get_text('market_struct', lang)}**: {get_text('market_struct_desc', lang)}")
    st.write(f"- 8. **{get_text('prod_opt', lang)}**: {get_text('prod_opt_desc', lang)}")
    st.write(f"- 12. **{get_text('game_theory', lang)}**: {get_text('game_theory_desc', lang)}")
    st.write(f"- 14. **{get_text('investment', lang)}**: {get_text('investment_desc', lang)}")

with col2:
    st.markdown(f"#### 🌍 {get_text('macro', lang)}")
    st.write(f"- 4. **{get_text('growth', lang)}**: {get_text('growth_desc', lang)}")
    st.write(f"- 5. **{get_text('equil', lang)}**: {get_text('equil_desc', lang)}")
    st.write(f"- 10. **{get_text('growth', lang)} (AI)**: {get_text('growth_desc', lang)}")
    st.write(f"- 11. **{get_text('wage', lang)}**: {get_text('wage_desc', lang)}")

with col3:
    st.markdown(f"#### 🧪 {get_text('metrics', lang)}")
    st.write(f"- 7. **{get_text('lab', lang)}**: {get_text('lab_desc', lang)}")
    st.write(f"- 9. **{get_text('forecasting', lang)}**: {get_text('forecasting_desc', lang)}")
    st.write(f"- 13. **{get_text('real_data', lang)}**: {get_text('real_data_desc', lang)}")

st.markdown("---")
st.caption("*Built with Streamlit, Altair, Scipy, World Bank API & Python.*")
