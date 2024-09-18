import streamlit as st
import yfinance as yf
from newsapi import NewsApiClient
import openai
import os
from datetime import datetime
import pandas as pd

# Set the API keys
newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')
openai.api_key = 'YOUR_OPENAI_API_KEY'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

# Streamlit UI
st.title('Sentiment Analysis of News')
st.sidebar.header('Options')

stock_name = st.sidebar.text_input("Enter the stock (e.g., AAPL, GOOGL, NVDA, MSFT)")
news_start_date = st.sidebar.text_input("Enter the start date for news (e.g., 2022-01-01)")
news_end_date = st.sidebar.text_input("Enter the end date for news (e.g., 2022-01-31)")

# Options to select which data to Get and Analyze
fetch_news = st.sidebar.checkbox('Fetch and Analyze News', value=True)

if st.sidebar.button('Fetch News and Analyze'):
    if not stock_name:
        st.error('Please enter a stock name.')
    elif not news_start_date or not news_end_date:
        st.error('Please enter the news start and end dates.')
    else:
        if not os.path.exists(stock_name):
            os.makedirs(stock_name)

        try:
            # Fetch news articles
            news = newsapi.get_everything(q=stock_name,
                                          from_param=news_start_date,
                                          to=news_end_date,
                                          language='en',
                                          sort_by='relevancy')
            articles = news['articles']

            if articles:
                # Save articles to a JSON file
                articles_df = pd.DataFrame(articles)
                articles_df.to_json(f"{stock_name}/news_articles.json")
                st.success('News articles saved.')

                # Analyze sentiment of news articles using OpenAI
                def analyze_sentiment(articles):
                    sentiments = []
                    for article in articles:
                        content = article['content']
                        if content:
                            prompt = f"Analyze the sentiment of the following news article content: {content}"
                            response = openai.Completion.create(
                                model="text-davinci-003",
                                prompt=prompt,
                                max_tokens=50
                            )
                            sentiment = response.choices[0].text.strip()
                            sentiments.append(sentiment)
                    return sentiments

                sentiments = analyze_sentiment(articles)
                articles_df['sentiment'] = sentiments
                articles_df.to_json(f"{stock_name}/news_articles_with_sentiment.json")
                st.success('Sentiment analysis completed and saved.')

                st.write(articles_df)

            else:
                st.warning('No news articles found for the given dates and stock.')

        except Exception as e:
            st.error(f"Failed to fetch news or analyze sentiment: {e}")

        st.write("")
        st.write("")
        st.write("Congratulations! All of the data has been fetched and analyzed.")
