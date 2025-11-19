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
   return pd.read_csv("dados_final_com_uf.csv", encoding="utf-8")

df = carregar_dados()
df.columns = df.columns.str.strip()

# Remove coluna redundante
if "nome" in df.columns:
    df.drop(columns=["nome"], inplace=True)

# Formata colunas
df["Município"] = df["Município"].str.strip().str.title()
df["Renda média 60+"] = pd.to_numeric(df["Renda média 60+"], errors="coerce")
df["Índice de envelhecimento"] = pd.to_numeric(df["Índice de envelhecimento"], errors="coerce")
df["Proporção casais sem filhos"] = pd.to_numeric(df["Proporção casais sem filhos"], errors="coerce")

# 🔄 Chama a função e limpa os dados
df = carregar_dados()
df.columns = df.columns.str.strip()
df["Renda média 60+"] = pd.to_numeric(df["Renda média 60+"], errors="coerce")
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

# Logo no topo do sidebar
st.sidebar.image("logo.png.png", use_column_width=True)

# 🎛️ Filtros interativos
st.sidebar.header("🎛️ Filtros")
ufs = sorted(df["UF"].dropna().unique())

uf_selecionada = st.sidebar.selectbox(
    "📍 Filtrar por UF",
    options=["Todas"] + list(ufs),
    key="uf_selecionada"
)

renda_max = df["Renda média 60+"].dropna().max()

if pd.isna(renda_max):
    st.error("❌ Nenhum valor válido encontrado na coluna 'Renda média 60+'. Verifique o CSV.")
else:
    renda_maxima = int(renda_max)
    renda_min = st.sidebar.slider(
        "💰 Renda média mínima (60+)",
        0, renda_maxima, 0,
        key="renda_min"
    )

if st.sidebar.button("🔄 Limpar filtros", key="reset_button"):
    st.session_state["uf_selecionada"] = "Todas"
    st.session_state["renda_min"] = 0

# Aplicar filtros com proteção
df_filtrado = df.copy()

if uf_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["UF"] == uf_selecionada]

if 'renda_min' in locals() and renda_min is not None:
    df_filtrado = df_filtrado[df_filtrado["Renda média 60+"] >= renda_min]

# 🔍 Diagnóstico rápido
if df_filtrado.empty:
    st.warning("⚠️ Nenhum município encontrado com os filtros selecionados.")
    st.stop()

# 🗂️ Menu de navegação
aba = st.sidebar.radio("Escolha uma aba", [
    "📘 Sobre o Projeto", "Indicadores Gerais", "Ranking de Envelhecimento",
    "Hotspots Econômicos", "Índice Prateado", "Oportunidades Emergentes",
    "Sobre a Autora"
])

