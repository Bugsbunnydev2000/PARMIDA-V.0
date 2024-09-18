#Import all  library we need

import streamlit as st # Streamlit for GUI in web

import yfinance as yf # Yfinance for get data and news 

import quandl # Quandl for get data

from fredapi import Fred # FRED for get data

from alpha_vantage.timeseries import TimeSeries #alpha_vantage for get data

from alpha_vantage.foreignexchange import ForeignExchange #alpha_vantage for get data

import pandas as pd # Pandas for show plot

import os # OS for save data

import openai # openai for Model of GPT

import plotly.graph_objects as go # Plotly for show data

import ta # ta for actoin Indicators



# Set the API keys


quandl.ApiConfig.api_key = 'Your-key'
fred = Fred(api_key='Your-key')
alpha_vantage_key = 'Your-key'
openai.api_key = 'Your-key'
OPENAI_API_KEY = "Your-key"

# Show data in pandas
ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')
fx = ForeignExchange(key=alpha_vantage_key, output_format='pandas')

# Streamlit UI


st.title('Stock Market Analyze')
st.sidebar.header('Option/Feature')

stock_name = st.sidebar.text_input("Enter the stock (e.g., AAPL, GOOGL)")

# Options to select which data to Get and Analyze
fetch_stock_prices = st.sidebar.checkbox('Get and Analyze Stock Prices', value=True)
fetch_dividends = st.sidebar.checkbox('Get and Analyze Dividends', value=True)
fetch_fred_data = st.sidebar.checkbox('Get and Analyze FRED Data', value=True)
fetch_alpha_vantage_data = st.sidebar.checkbox('Get and Analyze Alpha Vantage Data', value=True)
fetch_quandl_data = st.sidebar.checkbox('Get and Analyze Quandl Data', value=True)
fetch_news_and_sentiment = st.sidebar.checkbox('Get and Analyze News and Sentiment Analysis', value=True)
fetch_indicators = st.sidebar.checkbox('Get and Analyze Technical Indicators', value=True)

# Error for Enter the stock
if st.sidebar.button('Get and Analyze Data'):
    if not stock_name:
        st.error('Please enter a stock name.')
    else:
        if not os.path.exists(stock_name):
            os.makedirs(stock_name)

#Save data in any Format

        def save_data(data, name):
            try:
                data.to_json(f"{stock_name}/{name}.json")
                st.success(f"{name} data saved as JSON.")
            except Exception as e:
                st.error(f"Failed to save {name} as JSON: {e}")
                try:
                    data.to_csv(f"{stock_name}/{name}.csv")
                    st.warning(f"Saved {name} as CSV instead.")
                except Exception as csv_e:
                    st.error(f"Failed to save {name} as CSV: {csv_e}")

# Save FRED data

        def fetch_and_save_fred_data(series_id, name):
            try:
                series = fred.get_series(series_id)
                series_df = pd.DataFrame(series)
                save_data(series_df, name)
                st.success(f"{name} data saved in folder {stock_name} (FRED).")
            except Exception as e:
                st.error(f"Cannot get data from FRED for {name}: {e}")

# Save alpha_vantage data               

        def fetch_and_save_alpha_vantage_data(fetch_function, name):
            try:
                data, _ = fetch_function
                save_data(data, name)
                st.success(f"{name} data saved in folder {stock_name} (Alpha Vantage).")
            except Exception as e:
                st.error(f"Cannot get data from Alpha Vantage for {name}: {e}")

#News ai and save news of stock 

        def fetch_news_and_analyze_sentiment(ticker):
            try:
                news = yf.Ticker(ticker).news
                news_df = pd.DataFrame(news)
                save_data(news_df, "news")
                st.success(f"News data for {ticker} saved as JSON.")
                st.write("Analyzing sentiment of the news...")

                news_texts = [item['title'] + ". " + item.get('summary', '') for item in news]
                sentiment_results = []

                for text in news_texts:
                    client = openai.Client(api_key=os.getenv(OPENAI_API_KEY))

                    instructions = f"Stock Name: {stock_name}\nAnalyze the sentiment of this news:\n{text}"

                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": instructions},
                            {"role": "user", "content": text}
                        ]
                    )

                    response = completion.choices[0].message.content
                    sentiment = response
                    sentiment_results.append(sentiment)

                sentiment_df = pd.DataFrame({
                    "news": news_texts,
                    "sentiment": sentiment_results
                })

                save_data(sentiment_df, "news_sentiment")
                st.success(f"Sentiment analysis for {ticker} saved as JSON.")
                st.write(sentiment_df)

            except Exception as e:
                st.error(f"Failed to fetch or analyze news for {ticker}: {e}")


