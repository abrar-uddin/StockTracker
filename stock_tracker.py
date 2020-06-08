import yfinance as yf
import streamlit as st

st.sidebar.title('Stock Tracker')
ticker = st.sidebar.text_input("Enter ticker: ")
st.title(ticker.upper())
ticker = yf.Ticker(ticker)

chart = st.empty()
time = st.sidebar.radio("Time Period", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                        index=1)


@st.cache
# Function used to call Yahoo Finance API for data
def get_data(period):
    data = ticker.history(period=period)
    return data


chart.line_chart(get_data(time).Close)
