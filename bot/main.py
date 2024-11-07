import asyncio
import time
from telegram.ext import Application, CommandHandler
from bot.config import BOT_TOKEN, CHAT_ID
from bot.commands import start, help_command
from bot.send_info_board import send_info_board
from api_test.get_last_txn_info import getLast_trans_info_of_coin  # Correct import

# Initialize the application globally
# application = Application.builder().token(BOT_TOKEN).build()
application = Application.builder().token(BOT_TOKEN).read_timeout(20).write_timeout(20).build()
LastTxnDigest = ""

async def other_task():
    while True:
        await asyncio.sleep(10)  # Example delay for other processing

async def get_transaction_data(coin_type):
    # Fetch transaction data and potentially call the imported function
    global LastTxnDigest
    global context

    print(f"Fetching Last_txn for {coin_type} at {time.strftime('%X')}")
    
    txn_info = await getLast_trans_info_of_coin(coin_type)  # Use await here
    
    # Ensure txn_info has the expected structure before accessing 'digest'
    if 'digest' not in txn_info:
        return  # Handle the case where digest is not available

    if LastTxnDigest == txn_info['digest']:
        print("Continue, not new!")
        return
    else:
        LastTxnDigest = txn_info['digest']
        print(txn_info)  # Print or process the transaction info as needed

    try:
        await send_info_board(application.bot, CHAT_ID, txn_info)
    except Exception as e:
        print(f"Error sending message: {e}")

    await asyncio.sleep(0.1)  # Simulate processing time


async def poll_transactions(coin_type, interval=10):
    while True:
        await get_transaction_data(coin_type)
        await asyncio.sleep(interval)  # Wait for the specified interval

async def main():
    coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"  # Set the coin type you want to track
    global LastTxnDigest 
    LastTxnDigest = ""
    await asyncio.gather(
        poll_transactions(coin_type, interval=60),  # or listen_to_transactions(coin_type) for WebSocket
        other_task()
    )

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

if __name__ == "__main__":
    asyncio.run(main())
