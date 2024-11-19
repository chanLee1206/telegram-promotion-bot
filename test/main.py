import asyncio
import socketio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import logging

# Initialize the Socket.IO client
sio = socketio.AsyncClient()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your Telegram bot token
from config import BOT_TOKEN, CHAT_ID

# Function to start the bot and handle commands
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! I'm a bot that tracks transactions.")

async def help(update: Update, context: CallbackContext):
    await update.message.reply_text("Use /start to get started.\nI track WebSocket transactions in real-time.")

async def send_transaction(update: Update, context: CallbackContext):
    # Sample function to send a manual message or the latest transaction
    # Replace with your own logic if needed
    await update.message.reply_text("Fetching latest transaction...")

# Initialize the bot and set up command handlers
async def telegram_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("send_txn", send_transaction))

    # Start the bot
    await application.initialize()
    await application.start_polling()

# Asynchronous function to handle incoming transactions from WebSocket
async def on_connect():
    subscription_message = {
        "event": "SUBSCRIBE_REALTIME_TRANSACTION",
        "data": {}
    }
    print("Connected to WebSocket!")
    await sio.emit("SUBSCRIBE_REALTIME_TRANSACTION", subscription_message)
    print("Subscription message sent.")

@sio.event
async def connect():
    print("Socket connected!")
    await on_connect()

@sio.event
async def connect_error(data):
    print(f"Connection failed with error: {data}")

@sio.event
async def disconnect():
    print("Disconnected from WebSocket!")

@sio.on("TRANSACTION")
async def handle_transaction(data):
    try:
        coin_symbol = data["pairId"]
        digest = data["hash"]
        txn_info = {
            "digest": digest,
            "coinSymbol": coin_symbol,
            "baseAmount": data["baseAmount"],
            "priceUsd": data["priceUsd"],
            "timestamp": data["timestamp"],
        }
        # Print the transaction to the console
        print(f"New transaction for {coin_symbol}: {txn_info}")
    except Exception as e:
        print(f"Error processing transaction: {e}")

# Main function to run the bot and WebSocket client concurrently
async def main():
    SOCKET_URL = "wss://ws-sui.raidenx.io"  # WebSocket URL
    try:
        # Start the WebSocket connection
        await sio.connect(SOCKET_URL)
        print("Attempting to connect to WebSocket server...")

        # Start the Telegram bot
        asyncio.create_task(telegram_bot())  # Run the Telegram bot in the background

        # Keep the WebSocket connection running
        await sio.wait()
    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
