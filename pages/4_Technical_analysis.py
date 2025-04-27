import streamlit as st
import yfinance as yf
import altair as alt
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import talib
from plotly.subplots import make_subplots

st.set_page_config(layout='wide')

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
    return stock.history(period='5y', interval = '1wk')

@st.cache_data
def fetch_daily_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='5y', interval = '1d')

@st.cache_data
def fetch_monthly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='5y', interval = '1mo')


symbol =  st.session_state.symbol

info = fetch_stock_info(symbol)

st.title(f':blue[{symbol}] Technical Analysis')

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







weekly_price_history = fetch_weekly_price_history(symbol)
weekly_price_history = weekly_price_history.reset_index()
weekly_price_history['Date'] = pd.to_datetime(weekly_price_history['Date']).dt.tz_localize(None)


daily_price_history = fetch_daily_price_history(symbol)
daily_price_history = daily_price_history.reset_index()
daily_price_history['Date'] = pd.to_datetime(daily_price_history['Date']).dt.tz_localize(None)

monthly_price_history = fetch_monthly_price_history(symbol)
monthly_price_history = monthly_price_history.reset_index()
monthly_price_history['Date'] = pd.to_datetime(monthly_price_history['Date']).dt.tz_localize(None)


RSI = talib.RSI(daily_price_history['Close'], timeperiod=14)
daily_price_history['RSI'] = RSI
daily_price_history['RSI'] = daily_price_history['RSI'].dropna()

SMA_50 = talib.SMA(daily_price_history['Close'], timeperiod=50)
daily_price_history['SMA_50'] = SMA_50
daily_price_history['SMA_50'] = daily_price_history['SMA_50'].dropna() 

SMA_200 = talib.SMA(daily_price_history['Close'], timeperiod=200)
daily_price_history['SMA_200'] = SMA_200
daily_price_history['SMA_200'] = daily_price_history['SMA_200'].dropna()

EMA_12 = talib.EMA(daily_price_history['Close'], timeperiod=12)
daily_price_history['EMA_12'] = EMA_12
daily_price_history['EMA_12'] = daily_price_history['EMA_12'].dropna()

EMA_26 = talib.EMA(daily_price_history['Close'], timeperiod=26)
daily_price_history['EMA_26'] = EMA_26
daily_price_history['EMA_26'] = daily_price_history['EMA_26'].dropna()

BB = talib.BBANDS(daily_price_history['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
daily_price_history['Upper_Band'] = BB[0]
daily_price_history['Lower_Band'] = BB[1]
daily_price_history['Upper_Band'] = daily_price_history['Upper_Band'].dropna()
daily_price_history['Lower_Band'] = daily_price_history['Lower_Band'].dropna()

MACD, MACD_Signal, MACD_Histogram = talib.MACD(daily_price_history['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
daily_price_history['MACD'] = MACD
daily_price_history['MACD_Signal'] = MACD_Signal
daily_price_history = daily_price_history.dropna(subset=['MACD', 'MACD_Signal'])

SAR = talib.SAR(daily_price_history['High'], daily_price_history['Low'], acceleration=0.02, maximum=0.2)
daily_price_history['SAR'] = SAR
daily_price_history['SAR'] = daily_price_history['SAR'].dropna()

OBV = talib.OBV(daily_price_history['Close'], daily_price_history['Volume'])
daily_price_history['OBV'] = OBV
daily_price_history['OBV'] = daily_price_history['OBV'].dropna()

ATR = talib.ATR(daily_price_history['High'], daily_price_history['Low'], daily_price_history['Close'], timeperiod=14)
daily_price_history['ATR'] = ATR
daily_price_history['ATR'] = daily_price_history['ATR'].dropna()



if start_date and end_date:
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

  
    weekly_price_history = weekly_price_history[
        (weekly_price_history['Date'] >= start_date) &
        (weekly_price_history['Date'] <= end_date)
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

st.sidebar.write('**Add additional indicators below**')

Indicator_options = st.sidebar.multiselect(
    "**Technical Indicators**", 
    ("SMA_50", "SMA_200", "EMA_12", "EMA_26", "BBands", "SAR"))





col1,  = st.columns(1, border=True)

with col1:




    # Create candlestick chart
    candle_stick_chart = go.Figure(data=go.Candlestick(
        x=daily_price_history['Date'],
        open=daily_price_history['Open'],
        high=daily_price_history['High'],
        low=daily_price_history['Low'],
        close=daily_price_history['Close']
    ))

    if 'SMA_50' in Indicator_options:

        # SMA_50 Line
        candle_stick_chart.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['SMA_50'],
            mode='lines',
            name='SMA_50',
            line=dict(color='purple')
        ))
    if 'SMA_200' in Indicator_options:
        # SMA_200 Line
        candle_stick_chart.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['SMA_200'],
            mode='lines',
            name='SMA_200',
            line=dict(color='yellow')
        ))
    if 'EMA_12' in Indicator_options:
        # EMA_12 Line
        candle_stick_chart.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['EMA_12'],
            mode='lines',
            name='EMA_12',
            line=dict(color='orange')
        ))
    if 'EMA_26' in Indicator_options:
        # EMA_26 Line
        candle_stick_chart.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['EMA_26'],
            mode='lines',
            name='EMA_26',
            line=dict(color='blue')
        ))
    if 'BBands' in Indicator_options:
        # Bollinger Bands
        candle_stick_chart.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['Upper_Band'],
            mode='lines',
            name='Upper Band',
            line=dict(color='white')
        ))
        candle_stick_chart.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['Lower_Band'],
            mode='lines',
            name='Lower Band',
            line=dict(color='white')
        ))

    if 'SAR' in Indicator_options:
        # SAR
        candle_stick_chart.add_trace(go.Scatter(
            x=daily_price_history['Date'],
            y=daily_price_history['SAR'],
            mode='markers',
            name='SAR',
            marker=dict(color='red', size=1)
        ))



    candle_stick_chart.update_xaxes(rangeslider_visible=False)
    candle_stick_chart.update_layout(height=350,
                                    title = f'{symbol.upper()} Candlestick',
                                    yaxis_title='Price',
                                    showlegend=False,
                                    margin=dict(l=0, r=0, t=25, b=0))
    
    st.plotly_chart(candle_stick_chart, use_container_width=True) 

