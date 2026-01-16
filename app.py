
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

#### 🧠 {get_text('micro', lang)}
- **{get_text('supply_demand', lang)}**: {get_text('supply_demand_desc', lang)}
- **{get_text('market_struct', lang)}**: {get_text('market_struct_desc', lang)}
- **{get_text('prod_opt', lang)}**: {get_text('prod_opt_desc', lang)}
- **{get_text('policy', lang)}**: {get_text('policy_desc', lang)}

#### 🌍 {get_text('macro', lang)}
- **{get_text('growth', lang)}**: {get_text('growth_desc', lang)}
- **{get_text('equil', lang)}**: {get_text('equil_desc', lang)}
- **{get_text('indices', lang)}**: {get_text('indices_desc', lang)}

#### 🧪 {get_text('metrics', lang)}
- **{get_text('lab', lang)}**: {get_text('lab_desc', lang)}

---
*Built with Streamlit, Altair, and Python.*
""")

# Note: Sidebar navigation pages cannot be renamed dynamically from here easily in Streamlit.
# We will just update the content inside the pages to be bilingual.
st.sidebar.success(get_text('select_language', lang)) # Just a placeholder success message

