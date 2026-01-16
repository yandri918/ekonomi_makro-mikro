
import streamlit as st

st.set_page_config(
    page_title="Economics & Data Science Portfolio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Economics & Data Science Portfolio")
st.markdown("""
### Welcome to the Intersection of Theory and Data

This portfolio demonstrates advanced **Microeconomics** and **Macroeconomics** concepts visualized through **Data Science** techniques. 
Explore the modules in the sidebar to interact with dynamic models, simulations, and econometric analyses.

#### 🧠 Microeconomics
- **Supply & Demand**: Interact with market forces.
- **Elasticity**: Calculate and visualize sensitivity.
- **Market Structures**: Compare Perfect Competition, Monopoly, and Oligopoly.
- **Public Policy**: Simulate taxes, subsidies, and minimum wages.

#### 🌍 Macroeconomics
- **Growth Models**: Solow Growth Model simulation.
- **Equilibrium**: IS-LM and AD-AS frameworks.
- **Indices**: Logic behind CPI, GDP Deflator, and PPP.

#### 🧪 Econometrics Lab
- **Regression Analysis**: Estimate demand functions and consumption models.
- **Time Series**: Explore economic trends.

---
*Built with Streamlit, Altair, and Python.*
""")

st.sidebar.success("Select a module above to begin.")
