!/usr/bin/env python
# coding: utf-8



import requests
import tweepy
import pandas as pd



access_token = "1742678488459497472-HXtM9OzHTPWGxkfjmImYnp90BlZ1ml"

access_token_secret = "dewtRu0YP6KdlCA4IzNkUfzQoChv4s6YhnQhFTRizKnR2"

bearer = "AAAAAAAAAAAAAAAAAAAAAPUOrwEAAAAA3tPnHW%2FpNuVoJ8UPHM707hUkv8Q%3Ds1aKKU5HpsiK17zd4oZmjTsAsvbQ2YyGVb1tFrvtJ9RzOiOLHg"

api_key = "n34SJHko4ZB6TQU9CzqC3G3i5"

api_key_secret = "QIXDDf58EduQkiHiY064QOEeM2shtpsGkIOTNIyy2w9cykcTM4"



def post(text: str):
    
    # Authenticate to Twitter
    client = tweepy.Client(
        bearer_token = bearer,
        consumer_key=api_key,
        consumer_secret=api_key_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Post Tweet
    message = text
    client.create_tweet(text=message)
    
    return None



api = "f30a7111-fdbc-4608-a34d-ef8a426ca0ad"
API_KEY = api



# Replace 'YOUR_API_KEY' with your actual API key
#API_KEY = 'YOUR_API_KEY'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

def get_all_crypto_data(limit=300):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'limit': limit,
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    if 'error' in data:
        print("Error:", data['status']['error_message'])
        return None
    else:
        return data['data']

# Get data for the first 500 cryptocurrencies
crypto_data = get_all_crypto_data()

# Extract relevant information into a DataFrame
crypto_df = pd.DataFrame({
    'Name': [crypto['name'] for crypto in crypto_data],
    'Symbol': [crypto['symbol'] for crypto in crypto_data],
    'Price (USD)': [crypto['quote']['USD']['price'] for crypto in crypto_data],
    'Market Cap (USD)': [crypto['quote']['USD']['market_cap'] for crypto in crypto_data],
    'Volume 24h (USD)': [crypto['quote']['USD']['volume_24h'] for crypto in crypto_data],
    'Percent Change 24h (%)': [crypto['quote']['USD']['percent_change_24h'] for crypto in crypto_data]
})



# Extract relevant information into a DataFrame
crypto_df = pd.DataFrame({
    'Name': [crypto['name'] for crypto in crypto_data],
    'Symbol': [crypto['symbol'] for crypto in crypto_data],
    'Price (USD)': [crypto['quote']['USD']['price'] for crypto in crypto_data],
    'Market Cap (USD)': [crypto['quote']['USD']['market_cap'] for crypto in crypto_data],
    'Volume 24h (USD)': [crypto['quote']['USD']['volume_24h'] for crypto in crypto_data],
    'Percent Change 24h (%)': [crypto['quote']['USD']['percent_change_24h'] for crypto in crypto_data],
    'Percent Change 1h (%)': [crypto['quote']['USD']['percent_change_1h'] for crypto in crypto_data]
})

# Calculate volume-to-marketcap ratio
crypto_df['Volume to MarketCap Ratio'] = crypto_df['Volume 24h (USD)'] / crypto_df['Market Cap (USD)']



crypto_df

















# Sort the DataFrame by the Percent Change 24h column
sorted_crypto_df = crypto_df.sort_values(by='Percent Change 1h (%)', ascending=False)








threshold = 10**7
threshold



sorted_crypto_df = sorted_crypto_df[sorted_crypto_df["Market Cap (USD)"]>threshold]
sorted_crypto_df








# Display the sorted DataFrame
sorted_crypto_df.tail(10)



df_performance_sorted_1y = sorted_crypto_df.tail(10)
df_performance_sorted_1y








df_performance_sorted_1y['Volume to MarketCap Ratio'] = df_performance_sorted_1y.index








df_performance_sorted_1y













top_1_symbol = df_performance_sorted_1y["Symbol"].iloc[-1]
top_1_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-1], 2)
top_1_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-1], 2)

top_2_symbol = df_performance_sorted_1y["Symbol"].iloc[-2]
top_2_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-2], 2)
top_2_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-2], 2)

top_3_symbol = df_performance_sorted_1y["Symbol"].iloc[-3]
top_3_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-3], 2)
top_3_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-3], 2)

top_4_symbol = df_performance_sorted_1y["Symbol"].iloc[-4]
top_4_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-4], 2)
top_4_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-4], 2)

top_5_symbol = df_performance_sorted_1y["Symbol"].iloc[-5]
top_5_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-5], 2)
top_5_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-5], 2)

top_6_symbol = df_performance_sorted_1y["Symbol"].iloc[-6]
top_6_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-6], 2)
top_6_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-6], 2)

top_7_symbol = df_performance_sorted_1y["Symbol"].iloc[-7]
top_7_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-7], 2)
top_7_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-7], 2)

top_8_symbol = df_performance_sorted_1y["Symbol"].iloc[-8]
top_8_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-8], 2)
top_8_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-8], 2)

top_9_symbol = df_performance_sorted_1y["Symbol"].iloc[-9]
top_9_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-9], 2)
top_9_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-9], 2)

top_10_symbol = df_performance_sorted_1y["Symbol"].iloc[-10]
top_10_perc_change = round(df_performance_sorted_1y["Percent Change 1h (%)"].iloc[-10], 2)
top_10_volume_to_marketcap = round(df_performance_sorted_1y["Volume to MarketCap Ratio"].iloc[-10], 2)

best_1y = f"#Cryptos Bottom-10! 1hour % & Ranking! \n" 
best_1y += f"1 ${top_1_symbol} {top_1_perc_change} % -> {top_1_volume_to_marketcap}\n"
best_1y += f"2 ${top_2_symbol} {top_2_perc_change} % -> {top_2_volume_to_marketcap}\n"
best_1y += f"3 ${top_3_symbol} {top_3_perc_change} % -> {top_3_volume_to_marketcap}\n"
best_1y += f"4 ${top_4_symbol} {top_4_perc_change} % -> {top_4_volume_to_marketcap}\n"
best_1y += f"5 ${top_5_symbol} {top_5_perc_change} % -> {top_5_volume_to_marketcap}\n"
best_1y += f"6 ${top_6_symbol} {top_6_perc_change} % -> {top_6_volume_to_marketcap}\n"
best_1y += f"7 ${top_7_symbol} {top_7_perc_change} % -> {top_7_volume_to_marketcap}\n"
best_1y += f"8 ${top_8_symbol} {top_8_perc_change} % -> {top_8_volume_to_marketcap}\n"
best_1y += f"9 ${top_9_symbol} {top_9_perc_change} % -> {top_9_volume_to_marketcap}\n"
best_1y += f"10 ${top_10_symbol} {top_10_perc_change} % -> {top_10_volume_to_marketcap}\n"

best_1y = best_1y + "#gems"



print(best_1y)



len(best_1y)







post(best_1y)



















