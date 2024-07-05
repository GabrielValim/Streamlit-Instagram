import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt

df = pd.read_excel('dados_instagram.xlsx') 

st.set_page_config(layout="wide")

st.sidebar.title('Análise de Engajamento do Instagram')
abas = ['Visão Geral', 'Análise por Tipo de Publicação', 'Análise de Conteúdo', 'Análise de Presença Humana']
aba_selecionada = st.sidebar.radio('Selecione uma aba', abas)


if aba_selecionada == 'Visão Geral':
    st.header('Visão Geral do Engajamento')

    fig_tipo_publicacao = px.bar(df, x='Data', y='Tipo', color='Tipo', title='Quantidade de Publicações por Tipo ao longo do tempo')
    fig_tipo_publicacao.update_layout(xaxis_tickmode='linear', xaxis_dtick=7)
    st.plotly_chart(fig_tipo_publicacao, use_container_width=True)

    fig_curtidas = px.line(df, x='Data', y='Curtidas', title='Evolução das Curtidas')
    fig_curtidas.update_layout(xaxis_tickmode='linear', xaxis_dtick=7)
    st.plotly_chart(fig_curtidas, use_container_width=True)

    st.markdown("---")

    st.subheader('Proporção de Tipos de Publicação')
    # Agrupa os dados por tipo de publicação e conta a quantidade de cada tipo
    tipo_counts = df['Tipo'].value_counts()

    # Cria o gráfico de barras
    fig_tipos_publicacao = px.bar(
        x=tipo_counts.index,
        y=tipo_counts.values,
        color=tipo_counts.index,
        title='Quantidade de Publicações por Tipo'
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig_tipos_publicacao, use_container_width=True)

    st.markdown("---")

    st.subheader('Indicadores de Engajamento')
    tabela_indicadores = df.describe().T
    tabela_indicadores = tabela_indicadores.rename(columns={'count': 'Total', 'mean': 'Média', 'std': 'Desvio Padrão', 'min': 'Mínimo', '25%': '1º Quartil', '50%': 'Mediana', '75%': '3º Quartil', 'max': 'Máximo'})
    st.dataframe(tabela_indicadores, use_container_width=True)

    st.write("**Total:** Número total de publicações.")
    st.write("**Média:** Valor médio de **curtidas**, **comentários**, **interações**, etc.")
    st.write("**Desvio Padrão:** Medida de dispersão dos dados em relação à média de **curtidas**, **comentários**, **interações**, etc.")
    st.write("**Mínimo:** Menor valor de **curtidas**, **comentários**, **interações**, etc.")
    st.write("**1º Quartil:** Valor que separa os 25% menores valores de **curtidas**, **comentários**, **interações**, etc.")
    st.write("**Mediana:** Valor que separa os 50% menores valores de **curtidas**, **comentários**, **interações**, etc.")
    st.write("**3º Quartil:** Valor que separa os 75% menores valores de **curtidas**, **comentários**, **interações**, etc.")
    st.write("**Máximo:** Maior valor de **curtidas**, **comentários**, **interações**, etc.") 
elif aba_selecionada == 'Análise por Tipo de Publicação':
    st.header('Análise por Tipo de Publicação')
    
    tipo_counts = df['Tipo'].value_counts()
    # Gráfico de Pizza
    fig_proporcao_tipos = px.pie(
        values=tipo_counts.values,
        names=tipo_counts.index,
        title='Proporção de Tipos de Publicação'
    )
    st.plotly_chart(fig_proporcao_tipos, use_container_width=True)

    st.markdown("---")

    # Gráfico de Barras - Curtidas
    fig_media_curtidas = px.bar(
        df,
        x='Tipo',
        y='Curtidas',
        title='Média de Curtidas por Tipo de Publicação',
        color='Tipo',
 # Cores do Instagram
    )
    st.plotly_chart(fig_media_curtidas, use_container_width=True)

    # Gráfico de Barras - Comentários
    fig_media_comentarios = px.bar(
        df,
        x='Tipo',
        y='Qtd_Comentarios',
        title='Média de Comentários por Tipo de Publicação',
        color='Tipo',
 # Cores do Instagram
    )
    st.plotly_chart(fig_media_comentarios, use_container_width=True)

    # Gráfico de Barras - Interações
    fig_media_interacoes = px.bar(
        df,
        x='Tipo',
        y='Interacoes',
        title='Média de Interações por Tipo de Publicação',
        color='Tipo',
 # Cores do Instagram
    )
    st.plotly_chart(fig_media_interacoes, use_container_width=True)
