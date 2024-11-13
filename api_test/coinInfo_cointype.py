import requests

import aiohttp
import asyncio

import globals

async def fetch_coin_details(coin_type):
    url = f"https://api.blockberry.one/sui/v1/coins/{coin_type}"
    headers = {
        "accept": "*/*",
        "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"
    }

    # Use aiohttp to make an asynchronous GET request
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            # Check response status and return the result if successful
            
            if response.status == 200:
                coin_details = await response.json()
                # print(global_token_arr)
                coin_extract_info = {
                    'coinType': coin_details.get('coinType'),
                    'name': coin_details.get('coinName'),
                    'symbol': coin_details.get('coinSymbol'),
                    'decimals': coin_details.get('decimals'),
                    'price': coin_details.get('price'),
                    'supply': coin_details.get('supply'),
                    'marketCap': coin_details.get('fdv')
                }
                return coin_extract_info
            else:
                print(f"Error: {response.status}")
                return None

# Example usage

async def getUnitCoin() :
    sui_coinType = "0x2::sui::SUI"
    sui_coin = await fetch_coin_details(sui_coinType)
    globals.unit_coin_price = sui_coin.get('price', 2.0)
    return {'unit_coin_price': globals.unit_coin_price}

async def main():
    # coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    # coin_type = "0x82f7064c75c9b0533030f77715225ab438a359071dadfa316ef0b4cc8a184c8e::bubl::BUBL"
    coin_type = "0xe0fbaffa16409259e431b3e1ff97bf6129641945b42e5e735c99aeda73a595ac::suiyan::SUIYAN"
                    # "0xe0fbaffa16409259e431b3e1ff97bf6129641945b42e5e735c99aeda73a595ac::suiyan::SUIYAN"
    details = await fetch_coin_details(coin_type)
    print(details)

# Running the example
if __name__ == "__main__":
    asyncio.run(main())


