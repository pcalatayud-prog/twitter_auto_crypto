# main.py

from src.twitter_client import TwitterClient
from src.crypto_tracker import CryptoTracker
from src.market_analyzer import MarketAnalyzer
import time


def main():
    # Initialize clients

    try:
        # Post TRUMP update
        trump_twitter = TwitterClient(account_type='TRUMP')
        trump_tracker = CryptoTracker('TRUMP-USD')
        trump_report = trump_tracker.run()
        trump_twitter.post_tweet(trump_report)
    except:
        print('error trump')

    try:
        # Post BTC update
        btc_twitter = TwitterClient(account_type='BTC')
        btc_tracker = CryptoTracker('BTC-USD')
        btc_report = btc_tracker.run()
        btc_twitter.post_tweet(btc_report)
    except:
        print('error btc')
    
    # Add delay between posts
    time.sleep(2)

    try:
        # Post ADA update
        ada_twitter = TwitterClient(account_type='ADA')
        ada_tracker = CryptoTracker('ADA-USD')
        ada_report = ada_tracker.run()
        ada_twitter.post_tweet(ada_report)
    except:
        print('error ada')
    
    
    # Add delay between posts
    time.sleep(2)

    try:
        # Post market analysis
        news_twitter = TwitterClient(account_type='NEWS')
        analyzer = MarketAnalyzer()
        crypto_data = analyzer.get_all_crypto_data()
        if crypto_data:
            market_df = analyzer.create_market_dataframe(crypto_data)
            top_gainers = analyzer.generate_top_movers_report(market_df)
            news_twitter.post_tweet(top_gainers)
    except:
        print('error crypto alert')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main execution: {e}")
