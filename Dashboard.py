import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go

st.set_page_config(layout='wide')

# Inicialize o analisador de sentimento do VADER
analyzer = SentimentIntensityAnalyzer()

# Função para calcular as métricas gerais
def get_general_metrics(df):
    total_posts = df.shape[0]
    mean_likes = round(df['Curtidas'].mean(), 2)
    mean_comments = round(df['Qtd_Comentarios'].mean(), 2)
    mean_interactions = round(df['Interacoes'].mean(), 2)
    return total_posts, mean_likes, mean_comments, mean_interactions

# Função para calcular a distribuição de interações
def get_interactions_distribution(df):
    fig_interactions_distribution = px.histogram(df, x='Interacoes', nbins=20, title='Distribuição de Interações')
    fig_interactions_distribution.update_layout(xaxis_title = "Número de Interações")
    fig_interactions_distribution.update_layout(yaxis_title = "Número de Postagens")
    return fig_interactions_distribution

# Função para criar a nuvem de palavras
def create_comment_wordcloud(df):
    comments = ' '.join(comment for comment in df['Comentarios'] if isinstance(comment, str))
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=400).generate(comments)
    return wordcloud

# Função para calcular a distribuição de postagens por tipo de conteúdo
def get_posts_distribution_by_type(df):
    posts_by_type = df['Tipo'].value_counts()
    return posts_by_type

# Função para calcular o engajamento médio por presença de pessoas
def get_engagement_by_person(df):
    person_engagement = df.groupby('Tem_Pessoa')[['Curtidas', 'Qtd_Comentarios']].mean().reset_index()
    person_engagement['Engajamento'] = (person_engagement['Curtidas'] + person_engagement['Qtd_Comentarios']) / 2
    return person_engagement

# Função para calcular a distribuição de postagens por presença de pessoas
def get_posts_distribution_by_person(df):
    posts_by_person = df['Tem_Pessoa'].value_counts()
    return posts_by_person

# Função para calcular as interações médias por tag
def get_interactions_by_tag(df):
    tag_interactions = df.explode('Tags')[['Tags', 'Interacoes']].groupby('Tags')['Interacoes'].mean().reset_index()
    tag_interactions = tag_interactions.sort_values('Interacoes', ascending=False)
    return tag_interactions

# Função para criar a nuvem de tags
def create_tag_wordcloud(df):
    tags = ' '.join(tag for tags in df['Tags'] for tag in tags.split(', '))
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=400).generate(tags)
    return wordcloud

# Função para calcular o engajamento médio por data
def get_engagement_over_time(df):
    df['Data'] = pd.to_datetime(df['Data'])
    engagement_over_time = df.groupby(df['Data'].dt.date)[['Curtidas', 'Qtd_Comentarios']].mean().reset_index()
    engagement_over_time['Engajamento'] = (engagement_over_time['Curtidas'] + engagement_over_time['Qtd_Comentarios']) / 2
    return engagement_over_time

def get_engagement_by_tag(df):
    # Tratamento dos valores de Tags
    df['Tags'] = df['Tags'].fillna('').str.replace('#', '')
    
    # Cálculo do engajamento médio por tag
    tag_engagement = df.groupby('Tags')[['Curtidas', 'Qtd_Comentarios']].mean().reset_index()
    tag_engagement['Engajamento'] = (tag_engagement['Curtidas'] + tag_engagement['Qtd_Comentarios']) / 2
    return tag_engagement.sort_values('Engajamento', ascending=False)

# Função para calcular a distribuição de carrossel
def get_carrossel_distribution(df):
    carrossel_counts = df['Carrossel'].value_counts()
    return carrossel_counts

# Função para calcular o engajamento médio por carrossel
def get_engagement_by_carrossel(df):
    df['Carrossel'] = df['Carrossel'].fillna('não')
    carrossel_engagement = df.groupby('Carrossel')[['Curtidas', 'Qtd_Comentarios']].mean().reset_index()
    carrossel_engagement['Engajamento'] = (carrossel_engagement['Curtidas'] + carrossel_engagement['Qtd_Comentarios']) / 2
    return carrossel_engagement



df = pd.read_excel('dados_instagram.xlsx')
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

