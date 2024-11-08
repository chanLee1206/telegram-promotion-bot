import asyncio
import time
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.config import BOT_TOKEN, CHAT_ID
from bot.commands import start, help_command, btn_trendStart_handler
from bot.send_info_board import send_info_board
from api_test.get_last_txn_info import getLast_trans_info_of_coin

from db.db import initialize_connection, close_connection, load_global_token_arr
from db.collet_last_txns import init_last_txns
import atexit

from globals import global_token_arr

# Initialize the application globally

last_txn_arr = []
cur_coin_idx = 0 

curCoinType = ""

async def other_task():
    while True:
        await asyncio.sleep(10)  # Example delay for other processing

def regist_lastTxn(txn_info):
    global last_txn_arr
    
    last_txn_arr[txn_info['coinSymbol']] = txn_info['digest']
   
    print('regist-', last_txn_arr)

async def track_coin_post(application, track_coin):
    global last_txn_arr

    print(f"Fetching Last_txn for {track_coin} at {time.strftime('%X')}")
    # print(last_txn_arr)

    txn_info = await getLast_trans_info_of_coin(track_coin['coinType'], last_txn_arr[track_coin['symbol']])
    
    print(txn_info)
    if 'digest' not in txn_info:
        print('old digest, or not formal transaction')
        return False
    # if LastTxnDigest == txn_info['digest']:
    # print('lastDigest-', txn_info['coinSymbol'], last_txn_arr[txn_info['coinSymbol']])

    if last_txn_arr[txn_info['coinSymbol']] == txn_info['digest']:
        print("Continue, not new!")
        return False
    else:
        LastTxnDigest = txn_info['digest']
        # print(txn_info)
        await send_info_board(application.bot, CHAT_ID, txn_info)
        regist_lastTxn(txn_info)

        return True
    


async def poll_transactions(application, interval=7):
    # global global_token_arr
    global cur_coin_idx

    # print(global_token_arr)
    while True:
        curCoin = global_token_arr[cur_coin_idx]

        postFlag = await track_coin_post(application, curCoin)

        await asyncio.sleep(interval) 
        
        cur_coin_idx = (cur_coin_idx + 1) % len(global_token_arr)
        # cur_coin_idx = 0


async def run_polling(application):
    """Runs the polling for the Telegram bot in the event loop."""
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Keep running until manually stopped
    while True:
        await asyncio.sleep(0.1)

async def main():
    global cur_coin_idx , last_txn_arr

    cur_coin_idx = 0

    initialize_connection()
    atexit.register(close_connection)

    load_global_token_arr()
    last_txn_arr = init_last_txns(global_token_arr)
    print("Initialized last_txn_arr:", last_txn_arr)  # Debugging line

    # return
    if not global_token_arr:
        print("Error: global_token_arr is empty after loading.")
        return

    # Now create the application instance
    application = Application.builder().token(BOT_TOKEN).read_timeout(20).write_timeout(20).build()

    # Add handlers for the /start and /help commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(btn_trendStart_handler, pattern="ready_to_start"))

    # Start polling for the bot
    global LastTxnDigest
    LastTxnDigest = ""

    # Start the polling for transactions
    asyncio.create_task(poll_transactions(application, interval=30))

    await run_polling(application)


if __name__ == "__main__":
    asyncio.run(main())  # Properly call the main function

