# trending-news
A simple web scraper to fetch trending news articles, built with Python and BeautifulSoup. <br>
Built with Streamlit to display trending and popular news from various Indonesian media sources in real-time. <br>

# Features
-   **Multi-Source Scraping**: Fetches data from **Tempo.co** (Trending Articles & Topics) and **Kompas.com** (Most Popular News).
-   **Tabbed Interface**: A clean UI with separate tabs for each news source, making navigation easy.
-   **KPI Metrics**: Displays key metrics such as the total number of articles found for each source.
-   **Dynamic Word Clouds**: Visualizes the most frequent words from news titles, topics, and categories.
-   **Custom Stopwords**: Utilizes an external `.txt` file for custom Indonesian stopwords to generate more relevant word clouds.
-   **Interactive Data Tables**: Displays the raw scraped data in sortable tables using Pandas DataFrames.
-   **Efficient Caching**: Uses Streamlit's caching functionality to speed up load times and reduce scraping frequency.

# Stack
-   **Language**: Python 3.13.2
-   **Web Framework**: Streamlit
-   **Web Scraping**:
    -   `Requests` - For making HTTP requests to websites.
    -   `BeautifulSoup4` - For parsing HTML and scraping data.
-   **Data & Visualization**:
    -   `Pandas` - For data manipulation and tabular display.
    -   `Wordcloud` - For generating word cloud visualizations.
    -   `Matplotlib` - As a backend for rendering the word cloud images.

# Running the app
```
streamlit run dashboard.py
```
