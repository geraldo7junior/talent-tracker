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

    # Exibir a tabela com o índice oculto e a primeira coluna como 'Skills'
    top_10_df = top_10.reset_index()
    top_10_df.columns = ['Skills', 'Contagem']  # Renomeando as colunas
    st.subheader(f"📊 Tabela do Top 10 - {title}")
    st.table(top_10_df)  # Mostrando a tabela sem o índice

# Função para gerar insights
def generate_insights(df):
    st.header("⭐ Principais Insights")

    # Função auxiliar para extrair o Top 5 de uma coluna, sem valores nulos
    def get_top_3(df, column):
        top_3 = df[column].dropna().str.split(";").explode().str.strip().value_counts()
        top_3 = top_3[top_3.index != '']
        top_3_df = top_3.nlargest(5).reset_index(drop=False)
        top_3_df.columns = ['Skills', 'Contagem']
        return top_3_df

    def get_bottom_3(df, column):
        bottom_3 = df[column].dropna().str.split(";").explode().str.strip().value_counts()
        # Remover valores nulos ou vazios
        bottom_3 = bottom_3[bottom_3.index != '']
        # Transformar em DataFrame, resetar o índice e renomear as colunas
        bottom_3_df = bottom_3.nsmallest(5).reset_index(drop=False)  # Converte para DataFrame e mantém a coluna de valores
    
        # Renomear as colunas para 'Skills' e 'Contagem'
        bottom_3_df.columns = ['Skills', 'Contagem']
        return bottom_3_df

    # Função para filtrar por cargo
    def filter_by_job(df, job_title, column):
        df_filtered = df[df['qual_seu_enquadramentocargo'] == job_title]
        return get_top_3(df_filtered, column)

    # Função para filtrar por vertical
    def filter_by_vertical(df, vertical_name, column):
        df_filtered = df[df['qual_a_sua_vertical'] == vertical_name]
        return get_top_3(df_filtered, column)

    sections = [
        ("Soft Skills", "agora_que_você_já_conhece_algumas_das_soft_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam"),
        ("Hard Skills Pesquisa e Inovação", "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam"),
        ("Hard Skills Sistemas Autônomos", "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam_1"),
        ("Hard Skills Data Science", "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam2"),
        ("Hard Skills Geoespacial", "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam3")
    ]

    for section_name, column in sections:
        st.subheader(f"🔍 {section_name}")
        # Exibir os Top 5 skills mais escolhidas e menos escolhidas lado a lado
        col1, col2 = st.columns(2)  # Divide em duas colunas

        with col1:
            st.write("**Top 5 skills mais escolhidas**:")
            st.write(get_top_3(df, column))

        with col2:
            st.write("**Top 5 skills menos escolhidas**:")
            st.write(get_bottom_3(df, column))


        # Exibir os Top 5 por cargos (Pesquisador Industrial I, II, Estagiário) lado a lado
        col1, col2, col3 = st.columns(3)  # Divide em três colunas

        with col1:
            st.write("**Top 5 para Pesquisador I:**")
            st.write(filter_by_job(df, 'Pesquisador Industrial I', column))

        with col2:
            st.write("**Top 5 para Pesquisador II:**")
            st.write(filter_by_job(df, 'Pesquisador Industrial II', column))

        with col3:
            st.write("**Top 5 para Estagiário:**")
            st.write(filter_by_job(df, 'Estagiário', column))


        # Exibir os Top 5 para as verticais (Ciência de Dados, Geoespacial) na primeira linha
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Top 5 para a vertical Ciência de Dados:**")
            st.write(filter_by_vertical(df, 'Ciência de Dados', column))

        with col2:
            st.write("**Top 5 para a vertical Geoespacial:**")
            st.write(filter_by_vertical(df, 'Geoespacial', column))

        # Exibir os Top 5 para as verticais (Engenharia de Sistemas, Sistemas Autônomos) na segunda linha
        col3, col4 = st.columns(2)

        with col3:
            st.write("**Top 5 para a vertical Engenharia de Sistemas:**")
            st.write(filter_by_vertical(df, 'Engenharia de Sistemas', column))

        with col4:
            st.write("**Top 5 para a vertical Sistemas Autônomos:**")
            st.write(filter_by_vertical(df, 'Sistemas Autônomos', column))

        # Adicionando os comentários estáticos após a seção de insights
        if section_name == "Soft Skills":
            st.markdown("""
            - Percebe-se que as Soft Skills mais críticas para os respondentes são voltadas para cenários de P&D e análise científica;
            - Softskills como: Capacidade de assumir riscos e Engajamento, não tiveram votos;
            - Estagiários consideram a principal soft skill sendo a de colaboração, pesquisadores I a de comunicação científica, e os pesquisadores II consideram ensino e mentoria;
            - Dentro das verticais, percebe-se um entendimento comum de priorizar soft skills voltadas para cenários de P&D e análise científica.
            """)

        elif section_name == "Hard Skills Pesquisa e Inovação":
            st.markdown("""
            - As principais hard skills de pesquisa e inovação vão na linha de resolução de problemas, tomadas de decisão e documentação clara;
            - As hard skills menos escolhidas são voltadas para cenários de codificação, como code review, QA e controle de versão;
            - Dentro das verticais, a de ciência de dados se diferencia, apontando como principal hard skill a modelagem de dados.
            """)

        elif section_name == "Hard Skills Sistemas Autônomos":
            st.markdown("""
            - Agentes cognitivos e deep learning são as principais skills;
            - Skills voltadas para embarcados e hardwares não receberam nenhum voto, apesar de terem sido mencionadas como essenciais.
            """)

        elif section_name == "Hard Skills Data Science":
            st.markdown("""
            - Implementação de machine learning, Python e análise de dados são as principais skills;
            - Skills como engenharia de dados e data governance não receberam nenhum voto.
            """)

        elif section_name == "Hard Skills Geoespacial":
            st.markdown("""
            - Análise de imagens multiespectrais, análise espacial e monitoramento de áreas são as skills principais;
            - Construção de UAS e eVTOL customizados não recebeu nenhum voto.
            """)


