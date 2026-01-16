
TRANSLATIONS = {
    'EN': {
        'sidebar_title': "Navigation",
        'select_language': "Select Language",
        'welcome_title': "Economics & Data Science Portfolio",
        'welcome_subtitle': "Welcome to the Intersection of Theory and Data",
        'intro_text': "This portfolio demonstrates advanced **Microeconomics** and **Macroeconomics** concepts visualized through **Data Science** techniques.",
        'micro': "Microeconomics",
        'macro': "Macroeconomics",
        'metrics': "Econometrics",
        'supply_demand': "Supply & Demand",
        'supply_demand_desc': "Simulate demand and supply forces.",
        'market_struct': "Market Structures",
        'market_struct_desc': "Perfect Comp vs Monopoly.",
        'prod_opt': "Production Optimization",
        'prod_opt_desc': "Isoquants & Isocosts.",
        'policy': "Public Policy",
        'policy_desc': "Taxes, Subsidies, DWL.",
        'growth': "Growth Models",
        'growth_desc': "Solow Growth Model.",
        'equil': "Macro Equilibrium",
        'equil_desc': "IS-LM & AD-AS.",
        'indices': "Economic Indices",
        'indices_desc': "CPI & PPP.",
        'lab': "Econometrics Lab",
        'lab_desc': "Regression Analysis."
    },
    'ID': {
        'sidebar_title': "Navigasi",
        'select_language': "Pilih Bahasa",
        'welcome_title': "Portofolio Ekonomi & Data Science",
        'welcome_subtitle': "Selamat Datang di Titik Temu Teori dan Data",
        'intro_text': "Portofolio ini mendemonstrasikan konsep **Ekonomi Mikro** dan **Makro** tingkat lanjut yang divisualisasikan melalui teknik **Data Science**.",
        'micro': "Ekonomi Mikro",
        'macro': "Ekonomi Makro",
        'metrics': "Ekonometrika",
        'supply_demand': "Permintaan & Penawaran",
        'supply_demand_desc': "Simulasi kekuatan pasar.",
        'market_struct': "Struktur Pasar",
        'market_struct_desc': "Persaingan Sempurna vs Monopoli.",
        'prod_opt': "Optimasi Produksi",
        'prod_opt_desc': "Isokuan & Isocost.",
        'policy': "Kebijakan Publik",
        'policy_desc': "Pajak, Subsidi, DWL.",
        'growth': "Model Pertumbuhan",
        'growth_desc': "Model Pertumbuhan Solow.",
        'equil': "Ekuilibrium Makro",
        'equil_desc': "IS-LM & AD-AS.",
        'indices': "Indikator Ekonomi",
        'indices_desc': "IHK & PPP.",
        'lab': "Lab Ekonometrika",
        'lab_desc': "Analisis Regresi."
    }
}

def get_text(key, lang='ID'):
    return TRANSLATIONS.get(lang, TRANSLATIONS['ID']).get(key, key)
