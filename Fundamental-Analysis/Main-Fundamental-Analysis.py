# Import all necessary libraries
import streamlit as st
import yfinance as yf
import quandl
from fredapi import Fred
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import pandas as pd
import os
import openai
import json
from pymongo import MongoClient

# Set the API keys

quandl.ApiConfig.api_key = 'YOUR-KEY'
fred = Fred(api_key='YOUR-KEY')
alpha_vantage_key = 'YOUR-KEY'
openai.api_key = 'YOUR-KEY'

# Initialize Alpha Vantage APIs
ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')
fx = ForeignExchange(key=alpha_vantage_key, output_format='pandas')

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017")

# Streamlit UI
st.title('PARMIDA V.3')
st.sidebar.header('Option/Feature')

stock_name = st.sidebar.text_input("Enter the stock (e.g., AAPL, GOOGL, NVDA, MSTF)")

# Options to select which data to Get and Analyze
fetch_stock_prices = st.sidebar.checkbox('Get and Analyze Stock Prices', value=True)
fetch_dividends = st.sidebar.checkbox('Get and Analyze Dividends', value=True)
fetch_fred_data = st.sidebar.checkbox('Get and Analyze FRED Data', value=True)
fetch_alpha_vantage_data = st.sidebar.checkbox('Get and Analyze Alpha Vantage Data', value=True)
fetch_quandl_data = st.sidebar.checkbox('Get and Analyze Quandl Data', value=True)

# Ensure stock_name directory exists
if st.sidebar.button('Analyze and get data'):
    if not stock_name:
        st.error('Please enter a stock name.')
    else:
        if not os.path.exists(stock_name):
            os.makedirs(stock_name)

#---------------------------------------------------------------------------------------------------------------

        # Function to save data in a clean JSON format and insert into MongoDB
        def save_data(data, name):
            try:
                if isinstance(data, pd.DataFrame):
                    data = data.to_dict(orient='index')
                elif isinstance(data, pd.Series):
                    data = data.to_dict()

                # Convert any Timestamp keys to string
                cleaned_data = {str(k): v for k, v in data.items()}

                # Save JSON file
                with open(f"{stock_name}/{name}.json", 'w') as f:
                    json.dump(cleaned_data, f, indent=4, sort_keys=True)

                # Insert data into MongoDB
                db = client[f"{stock_name}_data"]  # Database name: stockname_data
                collection = db[name]  # Collection name: same as the JSON file name
                collection.insert_one(cleaned_data)

                st.success(f"{name} data saved as JSON and inserted into MongoDB.")
            except Exception as e:
                st.error(f"Failed to save {name} as JSON: {e}")

        # Function to fetch and save FRED data
        def fetch_and_save_fred_data(series_id, name):
            try:
                series = fred.get_series(series_id)
                series_df = pd.DataFrame(series, columns=[name])
                save_data(series_df, name)
                st.success(f"{name} data saved in folder {stock_name} (FRED).")
            except Exception as e:
                st.error(f"Cannot get data from FRED for {name}: {e}")

        # Function to fetch and save Alpha Vantage data
        def fetch_and_save_alpha_vantage_data(fetch_function, name):
            try:
                data, _ = fetch_function
                save_data(data, name)
                st.success(f"{name} data saved in folder {stock_name} (Alpha Vantage).")
            except Exception as e:
                st.error(f"Cannot get data from Alpha Vantage for {name}: {e}")

        # FRED series to fetch
        fred_series = {
            'DFF': "interest_rate",
            'CPIAUCSL': "inflation_rate",
            'UNRATE': "unemployment_rate",
            'A191RL1Q225SBEA': "gdp_growth",
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

        # Fetch and save stock prices and dividends from YFinance
        if fetch_stock_prices or fetch_dividends:
            ticker = yf.Ticker(stock_name)
            if fetch_stock_prices:
                stock_prices = ticker.history(period="max")
                save_data(stock_prices, f"{stock_name}_stock_prices")
            if fetch_dividends:
                dividends = ticker.dividends
                save_data(dividends, f"{stock_name}_dividends")

        # Fetch and save FRED data
        if fetch_fred_data:
            for series_id, name in fred_series.items():
                fetch_and_save_fred_data(series_id, name)

        # Fetch and save Alpha Vantage data
        if fetch_alpha_vantage_data:
            fetch_and_save_alpha_vantage_data(fx.get_currency_exchange_rate(from_currency='USD', to_currency='EUR'), "exchange_rate_usd_eur")
            fetch_and_save_alpha_vantage_data(ts.get_daily(symbol='WTI', outputsize='full'), "oil_prices")
            fetch_and_save_alpha_vantage_data(ts.get_daily(symbol='GOLD', outputsize='full'), "gold_prices")

        # Fetch and save Quandl data
        if fetch_quandl_data:
            for code, name in quandl_mappings.items():
                try:
                    data = quandl.get(code)
                    save_data(data, name)
                    st.success(f"{name} data saved in folder {stock_name} (Quandl).")
                except Exception as e:
                    st.error(f"Cannot get data from Quandl for {name}: {e}")

#-----------------------------------------------------------------------------------------------

        # Analyze all data using OpenAI in smaller chunks
        def analyze_data_in_chunks(data, chunk_size=1000):
            try:
                instructions = f"Please analyze the following financial data for {stock_name}. Provide detailed analysis, identify key trends, patterns, and factors affecting the stock. Provide a forecast for future stock price and profitability:\n"
                responses = []
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i + chunk_size]
                    chunk_instructions = instructions + f"Data chunk {i // chunk_size + 1}:\n{chunk}\n\n"
                    completion = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": chunk_instructions},
                            {"role": "user", "content": "Provide a concise and precise analysis and forecast."}
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
            
            # Save the analysis results to a txt file
            with open(f"{stock_name}/analysis_results.txt", 'w') as result_file:
                result_file.write(combined_results)
            
            st.write(combined_results)

        except Exception as e:
            st.error(f"Failed to analyze data with OpenAI: {e}")

        st.write("Congratulations! ALL OF THE DATA SAVE AND ANALYZE")
        st.write("Data has been saved to separate files in the respective directory based on the stock name.")
