import streamlit as st
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import base64

st.set_page_config(page_title="Positive/Negative Sentiment Dashboard", layout="centered")

# Optional: theme switching if desired
def set_theme_by_sentiment(sentiment):
    css = {
        "positive": "#f0f9ff",
        "negative": "#1e1e1e",
        "neutral": "#fdf6e3"
    }
    text_color = "black" if sentiment == "positive" else "white" if sentiment == "negative" else "#333"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {css[sentiment]};
            color: {text_color};
        }}
        </style>
        """, unsafe_allow_html=True
    )

st.title("🧠 Sentiment Analysis Dashboard ")
bearer_token = st.text_input("🔐 Enter your Twitter Bearer Token", type="password")
keyword = st.text_input("🔍 Enter a keyword or company name", "Tesla")

if bearer_token and keyword:
    analyzer = SentimentIntensityAnalyzer()
    twitter_pos, twitter_neg = 0, 0
    news_pos, news_neg = 0, 0
    tweets_data = []
    news_data = []
    pos_text, neg_text = "", ""

    try:
        client = tweepy.Client(bearer_token=bearer_token)
        query = f"{keyword} -is:retweet lang:en"
        with st.spinner("Fetching Tweets..."):
            response = client.search_recent_tweets(query=query, max_results=50, tweet_fields=["created_at", "text"])

        if response.data:
            for tweet in response.data:
                text = tweet.text
                score = analyzer.polarity_scores(text)["compound"]
                if score >= 0.1:
                    twitter_pos += 1
                    tweets_data.append((text, "Positive"))
                    pos_text += " " + text
                elif score <= -0.1:
                    twitter_neg += 1
                    tweets_data.append((text, "Negative"))
                    neg_text += " " + text

    except tweepy.TooManyRequests:
        st.warning("Rate limit reached. Try again in a few minutes.")
    except Exception as e:
        st.error(f"Twitter error: {e}")

    sources = {
        "CNN": f"https://www.google.com/search?q={keyword}+site:cnn.com&tbm=nws",
        "Fox News": f"https://www.google.com/search?q={keyword}+site:foxnews.com&tbm=nws",
        "NBC News": f"https://www.google.com/search?q={keyword}+site:nbcnews.com&tbm=nws",
        "ABC News": f"https://www.google.com/search?q={keyword}+site:abcnews.go.com&tbm=nws",
        "CBS News": f"https://www.google.com/search?q={keyword}+site:cbsnews.com&tbm=nws"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    with st.spinner("Scraping News..."):
        for source, url in sources.items():
            try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.select('a')
                seen_titles = set()

                for link in links:
                    href = link.get('href')
                    if href and "http" in href and "webcache" not in href:
                        clean_url = href.split('&')[0].replace('/url?q=', '')
                        try:
                            article = Article(clean_url)
                            article.download()
                            article.parse()
                            title = article.title.strip().lower()
                            if keyword.lower() not in title or title in seen_titles:
                                continue

                            seen_titles.add(title)
                            full_text = article.text
                            score = analyzer.polarity_scores(full_text)['compound']

                            if score >= 0.1:
                                news_pos += 1
                                news_data.append((article.title, "Positive", clean_url))
                                pos_text += " " + full_text
                            elif score <= -0.1:
                                news_neg += 1
                                news_data.append((article.title, "Negative", clean_url))
                                neg_text += " " + full_text

                            if len(seen_titles) >= 5:
                                break
                        except:
                            continue
            except:
                continue

    # Determine overall tone
    total_pos = twitter_pos + news_pos
    total_neg = twitter_neg + news_neg
    dominant = "positive" if total_pos > total_neg else "negative"
    set_theme_by_sentiment(dominant)

    # Display Summary
    st.markdown(f"""
        ### 📊 Sentiment Summary:
        ✅ Twitter Positive: {twitter_pos} | ❌ Twitter Negative: {twitter_neg}  
        ✅ News Positive: {news_pos} | ❌ News Negative: {news_neg}
    """)

    # Visuals
    labels = ["Twitter Positive", "Twitter Negative", "News Positive", "News Negative"]
    values = [twitter_pos, twitter_neg, news_pos, news_neg]
    colors = ["#4CAF50", "#F44336", "#81C784", "#E57373"]

    st.markdown("### 📈 Sentiment Bar Chart")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(labels, values, color=colors)
    ax.set_ylabel("Count")
    ax.set_title("Positive vs Negative Sentiment")
    ax.tick_params(axis='x', rotation=20)
    st.pyplot(fig)

    st.markdown("### 🥧 Sentiment Pie Chart")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    filtered = [(l, v, c) for l, v, c in zip(labels, values, colors) if v > 0]
    if filtered:
        fl, fv, fc = zip(*filtered)
        ax2.pie(fv, labels=fl, autopct='%1.1f%%', startangle=140, colors=fc,
                explode=[0.05]*len(fv), textprops={'fontsize': 11})
        ax2.axis('equal')
        st.pyplot(fig2)

    # Word Cloud
    st.markdown("### ☁️ Word Cloud (Positive & Negative)")
    wc_text = pos_text + " " + neg_text
    wordcloud = WordCloud(width=900, height=400, background_color='white',
                          stopwords=STOPWORDS).generate(wc_text)
    fig_wc, ax_wc = plt.subplots(figsize=(12, 6))
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis("off")
    st.pyplot(fig_wc)

    # Display Tweets
    st.markdown("### 💬 Tweets by Sentiment")
    for text, sentiment in tweets_data:
        color = "green" if sentiment == "Positive" else "red"
        st.markdown(f"<p style='color:{color}'>{text}</p>", unsafe_allow_html=True)

    # Display News
    st.markdown("### 📰 News Headlines by Sentiment")
    for title, sentiment, url in news_data:
        color = "green" if sentiment == "Positive" else "red"
        st.markdown(f"<a href='{url}' target='_blank' style='color:{color}'>{title}</a>", unsafe_allow_html=True)
