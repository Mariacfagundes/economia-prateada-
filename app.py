import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


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
st.markdown("""
<div style='font-size: 36px; font-weight: bold; line-height: 1.3; margin-bottom: 20px;'>
🌎 O Impacto do Envelhecimento Populacional no Brasil
</div>
""", unsafe_allow_html=True)

# 📁 Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados_com_geo.csv", encoding="utf-8")

# 🔄 Chama a função e limpa os dados
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
    "Hotspots Econômicos", "Índice Prateado", "Oportunidades Emergentes",
    "Mapa Interativo", "Sobre a Autora"
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

    uf_texto = "todo o Brasil" if uf_selecionada == "Todas" else f"o estado de {uf_selecionada}"
    st.markdown(f"""
    Você selecionou **{uf_texto}** com renda mínima de **R$ {renda_min}**.  
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
    Os municípios no canto superior direito são verdadeiros hotspots da Economia Prateada — alta concentração de idosos com renda e autonomia.
    """)

    if df_filtrado.empty:
        st.warning("Nenhum município atende aos critérios selecionados.")
    else:
        # Garante que df_filtrado seja uma cópia segura
        df_filtrado = df_filtrado.copy()

        # Define os cortes para destacar os hotspots
        envelhecimento_corte = df_filtrado["Índice de envelhecimento"].quantile(0.75)
        renda_corte = df_filtrado["Renda média 60+"].quantile(0.75)

        # Cria a coluna de destaque
        df_filtrado["Hotspot"] = df_filtrado.apply(
            lambda row: "🔥 Hotspot" if row["Índice de envelhecimento"] >= envelhecimento_corte and row["Renda média 60+"] >= renda_corte else "Outros",
            axis=1
        )

        # Gera o gráfico
        fig2 = px.scatter(
            df_filtrado,
            x="Índice de envelhecimento",
            y="Proporção casais sem filhos",
            size="Renda média 60+",
            color="Hotspot",
            hover_name="Município",
            title="Dispersão entre envelhecimento, estrutura familiar e renda",
            labels={
                "Índice de envelhecimento": "Envelhecimento",
                "Proporção casais sem filhos": "Casais sem filhos",
                "Renda média 60+": "Renda média 60+"
            },
            height=600
        )

        st.plotly_chart(fig2, use_container_width=True)

# 💎 Aba 5: Índice Prateado
elif aba == "Índice Prateado":
    st.subheader("💎 Índice Composto da Economia Prateada")

    st.markdown("### 🧠 O que este índice revela:")
    st.markdown("""
    O Índice Prateado foi criado para sintetizar três dimensões fundamentais da Economia Prateada:

    - **Envelhecimento**: revela a proporção de idosos em relação aos jovens  
    - **Renda média 60+**: indica o poder de consumo da população idosa  
    - **Estrutura familiar**: mostra o grau de autonomia e demanda por serviços personalizados  

    Ao normalizar e combinar esses fatores, o índice permite identificar os municípios com maior potencial estratégico.  
    Essa métrica facilita comparações objetivas e orienta decisões públicas e privadas voltadas à longevidade, inovação social e investimentos.
    """)

    if df_filtrado.empty:
        st.warning("Nenhum município atende aos critérios selecionados.")
    else:
        df_filtrado = df_filtrado.copy()

        # Normaliza os indicadores
        df_filtrado["IE_norm"] = (df_filtrado["Índice de envelhecimento"] - df_filtrado["Índice de envelhecimento"].min()) / (df_filtrado["Índice de envelhecimento"].max() - df_filtrado["Índice de envelhecimento"].min())
        df_filtrado["Renda_norm"] = (df_filtrado["Renda média 60+"] - df_filtrado["Renda média 60+"].min()) / (df_filtrado["Renda média 60+"].max() - df_filtrado["Renda média 60+"].min())
        df_filtrado["Casais_norm"] = (df_filtrado["Proporção casais sem filhos"] - df_filtrado["Proporção casais sem filhos"].min()) / (df_filtrado["Proporção casais sem filhos"].max() - df_filtrado["Proporção casais sem filhos"].min())

        # Índice composto
        df_filtrado["Índice Prateado"] = (df_filtrado["IE_norm"] + df_filtrado["Renda_norm"] + df_filtrado["Casais_norm"]) / 3

        # Top 20 municípios
        top_prateado = df_filtrado.sort_values("Índice Prateado", ascending=False).head(20)

        fig_prateado = px.bar(
            top_prateado,
            x="Município",
            y="Índice Prateado",
            color="Renda média 60+",
            title="Top 20 municípios no Índice Prateado",
            labels={"Índice Prateado": "Índice Composto da Economia Prateada"},
            height=600
        )

        st.plotly_chart(fig_prateado, use_container_width=True)

        st.markdown("### 📊 Detalhamento dos municípios:")
        st.dataframe(top_prateado[[
            "Município", "UF", "Índice Prateado",
            "Índice de envelhecimento", "Renda média 60+", "Proporção casais sem filhos"
        ]])
        
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

