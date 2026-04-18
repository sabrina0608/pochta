import streamlit as st
import pandas as pd
import plotly.express as px

# Sahifa sarlavhasi
st.set_page_config(page_title="Kurs ishi", layout="wide")

st.title("📊 Ma'lumotlar Tahlili Dashboard")

# Faylni yuklash
@st.cache_data
def load_data():
    try:
        # Fayl nomi GitHub-dagidek aniq bo'lishi kerak
        return pd.read_csv('combined_data.csv')
    except Exception as e:
        st.error(f"Faylni o'qishda xatolik: {e}")
        return None

df = load_data()

if df is not None:
    # 1. Ma'lumotlarni ko'rish
    st.subheader("Ma'lumotlar jadvali")
    st.dataframe(df.head(10))

    # 2. Grafik chizish
    st.subheader("Vizualizatsiya")
    
    # Faqat raqamli ustunlarni tanlab olamiz
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            x_val = st.selectbox("X o'qini tanlang:", numeric_cols)
        with col2:
            y_val = st.selectbox("Y o'qini tanlang:", numeric_cols)
            
        fig = px.scatter(df, x=x_val, y=y_val, title=f"{x_val} va {y_val} bog'liqligi")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Grafik chizish uchun yetarli raqamli ma'lumotlar topilmadi.")
else:
    st.info("Iltimos, 'combined_data.csv' fayli GitHub-da borligini tekshiring.")
