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

## Future Features (Coming Soon)
Here are some features planned for future development:
-   **Sentiment Analysis**: Automatically analyze and visualize the sentiment (Positive, Negative, Neutral) of each news headline.
-   **Named Entity Recognition (NER)**: Identify and display the most frequently mentioned people, organizations, and locations in the news.
-   **Automated Article Summarization**: Use a pre-trained language model to generate a concise one-sentence summary for each article.
-   **Source Comparison View**: Add a dedicated view to compare how different news sources cover the same topic, analyzing sentiment and keyword usage side-by-side.
-   **Historical Trend Analysis**: Store daily data to track how a topic's popularity or sentiment changes over time with line charts.
-   **Interactive Filtering & Search**: Add a search bar to find articles containing specific keywords across all news sources, along with a date-range selector to analyze news from a particular period.
-   **Additional News Sources**: Integrate scrapers for other major news portals.

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
