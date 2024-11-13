import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from bot.config import BOT_TOKEN, CHAT_ID
# import globals

import datetime

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

async def send_pinned_message():
    global_token_arr = [
        {
            "id": 0,
            "symbol": "SUI",
            "name": "Sui",
            "coinType": "0x2::sui::SUI",
            "launchPad": "Move Pump",
            "launchURL": None,
            "decimals": 9,
            "supply": 10000000000,
            "allow": 1
        },
        {
            "id": 1,
            "symbol": "ANCY",
            "name": "Ancy Peosi",
            "coinType": "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY",
            "launchPad": "Move Pump",
            "launchURL": "https://movepump.com/token/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY",
            "decimals": 6,
            "supply": 10000000000,
            "allow": 1
        },
        {
            "id": 3,
            "symbol": "SUIYAN",
            "name": "Super Suiyan",
            "coinType": "0xe0fbaffa16409259e431b3e1ff97bf6129641945b42e5e735c99aeda73a595ac::suiyan::SUIYAN",
            "launchPad": "Move Pump",
            "launchURL": "https://movepump.com/token/0xe0fbaffa16409259e431b3e1ff97bf6129641945b42e5e735c99aeda73a595ac::suiyan::SUIYAN",
            "decimals": 6,
            "supply": 10000000000,
            "allow": 1
        },
        {
            "id": 5,
            "symbol": "AAA",
            "name": "aaa cat",
            "coinType": "0xd976fda9a9786cda1a36dee360013d775a5e5f206f8e20f84fad3385e99eeb2d::aaa::AAA",
            "launchPad": "Move Pump",
            "launchURL": "0xd976fda9a9786cda1a36dee360013d775a5e5f206f8e20f84fad3385e99eeb2d::aaa::AAA",
            "decimals": 6,
            "supply": 10000000000,
            "allow": 1
        }
    ]

    # Text content of the message
    rankingIcons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    formatted_tokens = []

    # Corrected for loop
    for index, token in enumerate(global_token_arr):
        rankIcon = rankingIcons[index] if index < len(rankingIcons) else "🔘"  # Default fallback icon if out of range
        coin_symbol = token["symbol"]
        launchPad = token.get("launchPad", "No URL")  # Default to "No URL" if launchPad is None
        formatted_tokens.append(f"{rankIcon} {coin_symbol} | {launchPad}")

    # Join all formatted token strings into a single paragraph
    rank_paragraph = "\n\n".join(formatted_tokens)

    # Get the current UTC time
    utc_time = datetime.datetime.now(datetime.timezone.utc)
    formatted_utc_time = utc_time.strftime("%H:%M:%S UTC")

    # Create the message text
    message_text = (
        f"🍒 <b>Ancy's Trending:</b> SUI, Move Pump, PUMPFUN, MOONSHOT ...\n\n"     
        f"{rank_paragraph}\n\n"
        f"📅 Update time: <code>{formatted_utc_time}</code>"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅Book Trending", url="https://t.me/suiTokenPromote_bot?start=1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message and pin it in the channel
    message = await bot.send_message(
        chat_id=CHAT_ID,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    
    # Pin the message
    await bot.pin_chat_message(chat_id=CHAT_ID, message_id=message.message_id)
    # globals.pinned_msgID = message.message_id
    # globals.pinned_trending_url = f"https://t.me/suitrending_boost/{message.message_id}"
    

# Run the asynchronous function
asyncio.run(send_pinned_message())
