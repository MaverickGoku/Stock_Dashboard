import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

@st.cache_data
def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

def get_institutional_holders(symbol):
    stock = yf.Ticker(symbol)
    return stock.institutional_holders

@st.cache_data
def fetch_quarterly_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

@st.cache_data
def fetch_annual_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.financials.T

symbol = st.session_state.symbol

info = fetch_stock_info(symbol)

Holders = get_institutional_holders(symbol)

dividends = yf.Ticker(symbol).dividends
dividends.index = dividends.index.date

stock_splits = yf.Ticker(symbol).splits
stock_splits.index = stock_splits.index.date

Company_info_on = st.sidebar.checkbox("Company Info", value=True)

Dividends_on = st.sidebar.checkbox("Dividends", value=False)

Stock_splits_on = st.sidebar.checkbox("Stock Splits", value=False)

Institutional_holders_on = st.sidebar.checkbox("Top Institutional Holders", value=False)

Financial_info_on = st.sidebar.checkbox("Financial Info", value=False)

quarterly_financials = fetch_quarterly_financials(symbol)
annual_financials = fetch_annual_financials(symbol)


st.title(f":blue[{symbol}] Company Information")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if Company_info_on:
        st.write(f"**Company:** {info['longName']}")
        st.write(f"**Sector:** {info['sector']}")
        st.write(f"**Industry:** {info['industry']}")
        st.write(f"**Country:** {info['country']}")
        st.write(f"**Market Cap:** ${info['marketCap']:,}")
with col2:
    if Company_info_on:
        
        st.write(f"**Dividend Yield:** {info['dividendYield']}")
        st.write(f"**P/E Ratio (Price-to-Earnings):** {info.get('trailingPE', 'Not available')}")
        st.write(f"**52 Week Low:** ${info.get('fiftyTwoWeekLow', 'Not available')}")
        st.write(f"**52 Week High:** ${info.get('fiftyTwoWeekHigh', 'Not available')}")
        st.write(f"**Beta:** {info.get('beta', 'Not available')}")

st.divider()





if Dividends_on:
    if not dividends.empty:
        st.write("**Dividends:**")
        st.dataframe(dividends.sort_index(ascending=False))
    else:
        st.write("**Dividends:** No dividend data available.")

    st.divider()


if Stock_splits_on:
    if not stock_splits.empty:
        st.write("**Stock Splits:**")
        st.dataframe(stock_splits.sort_index(ascending=False))
    else:
        st.write("**Stock Splits:** No stock split data available.")

    st.divider()


if Institutional_holders_on:
    if symbol:
        holders = get_institutional_holders(symbol)
        
        st.write('**Top Institutional Holders**')

        if holders is not None:
            st.dataframe(holders)
        else:
            st.info("No institutional holder data available.")
        
    st.divider()



if Financial_info_on:
    st.write("**Financial Information:**")
    selection = st.sidebar.segmented_control(options = ['Quarterly', 'Annual'], default = 'Quarterly', label = '**Select Period**')


    if selection == 'Quarterly':
        col1, col2 = st.columns(2, border=True)
        with col1:
            quarterly_financials = quarterly_financials.rename_axis('Quarter').reset_index()
            quarterly_financials['Quarter'] = quarterly_financials['Quarter'].astype(str)
            revenue_chart = alt.Chart(quarterly_financials).mark_bar(color='red').encode(
                x='Quarter:O',
                y='Total Revenue'
            )
            st.subheader(f'{symbol.upper()} Quarterly Revenue:')
            st.altair_chart(revenue_chart, use_container_width=True)
        
        with col2:
            net_income_chart = alt.Chart(quarterly_financials).mark_bar(color='orange').encode(
                x='Quarter:O',
                y='Net Income'
            )
            st.subheader(f'{symbol.upper()} Quarterly Income:')
            st.altair_chart(net_income_chart, use_container_width=True)

    if selection == 'Annual':
        col1, col2 = st.columns(2, border=True)
        with col1:
            annual_financials = annual_financials.rename_axis('Year').reset_index()
            annual_financials['Year'] = annual_financials['Year'].astype(str).transform(lambda year: year.split('-')[0])
            revenue_chart = alt.Chart(annual_financials).mark_bar(color = 'red').encode(
                x='Year:O',
                y='Total Revenue'
            )
            st.subheader(f'{symbol.upper()} Annual Revenue:')
            st.altair_chart(revenue_chart, use_container_width=True)
        with col2:
            net_income_chart = alt.Chart(annual_financials).mark_bar(color = 'orange').encode(
                x='Year:O',
                y='Net Income'
            )
      
            st.subheader(f'{symbol.upper()} Annual Income:')
            st.altair_chart(net_income_chart, use_container_width=True)