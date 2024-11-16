from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. Use /help to see what I can do.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('I can respond to:\n/start - Start the bot\n/help - Show this help message')

def main():
    """Run the bot."""
    # Create the application and pass in the bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for the /start and /help commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user sends a signal to stop
    application.run_polling()

if __name__ == '__main__':
    main()
