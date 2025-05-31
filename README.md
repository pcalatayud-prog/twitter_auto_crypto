# Bitcoin Twitter Bot

An automated Twitter bot that posts regular Bitcoin price updates with detailed metrics and analytics.

## Features

- Automated Bitcoin price tracking and reporting
- Multiple message formats:
  - Standard format (70% probability): Price and price changes across different time periods
  - Detailed format (30% probability): Focused on supply metrics, volume, market cap, ATH and key performance indicators
- Market analysis with top movers report
- Data sourced from CoinMarketCap API for current prices and metrics
- Historical data from Yahoo Finance for long-term analysis
- Automatic tweet posting (with mock option for testing)
- GitHub Actions integration for scheduled posts

## Requirements

- Python 3.8+
- Twitter API credentials
- CoinMarketCap API key

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys in the `.env` file

## Local Usage

Run the bot locally with:

```
python main.py
```

This will:
1. Fetch current Bitcoin data from CoinMarketCap
2. Generate a tweet with either standard or detailed format (randomly selected)
3. Post the tweet to the configured Twitter account
4. Generate and post a market analysis of top movers

## GitHub Actions Setup

This repo is configured to run automatically using GitHub Actions. To set this up:

1. Go to your GitHub repository's Settings tab
2. Click on "Secrets and variables" → "Actions"
3. Add the following repository secrets:
   - `BTC_ACCESS_TOKEN`
   - `BTC_ACCESS_TOKEN_SECRET`
   - `BTC_BEARER`
   - `BTC_API_KEY`
   - `BTC_API_KEY_SECRET`
   - `NEWS_ACCESS_TOKEN`
   - `NEWS_ACCESS_TOKEN_SECRET`
   - `NEWS_BEARER`
   - `NEWS_API_KEY`
   - `NEWS_API_KEY_SECRET`
   - `CMC_API_KEY`

The workflow is configured to run every 6 hours and can also be triggered manually from the Actions tab.

## Project Structure

- `main.py` - Entry point for the application
- `src/`
  - `crypto_tracker.py` - Bitcoin price and metrics tracking
  - `twitter_client.py` - Twitter API interaction
  - `market_analyzer.py` - Market analysis functionality
- `config/`
  - `api_keys.py` - Loads API credentials from environment variables
  - `constants.py` - Application constants and emojis
- `.github/workflows/`
  - `bitcoin_tweet.yml` - GitHub Actions workflow configuration
- `docs/`
  - `workflow.drawio` - Visual diagram of the application flow

## Security Notes

- API keys are stored as GitHub Actions secrets and never committed to the repository
- For local development, use the `.env` file (which is ignored by git)
- The `.env.example` file provides a template for required environment variables

## License

MIT
