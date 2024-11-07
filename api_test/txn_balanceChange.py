import aiohttp
import asyncio

async def get_transaction_amounts(transaction_digest):
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

    async with aiohttp.ClientSession() as session:
        # Make the POST request
        async with session.post(url, headers=headers, json=data) as response:
            # Check if the response was successful
            if response.status != 200:
                print(f"Error: {response.status} - {await response.text()}")
                return []

            # Parse response JSON and check if the required data is present
            result = await response.json()
            if not result or "result" not in result or "balanceChanges" not in result["result"]:
                print("Error: Missing 'balanceChanges' in response.")
                return []

            # Process balance changes
            timestampMs = result['result']['timestampMs']
            balance_changes = result['result']['balanceChanges']
            transContent = {'timestampMs': timestampMs, "unit_coin": 0, "cur_coin": 0}

            for entry in balance_changes:
                coin_type = entry['coinType']
                amount = int(entry['amount'])
                if coin_type == '0x2::sui::SUI':
                    transContent['unit_coin'] += amount
                else:
                    transContent['cur_coin'] += amount
            return transContent

async def main():
    # Example usage
    transaction_digest = "9AGukBwsEaTUNgimJViP4ykbThFR49cT98WZBUqUR86z"
    transaction_content = await get_transaction_amounts(transaction_digest)
    print(transaction_content)

if __name__ == "__main__":
    asyncio.run(main())
