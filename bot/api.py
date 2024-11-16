import aiohttp
import asyncio
from datetime import datetime, timezone
import globals

# Fetch coin details
async def fetch_coin_details(coin_type):
    url = f"https://api.blockberry.one/sui/v1/coins/{coin_type}"
    headers = {
        "accept": "*/*",
        "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                coin_details = await response.json()
                return {
                    'coinType': coin_details.get('coinType'),
                    'name': coin_details.get('coinName'),
                    'symbol': coin_details.get('coinSymbol'),
                    'decimals': coin_details.get('decimals'),
                    'price': coin_details.get('price'),
                    'supply': coin_details.get('supply'),
                    'marketCap': coin_details.get('fdv')
                }
            else:
                print(f"Error: {response.status}")
                return None
            
# Get transaction amounts
async def get_transaction_amounts(digest):
    url = f"https://api.blockberry.one/sui/v1/raw-transactions/{digest}"
    headers = {
        "accept": "*/*",
        "x-api-key": "F9Y7kRMOYmfHycPaRrWBjRNLrIQmx0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                res = await response.json()
                res_result = res.get('result')
                timestampMs = res_result.get('timestampMs')
                txn_balance = res_result.get('balanceChanges')
                txn_sender = res_result.get('transaction', {}).get('data', {}).get('sender', "unknown")

                transContent = {'timestampMs': timestampMs, "unit_coin": 0, "cur_coin": 0, "sender": txn_sender}

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

# Fetch account transactions
async def fetch_account_txns(account, amount, start_timestamp=1704067200000):
    url = f"https://api.blockberry.one/sui/v1/accounts/{account}/activity?size=20&orderBy=DESC"
    headers = {
        "accept": "*/*",
        "x-api-key": "F9Y7kRMOYmfHycPaRrWBjRNLrIQmx0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                res = await response.json()
                txn_detail = res.get('content')
                extracted_data = []
                for item in txn_detail:
                    timestamp = item.get('timestamp')
                    if timestamp < start_timestamp:
                        continue
                    coins = item.get('details').get('detailsDto').get('coins')[0]
                    digest = item.get('digest')
                    fromAccount = item.get('activityWith')[0].get('id')

                    new_dict = {
                        "account": account,
                        "timestamp": timestamp,
                        "amount": coins.get('amount'),
                        "digest": digest,
                        "symbol": coins.get("symbol"),
                        "coinType": coins.get('coinType'),
                        "fromAccount": fromAccount
                    }
                    if new_dict['coinType'] != "0x2::sui::SUI" or abs(new_dict['amount'] - amount) > 0.1:
                        continue
                    extracted_data.append(new_dict)
                return extracted_data
            else:
                print(f"Error: {response.status}")
                return None

# Get transaction hashes
async def get_tx_hashes(coin_type, page_size):
    url = f"https://api.blockberry.one/sui/v1/coins/{coin_type}/transactions?page=0&size={page_size}&orderBy=DESC&sortBy=AGE"
    headers = {
        "accept": "*/*",
        "x-api-key": "Lmn3IP5rbjuULtIJLNzUWJGfmbymVE"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                result_txns = await response.json()
                return [{'txHash': tx['txHash'], 'functions': tx.get('functions', [])} for tx in result_txns.get('content', [])]
            else:
                print(f"Error fetching transaction hashes: {response.status}")
                return []

# Format transaction data
def trans_view_format(combined_raw_info):
    unitCoinDecimals = 9
    utc_time = datetime.fromtimestamp(int(combined_raw_info["timestampMs"]) / 1000, tz=timezone.utc)
    formatted_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')

    cur_token = next((token for token in globals.global_token_arr if token['coinType'] == combined_raw_info["coinType"]), None)
    trans_view_info = {
        "digest": combined_raw_info["txHash"],
        "time": formatted_time,
        "sender": combined_raw_info["sender"],
        "coinName": combined_raw_info["coinName"],
        "coinSymbol": combined_raw_info["coinSymbol"],
        "coinType": combined_raw_info["coinType"],
        "price": combined_raw_info["price"],
        "decimals": combined_raw_info["decimals"],
        "function": combined_raw_info["function"],
        "marketCap": combined_raw_info["marketCap"],
        "realUnitCoinAmount": combined_raw_info['unitCoinAmount'] / 10**unitCoinDecimals,
        "realCurCoinAmount": combined_raw_info['curCoinAmount'] / 10**combined_raw_info['decimals'],
        "launchPad": cur_token.get('launchPad', "unknown"),
        "launchURL": cur_token.get('launchURL', "unknown")
    }
    return trans_view_info

# Get last transaction info
async def getLast_trans_info_of_coin(coin_type, lastTxn):
    tx_hashes = await get_tx_hashes(coin_type, 1)
    
    # Handle case where tx_hashes is None or empty
    if not tx_hashes or not isinstance(tx_hashes, list) or not tx_hashes[0]:
        print(f"No transaction hashes found for coin type: {coin_type}")
        return {"function": 'none'}  # Exit early if no hashes are found

    functions = tx_hashes[0].get('functions')  # Safely get 'functions' key

    # Handle case where 'functions' is None or empty
    if not functions or "buy" not in functions[0]:
        print(f"No valid 'buy' function found in transaction hash: {tx_hashes[0]['txHash']}")
        return {"function": 'none'}

    if tx_hashes[0]['txHash'] == lastTxn:
        print('No new transaction, skipping further checks.')
        return {"function": 'none'}

    # Proceed with other API calls only if the above checks pass
    await asyncio.sleep(5)

    coin_info = await fetch_coin_details(coin_type)
    if coin_info is None:
        print("Failed to fetch coin details.")
        return {"function": 'none'}

    transaction_info = await get_transaction_amounts(tx_hashes[0]["txHash"])
    if transaction_info is None:
        print("Failed to fetch transaction details.")
        return {"function": 'none'}

    # Combine and return formatted transaction data
    combined_info = {
        "txHash": tx_hashes[0]['txHash'],
        "timestampMs": transaction_info['timestampMs'],
        "sender": transaction_info['sender'],
        "coinSymbol": coin_info['symbol'],
        "coinName": coin_info['name'],
        "coinType": coin_info['coinType'],
        "price": coin_info['price'],
        "decimals": coin_info['decimals'],
        "function": functions[0],  # Using the first function safely
        "marketCap": coin_info['marketCap'],
        "unitCoinAmount": transaction_info['unit_coin'],
        "curCoinAmount": transaction_info['cur_coin']
    }
    return trans_view_format(combined_info)

# Main function
async def main():
    coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    TransInfo = await getLast_trans_info_of_coin(coin_type, lastTxn=None)
    print("Transaction Info:", TransInfo)

if __name__ == "__main__":
    asyncio.run(main())
