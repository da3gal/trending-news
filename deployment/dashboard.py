import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

st.set_page_config(layout="wide", page_title="Dashboard Trending News")

def load_stopwords(filepath):
    """Membaca file .txt dan mengembalikan isinya sebagai sebuah set."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}
        return stopwords
    except FileNotFoundError:
        st.warning(f"File stopwords di '{filepath}' tidak ditemukan. Word cloud akan dibuat tanpa filter stopwords.")
        return set()

STOPWORDS_ID = load_stopwords('list-of-stopwords.txt')


@st.cache_data(ttl=300)
def scrape_artikel_trending():
    """Mengambil data Artikel Trending dari Tempo.co menggunakan BeautifulSoup."""
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
        print(f"Error di scrape_artikel_trending: {e}")
    return data_list

@st.cache_data(ttl=300)
def scrape_topik_trending():
    """Mengambil data Topik Trending dari Tempo.co menggunakan BeautifulSoup."""
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
        print(f"Error di scrape_topik_trending: {e}")
    return data_list

# --- Tampilan Utama Dashboard ---
st.title("Dashboard Trending News")
st.markdown("Sumber data: **Tempo.co**")

artikel_data = scrape_artikel_trending()
topik_data = scrape_topik_trending()

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Artikel Trending Ditemukan", value=len(artikel_data))
with col2:
    st.metric("Total Topik Trending Ditemukan", value=len(topik_data))

st.markdown("---")
st.header("Word Clouds")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Dari Judul Artikel")
    if artikel_data:
        text_artikel = ' '.join(item['Judul'] for item in artikel_data)
        wordcloud = WordCloud(width=400, height=200, background_color='white', stopwords=STOPWORDS_ID).generate(text_artikel)
        st.image(wordcloud.to_array())
    else:
        st.warning("Tidak ada data artikel untuk dibuatkan Word Cloud.")

with col4:
    st.subheader("Dari Topik Trending")
    if topik_data:
        text_topik = ' '.join(item['Topik'].replace('#', '') for item in topik_data)
        wordcloud = WordCloud(width=400, height=200, background_color='white', stopwords=STOPWORDS_ID).generate(text_topik)
        st.image(wordcloud.to_array())
    else:
        st.warning("Tidak ada data topik untuk dibuatkan Word Cloud.")

st.markdown("---")
st.header("Data Lengkap")
if artikel_data:
    st.subheader("Daftar Artikel Trending")
    df_artikel = pd.DataFrame(artikel_data)
    st.dataframe(df_artikel, use_container_width=True)
else:
    st.error("Gagal mengambil data Artikel Trending.")

if topik_data:
    st.subheader("Daftar Topik Trending")
    df_topik = pd.DataFrame(topik_data)
    st.dataframe(df_topik, use_container_width=True)
else:
    st.error("Gagal mengambil data Topik Trending.")

st.info("Catatan: Jika data tidak muncul, itu disebabkan oleh konten dinamis pada situs sumber yang tidak dapat dijangkau oleh BeautifulSoup.")