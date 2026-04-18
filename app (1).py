import streamlit as st
import pandas as pd
import plotly.express as px

# Sahifa sozlamalari
st.set_page_config(page_title="Bashoratli Tahlil Dashboard", layout="wide")

# Chiroyli dizayn (CSS)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #4e73df; }
    h1 { color: #4e73df; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Ma'lumotlar Tahlili va Bashoratli Vizualizatsiya")
st.write("---")

@st.cache_data
def load_data():
    try:
        # Fayl nomi GitHub'dagidek bir xil bo'lishi shart
        return pd.read_csv('combined_data.csv')
    except:
        return None

df = load_data()

if df is not None:
    # 1. Asosiy ko'rsatkichlar (Metrics)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ma'lumotlar soni", len(df), "qator")
    c2.metric("O'zgaruvchilar", len(df.columns), "ustun")
    c3.metric("Loyiha holati", "Tayyor")

    st.markdown("### 📈 Diagrammalar va Bashorat")
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if len(numeric_cols) >= 2:
        tab1, tab2 = st.tabs(["📉 Trend Tahlili", "📊 Taqsimot va Bog'liqlik"])
        
        with tab1:
            x_ax = st.selectbox("X o'qini tanlang (Vaqt/Guruh):", numeric_cols, key='x1')
            y_ax = st.selectbox("Y o'qini tanlang (Qiymat):", numeric_cols, key='y1')
            
            # Trendline bashorat chizig'ini ko'rsatadi
            fig_line = px.scatter(df, x=x_ax, y=y_ax, trendline="ols", 
                                  title=f"{y_ax} ning {x_ax} ga bog'liqlik bashorati")
            st.plotly_chart(fig_line, use_container_width=True)
            
        with tab2:
            col_a, col_b = st.columns(2)
            with col_a:
                feat = st.selectbox("Taqsimot ustuni:", numeric_cols)
                fig_hist = px.histogram(df, x=feat, color_discrete_sequence=['#1cc88a'])
                st.plotly_chart(fig_hist, use_container_width=True)
            with col_b:
                fig_box = px.box(df, y=feat, title="Statistik taqsimot (Boxplot)")
                st.plotly_chart(fig_box, use_container_width=True)

    # 2. Ma'lumotlar jadvali
    with st.expander("📄 To'liq jadvalni ko'rish"):
        st.dataframe(df, use_container_width=True)
else:
    st.error("⚠️ 'combined_data.csv' fayli topilmadi. GitHub-da fayl nomi to'g'riligini tekshiring.")
