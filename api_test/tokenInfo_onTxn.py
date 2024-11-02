# def fetch_coin_details(coin_type):
# def get_transaction_amounts(transaction_digest):

# import fetch_coin_details from coinInfo_cointype
# import get_transaction_amounts from txn_balanceChange

from txns_cointype import get_tx_hashes 
from coinInfo_cointype import fetch_coin_details 
from txn_balanceChange import get_transaction_amounts

coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"

tx_hashes = get_tx_hashes(coin_type, 1)
coin_info = fetch_coin_details(coin_type)
transaction_info = get_transaction_amounts(tx_hashes[0]["txHash"])
# print(coin_info)
combined_info = {
    "name": coin_info['name'],
    "coinType" : coin_info['coinType'],
    # "timestamp": timestamp,
    "price": coin_info['price'],
    "function": tx_hashes[0]['functions'][0],  # Assuming we want the first function
    "marketCap": coin_info['marketCap'],
    "txHash": tx_hashes[0]['txHash'],
    "transInfo": transaction_info  # Adding transInfo list as it is
}
# print("digest-info", tx_hashes[0], "coin_info-", coin_info, "transInfo-",transaction_info)
print(combined_info)


