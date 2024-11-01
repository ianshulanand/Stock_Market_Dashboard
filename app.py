import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
from textblob import TextBlob

# Function to fetch sentiment analysis from news articles
def fetch_sentiment_analysis(stock_symbol):
    # Example URL for a hypothetical news API (we can replace it with a real one)
    # In a real implementation, we would fetch actual news data
    api_url = f"https://newsapi.org/v2/everything?q={stock_symbol}&apiKey=7065ae9fd9f6468f9b434e018614a12a"
    response = requests.get(api_url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    
    sentiments = []
    for article in articles:
        analysis = TextBlob(article['description'] or '')
        sentiments.append(analysis.sentiment.polarity)
        
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    return avg_sentiment

# Title of the dashboard
st.title("Stock Market Dashboard")

# Sidebar for user input
st.sidebar.header("User Input")

# Text input for stock symbol
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA):", "AAPL")

# Date range for historical data
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch stock data
if stock_symbol:
    stock_data = yf.Ticker(stock_symbol)
    df = stock_data.history(start=start_date, end=end_date)

    # Display data
    st.subheader(f"Data for {stock_symbol}")
    st.write(df)

    # Plotting stock performance
    st.subheader("Stock Performance")
    st.line_chart(df['Close'], use_container_width=True)

    # Moving Averages
    st.subheader("Moving Averages")
    df['50_MA'] = df['Close'].rolling(window=50).mean()
    df['200_MA'] = df['Close'].rolling(window=200).mean()
    
    # Plot moving averages
    st.line_chart(df[['Close', '50_MA', '200_MA']], use_container_width=True)

    # Comparative Analysis
    st.subheader("Comparative Analysis")
    comparison_stocks = st.sidebar.multiselect("Select Stocks to Compare", ["AAPL", "MSFT", "GOOGL", "TSLA"])
    
    if comparison_stocks:
        comparison_data = pd.DataFrame()
        for symbol in comparison_stocks:
            stock = yf.Ticker(symbol)
            comp_df = stock.history(start=start_date, end=end_date)
            comparison_data[symbol] = comp_df['Close']
        
        st.line_chart(comparison_data, use_container_width=True)

    # Sentiment Analysis
    if st.sidebar.checkbox("Perform Sentiment Analysis"):
        avg_sentiment = fetch_sentiment_analysis(stock_symbol)
        st.subheader("Sentiment Analysis")
        sentiment_label = "Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral"
        st.write(f"Average Sentiment for {stock_symbol}: {sentiment_label} (Polarity: {avg_sentiment:.2f})")

    # Downloadable Reports
    st.subheader("Download Stock Data")
    if st.button("Download CSV"):
        df.to_csv(f"{stock_symbol}_data.csv")
        st.success(f"{stock_symbol}_data.csv has been created for download.")

# Instructions
st.sidebar.header("Instructions")
st.sidebar.info("1. Enter the stock symbol to view data.")
st.sidebar.info("2. Adjust the date range to filter historical data.")
st.sidebar.info("3. Compare multiple stocks using the multiselect option.")
st.sidebar.info("4. Perform sentiment analysis to see market sentiment.")
st.sidebar.info("5. Download stock data as CSV.")

# Run the app using the command: streamlit run app.py
