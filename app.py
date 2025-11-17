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

# 📁 Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados_final.csv")

@st.cache_data
def carregar_geojson():
    with open("municipios.geojson", encoding="utf-8") as f:
        return json.load(f)

df = carregar_dados()
geojson_data = carregar_geojson()

# Padronizar nomes
df["Município"] = df["Município"].str.strip().str.lower()
for feature in geojson_data["features"]:
    feature["properties"]["name"] = feature["properties"]["name"].strip().lower()

# 🧩 Filtros interativos
st.sidebar.header("🎛️ Filtros")
ufs = sorted(df["UF"].unique())
uf_selecionada = st.sidebar.selectbox("📍 Filtrar por UF", options=["Todas"] + ufs)
renda_min = st.sidebar.slider("💰 Renda média mínima (60+)", 0, int(df["Renda média 60+"].max()), 0)

df_filtrado = df.copy()
if uf_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["UF"] == uf_selecionada]
df_filtrado = df_filtrado[df_filtrado["Renda média 60+"] >= renda_min]

# 🗂️ Menu de navegação
aba = st.sidebar.radio("Escolha uma aba", ["Mapa Interativo", "Hotspots Econômicos", "Oportunidades Emergentes"])

# 🗺️ Aba 1: Mapa Interativo
if aba == "Mapa Interativo":
    st.subheader("🗺️ Mapa Interativo de Envelhecimento")
    fig = px.choropleth(
        df_filtrado,
        geojson=geojson_data,
        locations="Município",
        featureidkey="properties.name",
        color="Índice de envelhecimento",
        hover_name="Município",
        color_continuous_scale="Viridis"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

# 📈 Aba 2: Hotspots Econômicos
elif aba == "Hotspots Econômicos":
    st.subheader("📈 Hotspots da Economia Prateada")
    st.markdown("Explore os municípios com alto índice de envelhecimento e renda média elevada entre idosos.")

    fig2 = px.scatter(
        df_filtrado,
        x="Índice de envelhecimento",
        y="Proporção casais sem filhos",
        size="Renda média 60+",
        hover_name="Município",
        color="Renda média 60+",
        title="Dispersão entre IE e estrutura domiciliar"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("🏆 Ranking dos municípios com maior índice de envelhecimento:")
    st.dataframe(df_filtrado.sort_values("Índice de envelhecimento", ascending=False).head(20))

# 🔍 Aba 3: Oportunidades Emergentes
elif aba == "Oportunidades Emergentes":
    st.subheader("🔍 Municípios com crescimento acelerado da população 60+")
    st.markdown("""
Nem todos os municípios com baixo índice de envelhecimento devem ser ignorados. Alguns apresentam renda elevada e estrutura familiar propícia para o crescimento da Economia Prateada.
""")
    filtro = df_filtrado[df_filtrado["Índice de envelhecimento"] < 30].sort_values("Renda média 60+", ascending=False)
    st.dataframe(filtro.head(20))

