import requests

import aiohttp
import asyncio

async def get_transaction_amounts(digest):
    url = f"https://api.blockberry.one/sui/v1/raw-transactions/{digest}"

    headers = {
        "accept": "*/*",
        "x-api-key": "F9Y7kRMOYmfHycPaRrWBjRNLrIQmx0"
    }

    # Use aiohttp to make an asynchronous GET request
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:

            if response.status == 200:
                res = await response.json()
                if not res or "balanceChanges" not in res["result"]:
                    print("Error: Missing 'balanceChanges' in response.")
                    return []
                res_result = res.get('result')
                
                # result = await response.json()

                timestampMs = res_result.get('timestampMs')
                txn_balance = res_result.get('balanceChanges')
                transContent = {'timestampMs': timestampMs, "unit_coin": 0, "cur_coin": 0}

                for entry in txn_balance:
                    coin_type = entry['coinType']
                    amount = int(entry['amount'])
                    if coin_type == '0x2::sui::SUI':
                        transContent['unit_coin'] += amount
                    else:
                        transContent['cur_coin'] += amount
                return transContent
            else:
                print(f"Error: {response.status}")
                return None

# Example usage
async def main():
    digest = "3nLpoHBakXq93oeCZ4AfXiYLBqbwr2hcx6cE731Si5SM"
    details = await get_transaction_amounts(digest)
    print(details)

# Running the example
if __name__ == "__main__":
    asyncio.run(main())


