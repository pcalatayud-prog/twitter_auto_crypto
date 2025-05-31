# config/api_keys.py
import os
from dotenv import load_dotenv

load_dotenv()  # Optional: load .env if it exists (for local dev)

class TwitterCredentials:
    # Bitcoin account
    BTC_ACCESS_TOKEN = os.getenv("BTC_ACCESS_TOKEN")
    BTC_ACCESS_TOKEN_SECRET = os.getenv("BTC_ACCESS_TOKEN_SECRET")
    BTC_BEARER = os.getenv("BTC_BEARER")
    BTC_API_KEY = os.getenv("BTC_API_KEY")
    BTC_API_KEY_SECRET = os.getenv("BTC_API_KEY_SECRET")

    # Crypto Alert News account
    NEWS_ACCESS_TOKEN = os.getenv("NEWS_ACCESS_TOKEN")
    NEWS_ACCESS_TOKEN_SECRET = os.getenv("NEWS_ACCESS_TOKEN_SECRET")
    NEWS_BEARER = os.getenv("NEWS_BEARER")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    NEWS_API_KEY_SECRET = os.getenv("NEWS_API_KEY_SECRET")


class CoinMarketCapCredentials:
    API_KEY = os.getenv("CMC_API_KEY")
