# src/twitter_client.py

import tweepy
from config.api_keys import TwitterCredentials

class TwitterClient:
    def __init__(self, account_type='BTC'):
        self.account_type = account_type
        self._setup_credentials()
        self._initialize_client()

    def _setup_credentials(self):
        if self.account_type == 'BTC':
            self.access_token = TwitterCredentials.BTC_ACCESS_TOKEN
            self.access_token_secret = TwitterCredentials.BTC_ACCESS_TOKEN_SECRET
            self.bearer = TwitterCredentials.BTC_BEARER
            self.api_key = TwitterCredentials.BTC_API_KEY
            self.api_key_secret = TwitterCredentials.BTC_API_KEY_SECRET
        elif self.account_type == 'ADA':
            self.access_token = TwitterCredentials.ADA_ACCESS_TOKEN
            self.access_token_secret = TwitterCredentials.ADA_ACCESS_TOKEN_SECRET
            self.bearer = TwitterCredentials.ADA_BEARER
            self.api_key = TwitterCredentials.ADA_API_KEY
            self.api_key_secret = TwitterCredentials.ADA_API_KEY_SECRET
        else:  # NEWS
            self.access_token = TwitterCredentials.NEWS_ACCESS_TOKEN
            self.access_token_secret = TwitterCredentials.NEWS_ACCESS_TOKEN_SECRET
            self.bearer = TwitterCredentials.NEWS_BEARER
            self.api_key = TwitterCredentials.NEWS_API_KEY
            self.api_key_secret = TwitterCredentials.NEWS_API_KEY_SECRET

    def _initialize_client(self):
        self.client = tweepy.Client(
            bearer_token=self.bearer,
            consumer_key=self.api_key,
            consumer_secret=self.api_key_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )

    def post_tweet(self, text: str) -> None:
        """Post a tweet with the given text."""
        try:
            self.client.create_tweet(text=text)
        except Exception as e:
            print(f"Error posting tweet: {e}")