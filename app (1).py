import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sahifa sozlamalari
st.set_page_config(page_title="Bashoratli Tahlil Dashboard", layout="wide")

# Dizayn (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_all_ Wood=True)

st.title("📈 Ma'lumotlar Tahlili va Bashoratli Diagrammalar")
st.markdown("---")

@st.cache_data
def load_data():
    try:
        return pd.read_csv('combined_data.csv')
    except:
        return None

df = load_data()

if df is not None:
    # Sidebar - Sozlamalar
    st.sidebar.header("📊 Filtrlash va Sozlamalar")
    
    # Metrikalar (Asosiy ko'rsatkichlar)
    col1, col2, col3 = st.columns(3)
    col1.metric("Jami ma'lumotlar", len(df))
    col2.metric("Ustunlar soni", len(df.columns))
    col3.metric("Status", "Faol")

    # Diagrammalar bo'limi
    tab1, tab2, tab3 = st.tabs(["📉 Trend Tahlili", "📊 Taqsimot", "🔍 Korrelyatsiya"])

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    with tab1:
        st.subheader("Trend va Bashorat Diagrammasi")
        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("X o'qini tanlang (vaqt yoki guruh):", numeric_cols, key='x1')
            y_axis = st.selectbox("Y o'qini tanlang (qiymat):", numeric_cols, key='y1')
            
            fig_line = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis}ning {x_axis} bo'yicha o'zgarishi",
                               template="plotly_white", markers=True)
            st.plotly_chart(fig_line, use_container_width=True)
        
    with tab2:
        st.subheader("Ma'lumotlar Taqsimoti")
        dist_col = st.selectbox("Tahlil uchun ustunni tanlang:", numeric_cols)
        fig_hist = px.histogram(df, x=dist_col, nbins=30, color_discrete_sequence=['#636EFA'],
                                 marginal="box", title=f"{dist_col} taqsimoti")
        st.plotly_chart(fig_hist, use_container_width=True)

    with tab3:
        st.subheader("Bashoratli Bog'liqlik (Scatter Plot)")
        if len(numeric_cols) >= 2:
            c1, c2 = st.columns(2)
            with c1: x_scat = st.selectbox("X o'qi:", numeric_cols, key='xs')
            with c2: y_scat = st.selectbox("Y o'qi:", numeric_cols, key='ys')
            
            fig_scatter = px.scatter(df, x=x_scat, y=y_scat, trendline="ols",
                                     title=f"{x_scat} va {y_scat} o'rtasidagi bog'liqlik tahlili")
            st.plotly_chart(fig_scatter, use_container_width=True)

    # Jadvalni ko'rsatish
    with st.expander("Barcha ma'lumotlarni ko'rish"):
        st.dataframe(df)

else:
    st.error("⚠️ 'combined_data.csv' fayli topilmadi. Iltimos, GitHub-ga yuklanganini tekshiring.")
    st.info("Eslatma: Fayl nomi kichik harflarda va qavslarsiz bo'lishi kerak.")
