#!/usr/bin/env python
# coding: utf-8

# In[29]:


import requests
import tweepy
import pandas as pd


#------------------bitcoin account -------------------#
import requests
import tweepy
import pandas as pd
import yfinance as yf


def post_2(text: str):
    
    access_token = "1795765251423543296-YQ3pLG6ltWwjml2DmKGkx2KwkQoAw2"

    access_token_secret = "Bk2UrP2dBlghvqubEMFywpPW4czx4JM7VFKFX16G6fQ8X"

    bearer = "AAAAAAAAAAAAAAAAAAAAAAkiuAEAAAAAMM6iOgVusW7HQK8kryygU7%2BFL70%3DkxD49c3YilKNb3l8Pn5VV0PzlyCBWnj1YXm7HmSnanFpKGUrLx"

    api_key = "XVJ6Y57C916dObzbAKjGyIoB1"

    api_key_secret = "5EEDsvh6lFBBJskYTVSppVxvVnTWZ8DIcZ2usqNBXWCm2CSNnv"
    
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

# Constants
green = "\U0001F7E2"
red = "\U0001F534"

#Retriving from CoinMarket
API_KEY = "f30a7111-fdbc-4608-a34d-ef8a426ca0ad"
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
parameters = {
    'symbol': 'BTC',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

response = requests.get(url, headers=headers, params=parameters)
data = response.json()

#Retriving EUR/USD
def get_eur_usd_exchange_rate(price):
    # Ticker for EUR/USD exchange rate
    ticker = 'EURUSD=X'
    
    # Get the ticker data
    eur_usd = yf.Ticker(ticker)
    
    # Fetch the current price
    exchange_rate = eur_usd.history(period='1d')['Close'].iloc[-1]
    
    return round((price/exchange_rate),2)

#Retriving Bitcoin 
# Define the ticker symbol for Bitcoin
ticker_symbol = 'BTC-USD'

# Fetch the historical data
bitcoin_data = yf.Ticker(ticker_symbol)

# Define the period and interval of the historical data
# Options for period: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
# Options for interval: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'
historical_data = bitcoin_data.history(period='max', interval='1d')

from datetime import datetime, timedelta

# Get the current date
current_date = historical_data.index[-1]

# Calculate the dates for one year ago and five years ago
one_year_ago = current_date - timedelta(days=365)
five_years_ago = current_date - timedelta(days=365 * 5)
ten_years_ago = current_date - timedelta(days=365 * 10)


# Find the closest dates manually
def find_closest_date(data, target_date):
    closest_date = min(data.index, key=lambda d: abs(d - target_date))
    return closest_date

one_year_ago_closest_date = find_closest_date(historical_data, one_year_ago)
five_years_ago_closest_date = find_closest_date(historical_data, five_years_ago)
ten_years_ago_closest_date = find_closest_date(historical_data, ten_years_ago)

# Get the rows for the closest dates
one_year_ago_row = historical_data.loc[one_year_ago_closest_date]
five_years_ago_row = historical_data.loc[five_years_ago_closest_date]
ten_years_ago_row = historical_data.loc[ten_years_ago_closest_date]

# Print the results
#print(f"Row from one year ago (closest to {one_year_ago.date()}):\n{one_year_ago_row}\n")
#print(f"Row from five years ago (closest to {five_years_ago.date()}):\n{five_years_ago_row}\n")
#print(f"Row from ten years ago (closest to {ten_years_ago.date()}):\n{ten_years_ago_row}\n")
#---------------#
#---------------#
#---------------#
price_usd = round(data["data"]["BTC"]["quote"]["USD"]["price"],2)
price=price_usd
print(price_usd)
#---------------#
#---------------#
#---------------#
price_eur = get_eur_usd_exchange_rate(price_usd)
print(price_eur)

price_usd = str(price_usd)
price_eur = str(price_eur)

def format_number_with_commas(number_str):
    # Split the number into integer and decimal parts
    if '.' in number_str:
        integer_part, decimal_part = number_str.split('.')
    else:
        integer_part, decimal_part = number_str, ''

    # Add commas to the integer part
    integer_part_with_commas = "{:,}".format(int(integer_part))

    # Combine the integer part with the decimal part
    if decimal_part:
        return f"{integer_part_with_commas}.{decimal_part}"
    else:
        return integer_part_with_commas

price_usd = format_number_with_commas(price_usd)
price_eur = format_number_with_commas(price_eur)

#------------#
one_year_ago_row_price = one_year_ago_row["Close"]
one_year_ago_row_price
#-----------#
five_years_ago_price = five_years_ago_row["Close"]
five_years_ago_price
#-----------#
ten_years_ago_price = ten_years_ago_row["Close"]
ten_years_ago_price
#----------#
price_change_1h = round(data["data"]["BTC"]["quote"]["USD"]["percent_change_1h"],2)
if price_change_1h>0:
    
    price_change_1h = str(price_change_1h) 
    
    price_change_1h = green + "1h -> +" + price_change_1h + " %"
    
    print(price_change_1h)
    
else:
    price_change_1h = str(price_change_1h) 
    
    price_change_1h = red + "1h -> " + price_change_1h + " %"
    
    print(price_change_1h)


price_change_24h = round(data["data"]["BTC"]["quote"]["USD"]["percent_change_24h"],2)
if price_change_24h>0:
    
    price_change_24h = str(price_change_24h) 
    
    price_change_24h = green + "24h -> +" + price_change_24h + " %"
    
    print(price_change_24h)
    
else:
    price_change_24h = str(price_change_24h) 
    
    price_change_24h = red + "24h -> " + price_change_24h + " %"
    
    print(price_change_24h)

percent_change_7d = round(data["data"]["BTC"]["quote"]["USD"]["percent_change_7d"],2)
if percent_change_7d>0:
    
    percent_change_7d = str(percent_change_7d) 
    
    percent_change_7d = green + "7d -> +" + percent_change_7d + " %"
    
    print(percent_change_7d)
    
else:
    percent_change_7d = str(percent_change_7d) 
    
    percent_change_7d = red + "7d -> " + percent_change_7d + " %"
    
    print(percent_change_7d)

percent_change_30d = round(data["data"]["BTC"]["quote"]["USD"]["percent_change_30d"],2)
if percent_change_30d>0:
    
    percent_change_30d = str(percent_change_30d) 
    
    percent_change_30d = green + "30d -> +" + percent_change_30d + " %"
    
    print(percent_change_30d)
    
else:
    percent_change_30d = str(percent_change_30d) 
    
    percent_change_30d = red + "30d -> " + percent_change_30d + " %"
    
    print(percent_change_30d)

percent_change_90d = round(data["data"]["BTC"]["quote"]["USD"]["percent_change_90d"],2)
if percent_change_90d>0:
    
    percent_change_90d = str(percent_change_90d) 
    
    percent_change_90d = green + "90d -> +" + percent_change_90d + " %"
    
    print(percent_change_90d)
    
else:
    percent_change_90d = str(percent_change_90d) 
    
    percent_change_90d = red + "90d -> " + percent_change_90d + " %"
    
    print(percent_change_90d)

percent_change_1y = round(100*(price-one_year_ago_row_price)/one_year_ago_row_price,2)
if percent_change_1y>0:
    
    percent_change_1y = str(percent_change_1y) 
    
    percent_change_1y = green + "1y -> +" + percent_change_1y + " %"
    
    print(percent_change_1y)
    
else:
    percent_change_1y = str(percent_change_1y) 
    
    percent_change_1y = red + "1y -> " + percent_change_1y + " %"
    
    print(percent_change_1y)

percent_change_5y = round(100*(price-five_years_ago_price)/five_years_ago_price,2)
if percent_change_5y>0:
    
    percent_change_5y = str(percent_change_5y) 
    
    percent_change_5y = green + "5y -> +" + percent_change_5y + " %"
    
    print(percent_change_5y)
    
else:
    percent_change_5y = str(percent_change_5y) 
    
    percent_change_5y = red + "5y -> " + percent_change_5y + " %"
    
    print(percent_change_5y)
    
percent_change_10y = round(100*(price-ten_years_ago_price)/ten_years_ago_price,2)
if percent_change_10y>0:
    
    percent_change_10y = str(percent_change_10y) 
    
    percent_change_10y = green + "10y -> +" + percent_change_10y + " %"
    
    print(percent_change_10y)
    
else:
    percent_change_10y = str(percent_change_10y) 
    
    percent_change_10y = red + "10y -> " + percent_change_10y + " %"
    
    print(percent_change_10y)

# percent_change_10y = format_number_with_commas(percent_change_10y)
# percent_change_5y = format_number_with_commas(percent_change_5y)
    
    
max_value = round(historical_data['High'].max(),2)
max_index = historical_data['High'].idxmax()
max_value_eur = round(get_eur_usd_exchange_rate(max_value),2)
formatted_date = max_index.strftime('%d/%m/%Y')

line_0 = f'ATH -> {formatted_date} -> {max_value} $  &  {max_value_eur} €'

    
line = f"#BTC #Bitcoin" + "\n"
line = line + price_usd + " $  &  " + price_eur + " €\n"
line = line + line_0 + "\n"
line = line + price_change_1h + "\n"
line = line + price_change_24h + "\n"
line = line + percent_change_7d + "\n"
line = line + percent_change_30d + "\n"
line = line + percent_change_90d + "\n"
line = line + percent_change_1y + "\n"
line = line + percent_change_5y + "\n"
line = line + percent_change_10y + "\n"

line = line + "#crypto #DeFi #blockchain #investing"

#------------#
print("\n\n\n\n\n")
print(len(line))
print("\n\n\n\n\n")
print(line)
post_2(line)


#------------------ada account -------------------#
import requests
import tweepy
import pandas as pd
import yfinance as yf


def post_ada(text: str):
    
    access_token = "1855621600214712320-kk4ECHBKFH3IfVJ1tV9XIaAlloQJiB"

    access_token_secret = "KclOgTpBOEjvS7y3VrSHex0SgPlbWq1HGJwCc0i8ixbgO"

    bearer = 'AAAAAAAAAAAAAAAAAAAAAKKQwwEAAAAAPfO3c6t12fOlm5mwCJWsG1SRUY0%3D8o2AOBSnIN2A4jN8y85Fzojqe6fWYybr5Ms6JkaLoiuC6fA1ZT'
    
    api_key = "lwt0MMcKkeAl9YEnOygQlTTER"

    api_key_secret = "X43Quom00ZyfDKIcd2gaXzLJozcdii5YeBEb17tfp9c2QBU6TL"

    
    
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


# Constants
green = "\U0001F7E2"
red = "\U0001F534"

#Retriving from CoinMarket
API_KEY = "f30a7111-fdbc-4608-a34d-ef8a426ca0ad"
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
parameters = {
    'symbol': 'ADA',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

response = requests.get(url, headers=headers, params=parameters)
data = response.json()

#Retriving EUR/USD
def get_eur_usd_exchange_rate(price):
    # Ticker for EUR/USD exchange rate
    ticker = 'EURUSD=X'
    
    # Get the ticker data
    eur_usd = yf.Ticker(ticker)
    
    # Fetch the current price
    exchange_rate = eur_usd.history(period='1d')['Close'].iloc[-1]
    
    return round((price/exchange_rate),2)

#Retriving Bitcoin 
# Define the ticker symbol for Bitcoin
ticker_symbol = 'ADA-USD'

# Fetch the historical data
bitcoin_data = yf.Ticker(ticker_symbol)

# Define the period and interval of the historical data
# Options for period: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
# Options for interval: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'
historical_data = bitcoin_data.history(period='max', interval='1d')

from datetime import datetime, timedelta

# Get the current date
current_date = historical_data.index[-1]

# Calculate the dates for one year ago and five years ago
one_year_ago = current_date - timedelta(days=365)
five_years_ago = current_date - timedelta(days=365 * 5)
ten_years_ago = current_date - timedelta(days=365 * 10)


# Find the closest dates manually
def find_closest_date(data, target_date):
    closest_date = min(data.index, key=lambda d: abs(d - target_date))
    return closest_date

one_year_ago_closest_date = find_closest_date(historical_data, one_year_ago)
five_years_ago_closest_date = find_closest_date(historical_data, five_years_ago)
ten_years_ago_closest_date = find_closest_date(historical_data, ten_years_ago)

# Get the rows for the closest dates
one_year_ago_row = historical_data.loc[one_year_ago_closest_date]
five_years_ago_row = historical_data.loc[five_years_ago_closest_date]
ten_years_ago_row = historical_data.loc[ten_years_ago_closest_date]

# Print the results
#print(f"Row from one year ago (closest to {one_year_ago.date()}):\n{one_year_ago_row}\n")
#print(f"Row from five years ago (closest to {five_years_ago.date()}):\n{five_years_ago_row}\n")
#print(f"Row from ten years ago (closest to {ten_years_ago.date()}):\n{ten_years_ago_row}\n")
#---------------#
#---------------#
#---------------#
price_usd = round(data["data"]["ADA"]["quote"]["USD"]["price"],2)
price=price_usd
print(price_usd)
#---------------#
#---------------#
#---------------#
price_eur = get_eur_usd_exchange_rate(price_usd)
print(price_eur)

price_usd = str(price_usd)
price_eur = str(price_eur)

def format_number_with_commas(number_str):
    # Split the number into integer and decimal parts
    if '.' in number_str:
        integer_part, decimal_part = number_str.split('.')
    else:
        integer_part, decimal_part = number_str, ''

    # Add commas to the integer part
    integer_part_with_commas = "{:,}".format(int(integer_part))

    # Combine the integer part with the decimal part
    if decimal_part:
        return f"{integer_part_with_commas}.{decimal_part}"
    else:
        return integer_part_with_commas

price_usd = format_number_with_commas(price_usd)
price_eur = format_number_with_commas(price_eur)

#------------#
one_year_ago_row_price = one_year_ago_row["Close"]
one_year_ago_row_price
#-----------#
five_years_ago_price = five_years_ago_row["Close"]
five_years_ago_price
#-----------#
ten_years_ago_price = ten_years_ago_row["Close"]
ten_years_ago_price
#----------#
price_change_1h = round(data["data"]["ADA"]["quote"]["USD"]["percent_change_1h"],2)
if price_change_1h>0:
    
    price_change_1h = str(price_change_1h) 
    
    price_change_1h = green + "1h -> +" + price_change_1h + " %"
    
    print(price_change_1h)
    
else:
    price_change_1h = str(price_change_1h) 
    
    price_change_1h = red + "1h -> " + price_change_1h + " %"
    
    print(price_change_1h)


price_change_24h = round(data["data"]["ADA"]["quote"]["USD"]["percent_change_24h"],2)
if price_change_24h>0:
    
    price_change_24h = str(price_change_24h) 
    
    price_change_24h = green + "24h -> +" + price_change_24h + " %"
    
    print(price_change_24h)
    
else:
    price_change_24h = str(price_change_24h) 
    
    price_change_24h = red + "24h -> " + price_change_24h + " %"
    
    print(price_change_24h)

percent_change_7d = round(data["data"]["ADA"]["quote"]["USD"]["percent_change_7d"],2)
if percent_change_7d>0:
    
    percent_change_7d = str(percent_change_7d) 
    
    percent_change_7d = green + "7d -> +" + percent_change_7d + " %"
    
    print(percent_change_7d)
    
else:
    percent_change_7d = str(percent_change_7d) 
    
    percent_change_7d = red + "7d -> " + percent_change_7d + " %"
    
    print(percent_change_7d)

percent_change_30d = round(data["data"]["ADA"]["quote"]["USD"]["percent_change_30d"],2)
if percent_change_30d>0:
    
    percent_change_30d = str(percent_change_30d) 
    
    percent_change_30d = green + "30d -> +" + percent_change_30d + " %"
    
    print(percent_change_30d)
    
else:
    percent_change_30d = str(percent_change_30d) 
    
    percent_change_30d = red + "30d -> " + percent_change_30d + " %"
    
    print(percent_change_30d)

percent_change_90d = round(data["data"]["ADA"]["quote"]["USD"]["percent_change_90d"],2)
if percent_change_90d>0:
    
    percent_change_90d = str(percent_change_90d) 
    
    percent_change_90d = green + "90d -> +" + percent_change_90d + " %"
    
    print(percent_change_90d)
    
else:
    percent_change_90d = str(percent_change_90d) 
    
    percent_change_90d = red + "90d -> " + percent_change_90d + " %"
    
    print(percent_change_90d)

percent_change_1y = round(100*(price-one_year_ago_row_price)/one_year_ago_row_price,2)
if percent_change_1y>0:
    
    percent_change_1y = str(percent_change_1y) 
    
    percent_change_1y = green + "1y -> +" + percent_change_1y + " %"
    
    print(percent_change_1y)
    
else:
    percent_change_1y = str(percent_change_1y) 
    
    percent_change_1y = red + "1y -> " + percent_change_1y + " %"
    
    print(percent_change_1y)

percent_change_5y = round(100*(price-five_years_ago_price)/five_years_ago_price,2)
if percent_change_5y>0:
    
    percent_change_5y = str(percent_change_5y) 
    
    percent_change_5y = green + "5y -> +" + percent_change_5y + " %"
    
    print(percent_change_5y)
    
else:
    percent_change_5y = str(percent_change_5y) 
    
    percent_change_5y = red + "5y -> " + percent_change_5y + " %"
    
    print(percent_change_5y)
    
percent_change_10y = round(100*(price-ten_years_ago_price)/ten_years_ago_price,2)
if percent_change_10y>0:
    
    percent_change_10y = str(percent_change_10y) 
    
    percent_change_10y = green + "10y -> +" + percent_change_10y + " %"
    
    print(percent_change_10y)
    
else:
    percent_change_10y = str(percent_change_10y) 
    
    percent_change_10y = red + "10y -> " + percent_change_10y + " %"
    
    print(percent_change_10y)

# percent_change_10y = format_number_with_commas(percent_change_10y)
# percent_change_5y = format_number_with_commas(percent_change_5y)
    
    
max_value = round(historical_data['High'].max(),2)
max_index = historical_data['High'].idxmax()
max_value_eur = round(get_eur_usd_exchange_rate(max_value),2)
formatted_date = max_index.strftime('%d/%m/%Y')

line_0 = f'ATH -> {formatted_date} -> {max_value} $  &  {max_value_eur} €'

    
line = f"#ADA #Cardano" + "\n"
line = line + price_usd + " $  &  " + price_eur + " €\n"
line = line + line_0 + "\n"
line = line + price_change_1h + "\n"
line = line + price_change_24h + "\n"
line = line + percent_change_7d + "\n"
line = line + percent_change_30d + "\n"
line = line + percent_change_90d + "\n"
line = line + percent_change_1y + "\n"
line = line + percent_change_5y + "\n"
line = line + percent_change_10y + "\n"

line = line + "#crypto #DeFi #blockchain #investing"

#------------#

post_ada(line)

#critpo alert news



# In[30]:


access_token = "1742678488459497472-HXtM9OzHTPWGxkfjmImYnp90BlZ1ml"

access_token_secret = "dewtRu0YP6KdlCA4IzNkUfzQoChv4s6YhnQhFTRizKnR2"

bearer = "AAAAAAAAAAAAAAAAAAAAAPUOrwEAAAAA3tPnHW%2FpNuVoJ8UPHM707hUkv8Q%3Ds1aKKU5HpsiK17zd4oZmjTsAsvbQ2YyGVb1tFrvtJ9RzOiOLHg"

api_key = "n34SJHko4ZB6TQU9CzqC3G3i5"

api_key_secret = "QIXDDf58EduQkiHiY064QOEeM2shtpsGkIOTNIyy2w9cykcTM4"


# In[31]:


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


# In[32]:


api = "f30a7111-fdbc-4608-a34d-ef8a426ca0ad"
API_KEY = api


# In[33]:


# Replace 'YOUR_API_KEY' with your actual API key
#API_KEY = 'YOUR_API_KEY'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

def get_all_crypto_data(limit=200):
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


# In[34]:


# Extract relevant information into a DataFrame
crypto_df = pd.DataFrame({
    'Name': [crypto['name'] for crypto in crypto_data],
    'Symbol': [crypto['symbol'] for crypto in crypto_data],
    'Price (USD)': [crypto['quote']['USD']['price'] for crypto in crypto_data],
    'Market Cap (USD)': [crypto['quote']['USD']['market_cap'] for crypto in crypto_data],
    'Volume 24h (USD)': [crypto['quote']['USD']['volume_24h'] for crypto in crypto_data],
    'Percent Change 24h (%)': [crypto['quote']['USD']['percent_change_24h'] for crypto in crypto_data]
})

# Calculate volume-to-marketcap ratio
crypto_df['Volume to MarketCap Ratio'] = crypto_df['Volume 24h (USD)'] / crypto_df['Market Cap (USD)']


# In[35]:


crypto_df


# In[36]:


# Sort the DataFrame by the Percent Change 24h column
sorted_crypto_df = crypto_df.sort_values(by='Percent Change 24h (%)', ascending=True)
# Display the sorted DataFrame
sorted_crypto_df


# In[37]:


sorted_crypto_df.tail(10)


# In[38]:


sorted_crypto_df.head(10)


# In[39]:


df_performance_sorted_1y = sorted_crypto_df


# In[40]:


top_1_symbol = df_performance_sorted_1y["Symbol"].iloc[-1]
top_1_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-1], 2)
top_1_volume_to_marketcap = round(df_performance_sorted_1y.index[-1], 2)

