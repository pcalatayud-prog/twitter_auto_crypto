# main.py

from src.twitter_client import TwitterClient
from src.crypto_tracker import CryptoTracker
from src.market_analyzer import MarketAnalyzer
import random
import time
import os
from loguru import logger

# Configure logger
logger.add("twitter_bot.log", rotation="1 day", level="DEBUG")
logger.info("Starting Bitcoin Twitter Bot")

def main():
    # Log environment variables (securely)
    logger.info("Checking environment variables:")
    logger.info(f"BTC_ACCESS_TOKEN exists: {bool(os.getenv('BTC_ACCESS_TOKEN'))}")
    logger.info(f"BTC_API_KEY exists: {bool(os.getenv('BTC_API_KEY'))}")
    logger.info(f"CMC_API_KEY exists: {bool(os.getenv('CMC_API_KEY'))}")
    
    try:
        # Post BTC update
        logger.info("Initializing Twitter client for Bitcoin updates")
        btc_twitter = TwitterClient(account_type='BTC')
        
        logger.info("Initializing CryptoTracker")
        btc_tracker = CryptoTracker('BTC-USD')
        
        # Select message format with probability distribution:
        # - standard: 50%
        # - detailed: 30%
        # - blocks: 20%
        message_type = random.choices(['standard', 'detailed', 'blocks'], weights=[0.4, 0.3, 0.3])[0]
        logger.info(f"Selected message format: {message_type}")
        
        btc_report = btc_tracker.run(message_type=message_type)
        
        btc_twitter.post_tweet(btc_report)
        logger.info(f'Successfully posted Bitcoin update with {message_type} format')
        print(f'Successfully posted Bitcoin update with {message_type} format')
    except Exception as e:
        logger.exception(f'Error posting Bitcoin update: {str(e)}')
        print(f'Error posting Bitcoin update: {e}')

    # Add delay between posts
    logger.info("Waiting 2 seconds before posting market analysis")
    time.sleep(2)

    try:
        # Post market analysis
        logger.info("Initializing Twitter client for market analysis")
        news_twitter = TwitterClient(account_type='NEWS')
        
        logger.info("Initializing MarketAnalyzer")
        analyzer = MarketAnalyzer()
        
        logger.info("Fetching crypto market data")
        crypto_data = analyzer.get_all_crypto_data()
        
        if crypto_data:
            logger.info(f"Creating market dataframe with {len(crypto_data)} cryptocurrencies")
            market_df = analyzer.create_market_dataframe(crypto_data)
            
            logger.info("Generating top movers report")
            top_movers = analyzer.generate_top_movers_report(market_df)
            
            news_twitter.post_tweet(top_movers)
            logger.info('Successfully posted market analysis')
            print('Successfully posted market analysis')
        else:
            logger.error("No crypto data returned from API")
    except Exception as e:
        logger.exception(f'Error posting market analysis: {str(e)}')
        print(f'Error posting market analysis: {e}')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main execution: {e}")
