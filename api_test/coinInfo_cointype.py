import requests

import aiohttp
import asyncio

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
""" async def main():
    coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    details = await fetch_coin_details(coin_type)
    print(details)

# Running the example
if __name__ == "__main__":
    asyncio.run(main()) """


