import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from bot.config import BOT_TOKEN, CHAT_ID

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

async def send_pinned_message():
    # Text content of the message
    message_text = "Welcome! Get started by booking your trending slot below. I'll list trending ranking here."
    
    # Define the inline keyboard with the "Book Trending" button
    keyboard = [
        [InlineKeyboardButton("Book Trending", url="https://t.me/suiTokenPromote_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message and pin it in the channel
    message = await bot.send_message(
        chat_id=CHAT_ID,
        text=message_text,
        reply_markup=reply_markup
    )
    
    # Pin the message
    await bot.pin_chat_message(chat_id=CHAT_ID, message_id=message.message_id)

# Run the asynchronous function
asyncio.run(send_pinned_message())
