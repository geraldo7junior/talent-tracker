import pandas as pd
import streamlit as st
import re

# Função para carregar e limpar os dados
@st.cache_data
def load_and_clean_data(file):
    xls = pd.ExcelFile(file)
    df = pd.read_excel(xls, sheet_name='Sheet1')

    # Função para limpar e simplificar os nomes das colunas
    def clean_column_name(col_name):
        # Remover caracteres especiais e espaços duplos
        col_name = re.sub(r'[^\w\s]', '', col_name)  # Remove pontuação
        col_name = re.sub(r'\s+', '_', col_name.strip())  # Substitui espaços por underscores
        return col_name.lower()  # Converte para minúsculas
    
    # Limpar os nomes das colunas
    cleaned_columns = [clean_column_name(col) for col in df.columns]
    
    # Verificar se há colunas duplicadas e renomear adicionando sufixos
    def resolve_duplicate_columns(columns):
        seen = {}
        result = []
        for col in columns:
            if col in seen:
                seen[col] += 1
                result.append(f"{col}_{seen[col]}")
            else:
                seen[col] = 0
                result.append(col)
        return result

    # Resolver colunas duplicadas
    df.columns = resolve_duplicate_columns(cleaned_columns)
    
    return df

# Função para gerar o Top 10
def generate_top_10(df, column, title):
    # Filtrar as respostas da coluna, dividindo as respostas múltiplas por ";"
    top_10 = df[column].dropna().str.split(";").explode().str.strip().value_counts()

    # Remover valores nulos ou vazios
    top_10 = top_10[top_10.index != '']

    # Garantir que sejam exibidos 10 resultados
    top_10 = top_10.head(10)
    
    # Gerar o gráfico com st.bar_chart() para exibir o Top 10
    st.subheader(f"Top 10 {title}")
    st.bar_chart(top_10)

    # Exibir a tabela ao lado do gráfico com a segunda coluna como "Tipo"
    st.subheader(f"📊 Tabela do Top 10 - {title}")
    st.table(top_10.reset_index().rename(columns={'index': 'Skill', top_10.name: 'Tipo'}))

# Função principal do aplicativo Streamlit
def main():
    # Título principal com emoticon
    st.title("📊 Dashboard - Talent Tracker")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader("Envie o arquivo Excel", type=["xlsx"])
    
    if uploaded_file is not None:
        # Carregar e limpar os dados
        df = load_and_clean_data(uploaded_file)

        # Barra lateral (sidebar) para os filtros
        st.sidebar.header("Filtros 📂")
        
        # Adicionar filtro por "qual_seu_enquadramentocargo"
        if 'qual_seu_enquadramentocargo' in df.columns:
            enquadramento_options = df['qual_seu_enquadramentocargo'].unique()
            selected_enquadramentos = st.sidebar.multiselect('Selecione um ou mais Enquadramentos/Cargos', options=enquadramento_options)

            # Filtrar o DataFrame com base nos enquadramentos/cargos selecionados
            if selected_enquadramentos:
                df = df[df['qual_seu_enquadramentocargo'].isin(selected_enquadramentos)]
        
        # Adicionar filtro por "qual_a_sua_vertical"
        if 'qual_a_sua_vertical' in df.columns:
            vertical_options = df['qual_a_sua_vertical'].unique()
            selected_verticals = st.sidebar.multiselect('Selecione uma ou mais Verticais', options=vertical_options)

            # Filtrar o DataFrame com base nas verticais selecionadas
            if selected_verticals:
                df = df[df['qual_a_sua_vertical'].isin(selected_verticals)]

        # Seção 1: Soft Skills
        st.header("🎯 Análise de Soft Skills")
        st.markdown("Nesta seção, você encontrará as habilidades interpessoais mais escolhidas pelos profissionais.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_soft_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam", "Soft Skills")

        # Separação visual para Hard Skills
        st.markdown("---")  # Linha horizontal para separar seções

        # Seção 2: Hard Skills
        st.header("🔍 Análise de Hard Skills Pesquisa e Inovação")
        st.markdown("Aqui estão as habilidades técnicas mais escolhidas.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam", "Hard Skills")

        # Separação visual para Hard Skills
        st.markdown("---")  # Linha horizontal para separar seções

        # Seção 3: Hard Skills Sistemas
        st.header("🤖 Análise de Hard Skills Sistemas Autônomos")
        st.markdown("Aqui estão as habilidades técnicas mais escolhidas.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam_1", "Hard Skills")

        # Separação visual para Hard Skills
        st.markdown("---")  # Linha horizontal para separar seções

        # Seção 2: Hard Skills
        st.header("💻 Análise de Hard Skills Data Science")
        st.markdown("Aqui estão as habilidades técnicas mais escolhidas.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam2", "Hard Skills")

        # Separação visual para Hard Skills
        st.markdown("---")  # Linha horizontal para separar seções

        # Seção 2: Hard Skills
        st.header("🗺️ Análise de Hard Skills Geoespacial")
        st.markdown("Aqui estão as habilidades técnicas mais escolhidas.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam3", "Hard Skills")

if __name__ == "__main__":
    main()
