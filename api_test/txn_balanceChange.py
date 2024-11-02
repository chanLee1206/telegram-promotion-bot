import requests

def get_transaction_amounts(transaction_digest):
    url = "https://sui.blockpi.network/v1/rpc/7a161850387357cc5e4c78aaa49a10c9205ffba1"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sui_getTransactionBlock",
        "params": [
            transaction_digest,
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

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)
    
    # Check if the response was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    # Parse response JSON and check if the required data is present
    result = response.json().get("result")
    if not result or "balanceChanges" not in result:
        print("Error: Missing 'balanceChanges' in response.")
        return []

    # Process balance changes
    timestampMs = result['timestampMs']
    balance_changes = result['balanceChanges']
    amounts_by_coin = {}

    for entry in balance_changes:
        coin_type = entry['coinType']
        amount = int(entry['amount'])

        if coin_type in amounts_by_coin:
            amounts_by_coin[coin_type] += amount
        else:
            amounts_by_coin[coin_type] = amount

    # Convert the result into the required array format
    transaction_amount = [{'coinType': coin_type, 'amount': str(amount)} for coin_type, amount in amounts_by_coin.items()]

    return {'timestampMs': timestampMs,  'transaction_content' : transaction_amount}

# Example usage
# transaction_digest = "9AGukBwsEaTUNgimJViP4ykbThFR49cT98WZBUqUR86z"
# transaction_content = get_transaction_amounts(transaction_digest)
# print(transaction_content)