# 📘 Aba: Sobre o Projeto
if aba == "📘 Sobre o Projeto":
    st.header(" Economia Prateada no Brasil . Contexto e Intenção")

    st.markdown("""
Imagine o Brasil em 2030: mais da metade dos municípios com população majoritariamente idosa, redes de saúde sobrecarregadas, e uma nova geração de consumidores com tempo, renda e autonomia. Esse futuro não é distante — ele já começou.

O projeto **"Economia Prateada no Brasil"** nasce como resposta a essa transformação silenciosa, mas profunda. Com base nos dados do **Censo Demográfico 2022**, o dashboard interativo revela onde o envelhecimento populacional está mais avançado, onde há maior poder de consumo entre os 60+, e onde a estrutura familiar aponta para novas demandas sociais.

Mais do que um painel de dados, este projeto é uma **ferramenta de antecipação estratégica** — para gestores públicos que precisam planejar políticas de saúde, moradia e mobilidade, e para investidores que buscam oportunidades em serviços voltados à longevidade.

---

### O que o projeto revela

Ao cruzar três indicadores-chave — **Índice de Envelhecimento**, **Renda média da população 60+**, e **Proporção de casais sem filhos** — o dashboard constrói uma visão territorial da Economia Prateada:

- **Hotspots consolidados**: Municípios do Sul e Sudeste com alta concentração de idosos com renda e autonomia, prontos para receber investimentos em saúde, lazer, moradia assistida e tecnologia.
- **Oportunidades emergentes**: Cidades do Norte e Nordeste com envelhecimento acelerado e estrutura familiar propícia, onde o mercado ainda está em formação — mas com alto potencial.
- **Índice Prateado**: Uma métrica composta que sintetiza os três fatores e permite comparar municípios de forma objetiva, revelando onde há maior urgência e oportunidade.

---

### Onde isso impacta

Este projeto impacta diretamente três frentes:

#### 1. Gestão Pública
Municípios com alto Índice Prateado exigem políticas específicas: unidades de saúde adaptadas, transporte acessível, moradias inclusivas e redes de apoio comunitário. O dashboard permite que gestores priorizem recursos com base em evidências territoriais.

#### 2. Investimento Privado
Empreendedores podem identificar cidades onde há demanda reprimida por serviços como home care, academias para idosos, turismo sênior, e tecnologia assistiva. O painel aponta onde o mercado já existe — e onde está prestes a surgir.

#### 3. Inovação Social
A mudança na estrutura domiciliar — mais casais sem filhos e idosos vivendo sozinhos — exige novas soluções: redes de vizinhança, plataformas de cuidado, e serviços personalizados. O projeto inspira inovação com base em dados reais.

---

### Conclusão

A Economia Prateada não é apenas uma consequência do envelhecimento — é uma **janela estratégica de transformação social e econômica**. Este projeto transforma dados em decisões, mapas em oportunidades, e estatísticas em histórias de futuro.

Você não está apenas vendo números. Está enxergando o Brasil que está por vir — e decidindo como agir agora.
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
    col3.metric("🏘️ Nº de Municípios com dados disponíveis", f"{len(df_filtrado)}")
    st.caption("Este número representa os municípios que atendem aos filtros selecionados.")
    
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

    st.markdown("""
📖 **Como interpretar o Índice de Envelhecimento:**  
O Índice de Envelhecimento representa a razão entre a população idosa (60+) e a população jovem (0 a 14 anos).  
**Quanto maior o índice, mais envelhecida é a estrutura demográfica do município.**

Esse indicador revela o avanço da transição demográfica e aponta para desafios e oportunidades em áreas como saúde, mobilidade, habitação, lazer e consumo.  
Municípios com alto índice de envelhecimento demandam políticas públicas e soluções de mercado voltadas à longevidade e à inclusão da população idosa.
""")

    if df_filtrado.empty:
        st.warning("Nenhum município atende aos critérios selecionados.")
    else:
        # Top 20 municípios mais envelhecidos
        ranking = df_filtrado.sort_values("Índice de envelhecimento", ascending=False).head(20)

        # Formata os nomes dos municípios
        ranking["Município"] = ranking["Município"].str.title()

        # Arredonda o índice
        ranking["Índice de envelhecimento"] = ranking["Índice de envelhecimento"].round(3)

        # Destaque do município mais envelhecido
        mais_envelhecido = ranking.iloc[0]

        st.markdown("### 📌 Destaque:")
        st.markdown(f"""
- O município mais envelhecido é **{mais_envelhecido['Município']}**, com índice de **{mais_envelhecido['Índice de envelhecimento']:.1f}**  
- Renda média 60+: **R$ {mais_envelhecido['Renda média 60+']:,.0f}**
""")

        # Gráfico
        fig_bar = px.bar(
            ranking,
            x="Município",
            y="Índice de envelhecimento",
            color="Renda média 60+",
            title="Top 20 municípios com maior IE",
            labels={"Índice de envelhecimento": "Índice de Envelhecimento"},
            height=600
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Tabela
        st.markdown("### 📊 Detalhamento dos municípios:")
        st.dataframe(ranking[["Município", "UF", "Índice de envelhecimento"]])
        
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
📖 **Como interpretar o Índice Prateado:**  
O Índice Prateado varia de 0 a 1 e representa o potencial estratégico de um município na Economia Prateada.  
**Quanto mais próximo de 1, melhores são as condições de vida e oportunidades para a população 60+.**

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

        # Formata os nomes dos municípios
        top_prateado["Município"] = top_prateado["Município"].str.title()

        # Remove coluna redundante se existir
        if "nome" in top_prateado.columns:
            top_prateado.drop(columns=["nome"], inplace=True)

        # Arredonda os índices para 3 casas decimais
        top_prateado = top_prateado.round({
            "Índice Prateado": 3,
            "Índice de envelhecimento": 3,
            "Proporção casais sem filhos": 3
        })

        # Gráfico
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

        # Tabela detalhada
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

# 👩‍💻 Aba 6: Sobre a Autora
elif aba == "Sobre a Autora":
    st.subheader("👩‍💻 Sobre a Autora")

    st.markdown("""
    <div style='font-size: 18px; line-height: 1.6'>
    <strong>Maria Clara Fagundes</strong><br>
    <em>Salvador, Bahia</em><br>
    <em>Engenheira de Dados</em><br><br>
    Apaixonada por transformar dados públicos em soluções estratégicas e acessíveis.<br>
    Atua na interseção entre tecnologia, impacto social e inteligência territorial.<br><br>
    Este projeto foi desenvolvido como parte do desafio Conexão desenvolve - Gamificação 2025. Com o tema<br>
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
• <em>Conexão desenvolve - Gamificação </em> • 2025
</div>
""", unsafe_allow_html=True)























