#Actoins the indicators


        def fetch_and_display_indicators(ticker):
            try:
                stock_data = yf.download(ticker, period="1y")
                stock_data['SMA_50'] = ta.trend.sma_indicator(stock_data['Close'], window=50) # SMA Indicators
                stock_data['SMA_200'] = ta.trend.sma_indicator(stock_data['Close'], window=200) # SMA Indicators
                stock_data['RSI'] = ta.momentum.RSIIndicator(stock_data['Close']).rsi() # RSI Indicators
                bollinger = ta.volatility.BollingerBands(stock_data['Close']) # bollinger Indicators
                stock_data['BB_High'] = bollinger.bollinger_hband() # Bollinger Indicators
                stock_data['BB_Low'] = bollinger.bollinger_lband() # Bollinger Indicators
                macd = ta.trend.MACD(stock_data['Close']) # MACD indicators
                stock_data['MACD'] = macd.macd() # MACD indicators
                stock_data['MACD_Signal'] = macd.macd_signal() # MACD indicators

                fig = go.Figure()#Show the data

                #Setting of show data

                fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close'))
                fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_50'], mode='lines', name='SMA 50'))
                fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_200'], mode='lines', name='SMA 200'))
                fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['BB_High'], mode='lines', name='Bollinger High'))
                fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['BB_Low'], mode='lines', name='Bollinger Low'))
                fig.update_layout(title=f'Technical Indicators for {ticker}', xaxis_title='Date', yaxis_title='Price')
                 #show data
                st.plotly_chart(fig)
                
                macd_fig = go.Figure()
                macd_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], mode='lines', name='MACD'))
                macd_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD_Signal'], mode='lines', name='MACD Signal'))
                macd_fig.update_layout(title=f'MACD for {ticker}', xaxis_title='Date', yaxis_title='Value')
                

                #Save data
                st.plotly_chart(macd_fig)

                save_data(stock_data, "technical_indicators")

            except Exception as e:
                st.error(f"Failed to fetch or display indicators for {ticker}: {e}")

#Fctors
        fred_series = {
            'DFF': "interest_rate",
            'CPIAUCSL': "inflation_rate",
            'UNRATE': "unemployment_rate",
            'A191RL1Q225SBEA': "gdp_growth",
            'CPIAUCSL': "consumer_price_index",
            'PPIACO': "producer_price_index",
            'HOUST': "housing_starts",
            'PI': "personal_income",
            'BOPGSTB': "trade_balance",
            'TCU': "capacity_utilization",
            'PAYEMS': "nonfarm_payrolls",
            'ICSA': "initial_jobless_claims",
            'RSXFS': "retail_sales",
            'UMCSENT': "consumer_sentiment",
            'NAPM': "manufacturing_pmi",
            'NAPMNON': "services_pmi",
            'CP': "corporate_profits",
            'RETAILIR': "retail_inventories",
            'CBI': "business_inventories"
        }

        quandl_mappings = {
            'FRED/PAYEMS': "nonfarm_payrolls",
            'FRED/ICSA': "initial_jobless_claims",
            'FRED/RSXFS': "retail_sales",
            'UMICH/SOC1': "consumer_sentiment",
            'ISM/MAN_PMI': "manufacturing_pmi",
            'ISM/NONMAN_NMI': "services_pmi",
            'FRED/CP': "corporate_profits",
            'FRED/RETAILIR': "retail_inventories",
            'FRED/CBI': "business_inventories"
        }

        if fetch_stock_prices or fetch_dividends:
            ticker = yf.Ticker(stock_name)
            if fetch_stock_prices:
                stock_prices = ticker.history(period='5y')
                save_data(stock_prices, f"{stock_name}_stock_prices")
            if fetch_dividends:
                dividends = ticker.dividends
                save_data(dividends, f"{stock_name}_dividends")

        if fetch_fred_data:
            for series_id, name in fred_series.items():
                fetch_and_save_fred_data(series_id, name)


        if fetch_alpha_vantage_data:
            fetch_and_save_alpha_vantage_data(fx.get_currency_exchange_rate(from_currency='USD', to_currency='EUR'), "exchange_rate_usd_eur")
            fetch_and_save_alpha_vantage_data(ts.get_daily(symbol='WTI', outputsize='full'), "oil_prices")
            fetch_and_save_alpha_vantage_data(ts.get_daily(symbol='GOLD', outputsize='full'), "gold_prices")

        if fetch_quandl_data:
            for code, name in quandl_mappings.items():
                try:
                    data = quandl.get(code)
                    save_data(data, name)
                    st.success(f"{name} data saved in folder {stock_name} (Quandl).")
                except Exception as e:
                    st.error(f"Cannot get data from Quandl for {name}: {e}")

        if fetch_news_and_sentiment:
            fetch_news_and_analyze_sentiment(stock_name)

        if fetch_indicators:
            fetch_and_display_indicators(stock_name)

        # Analyze all data using OpenAI in smaller chunks
        def analyze_data_in_chunks(data, chunk_size=1000):
            try:
                client = openai.Client(api_key=os.getenv(OPENAI_API_KEY))
                instructions = f"After getting the data, arrange them and make them readable, then analyze the stock according to the data and tell what the future of this stock will be and predict in terms of price and profitability. {stock_name}:\n"

                responses = []
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i + chunk_size]
                    chunk_instructions = instructions + f"Data chunk {i // chunk_size + 1}:\n{chunk}\n\n"

                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": chunk_instructions},
                            {"role": "user", "content": "Accurate prediction of stock prices in the future."}
                        ]
                    )

                    response = completion.choices[0].message.content
                    responses.append(response)

                return responses

            except Exception as e:
                st.error(f"Failed to analyze data with OpenAI: {e}")

        try:
            all_data = ""
            for file in os.listdir(stock_name):
                if file.endswith(".json"):
                    with open(os.path.join(stock_name, file), 'r') as f:
                        data = f.read()
                        all_data += data

            analysis_results = analyze_data_in_chunks(all_data)
            combined_results = "\n".join(analysis_results)
            st.write(combined_results)

        except Exception as e:
            st.error(f"Failed to analyze data with OpenAI: {e}")

        st.write("")
        st.write("")
        st.write("")
        st.write("congratulations ALL OF THE DATA SAVE AND ANALYZE")
        st.write("")
        st.write("")
        st.write("Data has been saved to separate files in the respective directory based on the stock name.")
