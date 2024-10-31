import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application

# Define your bot token and channel name
TOKEN = 'YOUR_BOT_TOKEN'
CHANNEL_ID = '@your_channel_name'

# Function to create and format the info message
def create_info_message():
    message_text = """
    <b>Welcome to Our Channel!</b>
    Here are some quick links:
    - <a href="https://example.com">Visit our website</a>
    - <a href="https://example.com/community">Join our community</a>

    <b>Services:</b>
    - 📦 Service 1: Description
    - 🔧 Service 2: Description

    <b>Contact us for more information!</b>
    """

    # Create inline buttons
    keyboard = [
        [InlineKeyboardButton("Visit Website", url='https://example.com')],
        [InlineKeyboardButton("Join Community", url='https://example.com/community')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    return message_text, reply_markup

# Function to send info message to the channel
async def send_info_message(bot: Bot):
    message_text, reply_markup = create_info_message()
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message_text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Main function to run the bot
async def main():
    # Initialize the application
    application = Application.builder().token(TOKEN).build()

    # Send the info message when the bot starts
    await send_info_message(application.bot)

    # Start polling for updates
    await application.run_polling()

# Run the bot using the correct event loop
if __name__ == '__main__':
    try:
        # Use existing event loop if it exists
        asyncio.get_running_loop().run_until_complete(main())
    except RuntimeError:  # No running loop
        asyncio.run(main())
