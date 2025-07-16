import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

st.set_page_config(layout="wide", page_title="Dashboard Trending News")

def load_stopwords(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}
        return stopwords
    except FileNotFoundError:
        st.warning(f"File stopwords di '{filepath}' tidak ditemukan.")
        return set()

@st.cache_data(ttl=300)
def scrape_artikel_trending_tempo():
    url = 'https://www.tempo.co'
    data_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        trending_header = soup.find('span', string='ARTIKEL TRENDING')
        if trending_header:
            main_container = trending_header.find_parent('div', class_='flex-col')
            if main_container:
                articles = main_container.find_all('figure')
                for article in articles[1:]:
                    figcaption = article.find('figcaption')
                    if figcaption and figcaption.a:
                        title = figcaption.a.get_text(strip=True).replace('Tempo Plus', '').strip()
                        link_url = figcaption.a.get('href', '')
                        full_link = url + link_url if link_url.startswith('/') else link_url
                        data_list.append({'Judul': title, 'Link': full_link})
    except Exception as e:
        print(f"Error di scrape_artikel_trending_tempo: {e}")
    return data_list

# --- SCRAPER UNTUK TEMPO ---

@st.cache_data(ttl=300)
def scrape_topik_trending_tempo():
    url = 'https://www.tempo.co'
    data_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        trending_header = soup.find('div', string=re.compile(r'\s*TOPIK TRENDING\s*'))
        if trending_header:
            topic_list_ul = trending_header.find_next_sibling('ul')
            if topic_list_ul:
                topics = topic_list_ul.find_all('li')
                for topic_item in topics:
                    if topic_item.a:
                        topic_name = topic_item.a.get_text(strip=True)
                        link_url = topic_item.a.get('href', '')
                        full_link = url + link_url if link_url.startswith('/') else link_url
                        data_list.append({'Topik': topic_name, 'Link': full_link})
    except Exception as e:
        print(f"Error di scrape_topik_trending_tempo: {e}")
    return data_list

# --- SCRAPER UNTUK KOMPAS ---
@st.cache_data(ttl=300)
def scrape_kompas_populer():
    url = 'https://indeks.kompas.com/terpopuler'
    data_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        article_container = soup.find('div', class_='articleList -list')
        if article_container:
            articles = article_container.find_all('div', class_='articleItem')
            for article in articles:
                title_element = article.find('h2', class_='articleTitle')
                link_element = article.find('a', class_='article-link')
                category_element = article.find('div', class_='articlePost-subtitle')
                
                title = title_element.get_text(strip=True) if title_element else 'N/A'
                link = link_element.get('href', '') if link_element else 'N/A'
                category = category_element.get_text(strip=True) if category_element else 'N/A'
                data_list.append({'Judul': title, 'Kategori': category, 'Link': link})
    except Exception as e:
        print(f"Error di scrape_kompas_populer: {e}")
    return data_list

# --- TAMPILAN UTAMA DASHBOARD ---
st.title("Trending News Dashboard")

STOPWORDS_ID = load_stopwords('list-of-stopwords.txt')

tab1, tab2 = st.tabs(["Tempo.co", "Kompas.com"])

# --- KONTEN TAB 1: TEMPO.CO ---
with tab1:
    st.header("Trending di Tempo.co")
    
    artikel_tempo = scrape_artikel_trending_tempo()
    topik_tempo = scrape_topik_trending_tempo()

    col1, col2 = st.columns(2)
    col1.metric("Total Artikel Trending", value=len(artikel_tempo))
    col2.metric("Total Topik Trending", value=len(topik_tempo))
    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Word Cloud Judul Artikel")
        if artikel_tempo:
            text = ' '.join(item['Judul'] for item in artikel_tempo)
            wordcloud = WordCloud(width=400, height=200, background_color='white', stopwords=STOPWORDS_ID).generate(text)
            st.image(wordcloud.to_array())
        else:
            st.warning("Tidak ada data artikel.")
    with col4:
        st.subheader("Word Cloud Topik Trending")
        if topik_tempo:
            text = ' '.join(item['Topik'].replace('#', '') for item in topik_tempo)
            wordcloud = WordCloud(width=400, height=200, background_color='white', stopwords=STOPWORDS_ID).generate(text)
            st.image(wordcloud.to_array())
        else:
            st.warning("Tidak ada data topik.")
    
    st.markdown("---")
    st.subheader("Data Lengkap")
    st.dataframe(pd.DataFrame(artikel_tempo))
    st.dataframe(pd.DataFrame(topik_tempo))

# --- KONTEN TAB 2: KOMPAS.COM ---
with tab2:
    st.header("Berita Terpopuler di Kompas.com")
    
    berita_kompas = scrape_kompas_populer()

    st.metric("Total Berita Populer Ditemukan", value=len(berita_kompas))
    st.markdown("---")
    
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Word Cloud Judul Berita")
        if berita_kompas:
            text = ' '.join(item['Judul'] for item in berita_kompas)
            wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS_ID).generate(text)
            st.image(wordcloud.to_array())
        else:
            st.warning("Tidak ada data judul.")
    with col6:
        st.subheader("Word Cloud Kategori Berita")
        if berita_kompas:
            text = ' '.join(item['Kategori'] for item in berita_kompas)
            wordcloud = WordCloud(width=400, height=400, background_color='white').generate(text)
            st.image(wordcloud.to_array())
        else:
            st.warning("Tidak ada data kategori.")
            
    st.markdown("---")
    st.subheader("Data Lengkap")
    st.dataframe(pd.DataFrame(berita_kompas))