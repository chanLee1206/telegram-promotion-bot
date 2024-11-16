
def init_last_txns(token_arr):
    txn_dict = {item['symbol']: '' for item in token_arr}
    return txn_dict