import streamlit as st
import yfinance as yf
import altair as alt
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import talib

@st.cache_data
def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

@st.cache_data
def fetch_quarterly_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

@st.cache_data
def fetch_annual_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.financials.T

@st.cache_data
def fetch_weekly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1y', interval = '1wk')

@st.cache_data
def fetch_daily_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1y', interval = '1d')

@st.cache_data
def fetch_monthly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1y', interval = '1mo')






if 'symbol' not in st.session_state:
    st.session_state.symbol = 'AAPL'

st.sidebar.write('Briefly explain the purpose of the dashboard')


symbol = st.sidebar.text_input('Enter a stock symbol', st.session_state.symbol)



if symbol != st.session_state.symbol:
    st.session_state.symbol = symbol

st.title(f':blue[{symbol}] LTM Performance Overview')

price_history = fetch_weekly_price_history(symbol)
price_history = price_history.reset_index()
price_history['Date'] = price_history['Date'].dt.tz_localize(None)
info = fetch_stock_info(symbol)

daily_price_history = fetch_daily_price_history(symbol)
daily_price_history = daily_price_history.reset_index()
daily_price_history['Date'] = pd.to_datetime(daily_price_history['Date']).dt.tz_localize(None)

monthly_price_history = fetch_monthly_price_history(symbol)
monthly_price_history = monthly_price_history.reset_index()
monthly_price_history['Date'] = pd.to_datetime(monthly_price_history['Date']).dt.tz_localize(None)


Chart_frequency = st.sidebar.radio("Select Chart Frequency", ('Daily', 'Weekly', 'Monthly'), horizontal=True, label_visibility="collapsed")


if Chart_frequency == 'Daily':
    col1, col2, col3, col4 = st.columns(4, border=True)

    with col1:
        st.write(f":blue[{symbol}] Daily Close")
        # Determine the arrow direction
        if daily_price_history['Open'].iloc[-1] > daily_price_history['Open'].iloc[-2]:
            arrow = "▲"  # Green arrow
            color = "green"
        else:
            arrow = "▼"  # Red arrow
            color = "red"
        # Display the close price with the arrow
        st.markdown(
            f"<span style='font-size: 24px;'>${daily_price_history['Close'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col2:
        st.write(f":blue[{symbol}] Daily Open")
        if daily_price_history['Open'].iloc[-1] > daily_price_history['Open'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${daily_price_history['Open'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col3:
        st.write(f":blue[{symbol}] Daily High")
        if daily_price_history['High'].iloc[-1] > daily_price_history['High'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${daily_price_history['High'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col4:
        st.write(f":blue[{symbol}] Daily Low")
        if daily_price_history['Low'].iloc[-1] > daily_price_history['Low'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${daily_price_history['Low'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )



    col1, = st.columns(1, border=True)
    with col1:


        candle_stick_chart = go.Figure(data=go.Candlestick(
            x=daily_price_history['Date'],
            open=daily_price_history['Open'],
            high=daily_price_history['High'],
            low=daily_price_history['Low'],
            close=daily_price_history['Close']
        ))
        candle_stick_chart.update_layout(height=300,
                                            title = f'{symbol.upper()} Candlestick Chart',
                                            margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(candle_stick_chart, use_container_width=True)







if Chart_frequency == 'Weekly':
    col1, col2, col3, col4 = st.columns(4, border=True)

    with col1:
        st.write(f":blue[{symbol}] Weekly Close")
        # Determine the arrow direction
        if price_history['Open'].iloc[-1] > price_history['Open'].iloc[-2]:
            arrow = "▲"  # Green arrow
            color = "green"
        else:
            arrow = "▼"  # Red arrow
            color = "red"
        # Display the close price with the arrow
        st.markdown(
            f"<span style='font-size: 24px;'>${price_history['Close'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col2:
        st.write(f":blue[{symbol}] Weekly Open")
        if price_history['Open'].iloc[-1] > price_history['Open'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${price_history['Open'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col3:
        st.write(f":blue[{symbol}] Weekly High")
        if price_history['High'].iloc[-1] > price_history['High'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${price_history['High'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col4:
        st.write(f":blue[{symbol}] Weekly Low")
        if price_history['Low'].iloc[-1] > price_history['Low'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${price_history['Low'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )



    col1, = st.columns(1, border=True)
    with col1:


        candle_stick_chart = go.Figure(data=go.Candlestick(
            x=price_history['Date'],
            open=price_history['Open'],
            high=price_history['High'],
            low=price_history['Low'],
            close=price_history['Close']
        ))
        candle_stick_chart.update_layout(height=300,
                                            title = f'{symbol.upper()} Candlestick Chart',
                                            margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(candle_stick_chart, use_container_width=True)




if Chart_frequency == 'Monthly':
    col1, col2, col3, col4 = st.columns(4, border=True)

    with col1:
        st.write(f":blue[{symbol}] Monthly Close")
        # Determine the arrow direction
        if monthly_price_history['Open'].iloc[-1] > monthly_price_history['Open'].iloc[-2]:
            arrow = "▲"  # Green arrow
            color = "green"
        else:
            arrow = "▼"  # Red arrow
            color = "red"
        # Display the close price with the arrow
        st.markdown(
            f"<span style='font-size: 24px;'>${monthly_price_history['Close'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col2:
        st.write(f":blue[{symbol}] Monthly Open")
        if monthly_price_history['Open'].iloc[-1] > monthly_price_history['Open'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${monthly_price_history['Open'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col3:
        st.write(f":blue[{symbol}] Monthly High")
        if monthly_price_history['High'].iloc[-1] > monthly_price_history['High'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${monthly_price_history['High'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )

    with col4:
        st.write(f":blue[{symbol}] Monthly Low")
        if monthly_price_history['Low'].iloc[-1] > monthly_price_history['Low'].iloc[-2]:
            arrow = "▲"
            color = "green"
        else:
            arrow = "▼"
            color = "red"
        st.markdown(
            f"<span style='font-size: 24px;'>${monthly_price_history['Low'].iloc[-1]:.2f} "
            f"<span style='color: {color};'>{arrow}</span></span>",
            unsafe_allow_html=True
        )



    col1, = st.columns(1, border=True)
    with col1:


        candle_stick_chart = go.Figure(data=go.Candlestick(
            x=monthly_price_history['Date'],
            open=monthly_price_history['Open'],
            high=monthly_price_history['High'],
            low=monthly_price_history['Low'],
            close=monthly_price_history['Close']
        ))
        candle_stick_chart.update_layout(height=300,
                                            title = f'{symbol.upper()} Candlestick Chart',
                                            margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(candle_stick_chart, use_container_width=True)