top_2_symbol = df_performance_sorted_1y["Symbol"].iloc[-2]
top_2_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-2], 2)
top_2_volume_to_marketcap = round(df_performance_sorted_1y.index[-2], 2)

top_3_symbol = df_performance_sorted_1y["Symbol"].iloc[-3]
top_3_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-3], 2)
top_3_volume_to_marketcap = round(df_performance_sorted_1y.index[-3], 2)

top_4_symbol = df_performance_sorted_1y["Symbol"].iloc[-4]
top_4_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-4], 2)
top_4_volume_to_marketcap = round(df_performance_sorted_1y.index[-4], 2)

top_5_symbol = df_performance_sorted_1y["Symbol"].iloc[-5]
top_5_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-5], 2)
top_5_volume_to_marketcap = round(df_performance_sorted_1y.index[-5], 2)

top_6_symbol = df_performance_sorted_1y["Symbol"].iloc[-6]
top_6_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-6], 2)
top_6_volume_to_marketcap = round(df_performance_sorted_1y.index[-6], 2)

top_7_symbol = df_performance_sorted_1y["Symbol"].iloc[-7]
top_7_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-7], 2)
top_7_volume_to_marketcap = round(df_performance_sorted_1y.index[-7], 2)

top_8_symbol = df_performance_sorted_1y["Symbol"].iloc[-8]
top_8_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-8], 2)
top_8_volume_to_marketcap = round(df_performance_sorted_1y.index[-8], 2)

