from api_test.txns_cointype import get_tx_hashes 
from api_test.coinInfo_cointype import fetch_coin_details 
# from api_test.txn_balanceChange import get_transaction_amounts
from api_test.txnInfo_digest import get_transaction_amounts

from datetime import datetime, timezone
import asyncio

import pdb
# from globals import global_last_txns

LastTxnDigest = ""

def trans_view_format(combined_raw_info):
    unitCoinDecimals = 9

    utc_time = datetime.fromtimestamp(int(combined_raw_info["timestampMs"]) / 1000, tz=timezone.utc)
    formatted_time = utc_time.strftime('%Y-%m-%d %H:%M:%S')

    trans_view_info = {
        "digest": combined_raw_info["txHash"],
        "time": formatted_time,
        "coinName": combined_raw_info["coinName"],
        "coinSymbol": combined_raw_info["coinSymbol"],
        "coinType": combined_raw_info["coinType"],
        "price": combined_raw_info["price"],
        "decimals": combined_raw_info["decimals"],
        "function": combined_raw_info["function"],
        "marketCap": combined_raw_info["marketCap"],
        "realUnitCoinAmount": combined_raw_info['unitCoinAmount'] / 10**unitCoinDecimals,
        "realCurCoinAmount": combined_raw_info['curCoinAmount'] / 10**combined_raw_info['decimals'],
    }
    return trans_view_info

async def getLast_trans_info_of_coin(coin_type, lastTxn):
    # pdb.set_trace()
    tx_hashes = await get_tx_hashes(coin_type, 1)
    
    if not tx_hashes or not isinstance(tx_hashes, list) or not tx_hashes[0]:
        return {"function": 'none'}  # Handle no hashes scenario

    functions = tx_hashes[0].get('functions')  # Use get to avoid KeyError

    if functions is None or len(functions) == 0:
        print(f"No functions found for transaction hash: {tx_hashes[0]['txHash']}")
        return {"function": 'none'}  # Handle the absence of function data

    if (tx_hashes[0]['txHash'] == lastTxn) :
        print('not new Txn, quit other apis')
        return {"function": 'none'}  # Handle the absence of function data

    # if "buy" not in functions[0]: 
    #     # print('not but function')
    #     return {"function": 'not buy'}

    await asyncio.sleep(5)  # Wait for the specified interval

    # custom_txHash = 'Bc3vPfA5D4ZGUSsXxdXEGewqpXtdJGg6JS3ZS5XQLzmB'
    coin_info = await fetch_coin_details(coin_type)
    await asyncio.sleep(5)

    if coin_info is None:        
        return {"function": 'none'}

    transaction_info = await get_transaction_amounts(tx_hashes[0]["txHash"])
    await asyncio.sleep(5)

    combined_info = {
        "txHash": tx_hashes[0]['txHash'],
        # 'txHash' : 'Bc3vPfA5D4ZGUSsXxdXEGewqpXtdJGg6JS3ZS5XQLzmB',
        "timestampMs": transaction_info['timestampMs'],
        "coinSymbol": coin_info['symbol'],
        "coinName": coin_info['name'],
        "coinType": coin_info['coinType'],
        "price": coin_info['price'],
        "decimals": coin_info['decimals'],
        "function": tx_hashes[0]['functions'][0],  # Assuming we want the first function
        "marketCap": coin_info['marketCap'],
        # "unitCoinAmount": abs(transaction_info['unit_coin']),  # Adding transInfo list as it is
        # "curCoinAmount": abs(transaction_info['cur_coin'])  # Adding transInfo list as it is
        "unitCoinAmount": transaction_info['unit_coin'],  # Adding transInfo list as it is
        "curCoinAmount": transaction_info['cur_coin']  # Adding transInfo list as it is
    }
    # pdb.set_trace()
    return trans_view_format(combined_info)

async def main():
    coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    TransInfo = await getLast_trans_info_of_coin(coin_type)
    print("\n Here coin info type:", TransInfo)

if __name__ == "__main__":
    asyncio.run(main())
