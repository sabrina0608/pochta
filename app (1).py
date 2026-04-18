import streamlit as st
import pandas as pd
import plotly.express as px

# Sahifa sozlamalari
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# Dizayn uchun CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { border: 1px solid #4e73df; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Kurs ishi: Ma'lumotlar Tahlili va Bashorat")

@st.cache_data
def load_data():
    try:
        # Fayl nomi GitHub'da qanday bo'lsa shunday yoziladi
        return pd.read_csv('combined_data.csv')
    except:
        return None

df = load_data()

if df is not None:
    # Metrikalar paneli
    m1, m2, m3 = st.columns(3)
    m1.metric("Ma'lumotlar soni", len(df))
    m2.metric("Xususiyatlar", len(df.columns))
    m3.metric("Holati", "Tayyor")

    st.divider()

    # Diagrammalar
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Taqsimot Diagrammasi")
            sel_col = st.selectbox("Ustunni tanlang:", numeric_cols)
            fig_hist = px.histogram(df, x=sel_col, color_discrete_sequence=['#4e73df'])
            st.plotly_chart(fig_hist, use_container_width=True)

        with col2:
            st.subheader("🔮 Bashoratli Bog'liqlik")
            x_ax = st.selectbox("X o'qi:", numeric_cols, key='x_axis')
            y_ax = st.selectbox("Y o'qi:", numeric_cols, key='y_axis')
            # Trendline bashorat chizig'ini ko'rsatadi
            fig_scat = px.scatter(df, x=x_ax, y=y_ax, trendline="ols")
            st.plotly_chart(fig_scat, use_container_width=True)
    
    st.subheader("📋 Ma'lumotlar jadvali")
    st.dataframe(df, use_container_width=True)
else:
    st.error("Xatolik: 'combined_data.csv' fayli topilmadi. Fayl nomini GitHub'da tekshiring!")
