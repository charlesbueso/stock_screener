import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from config import myportfolio


# Define a function to get stock data
def get_stock_data(ticker, period="5y"):
  """
  Downloads historical or current stock data for a given ticker symbol.

  Args:
      ticker (str): Stock ticker symbol.
      period (str, optional): Period for which to download data. Defaults to "1d" (one day).

  Returns:
      pandas.DataFrame: DataFrame containing stock data.
  """
  data = yf.download(ticker, period=period)
  return data

# Get data for each ticker and store in a dictionary
stock_data = {}
for ticker in myportfolio:
  data = get_stock_data(ticker)
  stock_data[ticker] = data
print(stock_data)

# Analyze and format the data for your needs (replace with your analysis logic)
analysis_results = {}
for ticker, data in stock_data.items():
  # Example: Get closing price
  closing_price = data["Close"][-1]
  analysis_results[ticker] = {"Closing Price": closing_price}
  # Add more analysis as needed

# Output results (replace with your preferred output method)
# Option 1: Print to console
print(analysis_results)


def get_stock_stddev(df, ticker):
  """
  Downloads the last year of closing prices for "GOOG" and calculates the standard deviation.

  Returns:
      float: The standard deviation of closing prices for the last year.
  """
  # Download data for the last year
  data = yf.download("GOOG", period="5y")

  # Get closing prices
  closing_prices = data["Close"].std()

  # Calculate standard deviation
  stddev = closing_prices.std()

  return stddev

def calculate_price_difference(stock_data):
    latest_price = stock_data.iloc[-1]["Close"]
    previous_year_price = stock_data.iloc[-252]["Close"] if len(stock_data) > 252 else stock_data.iloc[0]["Close"]
    price_difference = latest_price - previous_year_price
    percentage_difference = (price_difference / previous_year_price) * 100
    return price_difference, percentage_difference

def moving_average(stock_data):
   # Download data for the last year
  data = yf.download("GOOG", period="1y")

  # Get closing prices
  moving_average = data["Close"][0]

  return moving_average


def visualize_portfolio(tickers=myportfolio):
  #-- BOLIERPLATE --#
    st.set_page_config(page_title="Stock Dashboard", layout="wide", page_icon="📈")
    hide_menu_style = "<style> footer {visibility: hidden;} </style>"
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    
    st.title("📈 Stock Dashboard")
    symbol = st.sidebar.selectbox("Select a stock symbol:", tickers, index=2)
 
    st.sidebar.info('yaoyao')

    st.header(f"Stock Data for {symbol}")

    if symbol:
        stock_data = get_stock_data(symbol)
        # index = get_stock_data(symbol)

        if stock_data is not None:
            price_difference, percentage_difference = calculate_price_difference(stock_data)
            latest_close_price = stock_data.iloc[-1]["Close"]
            max_52_week_high = stock_data["High"].tail(252).max()
            min_52_week_low = stock_data["Low"].tail(252).min()
            stddev = stock_data["Close"].std()
            moving_average = moving_average(stock_data)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.metric("Close Price", f"${latest_close_price:.2f}")
            with col2:
                st.metric("Price Difference (YoY)", f"${price_difference:.2f}", f"{percentage_difference:+.2f}%")
            with col3:
                st.metric("52-Week High", f"${max_52_week_high:.2f}")
            with col4:
                st.metric("52-Week Low", f"${min_52_week_low:.2f}")
            with col5:
                st.metric("StdDev on close", f"{stddev:.5f}")
            with col6:
                st.metric("Moving average", f"{moving_average:.5f}")

            st.subheader("Candlestick Chart")
            candlestick_chart = go.Figure(data=[go.Candlestick(x=stock_data.index, open=stock_data['Open'], high=stock_data['High'], low=stock_data['Low'], close=stock_data['Close'])])
            candlestick_chart.update_layout(title=f"{symbol} Candlestick Chart", xaxis_rangeslider_visible=False)
            st.plotly_chart(candlestick_chart, use_container_width=True)

            st.subheader("Summary")
            st.dataframe(stock_data.tail())

            st.download_button("Download Stock Data Overview", stock_data.to_csv(index=True), file_name=f"{symbol}_stock_data.csv", mime="text/csv")


# Example usage
# stddev = get_googl_stddev()
# print(f"Standard deviation of GOOG closing prices (last year): {stddev:.2f}")
visualize_portfolio()