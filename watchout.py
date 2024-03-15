import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from config import myportfolio
import pickle
import locale



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
  moving_average = data["Close"].mean()

  return moving_average

def most_bought_senator_stock():
   """
    This function will:
    1. parse through all pdfs in https://efdsearch.senate.gov/search/
    2. save them in onedrive papia1999
    3. pass each pdf as context (as string) with a predefined set of questions
    4. pass pdf to Chat w RTX, save vector db storage on onedrive
    
    Returns:
    1. Most bought stocks descending (by who, percentage, biggest moves, etc)
      For this we will have to compute stock data as well
    2. Assign each public figure a lifetime portfolio %, when they started trading

    Pickle file obtained from /senatordata/senator-filings
    Df important features:
      - Unique trade amount estimates:[1001, 15001, 50001, 250001, 100001, 1000001, 500001, 5000001
        50000000, 25000001]
      - Unique order types: ['Purchase' 'Sale (Full)' 'Sale (Partial)' 'Exchange']
      - Unique names: ['Thomas R Carper' 'Thomas H Tuberville' 'Shelley M Capito'
                      'Daniel S Sullivan' 'Markwayne Mullin' 'Lindsey Graham' 'Gary C Peters'
                      'Rick Scott' 'Sheldon Whitehouse' 'Jerry Moran,  ' 'Angus S King, Jr.'
                      'John W Hickenlooper' 'William F Hagerty, IV' 'John Boozman'
                      'A. Mitchell McConnell, Jr.' 'Tina Smith' 'JD Vance' 'John P Ricketts'
                      'Mark R Warner' 'Thomas R Tillis' 'Ron L Wyden' 'Ladda Tammy Duckworth'
                      'Maria Cantwell' 'Susan M Collins' 'Roy Blunt' 'Debra S Fischer'
                      'John R Thune' 'Patrick J Toomey' 'Rafael E Cruz' 'Cynthia M Lummis'
                      'Rand Paul' 'David A Perdue , Jr' 'James M Inhofe' 'Pat Roberts'
                      'William Cassidy' 'Kelly Loeffler' 'Timothy M Kaine' 'Roger F Wicker'
                      'John Hoeven' 'John N Kennedy' 'Christopher A Coons' 'Jacklyn S Rosen'
                      'Thomas Udall' 'John F Reed' 'Jon Kyl' 'Dean Heller' 'Claire McCaskill'
                      'Steve Daines' 'Robert P Casey, Jr.' 'Thad Cochran' 'Jeffry L Flake'
                      'Tammy Duckworth' 'Michael F Bennet' 'Patty Murray' 'Joseph Manchin, III'
                      'Chris Van Hollen' 'John Cornyn' 'Robert P Corker, Jr.' 'Michael  B Enzi'
                      'Mike Rounds' 'Benjamin L Cardin' 'Cory A Booker']
      - Minimum tx_date, trade date: 2011-11-29 00:00:00
      - Minimum file_date: 2014-01-31 00:00:00
      - 1530 uniquely traded stocks

   """

   with open('./senatordata/senator-filings/senators_clean.pk1', 'rb') as f:

    raw_senators_tx = pickle.load(f)
    print(raw_senators_tx.info())

  
def create_senator_portfolios(senator_transactions_path='C:\\repos\\watchout\\senatordata\\senator-filings\\senators_clean.pk1', 
                             stock_prices_path='C:\\repos\\watchout\\senatordata\\senator-filings\\notebooks\\stocks'):
  """


  |Senator   Stock     Date      
  |----------------------
  |
  |----------------------
  |
  |
  |

  """
  #open senator data
  with open(senator_transactions_path, 'rb') as f:
    senator_data = pd.read_pickle(f)

  senator_names = set(senator_data['full_name'])

  # Filter purchases and separate sales (full and partial)
  purchases = senator_data[senator_data["order_type"] == "Purchase"]
  sales = senator_data[senator_data["order_type"].isin(["Sale (Full)", "Sale (Partial)"])]

  # 1 grafica por senador
  # senator_graph_ts = {senator1: {x: [dates_ascending_order], y: [absolute_return]}}
  for senator in senator_names:
     absolute_return(senator, purchases[purchases['full_name'] == senator], sales[sales['full_name'] == senator])
     
  return -1

def match_transactions(df):
  """
  Finds matching purchase/sale pairs of transactions from a DataFrame.

  Args:
      df (pandas.DataFrame): A DataFrame containing columns 'ORDER_TYPE', 'DATE', and 'AMOUNT'.
          - 'ORDER_TYPE': can be either 'PURCHASE', 'SALE-FULL', or 'SALE-PARTIAL'.
          - 'DATE': transaction date.
          - 'AMOUNT': transaction amount.

  Returns:
      dict: A dictionary where keys are timestamps of sale transactions and values are tuples containing:
          - timestamp of matching purchase transaction
          - remaining amount from the purchase (after covering the sale)


  """

  # Filter purchases and separate sales (full and partial)
  purchases = df[df["order_type"] == "Purchase"]
  sales = df[df["order_type"].isin(["Sale (Full)", "Sale (Partial)"])]

  # Sort by date for both purchases and sales (ascending order)
  purchases = purchases.sort_values(by="tx_date")
  sales = sales.sort_values(by="tx_date")

  matched_pairs = {}
  purchase_index = 0

  #empieza aqui, estas A NADAAAA (Piensa en DSA, creo que podrias iterar sales(n) y purchases (1)?)

  for sale_index, sale_row in sales.iterrows():
    while purchase_index < len(purchases) and purchases.iloc[purchase_index]["tx_date"] <= sale_row["tx_date"]:
      purchase_row = purchases.iloc[purchase_index]
      # Check if sale amount can be fully or partially covered by remaining purchase amount
      if sale_row["tx_estimate"] <= purchase_row["tx_estimate"]:
        remaining_amount = purchase_row["tx_estimate"] - sale_row["tx_estimate"]
        matched_pairs[sale_row["tx_date"]] = (purchase_row["tx_date"], remaining_amount)
        purchase_index += 1
        break  # Move to next sale after a match
      else:
        purchase_index += 1  # Move to next purchase if sale amount is higher
  return matched_pairs
   
   
def absolute_return(senator, purchases, sales):
   """
   1. Calculate initial value of portfolio - sum of all purchases
   2. Calculate final value of portfolio - sum of all sales
   3. Substract ((sum of all purchases) - (sum of all sales))
   """
   
   sum_of_purchases = 0
   sum_of_sales = 0

   for purchase_index, purchase_row in purchases.iterrows():
      quantity = purchase_row["tx_estimate"]
      sum_of_purchases += quantity

   for sales_index, sales_row in sales.iterrows():
        quantity = sales_row["tx_estimate"]
        sum_of_sales += quantity    

   absolute_return = sum_of_purchases - sum_of_sales
   locale.setlocale(locale.LC_ALL, '')
    
   return print("The absolute return for " + senator + " was " + f"{absolute_return:,.2f}$")



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
            

# visualize_portfolio()
            
# most_bought_senator_stock()


if __name__ == "__main__":
  create_senator_portfolios()