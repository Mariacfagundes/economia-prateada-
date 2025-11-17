import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Economia Prateada no Brasil", layout="wide")

# 🎨 Estilo personalizado
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
    }
    .main {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

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

    st.markdown("### 🧠 O que você verá nas próximas abas:")
    st.markdown("""
    - Indicadores gerais que revelam o perfil da população 60+ no Brasil  
    - Ranking dos municípios mais envelhecidos — e o que isso significa  
    - Hotspots econômicos com alto potencial de consumo prateado  
    - Oportunidades emergentes em cidades que estão envelhecendo rápido  
    """)

# 📊 Aba 2: Indicadores Gerais
elif aba == "Indicadores Gerais":
    st.subheader("📊 Indicadores Gerais")

    st.markdown("### 🧠 O que este painel mostra:")
    st.markdown(f"""
    Você selecionou **{uf_selecionada}** com renda mínima de **R$ {renda_min}**.  
    Este painel revela o perfil médio da população idosa nesses municípios — incluindo envelhecimento, renda e estrutura familiar.
    """)

    media_ie = df_filtrado["Índice de envelhecimento"].mean()
    media_renda = df_filtrado["Renda média 60+"].mean()

    st.markdown("### 📌 Insights automáticos:")
    st.markdown(f"""
    - O índice médio de envelhecimento é **{media_ie:.1f}**  
    - A renda média dos 60+ é **R$ {media_renda:,.0f}**
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Média do Índice de Envelhecimento", f"{media_ie:.1f}")
    col2.metric("💰 Renda Média 60+", f"R$ {media_renda:,.0f}")
    col3.metric("🏘️ Municípios Analisados", f"{len(df_filtrado)}")

    st.markdown("Distribuição da renda média da população 60+:")
    fig_hist = px.histogram(df_filtrado, x="Renda média 60+", nbins=30, color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig_hist, use_container_width=True)

# 🏆 Aba 3: Ranking de Envelhecimento
elif aba == "Ranking de Envelhecimento":
    st.subheader("🏆 Municípios com maior Índice de Envelhecimento")

    st.markdown("### 🧠 O que este ranking mostra:")
    st.markdown("""
    Aqui estão os 20 municípios com maior proporção de idosos em relação aos jovens.  
    Essas cidades estão na vanguarda da transição demográfica e exigem políticas públicas e soluções de mercado voltadas à longevidade.
    """)

    mais_envelhecido = df_filtrado.sort_values("Índice de envelhecimento", ascending=False).iloc[0]
    st.markdown("### 📌 Destaque:")
    st.markdown(f"""
    - O município mais envelhecido é **{mais_envelhecido['Município'].title()}**, com índice de **{mais_envelhecido['Índice de envelhecimento']:.1f}**  
    - Renda média 60+: **R$ {mais_envelhecido['Renda média 60+']:,.0f}**
    """)

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

    st.markdown("### 🧠 O que este gráfico mostra:")
    st.markdown("""
    Este gráfico cruza três dimensões: envelhecimento, estrutura familiar e renda.  
    Os municípios no canto superior direito são verdadeiros **hotspots da Economia Prateada** — alta concentração de idosos com renda e autonomia.
    """)

    hotspot = df_filtrado.sort

     # 🔍 Aba 5: Oportunidades Emergentes
elif aba == "Oportunidades Emergentes":
    st.subheader("🔍 Municípios com crescimento acelerado da população 60+")

    st.markdown("### 🧠 O que este painel revela:")
    st.markdown("""
    Nem toda cidade com baixo índice de envelhecimento deve ser ignorada.  
    Este painel destaca municípios com **renda elevada e estrutura familiar propícia**, que estão envelhecendo rapidamente e oferecem oportunidades emergentes.
    """)

    emergente = df_filtrado[df_filtrado["Índice de envelhecimento"] < 30].sort_values("Renda média 60+", ascending=False).head(1)
    if not emergente.empty:
        cidade = emergente.iloc[0]["Município"].title()
        renda = emergente.iloc[0]["Renda média 60+"]
        st.markdown("### 📌 Destaque:")
        st.markdown(f"""
        - O município emergente com maior renda é **{cidade}**, com renda média 60+ de **R$ {renda:,.0f}**.
        """)

    filtro = df_filtrado[df_filtrado["Índice de envelhecimento"] < 30].sort_values("Renda média 60+", ascending=False)
    st.dataframe(filtro.head(20))

    # 👩‍💻 Aba 6: Sobre a Autora
elif aba == "Sobre a Autora":
    st.subheader("👩‍💻 Sobre a Autora")
    st.markdown("...")


    <div style='font-size: 18px; line-height: 1.6'>
    <strong>Maria Clara Fagundes</strong>  
    📍 <em>Salvador, Bahia</em>  
    💼 <em>Engenheira de Dados</em>  
    <br><br>
    Apaixonada por transformar dados públicos em soluções estratégicas e acessíveis.  
    Atua na interseção entre tecnologia, impacto social e inteligência territorial.  
    <br><br>
    Este projeto foi desenvolvido como parte do desafio  
    <strong>“O Impacto do Envelhecimento Populacional no Brasil”</strong>,  
    com o objetivo de revelar oportunidades sociais e econômicas ligadas à  
    <strong>Economia Prateada</strong>.
    <br><br>
    📧 <a href="mailto:luzfaghundes@gmail.com">luzfaghundes@gmail.com</a>  
    🔗 <a href="https://www.linkedin.com/in/maria-clara-fagundes-32027680/" target="_blank">LinkedIn</a>  
    </div>
    """, unsafe_allow_html=True)
    
  # 📌 Rodapé (fora de qualquer bloco)
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 16px;'>
📊 <strong>Desenvolvido por Maria Clara Fagundes</strong>  
Desafio <em>Economia Prateada</em> • 2025
</div>
""", unsafe_allow_html=True)