elif aba_selecionada == 'Análise de Conteúdo':
    st.header('Análise de Conteúdo')

    # Junta todas as tags em uma única string
    todas_tags = ' '.join(df['Tags'].astype(str))

    # Cria a nuvem de palavras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(todas_tags)

    # Plota a nuvem de palavras
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    st.subheader('Nuvem de Palavras das Hashtags')
    st.pyplot(plt)

    st.markdown("---")

    # Junta todos os comentários em uma única string
    todos_comentarios = ' '.join(df['Comentarios'].astype(str))

    # Remove as stop words
    stop_words = set(stopwords.words('portuguese'))
    palavras_comentarios = [w for w in word_tokenize(todos_comentarios) if w not in stop_words and w.isalnum()]

    # Conta a frequência de cada palavra
    contagem_palavras = Counter(palavras_comentarios)

    # Seleciona as 20 palavras mais frequentes
    top_palavras = contagem_palavras.most_common(20)

    # Cria um gráfico de barras com as palavras mais frequentes
    palavras, contagem = zip(*top_palavras)
    plt.figure(figsize=(10, 6))
    plt.bar(palavras, contagem)
    plt.xticks(rotation=45) # Rotaciona as labels em 45 graus
    plt.xlabel('Palavras')
    plt.ylabel('Frequência')
    plt.title('Palavras Mais Frequentes nos Comentários')
    plt.tight_layout()

    st.subheader('Palavras Mais Frequentes nos Comentários')
    st.pyplot(plt)
    
    st.markdown("---")

    # Cria um DataFrame com a frequência de cada tag ao longo do tempo
    df_tags = df.explode('Tags').groupby(['Data', 'Tags']).size().reset_index(name='Frequência')

    # Seleciona as 10 tags mais frequentes
    top_tags = df_tags['Tags'].value_counts().index[:10]

    # Filtra o DataFrame para as 10 tags mais frequentes
    df_tags_filtrado = df_tags[df_tags['Tags'].isin(top_tags)]

    # Cria o gráfico de barras agrupado
    fig_frequencia_tags = px.bar(
        df_tags_filtrado,
        x='Data',
        y='Frequência',
        color='Tags',
        title='Frequência de Tags ao Longo do Tempo',
        barmode='group'
    )

    # Adiciona um filtro para selecionar as tags
    tags_selecionadas = st.multiselect('Selecione as tags:', top_tags)

    # Filtra o gráfico de acordo com as tags selecionadas
    if tags_selecionadas:
        fig_frequencia_tags.update_traces(visible=False)
        for tag in tags_selecionadas:
            fig_frequencia_tags.update_traces(visible=True, selector={'name': tag})

    st.subheader('Frequência de Tags ao Longo do Tempo')
    st.plotly_chart(fig_frequencia_tags, use_container_width=True)
    st.write("**Frequência:** Número de vezes que cada tag aparece em todas as publicações ao longo do tempo.")
elif aba_selecionada == 'Análise de Interações':
    pass
elif aba_selecionada == 'Análise de Presença Humana':
    st.header('Análise de Presença Humana')

    # Cria o gráfico de pizza
    fig_tem_pessoa = px.pie(df, names='Tem_Pessoa', title='Proporção de Publicações com e sem Pessoas')
    fig_tem_pessoa.update_traces(textfont_size=16) # Aumenta o tamanho das labels para 16
    st.plotly_chart(fig_tem_pessoa, use_container_width=True)

    st.markdown("---")

    # Cria o gráfico de barras
    fig_engajamento_pessoa = px.bar(
        df,
        x='Tem_Pessoa',
        y=['Curtidas', 'Qtd_Comentarios', 'Interacoes'],
        title='Engajamento Médio por Tipo de Publicação',
        barmode='group',
        color='Tipo' # Define a cor das barras de acordo com o tipo de publicação
    )
    st.plotly_chart(fig_engajamento_pessoa, use_container_width=True)
