# src/market_analyzer.py

import pandas as pd
import requests
import sys
import os
import json

# Add the project root to the path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.api_keys import CoinMarketCapCredentials
from typing import Tuple, Optional
from config.constants import Emojis
from loguru import logger

class MarketAnalyzer:
    def __init__(self):
        api_key = CoinMarketCapCredentials.API_KEY
        logger.info(f"Initializing MarketAnalyzer with API key: {'*****' + api_key[-4:] if api_key else 'None'}")
        
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }
        self.df = None

    def get_all_crypto_data(self, limit=150) -> Optional[dict]:
        """Fetch data for top cryptocurrencies."""
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {'limit': limit}
        
        logger.info(f"Fetching top {limit} cryptocurrencies data from CoinMarketCap")
        
        try:
            response = requests.get(url, headers=self.headers, params=parameters)
            logger.debug(f"API Response status code: {response.status_code}")
            
            data = response.json()
            
            # Log response structure for debugging
            logger.debug(f"API Response keys: {list(data.keys())}")
            
            if 'status' in data and data['status']['error_code'] != 0:
                error_msg = data['status'].get('error_message', 'Unknown error')
                logger.error(f"API Error: {error_msg}")
                return None
                
            if 'data' not in data:
                logger.error(f"Missing 'data' in API response: {json.dumps(data)[:500]}")
                return None
                
            logger.info(f"Successfully fetched data for {len(data['data'])} cryptocurrencies")
            return data['data']
            
        except Exception as e:
            logger.exception(f"Error fetching crypto data: {e}")
            return None

    def create_market_dataframe(self, crypto_data: dict) -> pd.DataFrame:
        """Create a DataFrame with market data."""
        try:
            df = pd.DataFrame({
                'Name': [crypto['name'] for crypto in crypto_data],
                'Symbol': [crypto['symbol'] for crypto in crypto_data],
                'Rank': [crypto['cmc_rank'] for crypto in crypto_data],
                'Price (USD)': [crypto['quote']['USD']['price'] for crypto in crypto_data],
                'Market Cap (USD)': [crypto['quote']['USD']['market_cap'] for crypto in crypto_data],
                'Volume 24h (USD)': [crypto['quote']['USD']['volume_24h'] for crypto in crypto_data],
                'Percent Change 24h (%)': [crypto['quote']['USD']['percent_change_24h'] for crypto in crypto_data]
            })

            df['Volume to MarketCap Ratio'] = df['Volume 24h (USD)'] / df['Market Cap (USD)']
            return df
        except Exception as e:
            print(f"Error creating DataFrame: {e}")
            return pd.DataFrame()

    def generate_top_movers_report(self, df: pd.DataFrame) -> str:
        """Generate a report of top movers (gainers or losers)."""
        try:
            df['abs'] = df['Percent Change 24h (%)'].abs()
            sorted_df = df.sort_values(by='abs', ascending=False)

            top_coins = sorted_df.head(10)
            report = [f"#Crypto 10-Movers 24-hour & rank!"]

            for i in range(10):
                symbol = sorted_df['Symbol'].iloc[i]
                rank = sorted_df['Rank'].iloc[i]
                change = round(sorted_df['Percent Change 24h (%)'].iloc[i])
                emoji = Emojis.GREEN_CIRCLE if change > 0 else Emojis.RED_CIRCLE

                report.append(f"{i+1}.{emoji} ${symbol} -> {change}% ({rank})")

            report.append("What do you think @Grok?")
            
            return '\n'.join(report)
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return ""

    def run(self) -> Tuple[str, str]:
        """
        Main method to run the entire analysis process.
        Returns tuple of (top_gainers_report, top_losers_report)
        """
        try:
            # Get crypto data
            crypto_data = self.get_all_crypto_data()
            if not crypto_data:
                return "", ""

            # Create DataFrame
            self.df = self.create_market_dataframe(crypto_data)
            if self.df.empty:
                return "", ""

            # Generate reports
            movers = self.generate_top_movers_report(self.df)

            return movers

        except Exception as e:
            print(f"Error in market analysis run: {e}")
            return "", ""


if __name__ == "__main__":
    market = MarketAnalyzer()
    movers = market.run()
    print(movers)
    print(len(movers))
