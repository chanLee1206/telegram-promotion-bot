import requests

coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
# url = "https://rpc-testnet.suiscan.xyz:443/v1/coins/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
url = f"https://api.blockvision.org/v2/sui/coin/detail?coinType={coin_type}"

headers = {
    "accept": "application/json",
    "x-api-key": "2oAWXc23NfVKN0E4TxFfnnVZP6Q"
}

# Make the GET request
response = requests.get(url, headers=headers)

print(response.json().get('result'))  # Use .json() to parse the response as JSON
