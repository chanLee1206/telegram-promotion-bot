import requests

# Replace 'your-rpc-key' with your actual RPC key
url = "https://sui.blockpi.network/v1/rpc/7a161850387357cc5e4c78aaa49a10c9205ffba1"
headers = {
    "Content-Type": "application/json"
}
data = {
 "jsonrpc": "2.0",
    "id": 1,
    "method": "suix_queryTransactionBlocks",
    "params": [
        {
            "filter": {
                "InputObject": "0x120504fb9e9e2788c7a4cdb44c754cdc34835f9049df83146aeeb403eddf667f"
            },
            "options": None
        },
        "CdL4cX5mPuedRvUiuGsCSYoeRZERUB6U7sjxcSoXPPt1",
        100,
        False
    ]
}

response = requests.post(url, headers=headers, json=data)

# Print the response
print(response.json().get('result'))
