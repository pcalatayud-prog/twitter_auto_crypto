# main.py

from src.twitter_client import TwitterClient
from src.crypto_tracker import CryptoTracker
from src.market_analyzer import MarketAnalyzer
import random
import time

def main():
    try:
        # Post BTC update
        btc_twitter = TwitterClient(account_type='BTC')
        btc_tracker = CryptoTracker('BTC-USD')
        
        # Select message format with 30% probability for detailed, 70% for standard
        message_type = random.choices(['standard', 'detailed'], weights=[0.7, 0.3])[0]
        btc_report = btc_tracker.run(message_type=message_type)
        
        btc_twitter.post_tweet(btc_report)
        print(f'Successfully posted Bitcoin update with {message_type} format')
    except Exception as e:
        print(f'Error posting Bitcoin update: {e}')

    # Add delay between posts
    time.sleep(2)

    try:
        # Post market analysis
        news_twitter = TwitterClient(account_type='BTC')  # Using BTC account for news as well
        analyzer = MarketAnalyzer()
        crypto_data = analyzer.get_all_crypto_data()
        if crypto_data:
            market_df = analyzer.create_market_dataframe(crypto_data)
            top_movers = analyzer.generate_top_movers_report(market_df)
            news_twitter.post_tweet(top_movers)
            print('Successfully posted market analysis')
    except Exception as e:
        print(f'Error posting market analysis: {e}')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main execution: {e}")