top_9_symbol = df_performance_sorted_1y["Symbol"].iloc[-9]
top_9_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-9], 2)
top_9_volume_to_marketcap = round(df_performance_sorted_1y.index[-9], 2)

top_10_symbol = df_performance_sorted_1y["Symbol"].iloc[-10]
top_10_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[-10], 2)
top_10_volume_to_marketcap = round(df_performance_sorted_1y.index[-10], 2)

best_1y = f"#Crypto Top-10! 24-hour % & Rank! \n" 
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


# In[ ]:





# In[41]:


print(best_1y)


# In[42]:


len(best_1y)


# In[43]:


post(best_1y)


# In[ ]:





# In[ ]:





# In[44]:


top_1_symbol = df_performance_sorted_1y["Symbol"].iloc[0]
top_1_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[0], 2)
top_1_volume_to_marketcap = round(df_performance_sorted_1y.index[0], 2)

top_2_symbol = df_performance_sorted_1y["Symbol"].iloc[1]
top_2_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[1], 2)
top_2_volume_to_marketcap = round(df_performance_sorted_1y.index[1], 2)

top_3_symbol = df_performance_sorted_1y["Symbol"].iloc[2]
top_3_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[2], 2)
top_3_volume_to_marketcap = round(df_performance_sorted_1y.index[2], 2)

