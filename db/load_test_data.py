import requests
import random
import json

# Example API URLs (replace with actual SUI API endpoints)
meme_token_url = "https://https://dexscreener.com/sui/bluemove"
nft_token_url = "https://https://dexscreener.com/sui/bluemove"

def fetch_tokens(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Assuming JSON response
    else:
        print(f"Failed to fetch data from {url}")
        return []

def select_random_tokens(tokens, count=10):
    return random.sample(tokens, min(len(tokens), count))

def main():
    # Fetch meme tokens and NFT tokens
    meme_tokens = fetch_tokens(meme_token_url)
    nft_tokens = fetch_tokens(nft_token_url)

    # Select 10 random meme tokens and 10 random NFT tokens
    selected_meme_tokens = select_random_tokens(meme_tokens, 10)
    selected_nft_tokens = select_random_tokens(nft_tokens, 10)

    # Combine them into a dictionary
    data = {
        "meme_tokens": selected_meme_tokens,
        "nft_tokens": selected_nft_tokens
    }

    # Write to a JSON file
    with open("db/tokens_data.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Random tokens saved to db/tokens_data.json")

if __name__ == "__main__":
    main()