# Função principal do aplicativo Streamlit
def main():
    # Título principal com emoticon
    st.title("📊 Dashboard - Talent Tracker")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader("Envie o arquivo Excel", type=["xlsx"])
    
    if uploaded_file is not None:
        # Carregar e limpar os dados
        df = load_and_clean_data(uploaded_file)

        # Geração de insights
        generate_insights(df)

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
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam", "Hard Skills Pesquisa e Inovação")

        # Separação visual para Hard Skills
        st.markdown("---")  # Linha horizontal para separar seções

        # Seção 3: Hard Skills Sistemas Autônomos
        st.header("🤖 Análise de Hard Skills Sistemas Autônomos")
        st.markdown("Aqui estão as habilidades técnicas mais escolhidas.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam_1", "Hard Skills Sistemas Autônomos")

        # Separação visual para Hard Skills
        st.markdown("---")  # Linha horizontal para separar seções

        # Seção 4: Hard Skills Data Science
        st.header("💻 Análise de Hard Skills Data Science")
        st.markdown("Aqui estão as habilidades técnicas mais escolhidas.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam2", "Hard Skills Data Science")

        # Separação visual para Hard Skills
        st.markdown("---")  # Linha horizontal para separar seções

        # Seção 5: Hard Skills Geoespacial
        st.header("🗺️ Análise de Hard Skills Geoespacial")
        st.markdown("Aqui estão as habilidades técnicas mais escolhidas.")
        generate_top_10(df, "agora_que_você_já_conhece_algumas_das_hard_skills_se_você_tivesse_que_escolher_apenas_5_das_descritas_acima_quais_seriam3", "Hard Skills Geoespacial")

if __name__ == "__main__":
    main()