# Tratamento dos valores de Tags
df['Tags'] = df['Tags'].fillna('').str.replace('#', '')

st.title("ANALISE DE ENGAJAMENTO DO INSTAGRAM :bar_chart: ")


interacoes_tipo = df.groupby('Tipo')[['Interacoes']].sum().sort_values('Interacoes', ascending=False)

interacoes_mensal = df.set_index('Data').groupby(pd.Grouper(freq='M'))['Interacoes'].sum().reset_index()
interacoes_mensal['Ano'] = interacoes_mensal['Data'].dt.year
interacoes_mensal['Mes'] = interacoes_mensal['Data'].dt.month_name()

fig_interacoes_mensal = px.line(interacoes_mensal,
                               x='Mes',
                               y='Interacoes',
                               markers=True,
                               range_y=(0, interacoes_mensal['Interacoes'].max()),
                               color='Ano',
                               line_dash='Ano',
                               title="Interação mensal")

fig_interacoes_mensal.update_layout(yaxis_title="Interações")
fig_interacoes_mensal.update_layout(xaxis_title="Mês")



# Visualização no StreamLit
aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(['Visão Geral', 'Análise por Tipo de Postagem', 'Análise por Presença de Pessoas', 'Análise por Hashtag', 'Análise por Carrossel', 'Análise Temporal' ])

with aba1:
    coluna1, coluna2, coluna3, coluna4 = st.columns(4)
    # Métricas gerais
    total_posts, mean_likes, mean_comments, mean_interactions = get_general_metrics(df)
    with coluna1:
        st.metric('Total de Postagens', int(total_posts))
    with coluna2:
        st.metric('Média de Curtidas', f"{mean_likes:.2f}")
    with coluna3:
        st.metric('Média de Comentários', f"{mean_comments:.2f}")
    with coluna4:
        st.metric('Média de Interações', f"{mean_interactions:.2f}")

    # Gráfico de distribuição de interações
    fig_interactions_distribution = get_interactions_distribution(df)
    st.plotly_chart(fig_interactions_distribution, use_container_width=True)

    interacoes_tipo_pessoa = df.groupby(['Tipo', 'Tem_Pessoa'])['Interacoes'].sum().unstack(fill_value=0)
    fig_interacoes_tipo_pessoa = px.bar(interacoes_tipo_pessoa, barmode='group', title='Interações por Tipo de Postagem e Presença de Pessoas')
    fig_interacoes_tipo_pessoa.update_layout(yaxis_title='Interações')

    st.plotly_chart(fig_interacoes_tipo_pessoa, use_container_width=True)

    # Nuvem de palavras dos comentários
    comment_wordcloud = create_comment_wordcloud(df)
    
    st.markdown("<h1 style='text-align: center;'>Nuvem de Comentarios</h1>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(comment_wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    st.pyplot(fig)
    
with aba2:
    coluna1, coluna2 = st.columns(2)
    posts_by_type = get_posts_distribution_by_type(df)
    with coluna1:
        # Agrupar por mês/ano e calcular a média de curtidas
        curtidas_por_tipo = df.groupby('Tipo')['Curtidas'].mean().reset_index()
        fig_curtidas_por_tipo = px.bar(curtidas_por_tipo, x='Tipo', y='Curtidas', text_auto=True)
        fig_curtidas_por_tipo.update_layout(title='Curtidas Médias por Tipo de Postagem')
        fig_curtidas_por_tipo.update_layout(yaxis_title="Curtidas Médias")
        st.plotly_chart(fig_curtidas_por_tipo, use_container_width=True)
    with coluna2:
        # Gráfico de barras
        fig_posts_by_type_bar = px.bar(posts_by_type, x=posts_by_type.index, y=posts_by_type, title='Distribuição de Postagens por Tipo de Postagem')
        st.plotly_chart(fig_posts_by_type_bar, use_container_width=True)
    # Gráfico de pizza
    fig_posts_by_type_pie = px.pie(posts_by_type, values=posts_by_type, names=posts_by_type.index, title='Distribuição de Postagens por Tipo de Postagem')
    st.plotly_chart(fig_posts_by_type_pie, use_container_width=True)

    curtidas_mensal = df.groupby(pd.Grouper(key='Data', freq='M'))['Curtidas'].mean().reset_index()
    curtidas_mensal['Ano'] = curtidas_mensal['Data'].dt.year
    curtidas_mensal['Mes'] = curtidas_mensal['Data'].dt.month_name()
    
   


with aba3:
    # Engajamento médio por presença de pessoas
    person_engagement = get_engagement_by_person(df)
    # Distribuição de postagens por presença de pessoas
    posts_by_person = get_posts_distribution_by_person(df)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        fig_engajamento_pessoa = px.bar(person_engagement, x='Tem_Pessoa', y='Engajamento', title='Engajamento Médio por Presença de Pessoas')
        st.plotly_chart(fig_engajamento_pessoa, use_container_width=True)
    with coluna2:
        # Gráfico de barras
        fig_posts_by_person_bar = px.bar(posts_by_person, x=posts_by_person.index, y=posts_by_person, title='Distribuição de Postagens por Presença de Pessoas')
        st.plotly_chart(fig_posts_by_person_bar, use_container_width=True)
    
    # Gráfico de pizza
    fig_posts_by_person_pie = px.pie(posts_by_person, values=posts_by_person, names=posts_by_person.index, title='Distribuição de Postagens por Presença de Pessoas')
    st.plotly_chart(fig_posts_by_person_pie, use_container_width=True)

    # Tabela de engajamento por presença de pessoas
    st.dataframe(person_engagement, use_container_width=True)


with aba4:
    coluna1, coluna2 = st.columns(2)
    tag_engagement = get_engagement_by_tag(df)
    # Interações médias por tag
    tag_interactions = get_interactions_by_tag(df)
    with coluna1:

        # Gráfico de barras
        fig_interactions_by_tag = px.bar(tag_interactions, x='Tags', y='Interacoes', title='Interações Médias por Tag')
        fig_interactions_by_tag.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_interactions_by_tag, use_container_width=True)
     
    with coluna2:
        # Nuvem de tags
        tag_wordcloud = create_tag_wordcloud(df)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(tag_wordcloud, interpolation='bilinear')
        ax.set_axis_off()
        st.pyplot(fig)

    # Tabela de engajamento por tag
    st.dataframe(tag_engagement, use_container_width=True)