##############################

add_lower_indicators = st.sidebar.checkbox("Add Lower Indicators")

if add_lower_indicators:
    selected_lower_indicator = st.sidebar.radio("Select the lower indicator you want to see", ("VOLUME", "RSI", "MACD", "OBV", "ATR"))
    #Trading Volume Chart


    if selected_lower_indicator == "VOLUME":

        col1, = st.columns(1, border=True)
        with col1:

            volume_chart = go.Figure()

            # Add Volume bars
            volume_chart.add_trace(go.Bar(
                x=daily_price_history['Date'],
                y=daily_price_history['Volume'],
                name='Volume',
                marker_color='orange'
            ))

            # Update layout
            volume_chart.update_layout(
                yaxis_title='Volume',
                height=150,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )

            # Display in Streamlit
            st.plotly_chart(volume_chart, use_container_width=True)


    ################################

    # RSI Chart


    if selected_lower_indicator == "RSI":

        col1, = st.columns(1, border=True)

        with col1:

            fig = go.Figure()

            # RSI Line
            fig.add_trace(go.Scatter(
                x=daily_price_history['Date'],
                y=daily_price_history['RSI'],
                mode='lines',
                name='RSI',
                line=dict(color='white')
            ))

            # Overbought line (70)
            fig.add_trace(go.Scatter(
                x=daily_price_history['Date'],
                y=[70] * len(daily_price_history),
                mode='lines',
                name='Overbought (70)',
                line=dict(color='red', dash='dash')
            ))

            # Oversold line (30)
            fig.add_trace(go.Scatter(
                x=daily_price_history['Date'],
                y=[30] * len(daily_price_history),
                mode='lines',
                name='Oversold (30)',
                line=dict(color='green', dash='dash')
            ))

            fig.update_layout(
                shapes=[
                    # Overbought zone (70–100)
                    dict(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, x1=1,
                        y0=70, y1=100,
                        fillcolor="rgba(255,0,0,0.1)",
                        line_width=0,
                        layer='below'
                    ),
                    # Oversold zone (0–30)
                    dict(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, x1=1,
                        y0=0, y1=30,
                        fillcolor="rgba(0,255,0,0.1)",
                        line_width=0,
                        layer='below'
                    )
                ],
                height=150,
                    title = f'{symbol.upper()} RSI',
                    yaxis_title='RSI',
                    legend=dict(orientation="h", yanchor="top", y=1.25, xanchor="center", x=0.75),
                    margin=dict(l=0, r=0, t=25, b=0))


            st.plotly_chart(fig, use_container_width=True)

    ################################



    ###############################










    if selected_lower_indicator == "MACD":

        col1,  = st.columns(1, border=True)



        with col1:
            fig = go.Figure()

    

            fig.add_trace(go.Scatter(
                x=daily_price_history['Date'],
                y=daily_price_history['MACD'],
                mode='lines',
                name='MACD',
                line=dict(color='orange')
            ))



            fig.add_trace(go.Scatter(
                x=daily_price_history['Date'],
                y=daily_price_history['MACD_Signal'],
                mode='lines',
                name='Signal Line',
                line=dict(color='blue')
            ))

        

            # Add MACD Histogram
            fig.add_trace(go.Bar(
                x=daily_price_history['Date'],
                y=daily_price_history['MACD'] - daily_price_history['MACD_Signal'],
                name='MACD Histogram',
                marker=dict(color='green', opacity=0.4)
            ))

            fig.update_layout(

            yaxis_title='MACD Value',
            margin=dict(l=0, r=0, t=25, b=0),
            legend=dict(orientation="h", yanchor="top", y=1.25, xanchor="center", x=0.75),
            height=150
        )
            st.plotly_chart(fig, use_container_width=True)




    if selected_lower_indicator == "OBV":

        col1,  = st.columns(1, border=True)

        with col1:
            fig = go.Figure()

            # OBV Line
            fig.add_trace(go.Scatter(
                x=daily_price_history['Date'],
                y=daily_price_history['OBV'],
                mode='lines',
                name='OBV',
                line=dict(color='purple')
            ))
            fig.update_layout(
                height=150,
                title = f'{symbol.upper()} OBV',
                yaxis_title='OBV',
                margin=dict(l=0, r=0, t=25, b=0),
                legend=dict(orientation="h", yanchor="top", y=1.25, xanchor="center", x=0.75)
            )
            st.plotly_chart(fig, use_container_width=True)
    ################################



    if selected_lower_indicator == "ATR":

        col1,  = st.columns(1, border=True)

        with col1:
            fig = go.Figure()

            # ATR Line
            fig.add_trace(go.Scatter(
                x=daily_price_history['Date'],
                y=daily_price_history['ATR'],
                mode='lines',
                name='ATR',
                line=dict(color='purple')
            ))
            fig.update_layout(
                height=150,
                title = f'{symbol.upper()} ATR',
                yaxis_title='ATR',
                margin=dict(l=0, r=0, t=25, b=0),
                legend=dict(orientation="h", yanchor="top", y=1.25, xanchor="center", x=0.75)
            )
            st.plotly_chart(fig, use_container_width=True)

    ################################