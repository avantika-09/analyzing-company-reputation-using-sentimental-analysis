
 Analyzing Company Reputation Using Sentiment Analysis

This project analyzes public sentiment about companies by collecting and classifying real-time tweets and news articles. The sentiment data is visualized through an interactive dashboard built using Streamlit.

 Project Purpose and Functionality

The main goal of this project is to provide a real-time understanding of public opinion on companies or keywords by combining data from Twitter and major news websites. It uses machine learning to classify sentiment as Positive or Negative and offers an engaging UI via Streamlit. Users input a keyword, and the application fetches tweets and news articles, performs sentiment analysis using a Logistic Regression model trained on the Sentiment140 dataset, and visualizes results with bar charts, pie charts, word clouds, and color-coded sentiment text.

 Setup Instructions

1. Unzip the provided project folder and navigate to it:
   cd Sentiment_analysis_final.py

2. Install required dependencies:
   pip install -r requirements.txt

   Key libraries:
   - streamlit
   - tweepy
   - newspaper3k
   - nltk
   - scikit-learn
   - pandas
   - matplotlib
   - wordcloud
   - beautifulsoup4
   - requests

3. Download required NLTK data:
   python3
   >>> import nltk
   >>> nltk.download('stopwords')
   >>> nltk.download('wordnet')
   >>> nltk.download('omw-1.4')

4. Run the application:
   streamlit run Sentiment_analysis_final.py

 Reproducing Results

To reproduce results:
- Enter your Twitter Bearer Token in the app when prompted.
- Input a keyword (e.g., "Tesla").
- The app will fetch and analyze tweets and news headlines.
- Sentiment summary, bar/pie charts, word cloud, and colored sentiment-labeled content will be displayed in the dashboard.

Note: Ensure you have a valid Twitter Developer account and set the Bearer Token properly to access Twitter data.
