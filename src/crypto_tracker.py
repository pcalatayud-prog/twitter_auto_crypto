import yfinance as yf
import requests
from datetime import datetime, timedelta
from config.api_keys import CoinMarketCapCredentials
from config.constants import Emojis
import pandas as pd
from typing import Dict, Tuple


class CryptoTracker:
    def __init__(self, symbol: str):
        self.symbol = symbol
        if symbol == 'ADA-USD':
            self.cmc_symbol = 'ADA'
            self.yf_symbol = 'ADA-USD'
            self.is_ada = True
            self.is_trump = False
        elif symbol == 'BTC-USD':
            self.cmc_symbol = 'BTC'
            self.yf_symbol = 'BTC-USD'
            self.is_ada = False
            self.is_trump = False
        elif symbol == 'TRUMP-USD':
            self.cmc_symbol = 'TRUMP'
            self.yf_symbol = 'TRUMP-USD'
            self.is_ada = False
            self.is_trump = True
        self.historical_data = None
        self._initialize_api()

    def _initialize_api(self) -> None:
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CoinMarketCapCredentials.API_KEY,
        }

    def get_current_data(self) -> Dict:
        """Get current price and changes from CoinMarketCap."""
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {'symbol': self.cmc_symbol, 'convert': 'USD'}

        response = requests.get(url, headers=self.headers, params=parameters)
        return response.json()['data'][self.cmc_symbol]

    def get_historical_data(self) -> pd.DataFrame:
        """Get historical price data from Yahoo Finance."""
        coin_data = yf.Ticker(self.yf_symbol)
        self.historical_data = coin_data.history(period='max', interval='1d')
        return self.historical_data

    def get_eur_price(self, usd_price: float) -> float:
        """Convert USD price to EUR using current exchange rate."""
        eur_usd = yf.Ticker('EURUSD=X')
        exchange_rate = eur_usd.history(period='1d')['Close'].iloc[-1]
        return round(usd_price / exchange_rate, 2)

    def format_price_change(self, change: float, period: str) -> str:
        """Format price change with emoji and period."""
        emoji = Emojis.GREEN_CIRCLE if change > 0 else Emojis.RED_CIRCLE
        sign = '+' if change > 0 else ''
        return f"{emoji}{period} -> {sign}{change} %"

    def format_price(self, price: float) -> str:
        """Format price based on coin type."""
        if self.is_ada or self.is_trump:
            return f"{price:,.2f}"  # Using 4 decimal places for TRUMP token
        else:
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
                returns[period] = round(((current_price - historical_price) / historical_price) * 100, 2)
            except:
                returns[period] = 0  # Handle case where historical data isn't available

        return returns

    def get_ath_data(self) -> Tuple[float, datetime, float]:
        """Get ATH data including price, date, and EUR equivalent."""
        max_price = self.historical_data['High'].max()
        ath_date = self.historical_data['High'].idxmax()
        ath_eur = self.get_eur_price(max_price)
        return max_price, ath_date, ath_eur

    def run(self) -> str:
        """Generate a complete price report."""
        try:
            # Get all necessary data
            current_data = self.get_current_data()
            historical_data = self.get_historical_data()

            # Current prices
            price_usd = round(current_data['quote']['USD']['price'], 4)  # 4 decimal places for TRUMP
            price_eur = self.get_eur_price(price_usd)

            # Get all time period changes
            changes = {
                '1h': current_data['quote']['USD']['percent_change_1h'],
                '24h': current_data['quote']['USD']['percent_change_24h'],
                '7d': current_data['quote']['USD']['percent_change_7d'],
                '30d': current_data['quote']['USD']['percent_change_30d'],
                '90d': current_data['quote']['USD']['percent_change_90d']
            }

            # Add historical returns
            historical_returns = self.calculate_historical_returns()
            changes.update(historical_returns)

            # Get ATH data
            ath_price, ath_date, ath_eur = self.get_ath_data()

            # Format the report
            # Get coin rank
            rank = current_data['cmc_rank']

            if self.cmc_symbol == 'BTC':
                symbol_tag = '#BTC #Bitcoin'
            elif self.cmc_symbol == 'ADA':
                symbol_tag = '#ADA #Cardano'
            else:
                symbol_tag = '#TRUMP'

            report = [
                f"{symbol_tag} (Rank #{rank})",
                f"{self.format_price(price_usd)} $  &  {self.format_price(price_eur)} €"
            ]

            # Add all period changes

            report.append(f"ATH -> {ath_date.strftime('%d/%m/%Y')} -> {self.format_price(ath_price)} $  &  {self.format_price(ath_eur)} €")
            
            for period, change in changes.items():
                
                report.append(self.format_price_change(round(change, 2), period))
            
            report.append("@Grok, ¿cómo afectara el historial de Bitcoin a su futuro? 🚀📉"")

            return '\n'.join(report)
        except Exception as e:
            print(f"Error generating report: {e}")
            return ""


if __name__ == "__main__":
    # Test all cryptocurrencies
    for symbol in ['BTC-USD', 'ADA-USD', 'TRUMP-USD']:
        tracker = CryptoTracker(symbol)
        report = tracker.run()
        print(f"{symbol} Report:")
        print(report)
        print("\n" + "=" * 50 + "\n")
