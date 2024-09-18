#library

import streamlit as st
import yfinance as yf
import quandl
from fredapi import Fred
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import os
import openai
import matplotlib.pyplot as plt
import ta
from ta.volatility import BollingerBands
from ta.trend import EMAIndicator, SMAIndicator, ADXIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volume import OnBalanceVolumeIndicator, ChaikinMoneyFlowIndicator
from ta.trend import PSARIndicator, IchimokuIndicator
import numpy as np

# Set the API keys
quandl.ApiConfig.api_key = 'YOUR-KEY'
fred = Fred(api_key='YOUR-KEY')
alpha_vantage_key = 'YOUR-KEY'
openai.api_key = 'YOUR-KEY'
OPENAI_API_KEY = "YOUR-KEY"

# Function to calculate CCI
def calculate_cci(df, n=20):
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['sma'] = df['TP'].rolling(n).mean()
    df['mad'] = df['TP'].rolling(n).apply(lambda x: pd.Series(x).mad())
    df['CCI'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])
    return df['CCI']

# Streamlit UI
st.title('Technical Analysis')
st.sidebar.header('Options')

stock_name = st.sidebar.text_input("Enter the stock (e.g., AAPL, GOOGL, NVDA, MSFT)")

# Options to select which data to Get and Analyze
fetch_ohlc = st.sidebar.checkbox('Get OHLC Data', value=True)
fetch_trend_indicators = st.sidebar.checkbox('Get Trend Indicators', value=True)
fetch_oscillators = st.sidebar.checkbox('Get Oscillators', value=True)
fetch_bands = st.sidebar.checkbox('Get Bands', value=True)
fetch_patterns = st.sidebar.checkbox('Get Patterns', value=True)
fetch_volume_indicators = st.sidebar.checkbox('Get Volume Indicators', value=True)
fetch_support_resistance = st.sidebar.checkbox('Get Support and Resistance Levels', value=True)
fetch_other_indicators = st.sidebar.checkbox('Get Other Indicators', value=True)

