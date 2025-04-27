import streamlit as st
import yfinance as yf
import altair as alt
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import talib
from plotly.subplots import make_subplots

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
def fetch_monthly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='5y', interval = '1mo')

@st.cache_data
def fetch_weekly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='5y', interval = '1wk')

@st.cache_data
def fetch_daily_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='5y', interval = '1d')




symbol =  st.session_state.symbol

info = fetch_stock_info(symbol)

st.title(f':blue[{symbol}] Financial Charts')

st.sidebar.write('**Select the date range to analyse**')

col1, col2 = st.columns(2)
with col1:
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('today') - pd.DateOffset(years=1),
                                            min_value = pd.to_datetime('today') - pd.DateOffset(years=5),
                                            max_value = pd.to_datetime('today'))
with col2:
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('today'),
                                        min_value = pd.to_datetime('today') - pd.DateOffset(years=5),
                                        max_value = pd.to_datetime('today'))



price_history = fetch_weekly_price_history(symbol)
price_history = price_history.reset_index()
price_history['Date'] = pd.to_datetime(price_history['Date']).dt.tz_localize(None)

daily_price_history = fetch_daily_price_history(symbol)
daily_price_history = daily_price_history.reset_index()
daily_price_history['Date'] = pd.to_datetime(daily_price_history['Date']).dt.tz_localize(None)

monthly_price_history = fetch_monthly_price_history(symbol)
monthly_price_history = monthly_price_history.reset_index()
monthly_price_history['Date'] = pd.to_datetime(monthly_price_history['Date']).dt.tz_localize(None)




if start_date and end_date:
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

  
    price_history = price_history[
        (price_history['Date'] >= start_date) &
        (price_history['Date'] <= end_date)
    ]
    daily_price_history = daily_price_history[
        (daily_price_history['Date'] >= start_date) &
        (daily_price_history['Date'] <= end_date)
    ]
    monthly_price_history = monthly_price_history[
        (monthly_price_history['Date'] >= start_date) &
        (monthly_price_history['Date'] <= end_date)
    ]



daily_price_history['Volume_MA'] = daily_price_history['Volume'].rolling(window=5).mean()



Chart_frequency = st.sidebar.radio("Select Chart Frequency", ('Daily', 'Weekly', 'Monthly'), horizontal=True, label_visibility="collapsed")

##############################

if Chart_frequency == 'Daily':


    #Daily High and Low Price Chart
    col1, col2 = st.columns(2, border=True)

    with col1:
        #Daily High Price Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['High'],
            mode='lines',
            line=dict(color='green')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} High Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
                showgrid=True  
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        #Daily Low Price Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['Low'],
            mode='lines',
            line=dict(color='red')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Low Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
                showgrid=True,
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    ##############################

    #Daily Open and Close Price Chart

    col1, col2 = st.columns(2, border=True)
    #Daily Open Price Chart
    with col1:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['Open'],
            mode='lines',
            line=dict(color='blue')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Open Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    #Daily Close Price Chart
    with col2:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['Close'],
            mode='lines',
            line=dict(color='orange')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Close Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25,   
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    ##############################

    #Daily Trading Volume Chart

    col1, = st.columns(1, border=True)
    with col1:

        volume_chart = go.Figure()

        volume_chart.add_trace(go.Bar(
            x=daily_price_history['Date'],
            y=daily_price_history['Volume'],
            marker_color='purple'
        ))

        volume_chart.update_layout(
            title=f'{symbol.upper()} Trading Volume',
            yaxis_title='Volume',
            yaxis=dict(
                showgrid=True,
            ),
            height=150,
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0)
        )

    
        st.plotly_chart(volume_chart, use_container_width=True)

    ################################

if Chart_frequency == 'Weekly':

    #Weekly High and Low Price Chart
    col1, col2 = st.columns(2, border=True)

    with col1:
        #Weekly High Price Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=price_history['Date'],
            y=price_history['High'],
            mode='lines',
            line=dict(color='green')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} High Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
                showgrid=True  
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        #Weekly Low Price Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=price_history['Date'],
            y=price_history['Low'],
            mode='lines',
            line=dict(color='red')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Low Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
                showgrid=True,
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    ##############################

    #Weekly Open and Close Price Chart

    col1, col2 = st.columns(2, border=True)
    #Weekly Open Price Chart
    with col1:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=price_history['Date'],
            y=price_history['Open'],
            mode='lines',
            line=dict(color='blue')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Open Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    #Weekly Close Price Chart
    with col2:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=price_history['Date'],
            y=price_history['Close'],
            mode='lines',
            line=dict(color='orange')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Close Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25,   
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    ##############################

    #Weekly Trading Volume Chart

    col1, = st.columns(1, border=True)
    with col1:

        volume_chart = go.Figure()

        volume_chart.add_trace(go.Bar(
            x=price_history['Date'],
            y=price_history['Volume'],
            marker_color='purple'
        ))

        volume_chart.update_layout(
            title=f'{symbol.upper()} Trading Volume',
            yaxis_title='Volume',
            yaxis=dict(
                showgrid=True,
            ),
            height=150,
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(volume_chart, use_container_width=True)

    ################################

if Chart_frequency == 'Monthly':

    #Monthly High and Low Price Chart
    col1, col2 = st.columns(2, border=True)

    with col1:
        #Monthly High Price Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly_price_history['Date'],
            y=monthly_price_history['High'],
            mode='lines',
            line=dict(color='green')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} High Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
                showgrid=True  
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        #Monthly Low Price Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly_price_history['Date'],
            y=monthly_price_history['Low'],
            mode='lines',
            line=dict(color='red')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Low Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
                showgrid=True,
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    ##############################

    #Monthly Open and Close Price Chart

    col1, col2 = st.columns(2, border=True)
    #Monthly Open Price Chart
    with col1:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly_price_history['Date'],
            y=monthly_price_history['Open'],
            mode='lines',
            line=dict(color='blue')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Open Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25, 
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    #Monthly Close Price Chart
    with col2:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly_price_history['Date'],
            y=monthly_price_history['Close'],
            mode='lines',
            line=dict(color='orange')
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Close Price',
            yaxis_title='Price',
                yaxis=dict(
                dtick=25,   
            ),
            margin=dict(l=0, r=0, t=25, b=0),
            showlegend=False,
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)

    ##############################

    #Monthly Trading Volume Chart

    col1, = st.columns(1, border=True)
    with col1:

        volume_chart = go.Figure()

        volume_chart.add_trace(go.Bar(
            x=monthly_price_history['Date'],
            y=monthly_price_history['Volume'],
            marker_color='purple'
        ))

        volume_chart.update_layout(
            title=f'{symbol.upper()} Trading Volume',
            yaxis_title='Volume',
            yaxis=dict(
                showgrid=True,
            ),
            height=150,
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(volume_chart, use_container_width=True)

    ################################