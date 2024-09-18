# PARMIDA-V.0
Professional stock market analyzer using LLM
how it works :
1-Getting fundamental analysis data from different APIs
2-Getting indicators (RSI, etc.), patterns (Fibonacci, etc.) and technical analysis data from different APIs
3-Getting the news and analyzing the sentiments of the news to identify the market in the future
4-We give all this information to LLM Chatgpt for analysis

Fundamental analysis factors:
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
----------------------------------------------------------------------


Technical analysis factors:
Trend indicators
Simple Moving Average (SMA): Identifying long-term trends.
Exponential Moving Average (EMA): More sensitive to recent price changes.
MACD (Moving Average Convergence Divergence): Identify trend changes and strengths.
ADX (Average Directional Index): measures the strength of the trend.
Volatility indicators
RSI (Relative Strength Index): Identifying the oversold situation.
Stochastic Oscillator: identifying buy and sell points.
CCI (Commodity Channel Index): identifying the saturation points of buying and selling.
ATR (Average True Range): A measure of price volatility.
Bands and tapes
Bollinger Bands: identify swings and potential reversal points.
Andrews Pitchfork: identification of support and resistance levels.
Graphic patterns
Candlestick patterns: such as doji pattern, evening star, etc.
Price patterns: such as the head and shoulders pattern, the pattern of two peaks and two valleys.
Triangle patterns: ascending, descending and symmetrical triangles.
Volume indicators
OBV (On-Balance Volume): Evaluation of volume flow.
Volume Price Trend (VPT): Combination of volume and price to identify trends.
Chaikin Money Flow (CMF): Assessing buying and selling pressure.
Support and resistance levels
Horizontal support and resistance levels: using price points that have acted as support or resistance in the past.
Trend Lines: Lines drawn on a price chart that show support and resistance levels.
Fibonacci: Using Fibonacci levels to predict possible support and resistance points.
Other indicators
Parabolic SAR: detection of stop and reversal points.
Ichimoku Cloud: identifying support and resistance levels and determining trend direction.
Williams %R: Identification of oversold conditions.
-----------------------------------------------------------------------------------------------------------------------------------------------------
interface of project :
![interface](https://github.com/user-attachments/assets/72b9190d-9f4a-404d-82f1-5bbf1ba1742f)
Technical photo:
![Show](https://github.com/user-attachments/assets/15f1faf8-2feb-4ef9-a582-2cbf6acad56f)
how to save data :
![Data-save](https://github.com/user-attachments/assets/a6b523d7-65f1-4f40-bb77-49d4a3d29e20)

------------------------------------------------------------------
how to run :
in the .env file enter the your api-key 

quandl.ApiConfig.api_key = 'Your-key'
fred = Fred(api_key='Your-key')
alpha_vantage_key = 'Your-key'
openai.api_key = 'Your-key'
OPENAI_API_KEY = "Your-key"
and after enter this command
streamlit run MVP-TEST.py
----------------------------------------------
The address of the llm analysis sample folder: doucment\result of AAPL.txt
Developer E-mail : dev.bugsbunny2000@gmail.com
Thanks for you support
