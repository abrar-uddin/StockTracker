import yfinance as yf
import streamlit as st
from urllib.error import HTTPError

st.sidebar.title('Stock Tracker')
ticker = st.sidebar.text_input("Enter ticker: ")
page_title = st.empty()
chart = st.empty()

time = st.sidebar.selectbox("Time Period", ['YTD', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'MAX'])


@st.cache
# Function used to call Yahoo Finance API for data
def get_data(search_ticker, period):
    ticker_obj = yf.Ticker(search_ticker)
    data = ticker_obj.history(period=period)
    return data


@st.cache
# Function to get current stock information
def get_info(search_ticker=None):
    ticker_obj = yf.Ticker(search_ticker)
    data = ticker_obj.info
    return data


# Default dictionary keys to retrieve
keys_to_get = ['open', 'regularMarketDayHigh', 'previousClose', 'trailingPE']
display_values = ['Open', 'High', 'Close', 'P/E']  # Formatting key values

# Data requests
try:
    chart.line_chart(get_data(ticker, time).Close)
    page_title.title(get_info(ticker)['shortName'])
    for x in range(4):
        info = "".join([display_values[x], ": ", str(get_info(ticker).get(keys_to_get[x]))])
        st.write(info)
except HTTPError:
    page_title.title('Please enter a valid ticker name')
except KeyError:
    page_title.title('Please enter a valid ticker name')
except IndexError:
    page_title.title('Please enter a valid ticker name')
