import requests
import json

def get_token_data(object_id):
    # Set the endpoint URL
    url = "https://fullnode.mainnet.sui.io:443"
    
    # Define the JSON-RPC payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sui_getObject",
        "params": [object_id]
    }
    
    # Set the headers for the request
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send the request to the Sui endpoint
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check for a successful response
    if response.status_code == 200:
        result = response.json()
        # Check if the result is valid and the object exists
        if "result" in result and result["result"].get("status") == "Exists":
            return result["result"]["data"]
        else:
            return f"Error: Object {object_id} not found or does not exist."
    else:
        return f"Error: Received status code {response.status_code}"

# Example usage:
object_id = "0x53e4567ccafa5f36ce84c80aa8bc9be64e0d5ae796884274aef3005ae6733809"  # Replace with your token's Object ID
token_data = get_token_data(object_id)
print(token_data)
