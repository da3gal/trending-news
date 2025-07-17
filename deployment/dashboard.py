import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Indonesia Trending News Dashboard", page_icon="📰")

def load_stopwords(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}
        return stopwords
    except FileNotFoundError:
        return set()

@st.cache_data(ttl=600)
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

@st.cache_data(ttl=600)
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

@st.cache_data(ttl=600)
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

# --- Tampilan Utama Dashboard ---

# --- SIDEBAR ---
with st.sidebar:
    st.title("**Trending News Dashboard**")
    st.info("Dashboard ini menampilkan berita trending & populer dari berbagai sumber media di Indonesia.")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    wib = timedelta(hours=7)
    last_update_time = (datetime.utcnow() + wib).strftime("%d %B %Y, %H:%M:%S WIB")
    st.write(f"**Update Terakhir:**")
    st.success(f"{last_update_time}")
    
    with st.expander("ℹ️ Tentang Aplikasi"):
        st.write("""
            Aplikasi ini dibuat dengan **Streamlit** dan melakukan web scraping menggunakan **Python**, **Requests**, dan **BeautifulSoup4**. 
            Tujuan dari proyek ini adalah untuk belajar dan mempraktikkan teknik-teknik data scraping dan visualisasi data.
        """)

st.header("Ringkasan Berita Terkini")

STOPWORDS_ID = load_stopwords('list-of-stopwords.txt')

artikel_tempo = scrape_artikel_trending_tempo()
topik_tempo = scrape_topik_trending_tempo()
berita_kompas = scrape_kompas_populer()

tab1, tab2 = st.tabs(["**Tempo.co**", "**Kompas.com**"])

# --- KONTEN UNTUK TAB 1: TEMPO.CO ---
with tab1:
    st.subheader("Analisis Trending di Tempo.co")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Artikel Trending", value=f"{len(artikel_tempo)} Artikel")
    col2.metric("Total Topik Trending", value=f"{len(topik_tempo)} Topik")
    
    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        st.write("#### Word Cloud Judul Artikel")
        if artikel_tempo:
            text = ' '.join(item['Judul'] for item in artikel_tempo)
            wordcloud = WordCloud(width=400, height=200, background_color='#FFFFFF', colormap='viridis', stopwords=STOPWORDS_ID).generate(text)
            st.image(wordcloud.to_array())
        else:
            st.warning("Tidak ada data artikel.")
            
    with col4:
        st.write("#### Word Cloud Topik Trending")
        if topik_tempo:
            text = ' '.join(item['Topik'].replace('#', '') for item in topik_tempo)
            wordcloud = WordCloud(width=400, height=200, background_color='#FFFFFF', colormap='plasma', stopwords=STOPWORDS_ID).generate(text)
            st.image(wordcloud.to_array())
        else:
            st.warning("Tidak ada data topik.")
    
    st.markdown("---")
    
    with st.expander("Lihat Data Lengkap Artikel Trending"):
        st.dataframe(pd.DataFrame(artikel_tempo))
        
    with st.expander("Lihat Data Lengkap Topik Trending"):
        st.dataframe(pd.DataFrame(topik_tempo))

# --- KONTEN UNTUK TAB 2: KOMPAS.COM ---
with tab2:
    st.subheader("Analisis Berita Terpopuler di Kompas.com")
    
    df_kompas = pd.DataFrame(berita_kompas)
    
    total_berita = len(df_kompas)
    kategori_unik = df_kompas['Kategori'].nunique()

    col_k1, col_k2 = st.columns(2)
    col_k1.metric("Total Berita Populer", value=f"{total_berita} Berita")
    col_k2.metric("Jumlah Kategori Berita", value=f"{kategori_unik} Kategori")
    st.markdown("---")

    st.write("#### Top 5 Kategori Berita Terpopuler")
    if not df_kompas.empty:
        category_counts = df_kompas['Kategori'].value_counts().head(5)
        st.bar_chart(category_counts)
    else:
        st.warning("Tidak ada data kategori.")
    
    st.markdown("---")

    st.write("#### Word Cloud Judul Berita")
    if not df_kompas.empty:
        text_judul = ' '.join(df_kompas['Judul'])
        wordcloud_judul = WordCloud(width=800, height=300, background_color='#FFFFFF', colormap='cividis', stopwords=STOPWORDS_ID).generate(text_judul)
        st.image(wordcloud_judul.to_array())
    else:
        st.warning("Tidak ada data judul.")
        
    st.markdown("---")
    
    with st.expander("Lihat Data Lengkap Berita Populer"):
        st.dataframe(df_kompas, use_container_width=True)