# main.py

from src.twitter_client import TwitterClient
from src.crypto_tracker import CryptoTracker
from src.market_analyzer import MarketAnalyzer
import time


def main():
    # Initialize clients
    btc_twitter = TwitterClient(account_type='BTC')
    ada_twitter = TwitterClient(account_type='ADA')
    news_twitter = TwitterClient(account_type='NEWS')

    # Post BTC update
    btc_tracker = CryptoTracker('BTC-USD')
    btc_report = btc_tracker.run()
    btc_twitter.post_tweet(btc_report)

    # Add delay between posts
    time.sleep(2)

    # Post ADA update
    ada_tracker = CryptoTracker('ADA-USD')
    ada_report = ada_tracker.run()
    ada_twitter.post_tweet(ada_report)

    # Add delay between posts
    time.sleep(2)

    # Post market analysis
    analyzer = MarketAnalyzer()
    crypto_data = analyzer.get_all_crypto_data()
    if crypto_data:
        market_df = analyzer.create_market_dataframe(crypto_data)
        top_gainers = analyzer.generate_top_movers_report(market_df)
        news_twitter.post_tweet(top_gainers)




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main execution: {e}")