top_4_symbol = df_performance_sorted_1y["Symbol"].iloc[3]
top_4_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[3], 2)
top_4_volume_to_marketcap = round(df_performance_sorted_1y.index[3], 2)

top_5_symbol = df_performance_sorted_1y["Symbol"].iloc[4]
top_5_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[4], 2)
top_5_volume_to_marketcap = round(df_performance_sorted_1y.index[4], 2)

top_6_symbol = df_performance_sorted_1y["Symbol"].iloc[5]
top_6_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[5], 2)
top_6_volume_to_marketcap = round(df_performance_sorted_1y.index[5], 2)

top_7_symbol = df_performance_sorted_1y["Symbol"].iloc[6]
top_7_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[6], 2)
top_7_volume_to_marketcap = round(df_performance_sorted_1y.index[6], 2)

top_8_symbol = df_performance_sorted_1y["Symbol"].iloc[7]
top_8_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[7], 2)
top_8_volume_to_marketcap = round(df_performance_sorted_1y.index[7], 2)

top_9_symbol = df_performance_sorted_1y["Symbol"].iloc[8]
top_9_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[8], 2)
top_9_volume_to_marketcap = round(df_performance_sorted_1y.index[8], 2)

top_10_symbol = df_performance_sorted_1y["Symbol"].iloc[9]
top_10_perc_change = round(df_performance_sorted_1y["Percent Change 24h (%)"].iloc[9], 2)
top_10_volume_to_marketcap = round(df_performance_sorted_1y.index[9], 2)

best_1y = f"#Crypto Bottom-10! 24-hour % & Rank! \n" 
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


# In[ ]:





# In[45]:


print(best_1y)


# In[46]:


len(best_1y)


# In[47]:


# post(best_1y)
