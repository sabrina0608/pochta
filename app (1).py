import streamlit as st
import pandas as pd
import plotly.express as px

# Sahifa sozlamalari
st.set_page_config(page_title="Kurs ishi | Dashboard", layout="wide")

st.title("🚀 Ma'lumotlar Tahlili Veb-ilovasi")
st.sidebar.header("Sozlamalar")

# Ma'lumotni yuklash funksiyasi
@st.cache_data
def load_data():
    return pd.read_csv('combined_data.csv')

try:
    data = load_data()
    
    # Ma'lumotlar haqida qisqacha statistika
    st.write("### Ma'lumotlar jadvali (dastlabki 10 ta qator)")
    st.dataframe(data.head(10))

    # Grafik yaratish bo'limi
    st.write("### Vizual tahlil")
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if numeric_cols:
        x_axis = st.sidebar.selectbox("X o'qi uchun ustunni tanlang:", numeric_cols)
        y_axis = st.sidebar.selectbox("Y o'qi uchun ustunni tanlang:", numeric_cols)
        
        fig = px.scatter(data, x=x_axis, y=y_axis, color_continuous_scale='Viridis',
                         title=f"{x_axis} va {y_axis} o'rtasidagi bog'liqlik")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Grafik chizish uchun raqamli ustunlar topilmadi.")

except Exception as e:
    st.error(f"Kutilmagan xatolik yuz berdi: {e}")
