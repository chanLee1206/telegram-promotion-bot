import aiohttp
import asyncio
from datetime import datetime, timezone
import globals

# Fetch coin details
async def fetch_coin_details(coinType):
    url = f"https://api.raidenx.io/api/v1/sui/tokens/{coinType}"
   
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                coin_details = await response.json()
                # dexes = coin_details.get('dexes')
                # liquidity_usd = sum(float(dex["liquidityUsd"]) for dex in dexes)
                return {
                    'symbol': coin_details.get('symbol'),
                    'name': coin_details.get('name'),
                    'coinType': coin_details.get('address'),
                    'decimals': coin_details.get('decimals'),
                    'price': coin_details.get('price'),
                    'supply': coin_details.get('totalSupply'),
                    'dexes': coin_details.get('dexes'),
                    # 'liquidity_usd' : liquidity_usd
                }
            else:
                print(f"Error: {response.status}")
                return None

async def fetch_coin_dexes(coinType):
    url = f"https://api.raidenx.io/api/v1/sui/tokens/{coinType}/dexes"
   
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                dex_details = await response.json()
                # dexes = coin_details.get('dexes')
                # liquidity_usd = sum(float(dex["liquidityUsd"]) for dex in dexes)
                return dex_details
            else:
                print(f"Error: {response.status}")
                return None
            
async def fetch_pair_details(pairId):
    url = f"https://api.raidenx.io/api/v1/sui/pairs/{pairId}"  
   
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                pair_details = await response.json()
                # return coin_details
                return pair_details
            else:
                print(f"Error: {response.status}")
                return None

async def load_rank_data():
    result_array = []

    for token in globals.global_token_arr:
        # Filter pairs matching the current token's coinType
        pairsOftoken = [pair["pairId"] for pair in globals.global_pair_arr if pair["coinType"] == token["coinType"]]

        # Initialize aggregated data
        token_data = {
            "coinType": token["coinType"],
            "symbol" : token["symbol"],
            "marketCap": 0,
            "holder": 0,
            "liquidity": 0,
            "volume": 0,
            "transaction": 0,
            "maker": 0,
        }

        for pair in pairsOftoken:
            # Fetch details for each pair
            pairInfo = await fetch_pair_details(pair)
            
            # Extract and aggregate relevant fields
            token_data["marketCap"] = float(pairInfo["tokenBase"]["priceUsd"]) * int(pairInfo["tokenBase"]["totalSupply"])
            token_data["holder"] = int(pairInfo["totalHolders"])
            token_data["liquidity"] += float(pairInfo["liquidity"])
            token_data["volume"] += (float(pairInfo["stats"]["volume"]['1h'])*24+float(pairInfo["stats"]["volume"]['6h'])*1.5 +float(pairInfo["stats"]["volume"]['24h'])*0.25)
            token_data["transaction"] += (float(pairInfo["stats"]["totalNumTxn"]['1h'])*24+float(pairInfo["stats"]["totalNumTxn"]['6h'])*1.5 +float(pairInfo["stats"]["totalNumTxn"]['24h'])*0.25)
            token_data["maker"] += (float(pairInfo["stats"]["maker"]['1h'])*24+float(pairInfo["stats"]["maker"]['6h'])*1.5 +float(pairInfo["stats"]["maker"]['24h'])*0.25)

        # Append the aggregated data to the result array
        result_array.append(token_data)  
    return result_array
            




# Main function
async def main():
    coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"

if __name__ == "__main__":
    asyncio.run(main())
