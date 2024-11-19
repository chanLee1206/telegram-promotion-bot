import requests
import json
# API_URL = "https://api.raidenx.io/"
API_URL = "https://api.raidenx.io/api/v1/sui/tokens/"

coinType = "0x8993129d72e733985f7f1a00396cbd055bad6f817fee36576ce483c8bbb8b87b::sudeng::SUDENG"

def fetch_transaction_data(coinType):
    url = f"{API_URL}{coinType}"    
    try:
        response = requests.get(url)        
        if response.status_code == 200:
            data = response.json()  
            print("Transaction data received:", json.dumps(data, indent=4))
        else:
            print(f"Failed to fetch transaction data. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def fetch_token_data(pair_id):
    url = f"{API_URL}/api/v1/sui/pairs/{pair_id}"    
    try:
        response = requests.get(url)        
        if response.status_code == 200:
            data = response.json()  
            print("Token data received:", json.dumps(data, indent=4))
        else:
            print(f"Failed to fetch token data. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
def main():
    # fetch_transaction_data(pair_id)    
    global coinType
    
    fetch_transaction_data(coinType)

if __name__ == "__main__":
    main()
