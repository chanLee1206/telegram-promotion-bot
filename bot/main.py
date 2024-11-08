import asyncio
import time
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.config import BOT_TOKEN, CHAT_ID
from bot.commands import start, help_command, btn_trendStart_handler
from bot.send_info_board import send_info_board
from api_test.get_last_txn_info import getLast_trans_info_of_coin

from db.getMemeTokens import load_global_token_arr
from globals import global_token_arr

# Initialize the application globally

LastTxnDigest = ""
cur_coin_idx = 0 

curCoinType = ""

async def other_task():
    while True:
        await asyncio.sleep(10)  # Example delay for other processing

async def get_transaction_data(application, coin_type):
    global LastTxnDigest
    print(f"Fetching Last_txn for {coin_type} at {time.strftime('%X')}")
    txn_info = await getLast_trans_info_of_coin(coin_type)
    
    if 'digest' not in txn_info:
        print('no digest, not buy or sell')
        return

    if LastTxnDigest == txn_info['digest']:
        print("Continue, not new!")
        return
    else:
        LastTxnDigest = txn_info['digest']
        print(txn_info)

    try:
        await send_info_board(application.bot, CHAT_ID, txn_info)
    except Exception as e:
        print(f"Error sending message: {e}")
    await asyncio.sleep(0.1)



async def poll_transactions(application, interval=7):
    # global global_token_arr
    global cur_coin_idx

    # print(global_token_arr)
    while True:
        curCoin = global_token_arr[cur_coin_idx]

        await get_transaction_data(application, curCoin['coinType'])
        await asyncio.sleep(interval)  # Wait for the specified interval
        
        cur_coin_idx = (cur_coin_idx + 1) % len(global_token_arr)


async def run_polling(application):
    """Runs the polling for the Telegram bot in the event loop."""
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Keep running until manually stopped
    while True:
        await asyncio.sleep(0.1)

async def main():
    global cur_coin_idx

    cur_coin_idx = 0
    # print(global_token_arr)
    token_arr = load_global_token_arr()
    
    # print("\n",len(global_token_arr), global_token_arr)
    # return
    
    if not token_arr:
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
    asyncio.create_task(poll_transactions(application, interval=40))

    await run_polling(application)


if __name__ == "__main__":
    asyncio.run(main())  # Properly call the main function

