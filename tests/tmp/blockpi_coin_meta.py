import requests

# Replace 'your-rpc-key' with your actual RPC key
url = "https://sui.blockpi.network/v1/rpc/7a161850387357cc5e4c78aaa49a10c9205ffba1"
headers = {
    "Content-Type": "application/json"
}
data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "suix_getCoinMetadata",
    "params": [
        "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    ]
}

response = requests.post(url, headers=headers, json=data)

# Print the response
print(response.json())