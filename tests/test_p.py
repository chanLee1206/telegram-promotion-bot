import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from bot.config import BOT_TOKEN

# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Welcome to the bot. Use /help to see available commands.")

# Define the /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = "Here are the available commands:\n" \
                "/start - Start the bot\n" \
                "/help - Show this help message"
    await update.message.reply_text(help_text)

# Define the periodic task function
async def my_action():
    while True:
        print("Starting action...")
        await asyncio.sleep(2)  # Simulate 10-second processing time
        print("Action completed.")
        await asyncio.sleep(5)  # Wait for 45 seconds before running again

# Run polling for the Telegram bot in the event loop
async def run_polling(application):
    """Runs the polling for the Telegram bot in the event loop."""
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Keep running until manually stopped
    while True:
        await asyncio.sleep(1)

# Main function to set up and run the bot with periodic task
async def main():
    # Create the application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for the /start and /help commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Start the periodic task in the background
    asyncio.create_task(my_action())

    # Start polling for the bot
    await run_polling(application)

# Run the bot and periodic function
if __name__ == "__main__":
    asyncio.run(main())
