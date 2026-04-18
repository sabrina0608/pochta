import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sahifa sozlamalari va dizayn
st.set_page_config(page_title="Bashoratli Tahlil Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .stMetric { border: 2px solid #4e73df; padding: 15px; border-radius: 10px; background: white; }
    h1 { color: #4e73df; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Kurs ishi: Bashoratli Ma'lumotlar Tahlili")
st.divider()

# 2. Ma'lumotlarni yuklash
@st.cache_data
def load_data():
    try:
        return pd.read_csv('combined_data.csv')
    except:
        return None

df = load_data()

if df is not None:
    # Metrikalar (Dashboard qismi)
    col1, col2, col3 = st.columns(3)
    col1.metric("Jami ma'lumotlar", len(df), "ta qator")
    col2.metric("O'zgaruvchilar", len(df.columns), "ta ustun")
    col3.metric("Loyiha holati", "Tayyor")

    # Diagrammalar bo'limi
    st.subheader("📈 Vizualizatsiya va Diagrammalar")
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols) >= 2:
        tab1, tab2 = st.tabs(["📉 Trend va Bashorat", "📊 Ma'lumotlar Taqsimoti"])
        
        with tab1:
            c1, c2 = st.columns(2)
            with c1: x_axis = st.selectbox("X o'qi (Bashorat asosi):", numeric_cols, key='x')
            with c2: y_axis = st.selectbox("Y o'qi (Natija):", numeric_cols, key='y')
            
            # Trendline bashoratli tahlil chizig'ini qo'shadi
            fig_scat = px.scatter(df, x=x_axis, y=y_axis, trendline="ols", 
                                 title=f"{x_axis} va {y_axis} bog'liqlik tahlili",
                                 color_discrete_sequence=['#4e73df'])
            st.plotly_chart(fig_scat, use_container_width=True)
            
        with tab2:
            sel_col = st.selectbox("Tahlil uchun ustunni tanlang:", numeric_cols)
            fig_hist = px.histogram(df, x=sel_col, title=f"{sel_col} taqsimoti", 
                                   marginal="box", color_discrete_sequence=['#1cc88a'])
            st.plotly_chart(fig_hist, use_container_width=True)
    
    # Ma'lumotlar jadvali
    with st.expander("📄 To'liq jadvalni ko'rish"):
        st.dataframe(df, use_container_width=True)

else:
    st.error("⚠️ 'combined_data.csv' fayli topilmadi. GitHub-da fayl nomi to'g'riligini tekshiring.")
