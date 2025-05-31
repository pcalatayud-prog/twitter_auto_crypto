# src/twitter_client.py

import tweepy
import sys
import os

# Add the project root to the path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.api_keys import TwitterCredentials
from loguru import logger

class TwitterClient:
    def __init__(self, account_type='BTC'):
        """Initialize Twitter client with specified account type.
        
        Args:
            account_type: Type of Twitter account to use (currently only 'BTC' is supported)
        """
        self.account_type = account_type
        self._setup_credentials()
        self._initialize_client()

    def _setup_credentials(self) -> None:
        """Set up API credentials based on account type."""
        if self.account_type == 'BTC':
            self.access_token = TwitterCredentials.BTC_ACCESS_TOKEN
            self.access_token_secret = TwitterCredentials.BTC_ACCESS_TOKEN_SECRET
            self.bearer = TwitterCredentials.BTC_BEARER
            self.api_key = TwitterCredentials.BTC_API_KEY
            self.api_key_secret = TwitterCredentials.BTC_API_KEY_SECRET
            logger.info(f"Using Bitcoin Twitter account")
        elif self.account_type == 'NEWS':
            self.access_token = TwitterCredentials.NEWS_ACCESS_TOKEN
            self.access_token_secret = TwitterCredentials.NEWS_ACCESS_TOKEN_SECRET
            self.bearer = TwitterCredentials.NEWS_BEARER
            self.api_key = TwitterCredentials.NEWS_API_KEY
            self.api_key_secret = TwitterCredentials.NEWS_API_KEY_SECRET
            logger.info(f"Using News Twitter account")
        else:
            logger.warning(f"Unsupported account type: {self.account_type}, defaulting to BTC")
            self.access_token = TwitterCredentials.BTC_ACCESS_TOKEN
            self.access_token_secret = TwitterCredentials.BTC_ACCESS_TOKEN_SECRET
            self.bearer = TwitterCredentials.BTC_BEARER
            self.api_key = TwitterCredentials.BTC_API_KEY
            self.api_key_secret = TwitterCredentials.BTC_API_KEY_SECRET

    def _initialize_client(self) -> None:
        """Initialize the Twitter API client with credentials."""
        self.client = tweepy.Client(
            bearer_token=self.bearer,
            consumer_key=self.api_key,
            consumer_secret=self.api_key_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )

    def post_tweet(self, text: str) -> None:
        """Post a tweet with the given text.
        
        Args:
            text: Content of the tweet to post
        """
        try:
            # Uncomment the line below to actually post tweets
            self.client.create_tweet(text=text)
            logger.info(f'Tweet content: {text}')
            # print(f'Mocking posting tweet: {text}')
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")