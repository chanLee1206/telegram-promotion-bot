import json
import random
import string
from datetime import datetime, timedelta

# Helper function to generate random coin names (3 capital letters)
def generate_coin_name():
    return ''.join(random.choices(string.ascii_uppercase, k=3))

# Helper function to generate random transaction ID
def generate_txn_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=43))

# Helper function to generate a random date from a range
def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%m/%d/%y")

# Set constant values
COIN_TYPE = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
LIQUIDITY = 886291
MAX_CAP = 46545446
NUM_MEME_TOKENS = 20
NUM_NFT_TOKENS = 10

# Generate random data for meme tokens
meme_tokens = []
start_date = datetime(2024, 10, 1)
end_date = datetime.now()

for _ in range(NUM_MEME_TOKENS):
    txn_id = generate_txn_id()
    meme_tokens.append({
        "coin_name": generate_coin_name(),
        "coin_type": COIN_TYPE,
        "txn_id": txn_id,
        "txn_date": generate_random_date(start_date, end_date),
        "txn_type": random.choice(["buy", "sell"]),
        "sui_cost": random.randint(10000000000, 500000000000),
        "txn_token_volume": random.randint(1, 1000),  # Example range for token volume
        "txn_link": txn_id,
        "coin_liquidity": LIQUIDITY,
        "coin_MCap": MAX_CAP
    })

# Generate random data for NFT tokens
nft_tokens = []
for _ in range(NUM_NFT_TOKENS):
    txn_id = generate_txn_id()
    nft_tokens.append({
        "nft_name": generate_coin_name(),
        "nft_id": COIN_TYPE,
        "nft_collection": COIN_TYPE,
        "txn_id": txn_id,
        "txn_date": generate_random_date(start_date, end_date),
        "txn_type": random.choice(["buy", "sell"]),
        "sui_cost": random.randint(10000000000, 500000000000),
        "txn_link": txn_id,
    })

# Combine the data into one dictionary
data = {
    "meme_tokens": meme_tokens,
    "nft_tokens": nft_tokens
}

# Write the data to a JSON file
with open("sui_tokens_info.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file with token information has been generated as 'sui_tokens_info.json'.")