# 👩‍💻 Aba 6: Mapa Interativo
elif aba == "Mapa Interativo":
    st.subheader("🗺️ Mapa Interativo da Economia Prateada")

    st.markdown("### 🌍 O que este mapa mostra:")
    st.markdown("""
    Cada bolha representa um município, com tamanho proporcional à renda média da população 60+  
    e cor de acordo com o Índice Prateado — uma métrica composta que sintetiza envelhecimento, renda e estrutura familiar.
    """)

    df_filtrado = df.copy()

    if df_filtrado.empty:
        st.warning("Nenhum município atende aos critérios selecionados.")
    else:
        # Cria o índice prateado se ainda não existir
        if "Índice Prateado" not in df_filtrado.columns:
            df_filtrado["IE_norm"] = (df_filtrado["Índice de envelhecimento"] - df_filtrado["Índice de envelhecimento"].min()) / (df_filtrado["Índice de envelhecimento"].max() - df_filtrado["Índice de envelhecimento"].min())
            df_filtrado["Renda_norm"] = (df_filtrado["Renda média 60+"] - df_filtrado["Renda média 60+"].min()) / (df_filtrado["Renda média 60+"].max() - df_filtrado["Renda média 60+"].min())
            df_filtrado["Casais_norm"] = (df_filtrado["Proporção casais sem filhos"] - df_filtrado["Proporção casais sem filhos"].min()) / (df_filtrado["Proporção casais sem filhos"].max() - df_filtrado["Proporção casais sem filhos"].min())
            df_filtrado["Índice Prateado"] = (df_filtrado["IE_norm"] + df_filtrado["Renda_norm"] + df_filtrado["Casais_norm"]) / 3

        # Gera o mapa
        fig_map = px.scatter_mapbox(
            df_filtrado.dropna(subset=["latitude", "longitude"]),
            lat="latitude",
            lon="longitude",
            size="Renda média 60+",
            color="Índice Prateado",
            hover_name="Município",
            hover_data=["UF", "Índice de envelhecimento", "Renda média 60+", "Proporção casais sem filhos"],
            color_continuous_scale="Viridis",
            size_max=20,
            zoom=3,
            height=600
        )

        fig_map.update_layout(mapbox_style="carto-positron")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        st.plotly_chart(fig_map, use_container_width=True)

# 👩‍💻 Aba 7: Sobre a Autora
elif aba == "Sobre a Autora":
    st.subheader("👩‍💻 Sobre a Autora")

    st.markdown("""
    <div style='font-size: 18px; line-height: 1.6'>
    <strong>Maria Clara Fagundes</strong><br>
    <em>Salvador, Bahia</em><br>
    <em>Engenheira de Dados</em><br><br>
    Apaixonada por transformar dados públicos em soluções estratégicas e acessíveis.<br>
    Atua na interseção entre tecnologia, impacto social e inteligência territorial.<br><br>
    Este projeto foi desenvolvido como parte do desafio<br>
    <strong>"O Impacto do Envelhecimento Populacional no Brasil"</strong>,<br>
    com o objetivo de revelar oportunidades sociais e econômicas ligadas à<br>
    <strong>Economia Prateada</strong>.<br><br>
    📧 <a href="mailto:luzfaghundes@gmail.com">luzfaghundes@gmail.com</a><br>
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
























