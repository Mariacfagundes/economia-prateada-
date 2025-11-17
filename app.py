import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Economia Prateada no Brasil", layout="wide")

# 🎯 Título
st.title("🌎 O Impacto do Envelhecimento Populacional no Brasil")

# 📁 Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados_final_com_uf.csv", encoding="utf-8")

df = carregar_dados()
df.columns = df.columns.str.strip()
df["Município"] = df["Município"].str.strip().str.lower()

# 🧼 Corrigir e mapear a coluna UF
uf_map = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
    "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA",
    "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
    "41": "PR", "42": "SC", "43": "RS",
    "50": "MS", "51": "MT", "52": "GO", "53": "DF"
}

df["UF"] = pd.to_numeric(df["UF"], errors="coerce")
df = df.dropna(subset=["UF"]).copy()
df["UF"] = df["UF"].astype(int).astype(str).map(uf_map)
df = df.dropna(subset=["UF"]).copy()

# 🎛️ Filtros interativos
st.sidebar.header("🎛️ Filtros")
ufs = sorted(df["UF"].dropna().unique())
uf_selecionada = st.sidebar.selectbox("📍 Filtrar por UF", options=["Todas"] + list(ufs))
renda_min = st.sidebar.slider("💰 Renda média mínima (60+)", 0, int(df["Renda média 60+"].max()), 0)

if st.sidebar.button("🔄 Limpar filtros"):
    st.experimental_rerun()

# Aplicar filtros
df_filtrado = df.copy()
if uf_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["UF"] == uf_selecionada]
df_filtrado = df_filtrado[df_filtrado["Renda média 60+"] >= renda_min]

# 🔍 Diagnóstico rápido
if df_filtrado.empty:
    st.warning("⚠️ Nenhum município encontrado com os filtros selecionados.")
    st.stop()

# 🗂️ Menu de navegação
aba = st.sidebar.radio("Escolha uma aba", [
    "Apresentação", "Indicadores Gerais", "Ranking de Envelhecimento",
    "Hotspots Econômicos", "Oportunidades Emergentes", "Sobre a Autora"
])

# 📘 Aba 1: Apresentação
if aba == "Apresentação":
    st.header("📘 Apresentação do Projeto")
    st.success("Bem-vinda ao painel da Economia Prateada! Explore os dados e descubra oportunidades.")
    st.markdown("""
    O Brasil está envelhecendo — e rápido. Com base no Censo 2022, este projeto analisa o avanço da **Economia Prateada**, um mercado em expansão voltado para a população com 60 anos ou mais.

    ### 🎯 Objetivo
    Identificar municípios com alto potencial de consumo, demanda social e oportunidades de investimento para a população idosa.

    ### 🔍 Metodologia
    Cruzamos três indicadores:
    - **Índice de Envelhecimento**
    - **Proporção de casais sem filhos**
    - **Renda média da população 60+**

    ### 💡 Principais Insights
    - Municípios do Sul e Sudeste concentram os maiores índices de envelhecimento e renda.
    - Regiões do Norte e Nordeste apresentam **tendência de envelhecimento acelerado**, com oportunidades emergentes.
    - A estrutura domiciliar (casais sem filhos) reforça o potencial de consumo e necessidade de serviços personalizados.

    ### 🧭 Público-Alvo
    - **Gestores públicos**: para políticas de saúde, moradia e mobilidade.
    - **Empreendedores e investidores**: para identificar hotspots de mercado prateado.

    ### 📌 Conclusão
    A Economia Prateada não é apenas um desafio demográfico — é uma **janela estratégica de inovação social e econômica**.
    """)

# 📊 Aba 2: Indicadores Gerais
elif aba == "Indicadores Gerais":
    st.subheader("📊 Indicadores Gerais")
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Média do Índice de Envelhecimento", f"{df_filtrado['Índice de envelhecimento'].mean():.1f}")
    col2.metric("💰 Renda Média 60+", f"R$ {df_filtrado['Renda média 60+'].mean():,.0f}")
    col3.metric("🏘️ Municípios Analisados", f"{len(df_filtrado)}")

    st.markdown("Distribuição da renda média da população 60+:")
    fig_hist = px.histogram(df_filtrado, x="Renda média 60+", nbins=30, color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig_hist, use_container_width=True)

# 🏆 Aba 3: Ranking de Envelhecimento
elif aba == "Ranking de Envelhecimento":
    st.subheader("🏆 Municípios com maior Índice de Envelhecimento")
    top_ie = df_filtrado.sort_values("Índice de envelhecimento", ascending=False).head(20)
    fig_bar = px.bar(
        top_ie,
        x="Município",
        y="Índice de envelhecimento",
        color="Renda média 60+",
        title="Top 20 municípios com maior IE",
        labels={"Índice de envelhecimento": "Índice de Envelhecimento"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.dataframe(top_ie)

# 📈 Aba 4: Hotspots Econômicos
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

# 🔍 Aba 5: Oportunidades Emergentes
elif aba == "Oportunidades Emergentes":
    st.subheader("🔍 Municípios com crescimento acelerado da população 60+")
    st.markdown("""
    Nem todos os municípios com baixo índice de envelhecimento devem ser ignorados. Alguns apresentam renda elevada e estrutura familiar propícia para o crescimento da Economia Prateada.
    """)
    filtro = df_filtrado[df_filtrado["Índice de envelhecimento"] < 30].sort_values("Renda média 60+", ascending=False)
    st.dataframe(filtro.head(20))

# 👩‍💻 Aba 6: Sobre a Autora
elif aba == "Sobre a Autora":
    st.subheader("👩‍💻 Sobre a Autora")
    st.markdown("""
    **Maria Clara Fagundes**  
    📍 Salvador, Bahia  
    💼 Engenheira de Dados  

    Apaixonada por transformar dados públicos em soluções estratégicas.  
    Este projeto foi desenvolvido como parte do desafio “O Impacto do Envelhecimento Populacional no Brasil”, com foco em revelar oportunidades sociais e econômicas ligadas à Economia Prateada.

    📧 luzfaghundes@gmail.com  
    🔗 [LinkedIn](https://www.linkedin.com/in/maria-clara-fagundes-32027680/)
    """)

# 📌 Rodapé
st.markdown("---")
st.markdown("📊 Desenvolvido por Maria Clara Fagundes • Desafio Economia Prateada • 2025")
