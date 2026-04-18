import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Sahifa sarlavhasi
st.set_page_config(page_title="Kurs Ishi Dashboard", layout="wide")

st.title("📊 Ma'lumotlar Tahlili va Vizualizatsiya")

# 2. Ma'lumotlarni yuklash funksiyasi
@st.cache_data
def load_data():
    try:
        # Fayl nomi GitHub-dagidek bir xil bo'lishi shart
        data = pd.read_csv('combined_data.csv')
        return data
    except Exception as e:
        return None

df = load_data()

# 3. Interfeys qismi
if df is not None:
    st.success("Ma'lumotlar muvaffaqiyatli yuklandi!")
    
    # Ma'lumotlar jadvali
    st.subheader("📋 Jadvalning bir qismi")
    st.write(df.head(10))

    # Grafik chizish
    st.subheader("📈 Grafik yaratish")
    
    # Faqat sonli ustunlarni filtrlaymiz
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_columns) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X o'qi (Gorizontal):", numeric_columns)
        with col2:
            y_axis = st.selectbox("Y o'qi (Vertikal):", numeric_columns)
            
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{x_axis} va {y_axis} taqsimoti")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Grafik chizish uchun yetarli sonli ustunlar mavjud emas.")
else:
    st.error("Xatolik: 'combined_data.csv' fayli GitHub-da topilmadi!")
