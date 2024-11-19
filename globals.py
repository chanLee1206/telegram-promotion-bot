
import json
import os
from bot.db import load_global_token_arr

FILENAME = os.path.join(os.path.dirname(__file__), "global_data.json")

global_token_arr = []
unit_coin_price = 2.0
pinned_trending_url = "https://t.me/suitrending_boost/571"
pinned_msgID = 571
last_txn_arr = []
total_account_arr = ['0xd6840994167c67bf8063921f5da138a17da41b3f64bb328db1687ddd713c5281']

# def remove_deffect_txn_arr(global_token_arr, last_txn_arr):
#     for token in global_token_arr:
#         if token['symbol'] not in last_txn_arr:
#             # last_txn_arr[token['symbol']] = ''  # Add with empty string if missing

#     return last_txn_arr

def load_globals():
    global global_token_arr, unit_coin_price, pinned_trending_url, pinned_msgID, last_txn_arr

    global_token_arr = load_global_token_arr() #load from db
    if global_token_arr :
        try:
            with open(FILENAME, "r") as f:
                data = json.load(f)
                # last_txn_arr = data.get("last_txn_arr", [])
                # remove_deffect_txn_arr(global_token_arr, last_txn_arr)
                unit_coin_price = data.get("unit_coin_price", 2.0)
                pinned_trending_url = data.get("pinned_trending_url")
                pinned_msgID = data.get("pinned_msgID")
        except FileNotFoundError:
            print(f"Warning: {FILENAME} not found. Using default values.")
    else :
        try:
            with open(FILENAME, "r") as f:
                data = json.load(f)
                global_token_arr = data.get("global_token_arr")
                last_txn_arr = data.get("last_txn_arr", [])
                # remove_deffect_txn_arr(global_token_arr, last_txn_arr)
                
                unit_coin_price = data.get("unit_coin_price", 2.0)
                pinned_trending_url = data.get("pinned_trending_url")
                pinned_msgID = data.get("pinned_msgID")
        except FileNotFoundError:
            print(f"Warning: {FILENAME} not found. Using default values.")
            
# Function to save current global values to JSON file
def save_globals():
    data = {
        "global_token_arr": global_token_arr,
        "last_txn_arr": last_txn_arr,
        "unit_coin_price": unit_coin_price,
        "pinned_trending_url": pinned_trending_url,
        "pinned_msgID": pinned_msgID,
    }
    with open(FILENAME, "w") as f:
        json.dump(data, f)

# Initialize globals on import
