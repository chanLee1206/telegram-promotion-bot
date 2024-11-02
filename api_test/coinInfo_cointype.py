import requests

def fetch_coin_details(coin_type):
    url = f"https://api.blockvision.org/v2/sui/coin/detail?coinType={coin_type}"
    headers = {
        "accept": "application/json",
        "x-api-key": "2oAWXc23NfVKN0E4TxFfnnVZP6Q"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check response status and return the result if successful
    if response.status_code == 200:
        coin_details = response.json().get('result')
        coin_extract_info ={
            'coinType' : coin_details.get('coinType'),
            'name': coin_details.get('name'),
            'symbol': coin_details.get('symbol'),
            'decimals': coin_details.get('decimals'),
            'price': coin_details.get('price'),
            'priceChangePercentage24H': coin_details.get('priceChangePercentage24H'),
            'totalSupply': coin_details.get('totalSupply'),
            'marketCap': coin_details.get('marketCap')
        }
        return coin_extract_info        
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
# coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
# coin_info = fetch_coin_details(coin_type)

# print(coin_info)