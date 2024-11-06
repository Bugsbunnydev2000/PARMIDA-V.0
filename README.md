# PARMIDA-V.0
Professional stock market analyzer using LLM

how it works :

1-Getting fundamental analysis data from different APIs

2-Getting indicators (RSI, etc.), patterns (Fibonacci, etc.) and technical analysis data from different APIs

3-Getting the news and analyzing the sentiments of the news to identify the market in the future

4-We give all this information to LLM Chatgpt for analysis

-----------
**Fundamental analysis factors:**

Company financial data:

Revenue

Net Income

Earnings before interest and taxes (EBIT)

Earnings before interest, taxes, depreciation and amortization (EBITDA)

Profit Margin

dividend

Dividend Payout Ratio

Earnings Per Share - EPS

Price-to-earnings ratio (P/E Ratio)

P/B Ratio

return on equity (ROE)

return on assets (ROA)

Free Cash Flow

Debt to Equity Ratio (D/E)

Current Ratio

Quick Ratio

balance sheet

Income Statement

Cash Flow Statement

Economic data:

Interest Rate

inflation rate

Exchange Rate

GDP Growth Rate

Unemployment Rate

Consumer Price Index (CPI)

Producer Price Index (PPI)

Trade Balance

Changes in monetary and fiscal policies

**how to run Fundamental-Analysis:**

first download library :

```bash
pip install requirements.txt
```

enter the api key of .env file :

```bash
QUANDL_API =  "Your QUANDL_API"
OPENAI_API_KEY = "Your OPENAI_API_KEY"
FRED_API = "Your FRED_API"
ALPHA_VANTAGE_API = "Your ALPHA_VANTAGE_API" 
```

go to directory : Fundamental-Analysis and enter this command
```bash
streamlit run Main-Fundamental-Analysis.py.py
```
----------------------------------------------------------------------

**Technical analysis factors:**


**Trend indicators:**

Simple Moving Average (SMA): Identifying long-term trends.

Exponential Moving Average (EMA): More sensitive to recent price changes.

MACD (Moving Average Convergence Divergence): Identify trend changes and strengths.

ADX (Average Directional Index): measures the strength of the trend.

**Volatility indicators:**
RSI (Relative Strength Index): Identifying the oversold situation.

Stochastic Oscillator: identifying buy and sell points.

CCI (Commodity Channel Index): identifying the saturation points of buying and selling.

ATR (Average True Range): A measure of price volatility.

**Bands and tapes:**

Bollinger Bands: identify swings and potential reversal points.

Andrews Pitchfork: identification of support and resistance levels.

**Graphic patterns:**:

Candlestick patterns: such as doji pattern, evening star, etc.

Price patterns: such as the head and shoulders pattern, the pattern of two peaks and two valleys.

Triangle patterns: ascending, descending and symmetrical triangles.

**Volume indicators**:

OBV (On-Balance Volume): Evaluation of volume flow.

Volume Price Trend (VPT): Combination of volume and price to identify trends.

Chaikin Money Flow (CMF): Assessing buying and selling pressure.

**Support and resistance levels**:

Horizontal support and resistance levels: using price points that have acted as support or resistance in the past.

Trend Lines: Lines drawn on a price chart that show support and resistance levels.

Fibonacci: Using Fibonacci levels to predict possible support and resistance points.

**Other indicators:**
Parabolic SAR: detection of stop and reversal points.

Ichimoku Cloud: identifying support and resistance levels and determining trend direction.

Williams %R: Identification of oversold conditions.

**how to run Technical-Analysis:**

first download library :

```bash
pip install requirements.txt
```

enter the api key of .env file :

```bash
QUANDL_API =  "Your QUANDL_API"
OPENAI_API_KEY = "Your OPENAI_API_KEY"
FRED_API = "Your FRED_API"
ALPHA_VANTAGE_API = "Your ALPHA_VANTAGE_API" 
```

go to directory : Technical-Analysis and enter this command
```bash
streamlit run Main-Technical-Analysis.py
```
-----------------------------------------------------------------------------------------------------------------------------------------------------
interface of project :
![interface](https://github.com/user-attachments/assets/72b9190d-9f4a-404d-82f1-5bbf1ba1742f)
Technical photo:
![Show](https://github.com/user-attachments/assets/15f1faf8-2feb-4ef9-a582-2cbf6acad56f)
how to save data :
![Data-save](https://github.com/user-attachments/assets/a6b523d7-65f1-4f40-bb77-49d4a3d29e20)

------------------------------------------------------------------
#how to run :

in the .env file enter  your api-key 

```bash
QUANDL_API =  "Your QUANDL_API"
OPENAI_API_KEY = "Your OPENAI_API_KEY"
FRED_API = "Your FRED_API"
ALPHA_VANTAGE_API = "Your ALPHA_VANTAGE_API" 
```
----------------------------------------------
**how to run MVP-TEST **:

first download library :

```bash
pip install requirements.txt
```
```bash
streamlit run MVP-TEST.py
```

**suggestion: **
If you want to use this source code for stock market analysis seriously, not for educational purposes:
I suggest you do this:
1-Change the prompt of Openai :
```bash
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
```
2- set the time for get data.
**This project is for educational purposes only and is not guaranteed to analyze stock markets**
The address of the llm analysis sample folder: doucment\result of AAPL.txt

Developer E-mail : dev.bugsbunny2000@gmail.com

Thanks for you support:)))))
