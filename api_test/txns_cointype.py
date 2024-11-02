import requests

def get_tx_hashes(coin_type, page_size):
    url = f"https://api.blockberry.one/sui/v1/coins/{coin_type}/transactions?page=0&size={page_size}&orderBy=DESC&sortBy=AGE"
    headers = {
        "accept": "*/*",
        "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"  # Replace with your actual API key
    }
    try:
        response = requests.post(url, headers=headers)
        result_txns = response.json().get('content', [])
        # tx_hashes = [tx['txHash'] for tx in result_txns]
        # return tx_hashes
        transaction_details = [{'functions': tx.get('functions', []), 'txHash': tx['txHash']} for tx in result_txns]
        tx_hashes = [{'txHash': tx['txHash'], 'functions': tx.get('functions', [])} for tx in result_txns]
        return tx_hashes
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except ValueError:
        print("Error parsing JSON response.")
        return []

# Example usage:
# coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
# tx_hashes = get_tx_hashes(coin_type, 1)
# print(tx_hashes)
