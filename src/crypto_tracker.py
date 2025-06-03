import yfinance as yf
import requests
import sys
import json
from datetime import datetime, timedelta
import os

# Add the project root to the path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.api_keys import CoinMarketCapCredentials
from config.constants import Emojis
import pandas as pd
from typing import Dict, Tuple, Optional
from loguru import logger
from src.bitcoin_blocks_call import get_bitcoin_block_height, estimate_halving_end, format_twitter_message


class CryptoTracker:
    def __init__(self, symbol: str):
        self.symbol = symbol
        # We're only supporting BTC now
        self.cmc_symbol = 'BTC'
        self.yf_symbol = 'BTC-USD'
        self.historical_data = None
        self._initialize_api()

    def _initialize_api(self) -> None:
        api_key = CoinMarketCapCredentials.API_KEY
        logger.info(f"Initializing API with key: {'*****' + api_key[-4:] if api_key else 'None'}")
        
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

    def get_current_data(self) -> Dict:
        """Get current price and changes from CoinMarketCap."""
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {'symbol': self.cmc_symbol, 'convert': 'USD'}
        
        logger.info(f"Fetching data for {self.cmc_symbol} from CoinMarketCap")
        
        try:
            response = requests.get(url, headers=self.headers, params=parameters)
            response_json = response.json()
            
            # Log the response structure
            logger.debug(f"API Response status code: {response.status_code}")
            logger.debug(f"API Response keys: {list(response_json.keys())}")
            
            if 'status' in response_json and response_json['status']['error_code'] != 0:
                error_msg = response_json['status'].get('error_message', 'Unknown error')
                logger.error(f"API Error: {error_msg}")
                raise Exception(f"API Error: {error_msg}")
                
            if 'data' not in response_json:
                logger.error(f"Missing 'data' in API response: {json.dumps(response_json)[:500]}")
                raise Exception("Missing 'data' in API response")
                
            if self.cmc_symbol not in response_json['data']:
                logger.error(f"Symbol {self.cmc_symbol} not found in response data")
                logger.debug(f"Available symbols: {list(response_json['data'].keys())}")
                raise Exception(f"Symbol {self.cmc_symbol} not found in response")
                
            return response_json['data'][self.cmc_symbol]
            
        except Exception as e:
            logger.exception(f"Error getting current data: {str(e)}")
            raise

    def get_historical_data(self) -> pd.DataFrame:
        """Get historical price data from Yahoo Finance."""
        coin_data = yf.Ticker(self.yf_symbol)
        self.historical_data = coin_data.history(period='max', interval='1d')
        return self.historical_data

    def get_eur_price(self, usd_price: float) -> float:
        """Convert USD price to EUR using current exchange rate."""
        eur_usd = yf.Ticker('EURUSD=X')
        exchange_rate = eur_usd.history(period='1d')['Close'].iloc[-1]
        return round(usd_price / exchange_rate, 1)

    def format_price_change(self, change: float, period: str) -> str:
        """Format price change with emoji and period."""
        emoji = Emojis.GREEN_CIRCLE if change > 0 else Emojis.RED_CIRCLE
        sign = '+' if change > 0 else ''
        return f"{emoji}{period} -> {sign}{change} %"

    def format_price(self, price: float) -> str:
        """Format price based on coin type."""
        return f"{int(price):,}"

    def calculate_historical_returns(self) -> Dict[str, float]:
        """Calculate returns for all time periods."""
        current_date = self.historical_data.index[-1]
        current_price = self.historical_data['Close'].iloc[-1]

        periods = {
            '1y': 365,
            '5y': 365 * 5,
            '10y': 365 * 10
        }

        returns = {}
        for period, days in periods.items():
            try:
                target_date = current_date - timedelta(days=days)
                closest_date = min(self.historical_data.index, key=lambda d: abs(d - target_date))
                historical_price = self.historical_data.loc[closest_date, 'Close']
                returns[period] = round(((current_price - historical_price) / historical_price) * 100, 1)
            except:
                returns[period] = 0  # Handle case where historical data isn't available

        return returns

    def get_ath_data(self) -> Tuple[float, datetime, float]:
        """Get ATH data including price, date, and EUR equivalent."""
        max_price = self.historical_data['High'].max()
        ath_date = self.historical_data['High'].idxmax()
        ath_eur = self.get_eur_price(max_price)
        return max_price, ath_date, ath_eur

    def generate_standard_report(self, data: Dict) -> str:
        """Generate standard Bitcoin price report."""
        current_data = data['current_data']
        price_usd = data['price_usd']
        price_eur = data['price_eur']
        changes = data['changes']
        rank = current_data['cmc_rank']

        report = [
            f"#BTC #Bitcoin (Rank #{rank})",
            f"{self.format_price(price_usd)} $  &  {self.format_price(price_eur)} €"
        ]

        for period, change in changes.items():
            report.append(self.format_price_change(round(change, 2), period))
        
        report.append("@Grok, ¿Como ves bitcoin? 🚀📉")

        return '\n'.join(report)

    def generate_detailed_report(self, data: Dict) -> str:
        """Generate detailed Bitcoin report with supply and volume metrics."""
        current_data = data['current_data']
        price_usd = data['price_usd']
        price_eur = data['price_eur']
        changes = data['changes']
        rank = current_data['cmc_rank']
        ath_price = data['ath_price']
        ath_date = data['ath_date']
        ath_eur = data['ath_eur']
        
        # Extract additional metrics from the data
        circulating_supply = current_data['circulating_supply']
        max_supply = current_data['max_supply']
        supply_percentage = round((circulating_supply / max_supply) * 100,4) if max_supply else 0
        volume_24h = current_data['quote']['USD']['volume_24h']
        market_cap = current_data['quote']['USD']['market_cap']
        volume_to_mcap = (volume_24h / market_cap) * 100 if market_cap else 0

        report = [
            f"#BTC #Bitcoin (Rank #{rank})",
            f"💰 Price: {self.format_price(price_usd)} $ | {self.format_price(price_eur)} €",
            f"🏆 ATH: {self.format_price(ath_price)} $ ({ath_date.strftime('%d/%m/%Y')})"]
        
        # Add supply metrics
        report.append(f"⛏️ Supply -> {round(supply_percentage, 2)}% minado,  {int(circulating_supply):,}/{int(max_supply):,} ")
        
        # Add volume metrics
        report.append(f"💱 24h Volume: ${int(volume_24h/1000000):,}M")
        report.append(f"📈 Vol/MCap: {round(volume_to_mcap, 2)}%")
        
        # Add key period changes
        report.append("🔍 Performance:")
        for period in ['7d', '30d', '90d']:
            if period in changes:
                report.append(self.format_price_change(round(changes[period], 2), period))
        
        report.append("@Grok, que piensas?  🧠🚀")

        return '\n'.join(report)
        
    def generate_blocks_report(self, data: Dict) -> str:
        """Generate Bitcoin report focused on block information and halving."""
        logger.info("Generating Bitcoin blocks report")
        
        # Get the current Bitcoin block height
        block_height = get_bitcoin_block_height()
        if block_height is None:
            logger.error("Failed to fetch Bitcoin block height")
            # Fallback to standard report if block height fetch fails
            return self.generate_standard_report(data)
            
        # Calculate halving-related metrics
        remainder = block_height % 210_000
        halving_end = estimate_halving_end(remainder)
        
        # Create the formatted message
        blocks_report = format_twitter_message(block_height, remainder, halving_end)
        
        # Add the price at the end for context
        current_data = data['current_data']
        price_usd = data['price_usd']
        
        blocks_report += f"\n\nPrice: ${self.format_price(price_usd)} | Rank #{current_data['cmc_rank']}"
        blocks_report += f"\n@Grok, ¿Que precio crees que tendra bitcoin en el siguiente halving en {halving_end}? 🕙⛓️"
        
        return blocks_report

    def run(self, message_type: str = 'standard') -> str:
        """Generate a complete price report with the specified message format."""
        try:
            logger.info("Starting to generate Bitcoin report")
            
            # Get all necessary data
            logger.info("Fetching current price data from CoinMarketCap")
            current_data = self.get_current_data()
            
            logger.info("Fetching historical data from Yahoo Finance")
            historical_data = self.get_historical_data()

            # Current prices
            price_usd = current_data['quote']['USD']['price']
            logger.info(f"Current BTC price: ${price_usd:,.2f}")
            
            logger.info("Converting to EUR")
            price_eur = self.get_eur_price(price_usd)

            # Get all time period changes
            logger.info("Extracting time period changes")
            changes = {
                '1h': current_data['quote']['USD']['percent_change_1h'],
                '24h': current_data['quote']['USD']['percent_change_24h'],
                '7d': current_data['quote']['USD']['percent_change_7d'],
                '30d': current_data['quote']['USD']['percent_change_30d'],
                '90d': current_data['quote']['USD']['percent_change_90d']
            }

            # Add historical returns
            logger.info("Calculating historical returns")
            historical_returns = self.calculate_historical_returns()
            changes.update(historical_returns)

            # Get ATH data
            logger.info("Retrieving ATH data")
            ath_price, ath_date, ath_eur = self.get_ath_data()
            logger.info(f"ATH: ${ath_price:,.2f} on {ath_date}")

            # Prepare data dictionary for report generation
            data = {
                'current_data': current_data,
                'price_usd': price_usd,
                'price_eur': price_eur,
                'changes': changes,
                'ath_price': ath_price,
                'ath_date': ath_date,
                'ath_eur': ath_eur
            }

            # Generate report based on message type
            logger.info(f"Generating {message_type} report")
            if message_type == 'detailed':
                return self.generate_detailed_report(data)
            elif message_type == 'blocks':
                return self.generate_blocks_report(data)
            else:  # standard format
                return self.generate_standard_report(data)
                
        except Exception as e:
            logger.exception(f"Error generating report: {str(e)}")
            return ""


if __name__ == "__main__":
    # Test all message formats for Bitcoin
    tracker = CryptoTracker('BTC-USD')

    import random

    report_type = random.choice(['standard', 'detailed', 'blocks'])
    report = tracker.run(report_type)

    print(f"{report_type.capitalize()} Report:")
    print(report)
    print("\n" + "=" * 50 + "\n")

