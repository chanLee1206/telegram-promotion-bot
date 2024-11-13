import aiohttp
import asyncio


async def fetch_account_txns(account, amount, start_timestamp=1704067200000):
    # start_timestamp=0
    url = f"https://api.blockberry.one/sui/v1/accounts/{account}/activity?size=20&orderBy=DESC"
    headers = {
        "accept": "*/*",
        "x-api-key": "F9Y7kRMOYmfHycPaRrWBjRNLrIQmx0"
    }
    
    # Use aiohttp to make an asynchronous GET request
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            # Check response status and return the result if successful
            
            if response.status == 200:
                res = await response.json()
                txn_detail = res.get('content')
                # print(global_token_arr)
                extracted_data = []
                for item in txn_detail:
                    timestamp = item.get('timestamp')
                    if(timestamp < start_timestamp) : continue
                    
                    coins = item.get('details').get('detailsDto').get('coins')[0]
                    digest = item.get('digest')
                    fromAccount = item.get('activityWith')[0].get('id')
                                   
                    new_dict = {
                        "account" : account,
                        "timestamp": timestamp,
                        "amount": coins.get('amount'),
                        "digest": digest,
                        "symbol": coins.get("symbol"),
                        "coinType": coins.get('coinType'),     # Set to None or an actual value if available
                        "fromAccount": fromAccount
                    }
                    if new_dict['coinType'] != "0x2::sui::SUI" :
                        continue
                    if abs(new_dict['amount'] - amount) > 0.1 :
                        continue
                    extracted_data.append(new_dict)
                return extracted_data
            else:
                print(f"Error: {response.status}")
                return None

# Example usage
async def main():
    account = "0xd6840994167c67bf8063921f5da138a17da41b3f64bb328db1687ddd713c5281"

    details = await fetch_account_txns(account, 100000000, 1730427928668)
    print(details)

# Running the example
if __name__ == "__main__":
    asyncio.run(main())


