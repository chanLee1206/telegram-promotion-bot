import requests

# Replace 'your-rpc-key' with your actual RPC key
url = "https://sui.blockpi.network/v1/rpc/7a161850387357cc5e4c78aaa49a10c9205ffba1"
headers = {
    "Content-Type": "application/json"
}
data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "sui_getTransactionBlock",
    "params": [
      "2C7AoqvCSEqg1o6QBMyCNj2QveRiEuQuiY8EZxDquXRc",
      {
        "showInput": False,
        "showRawInput": False,
        "showEffects": False,
        "showEvents": False,
        "showObjectChanges": False,
        "showBalanceChanges": True,
        "showRawEffects": False
      }
    ]
}

response = requests.post(url, headers=headers, json=data)

# Print the response
print(response.json().get("result"))