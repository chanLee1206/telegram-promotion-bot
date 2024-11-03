# main.py
import asyncio
import time

from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN, CHAT_ID
from commands import start, help_command
from send_info_board import send_info_board  # Import clear_bot_messages

async def other_task():
    while True:
        print("Performing other task")
        await asyncio.sleep(10)  # Example delay for other processin

async def get_transaction_data(coin_type):
    # This is your function that fetches the transaction data
    # Simulate API call with a delay
    print(f"Fetching transactions for {coin_type} at {time.strftime('%X')}")
    # Process your transaction data here
    await asyncio.sleep(1)  # Simulate processing time

async def poll_transactions(coin_type, interval=7):
    while True:
        await get_transaction_data(coin_type)
        await asyncio.sleep(interval)  # Wait for the specified interval

def main():

async def main():
    coin_type = "your_coin_type"
    await asyncio.gather(
        poll_transactions(coin_type, interval=5),  # or listen_to_transactions(coin_type) for WebSocket
        other_task()
    )

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application = Application.builder().token(BOT_TOKEN).build()
# application.run_polling()
asyncio.run(main())