with aba5:
    coluna1, coluna2 = st.columns(2)

    with coluna1:
        # Análise da distribuição de carrossel
        carrossel_distribution = get_carrossel_distribution(df)
        fig_carrossel_distribution = px.pie(carrossel_distribution, values=carrossel_distribution, names=carrossel_distribution.index, title='Distribuição de Carrossel')
        st.plotly_chart(fig_carrossel_distribution, use_container_width=True)
    with coluna2:   
        # Análise de engajamento por carrossel
        carrossel_engagement = get_engagement_by_carrossel(df)
        fig_engajamento_carrossel = px.bar(carrossel_engagement, x='Carrossel', y='Engajamento', title='Engajamento Médio por Carrossel')
        st.plotly_chart(fig_engajamento_carrossel, use_container_width=True)

    # Tabela de engajamento por carrossel
    st.dataframe(carrossel_engagement, use_container_width=True)


with aba6:
     # Evolução do engajamento ao longo do tempo
    engagement_over_time = get_engagement_over_time(df)
    
    # Gráfico de linha
    fig_engagement_line = px.line(engagement_over_time, x='Data', y=['Curtidas', 'Qtd_Comentarios', 'Engajamento'], title='Evolução do Engajamento')
    st.plotly_chart(fig_engagement_line, use_container_width=True)

    st.plotly_chart(fig_interacoes_mensal, use_container_width=True)

    fig_curtidas_mensal = px.line(curtidas_mensal, x='Mes', y='Curtidas', markers=True, color='Ano', line_dash='Ano', title="Evolução das Curtidas Médias Mensais")
    fig_curtidas_mensal.update_layout(yaxis_title="Curtidas Médias")
    fig_curtidas_mensal.update_layout(xaxis_title="Mês")
    st.plotly_chart(fig_curtidas_mensal, use_container_width=True)