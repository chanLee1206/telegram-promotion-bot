import requests
import json
# API_URL = "https://api.raidenx.io/"


def fetch_pairId(coinType):
    url = f"https://api.raidenx.io/api/v1/sui/tokens/{coinType}"
    # url = f"{API_URL}{coinType}"    
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
    url = f"https://api.raidenx.io/api/v1/sui/pairs/{pair_id}"    
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
    coinType = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    fetch_pairId(coinType)
    pair_id = "05983d81397bdb221f592d228b16e587ed1fd8c0d5200ce203f1ff69a980796a"
    fetch_token_data(pair_id)    
    # pair_id = "d09bf618022cf4f820a009fcd86c46bf6509ba8b0a7f5b52edd3b7b9f9ceef6c"
    # fetch_token_data(pair_id)    
    # # fetch_token_data(pair_id)

if __name__ == "__main__":
    main()
