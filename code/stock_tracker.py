import yfinance as yf
import streamlit as st
from urllib.error import HTTPError
import plotly.graph_objects as go
import pandas as pd

st.sidebar.title('Stock Tracker')
ticker = st.sidebar.text_input("Enter ticker: ")
page_title = st.empty()
chart = st.empty()

time = st.sidebar.selectbox("Time Period", ['YTD', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'MAX'])
show_elections = st.sidebar.checkbox('Show Elections')
st.sidebar.info("Last 10 elections")


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
    page_title.title(get_info(ticker)['shortName'])

    us_election_dates = pd.read_csv('data/us_election_dates.csv', usecols=['Date Presidential'])
    us_election_dates = us_election_dates.drop([*range(0, 50)])
    us_election_dates['Date Presidential'] = us_election_dates['Date Presidential'].apply(lambda x: x.replace('*', ''))
    us_election_dates['Date Presidential'] = pd.to_datetime(us_election_dates['Date Presidential'])

    data = get_data(ticker, time)
    price = pd.DataFrame(data)
    fig = go.Figure()

    # Add scatter trace for line
    fig.add_trace(go.Scatter(
        x=price.index,
        y=price.Close,
        mode="lines"
    ))

    if(show_elections):
        # Add shape regions
        shapes_list = []
        for x in us_election_dates['Date Presidential']:
            shapes = go.layout.Shape(type="rect",
                                     xref="x",
                                     yref="paper",
                                     x0=x,
                                     y0=0,
                                     x1=x + pd.Timedelta(days=5),
                                     y1=1,
                                     fillcolor="red",
                                     opacity=0.5,
                                     layer="below",
                                     line_width=2, )

            shapes_list.append(shapes)
        fig.update_layout(
            shapes=shapes_list
        )
    st.plotly_chart(fig)

    for x in range(len(keys_to_get)):
        info = "".join([display_values[x], ": ", str(get_info(ticker).get(keys_to_get[x]))])
        st.write(info)
except HTTPError:
    page_title.title('Please enter a valid ticker name')
except KeyError:
    page_title.title('Please enter a valid ticker name')
except IndexError:
    page_title.title('Please enter a valid ticker name')
