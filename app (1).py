import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Bashoratli Tahlil", layout="wide")

# 2. Dizayn (CSS) - boyagi xato shu yerda edi, endi tuzatildi
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Kurs ishi: Bashoratli Tahlil va Diagrammalar")

# 3. Ma'lumotlarni yuklash
@st.cache_data
def load_data():
    try:
        return pd.read_csv('combined_data.csv')
    except:
        return None

df = load_data()

if df is not None:
    # Metrikalar
    c1, c2, c3 = st.columns(3)
    c1.metric("Ma'lumotlar soni", len(df))
    c2.metric("Ustunlar", len(df.columns))
    c3.metric("Loyiha holati", "Tayyor")

    # Diagrammalar
    st.subheader("📈 Vizual Tahlil va Diagrammalar")
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_cols) >= 2:
        tab1, tab2 = st.tabs(["Chiziqli diagramma", "Gistogramma"])
        
        with tab1:
            x_ax = st.selectbox("X o'qi:", numeric_cols, key='x')
            y_ax = st.selectbox("Y o'qi:", numeric_cols, key='y')
            fig1 = px.line(df, x=x_ax, y=y_ax, title=f"{y_ax} ning o'zgarishi", template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
            
        with tab2:
            feat = st.selectbox("Taqsimot ustunini tanlang:", numeric_cols)
            fig2 = px.histogram(df, x=feat, title=f"{feat} taqsimoti", color_discrete_sequence=['indianred'])
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Diagramma uchun raqamli ustunlar yetarli emas.")
        
    st.write("### 📄 Ma'lumotlar jadvali")
    st.dataframe(df.head(20))
else:
    st.error("Xatolik: 'combined_data.csv' fayli topilmadi!")
