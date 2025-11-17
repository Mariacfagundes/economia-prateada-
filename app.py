import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Economia Prateada no Brasil", layout="wide")

# 🎯 Título e introdução
st.title("🌎 O Impacto do Envelhecimento Populacional no Brasil")
st.markdown("""
O Brasil está passando por uma transição demográfica acelerada. Este dashboard explora os dados do Censo 2022 para identificar **hotspots da Economia Prateada**, cruzando indicadores como:
- Índice de Envelhecimento
- Proporção de casais sem filhos
- Renda média da população 60+
""")

# 📁 Carregar dados tratados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_final.csv")
    return df

df = carregar_dados()

# 📁 Carregar geometria dos municípios
@st.cache_data
def carregar_geojson():
    with open("municipios.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)
    return geojson_data

geojson_data = carregar_geojson()

# 🗂️ Menu de navegação
aba = st.sidebar.radio("Escolha uma aba", ["Mapa Interativo", "Hotspots Econômicos", "Oportunidades Emergentes"])

# 🗺️ Aba 1: Mapa Interativo
if aba == "Mapa Interativo":
    st.subheader("🗺️ Mapa Interativo de Envelhecimento")
    fig = px.choropleth(
        df,
        geojson=geojson_data,
        locations="Município",
        featureidkey="properties.NM_MUN",  # ajuste conforme seu GeoJSON
        color="Índice de envelhecimento",
        hover_name="Município",
        color_continuous_scale="Viridis"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

# 📈 Aba 2: Hotspots Econômicos
elif aba == "Hotspots Econômicos":
    st.subheader("📈 Hotspots da Economia Prateada")
    fig2 = px.scatter(
        df,
        x="Índice de envelhecimento",
        y="Proporção casais sem filhos",
        size="Renda média 60+",
        hover_name="Município",
        color="Renda média 60+",
        title="Dispersão entre IE e estrutura domiciliar"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df.sort_values("Índice de envelhecimento", ascending=False))

# 🔍 Aba 3: Oportunidades Emergentes
elif aba == "Oportunidades Emergentes":
    st.subheader("🔍 Municípios com crescimento acelerado da população 60+")
    st.markdown("Aqui você pode destacar municípios com IE baixo, mas tendência forte de envelhecimento.")
    st.dataframe(df[df["Índice de envelhecimento"] < 30].sort_values("Renda média 60+", ascending=False))
