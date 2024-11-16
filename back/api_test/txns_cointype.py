import aiohttp
import asyncio

async def get_tx_hashes(coin_type, page_size):
    url = f"https://api.blockberry.one/sui/v1/coins/{coin_type}/transactions?page=0&size={page_size}&orderBy=DESC&sortBy=AGE"
    headers = {
        "accept": "*/*",
        "x-api-key": "Lmn3IP5rbjuULtIJLNzUWJGfmbymVE"  # Replace with your actual API key
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                response.raise_for_status()  # Raise an error for bad responses
                result_txns = await response.json()
                tx_hashes = [{'txHash': tx['txHash'], 'functions': tx.get('functions', [])} for tx in result_txns.get('content', [])]
                # print(tx_hashes)
                return tx_hashes
    except Exception as e:
        print(f"Error fetching transaction hashes: {e}")
        return []     
""" async def main():
    # Define your test parameters
    coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    page_size = 1  # Adjust the page size as needed

    # Call the get_tx_hashes function
    tx_hashes = await get_tx_hashes(coin_type, page_size)

    # Print the output
    if tx_hashes:
        print("Transaction Hashes:")
        for txn in tx_hashes:
            print(f"TxHash: {txn['txHash']}, Functions: {txn['functions']}")
    else:
        print("No transaction hashes returned or an error occurred.")

if __name__ == "__main__":
    asyncio.run(main()) """
