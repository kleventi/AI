import streamlit as st
from openai import OpenAI
import yfinance as yf
import pandas as pd
import numpy as np
import ta

# Replace "your_api_key_here" with your actual OpenAI API key
client = OpenAI(api_key="your_api_key_here")

st.title('Interactive Financial Stock Market Comparative Analysis Tool')

# Function to fetch stock data, date range selected by the user and error handling added
def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.error(f"No datafound for {ticker}. Please check the ticker and try again.")
            return None
        return data
    except Exception as e:
        st.error(f"AN error occerred while fetching data for {ticker}: {str(e)}")
        return None

# Sidebar for user inputs
st.sidebar.header('User Input Options')
selected_stock = st.sidebar.text_input('Enter Stock Ticker 1', 'AAPL').upper()
selected_stock2 = st.sidebar.text_input('Enter Stock Ticker 2', 'GOOGL').upper()

# User selected date range for analysis
start_date = st.sidebar.date_input("Select start date:", value = pd.to_datetime("2023-08-01"))
end_date = st.sidebar.date_input("Select end date:", value = pd.to_datetime("2024-08-01"))

# Fetch stock data for the selected date range

stock_data = get_stock_data(selected_stock, start_date = start_date, end_date = end_date)
# Calculate the mean Close data, will be used in the line chart of Close data
closeData_mean = np.full(len(stock_data['Close']), stock_data['Close'].mean()) 
stock_data['Close Mean'] = closeData_mean

stock_data2 = get_stock_data(selected_stock2, start_date = start_date, end_date = end_date)
# Calculate the mean Close data, will be used in the line chart of Close data
closeData_mean2 = np.full(len(stock_data2['Close']), stock_data2['Close'].mean()) 
stock_data2['Close Mean'] = closeData_mean2

