#commands.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # The bot instance is already available via context
    bot = context.bot
    
    message_text = (
        "📈 Sui Trending Fast Track\n\n"
        "@Trending_Sui\n\n"
        "How to use:\n"
        "1️⃣ Click 'I'm ready to Trend'\n"
        "2️⃣ Paste your token's contract address\n"
        "3️⃣ Bot will find your tg/twitter/web automatically (you will be able to change)\n"
        "4️⃣ Choose desired position & duration for trending\n"
        "5️⃣ Pay SUI to the given wallet within 10 min\n"
        "6️⃣ Wait for tx confirmation and click 'Start Trending'"
    )

    # Define the inline keyboard with the "I'm ready to start" button
    keyboard = [
        [InlineKeyboardButton("I'm ready to trend", callback_data="ready_to_start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline button
    await bot.send_message(
        chat_id=update.message.chat_id,
        text=message_text,
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to:\n/start - Start the bot\n/help - Show this help message'
    )

# Define a callback function to handle the button click
async def button_callback(update: Update, context: CallbackContext) -> None:
    # Acknowledge the button click and respond with the new message
    query = update.callback_query
    await query.answer()  # Required to stop the "loading" circle

    # Send the reply to prompt for token contract input
    # await query.edit_message_text(text="Select token to boost trending")
    await query.message.reply_text(text = "Select token to boost trending")


