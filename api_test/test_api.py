from api_test.coinInfo_cointype import fetch_coin_details 

def getLast_trans_info_of_coin(coin_type):
    coin_info = fetch_coin_details(coin_type)
    return coin_info

coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
TransInfo = getLast_trans_info_of_coin(coin_type)
print("\n here coininfo_type", TransInfo)