# Check if data is available
if stock_data is not None and stock_data2 is not None:
    
    col1, col2 = st.columns(2)

    # Display stock data (more chart types added)
    with col1:
       
        st.subheader(f"Displaying data for:")
        st.subheader(f"*{selected_stock}*")
        # Convert the 'Time' part of the DateTimeIndex, since the 'Time' part is 00:00:00]
        stock_data.index = stock_data.index.date
        st.write(stock_data)
        
        st.write(f"Close data for *{selected_stock}*")
        chart_type = st.sidebar.selectbox(f'Select Chart Type for {selected_stock}', ['Line', 'Bar', 'Scatter', 'Area'])
        if chart_type == 'Line':
            st.line_chart(stock_data[['Close', 'Close Mean']])
        elif chart_type == 'Bar':
            st.bar_chart(stock_data['Close'])
        elif chart_type == 'Scatter':
            st.scatter_chart(stock_data['Close'])
        elif chart_type == 'Area':
            st.area_chart(stock_data['Close'])
            
        # Display additional financial metrics - Simple Moving Averages
        stock_data['20_SMA'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['50_SMA'] = stock_data['Close'].rolling(window=50).mean()
        st.write("Simple Moving Averages (20 & 50 days)")
        if chart_type == 'Line':
            st.line_chart(stock_data[['Close', '20_SMA', '50_SMA']])
        elif chart_type == 'Bar':
            st.bar_chart(stock_data[['Close', '20_SMA', '50_SMA']])
        elif chart_type == 'Scatter':
            st.scatter_chart(stock_data[['Close', '20_SMA', '50_SMA']])
        elif chart_type == 'Area':
            st.area_chart(stock_data[['Close', '20_SMA', '50_SMA']])
        
        
        # Display additional financial metrics - RSI
        stock_data['RSI'] = ta.momentum.RSIIndicator(stock_data['Close']).rsi()
        st.write("RSI (Relative Strength Index)")
        if chart_type == 'Line':
            st.line_chart(stock_data['RSI'])
        elif chart_type == 'Bar':
            st.bar_chart(stock_data['RSI'])
        elif chart_type == 'Scatter':
            st.scatter_chart(stock_data['RSI'])
        elif chart_type == 'Area':
            st.area_chart(stock_data['RSI'])
        
        
        # Display additional financial metrics - Bollinger Bands
        stock_data['Upper Band'], stock_data['Middle Band'], stock_data['Lower Band'] = ta.volatility.BollingerBands(stock_data['Close']).bollinger_hband(), ta.volatility.BollingerBands(stock_data['Close']).bollinger_mavg(), ta.volatility.BollingerBands(stock_data['Close']).bollinger_lband()
        st.write("Bollinger Bands")
        if chart_type == 'Line':
            st.line_chart(stock_data[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        elif chart_type == 'Bar':
            st.bar_chart(stock_data[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        elif chart_type == 'Scatter':
            st.scatter_chart(stock_data[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        elif chart_type == 'Area':
            st.area_chart(stock_data[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        
         
        
    with col2:
        st.subheader(f"Displaying data for:")
        st.subheader(f"*{selected_stock2}*")
        # Convert the 'Time' part of the DateTimeIndex, since the 'Time' part is 00:00:00]
        stock_data2.index = stock_data2.index.date
        st.write(stock_data2)
        
        st.write(f"Close data for *{selected_stock2}*")
        chart_type2 = st.sidebar.selectbox(f'Select Chart Type for {selected_stock2}', ['Line', 'Bar', 'Scatter', 'Area'])
        if chart_type2 == 'Line':
            st.line_chart(stock_data2[['Close', 'Close Mean']])
        elif chart_type2 == 'Bar':
            st.bar_chart(stock_data2['Close'])
        elif chart_type2 == 'Scatter':
            st.scatter_chart(stock_data2['Close'])
        elif chart_type2 == 'Area':
            st.area_chart(stock_data2['Close'])
            
        # Display additional financial metrics - Simple Moving Averages
        stock_data2['20_SMA'] = stock_data2['Close'].rolling(window=20).mean()
        stock_data2['50_SMA'] = stock_data2['Close'].rolling(window=50).mean()
        st.write("Simple Moving Averages (20 & 50 days)")
        if chart_type2 == 'Line':
            st.line_chart(stock_data2[['Close', '20_SMA', '50_SMA']])
        elif chart_type2 == 'Bar':
            st.bar_chart(stock_data2[['Close', '20_SMA', '50_SMA']])
        elif chart_type2 == 'Scatter':
            st.scatter_chart(stock_data2[['Close', '20_SMA', '50_SMA']])
        elif chart_type2 == 'Area':
            st.area_chart(stock_data2[['Close', '20_SMA', '50_SMA']])
        
        # Display additional financial metrics - RSI
        stock_data2['RSI'] = ta.momentum.RSIIndicator(stock_data2['Close']).rsi()
        st.write("RSI (Relative Strength Index)")
        if chart_type2 == 'Line':
            st.line_chart(stock_data2['RSI'])
        elif chart_type2 == 'Bar':
            st.bar_chart(stock_data2['RSI'])
        elif chart_type2 == 'Scatter':
            st.scatter_chart(stock_data2['RSI'])
        elif chart_type2 == 'Area':
            st.area_chart(stock_data2['RSI'])
        
        # Display additional financial metrics - Bollinger Bands
        stock_data2['Upper Band'], stock_data2['Middle Band'], stock_data2['Lower Band'] = ta.volatility.BollingerBands(stock_data2['Close']).bollinger_hband(), ta.volatility.BollingerBands(stock_data2['Close']).bollinger_mavg(), ta.volatility.BollingerBands(stock_data2['Close']).bollinger_lband()
        st.write("Bollinger Bands")
        if chart_type2 == 'Line':
            st.line_chart(stock_data2[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        elif chart_type2 == 'Bar':
            st.bar_chart(stock_data2[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        elif chart_type2 == 'Scatter':
            st.scatter_chart(stock_data2[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])
        elif chart_type2 == 'Area':
            st.area_chart(stock_data2[['Close', 'Upper Band', 'Middle Band', 'Lower Band']])

    # Comparative analysis will be described in detail using Markdown for a better presentation
    st.divider()
    st.markdown("**To view a detailed comparative analysis, with highlights for each stock and a conclusion, please press the button below.**")
    if st.button('Generate Comparative Analysis'):
        with st.spinner('Generating comparative analysis...'):
          response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a financial assistant that retrieves and compares financial market data. Provide a detailed comparative analysis in markdown format. Finally, summarize the comparative performance in text, in full detail with highlights for each stock and also a conclusion with a markdown output. BE VERY STRICT ON YOUR OUTPUT"},
                    {"role": "user", "content": f"Analyze and compare these two stocks:\n\n{selected_stock}:\n{stock_data.to_string()}\n\n{selected_stock2}:\n{stock_data2.to_string()}"}
                  ]
            )
          st.write(response.choices[0].message.content)
else:
    st.write("Please enter valid stock tickers and ensure data is available for the selected date range.")