import requests

BASE_URL = "https://api.raidenx.io"


# Example function to fetch market data
def get_market_data():
    # url = f"{BASE_URL}/api/v1/markets/{pair}"
    url = f"{BASE_URL}/api/v1/markets/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "price": data.get("price"),
            "volume": data.get("volume"),
            "market_cap": data.get("market_cap"),
        }
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
def main() : 
    get_market_data()

if __name__ == "__main__":
    main()