if st.sidebar.button('Analyze and get data'):
    if not stock_name:
        st.error('Please enter a stock name.')
    else:
        if not os.path.exists(stock_name):
            os.makedirs(stock_name)

        # Fetch OHLC data
        if fetch_ohlc:
            ticker = yf.Ticker(stock_name)
            ohlc_data = ticker.history(start="2020-01-01", end="2024-07-23")
            ohlc_data.to_csv(f"{stock_name}/ohlc_data.csv")
            st.success('OHLC data saved.')
            st.write("OHLC Data")
            st.line_chart(ohlc_data[['Open', 'High', 'Low', 'Close']])

        ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')
        ti = TechIndicators(key=alpha_vantage_key, output_format='pandas')

        # Fetch Trend Indicators
        if fetch_trend_indicators:
            sma_data, _ = ti.get_sma(symbol=stock_name, interval='daily', time_period=20)
            sma_data.to_csv(f"{stock_name}/sma_data.csv")
            st.success('SMA data saved.')
            st.write("SMA Data")
            st.line_chart(sma_data)

            ema_data, _ = ti.get_ema(symbol=stock_name, interval='daily', time_period=20)
            ema_data.to_csv(f"{stock_name}/ema_data.csv")
            st.success('EMA data saved.')
            st.write("EMA Data")
            st.line_chart(ema_data)

            macd_data, _ = ti.get_macd(symbol=stock_name, interval='daily')
            macd_data.to_csv(f"{stock_name}/macd_data.csv")
            st.success('MACD data saved.')
            st.write("MACD Data")
            st.line_chart(macd_data)

            adx_data, _ = ti.get_adx(symbol=stock_name, interval='daily', time_period=14)
            adx_data.to_csv(f"{stock_name}/adx_data.csv")
            st.success('ADX data saved.')
            st.write("ADX Data")
            st.line_chart(adx_data)

        # Fetch Oscillators
        if fetch_oscillators:
            rsi_data, _ = ti.get_rsi(symbol=stock_name, interval='daily', time_period=14)
            rsi_data.to_csv(f"{stock_name}/rsi_data.csv")
            st.success('RSI data saved.')
            st.write("RSI Data")
            st.line_chart(rsi_data)

            stochastic_data, _ = ti.get_stoch(symbol=stock_name, interval='daily')
            stochastic_data.to_csv(f"{stock_name}/stochastic_data.csv")
            st.success('Stochastic data saved.')
            st.write("Stochastic Data")
            st.line_chart(stochastic_data)

            # Calculate and save CCI manually
            cci_data = calculate_cci(ohlc_data)
            cci_data.to_csv(f"{stock_name}/cci_data.csv")
            st.success('CCI data saved.')
            st.write("CCI Data")
            st.line_chart(cci_data)

            atr_data, _ = ti.get_atr(symbol=stock_name, interval='daily', time_period=14)
            atr_data.to_csv(f"{stock_name}/atr_data.csv")
            st.success('ATR data saved.')
            st.write("ATR Data")
            st.line_chart(atr_data)

        # Fetch Bands
        if fetch_bands:
            bollinger_data, _ = ti.get_bbands(symbol=stock_name, interval='daily', time_period=20)
            bollinger_data.to_csv(f"{stock_name}/bollinger_data.csv")
            st.success('Bollinger Bands data saved.')
            st.write("Bollinger Bands Data")
            st.line_chart(bollinger_data)

        # Fetch Patterns
        if fetch_patterns:
            candlestick_patterns = {
                "Doji": ta.candlestick.cdl_doji,
                "Evening Star": ta.candlestick.cdl_evening_star,
                # Add other candlestick patterns
                
            }
            for pattern_name, pattern_function in candlestick_patterns.items():
                pattern_data = pattern_function(ohlc_data)
                pattern_data.to_csv(f"{stock_name}/{pattern_name.lower().replace(' ', '_')}_data.csv")
                st.success(f'{pattern_name} data saved.')
                st.write(f"{pattern_name} Data")
                st.line_chart(pattern_data)

        # Fetch Volume Indicators
        if fetch_volume_indicators:
            obv_data, _ = ti.get_obv(symbol=stock_name, interval='daily')
            obv_data.to_csv(f"{stock_name}/obv_data.csv")
            st.success('OBV data saved.')
            st.write("OBV Data")
            st.line_chart(obv_data)

            vpt_data = ta.volume.volume_price_trend(close=ohlc_data['Close'], volume=ohlc_data['Volume'])
            vpt_data.to_csv(f"{stock_name}/vpt_data.csv")
            st.success('VPT data saved.')
            st.write("VPT Data")
            st.line_chart(vpt_data)

            cmf_data = ta.volume.chaikin_money_flow(high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'], volume=ohlc_data['Volume'])
            cmf_data.to_csv(f"{stock_name}/cmf_data.csv")
            st.success('CMF data saved.')
            st.write("CMF Data")
            st.line_chart(cmf_data)

        # Fetch Support and Resistance Levels
        if fetch_support_resistance:
            # Horizontal support and resistance levels
            support_levels = []
            resistance_levels = []
            for i in range(2, len(ohlc_data) - 2):
                if ohlc_data['Low'][i] < ohlc_data['Low'][i - 1] and ohlc_data['Low'][i] < ohlc_data['Low'][i + 1]:
                    support_levels.append(ohlc_data['Low'][i])
                if ohlc_data['High'][i] > ohlc_data['High'][i - 1] and ohlc_data['High'][i] > ohlc_data['High'][i + 1]:
                    resistance_levels.append(ohlc_data['High'][i])
            support_levels = list(set(support_levels))
            resistance_levels = list(set(resistance_levels))

            st.write("Support Levels")
            st.write(support_levels)
            st.write("Resistance Levels")
            st.write(resistance_levels)

            # Trend lines
            fig, ax = plt.subplots()
            ax.plot(ohlc_data.index, ohlc_data['Close'])
            for level in support_levels:
                ax.axhline(y=level, color='r', linestyle='--')
            for level in resistance_levels:
                ax.axhline(y=level, color='g', linestyle='--')
            st.pyplot(fig)

            # Fibonacci retracement
            max_price = ohlc_data['Close'].max()
            min_price = ohlc_data['Close'].min()
            difference = max_price - min_price
            levels = [max_price - difference * ratio for ratio in [0.236, 0.382, 0.5, 0.618, 0.786]]
            
            fig, ax = plt.subplots()
            ax.plot(ohlc_data.index, ohlc_data['Close'])
            for level in levels:
                ax.axhline(y=level, color='b', linestyle='--')
            st.write("Fibonacci Levels")
            st.pyplot(fig)

            # Andrews' Pitchfork
            def draw_andrews_pitchfork(df):
                fig, ax = plt.subplots()
                ax.plot(df.index, df['Close'], label='Close')
                try:
                    points = []
                    for i in range(3):
                        points.append(st.slider(f"Select Point {i+1}", min_value=0, max_value=len(df)-1, value=(i+1)*len(df)//4))
                    x = [df.index[point] for point in points]
                    y = [df['Close'][point] for point in points]

                    ax.plot(x, y, 'ro-')

                    midpoint = [(x[0] + x[2]) / 2, (y[0] + y[2]) / 2]
                    slope1 = (y[1] - midpoint[1]) / (x[1] - midpoint[0])
                    slope2 = (y[2] - y[0]) / (x[2] - x[0])

                    for i in range(len(df)):
                        ax.plot(df.index[i], midpoint[1] + slope1 * (df.index[i] - midpoint[0]), 'g--')
                        ax.plot(df.index[i], y[0] + slope2 * (df.index[i] - x[0]), 'r--')
                        ax.plot(df.index[i], y[2] + slope2 * (df.index[i] - x[2]), 'b--')

                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error drawing Andrews' Pitchfork: {e}")

            draw_andrews_pitchfork(ohlc_data)

        # Fetch Other Indicators
        if fetch_other_indicators:
            sar_data = ta.trend.psar_up(high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'])
            sar_data.to_csv(f"{stock_name}/sar_data.csv")
            st.success('Parabolic SAR data saved.')
            st.write("Parabolic SAR Data")
            st.line_chart(sar_data)

            ichimoku_data = ta.trend.ichimoku_a(high=ohlc_data['High'], low=ohlc_data['Low'])
            ichimoku_data.to_csv(f"{stock_name}/ichimoku_data.csv")
            st.success('Ichimoku Cloud data saved.')
            st.write("Ichimoku Cloud Data")
            st.line_chart(ichimoku_data)

            williams_r_data, _ = ti.get_willr(symbol=stock_name, interval='daily', time_period=14)
            williams_r_data.to_csv(f"{stock_name}/williams_r_data.csv")
            st.success('Williams %R data saved.')
            st.write("Williams %R Data")
            st.line_chart(williams_r_data)

        # Analyze all data using OpenAI in smaller chunks
        def analyze_data_in_chunks(data, chunk_size=1000):
            try:
                client = openai.Client(api_key=os.getenv(OPENAI_API_KEY))
                instructions = f"Please analyze the following historical financial data for {stock_name}. Based on this data, provide insights, trends, and potential future performance predictions."

                responses = []
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i + chunk_size]
                    chunk_instructions = instructions + f"Data chunk {i // chunk_size + 1}:\n{chunk}\n\n"

                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": chunk_instructions},
                            {"role": "user", "content": "Please analyze the following historical financial data for {stock_name}. Based on this data, provide insights, trends, and potential future performance predictions."}
                        ]
                    )

                    response = completion.choices[0].message.content
                    responses.append(response)

                return responses
                return " ".join(responses)
            except Exception as e:
                st.error(f"Error during data analysis: {e}")
                return None

        # Load data from CSV files for analysis
        all_data = []
        for file in os.listdir(stock_name):
            if file.endswith(".csv"):
                data = pd.read_csv(os.path.join(stock_name, file))
                all_data.append(data.to_string())

        analysis_result = analyze_data_in_chunks(" ".join(all_data))

        if analysis_result:
            st.write("Analysis Result")
            st.text(analysis_result)
            with open(f"{stock_name}/analysis_result.txt", 'w') as f:
                f.write(analysis_result)
            st.success('Analysis result saved.')
