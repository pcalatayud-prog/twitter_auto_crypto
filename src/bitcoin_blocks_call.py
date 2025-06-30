import requests
from datetime import datetime, timedelta
from loguru import logger

Reward_BTC = 3.125

def get_last_block_info():
    try:
        # Get the latest block hash
        latest_block = requests.get("https://blockchain.info/latestblock").json()
        block_hash = latest_block['hash']
        block_height = latest_block['height']

        # Get full block data
        block_data = requests.get(f"https://blockchain.info/rawblock/{block_hash}").json()

        # Extract key information
        block_reward_satoshis = block_data['tx'][0]['out'][0]['value']
        block_reward_btc = block_reward_satoshis / 1e8

        fees = round(block_reward_btc-Reward_BTC,8)

        return fees


    except Exception as e:
        return {"error": str(e)}

def get_bitcoin_block_height():
    """
    Fetches the current Bitcoin block height from Blockstream's public API.
    """
    url = "https://blockstream.info/api/blocks/tip/height"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return int(response.text)
    except requests.RequestException as e:
        logger.error(f"Error fetching block height: {e}")
        return None

def estimate_halving_end(remainder, current_time=None):
    """
    Estimates the end date and time of the current halving cycle.
    """
    blocks_left = 210_000 - remainder
    minutes_per_block = 10
    total_minutes = blocks_left * minutes_per_block

    if current_time is None:
        current_time = datetime.utcnow()

    return current_time + timedelta(minutes=total_minutes)

def format_twitter_message(block_height, remainder, halving_end):
    blocks_left = 210_000 - remainder
    percent_complete = (remainder / 210_000) * 100
    formatted_time = halving_end.strftime('%b %d, %Y %H:%M UTC')
    time_left = halving_end - datetime.utcnow()
    days_left = int(time_left.total_seconds() // (60 * 60 * 24))

    fees = get_last_block_info()

    return (
        "🟧 #Bitcoin Halving Status:\n\n"
        f"🔢 Bloques minados (Block Height) {block_height:,}\n"
        f"📦 Progress: {remainder:,} / 210,000 ({percent_complete:.4f}%)\n"
        f"⏳ Bloques restantes para Halving: {blocks_left:,} blocks (~{days_left} days)\n"
        f"📅 Estimacion del siguiente halving: {formatted_time}\n"
        f"💰La recompensa actual por bloque minado en Bitcoin es de 3.125 BTC\n"
        f"💸 Comisiones en el último bloque: {fees} BTC\n"        
        "#BTC #Halving #Crypto"
    )

def main():
    logger.info("Fetching current Bitcoin block height...")
    block_height = get_bitcoin_block_height()
    if block_height is None:
        return

    remainder = block_height % 210_000
    halving_end = estimate_halving_end(remainder)

    logger.success(f"Current block height: {block_height}")
    logger.info(f"Blocks mined this halving cycle: {remainder}")
    logger.info(f"Estimated halving end: {halving_end.strftime('%Y-%m-%d %H:%M:%S')} UTC")

    tweet = format_twitter_message(block_height, remainder, halving_end)
    logger.info("\n" + tweet)

if __name__ == "__main__":
    main()
