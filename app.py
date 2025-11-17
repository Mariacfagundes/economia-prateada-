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
import geopandas as gpd

@st.cache_data
def carregar_geojson():
    gdf = gpd.read_file("municipios.geojson")
    return gdf

gdf = carregar_geojson()

# Padronizar nomes
df["Município"] = df["Município"].str.strip().str.lower()
gdf["name"] = gdf["name"].str.strip().str.lower()

# Juntar os dados
gdf = gdf.merge(df, left_on="name", right_on="Município")

# Mapa interativo
if aba == "Mapa Interativo":
    st.subheader("🗺️ Mapa Interativo de Envelhecimento")
    fig = px.choropleth(
        gdf,
        geojson=gdf.set_geometry("geometry"),
        locations=gdf.index,
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







