import requests
import json
API_URL = "https://api.raidenx.io/"
pair_id = "fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356"

def fetch_transaction_data(pair_id):
    url = f"{API_URL}/api/v1/sui/transaction/{pair_id}"    
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
    fetch_token_data(pair_id)

if __name__ == "__main__":
    main()
