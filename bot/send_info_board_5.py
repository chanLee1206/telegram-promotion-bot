# send_info_board.py

import random
import string
from datetime import datetime, timedelta
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

def generate_random_transaction():
    coin_name = random.choice(["$BLUB", "$XYZ", "$ABC"])  # Randomly select a coin name
    txn_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    txn_type = random.choice(["Buy", "Sell"])
    sui_cost = round(random.uniform(500, 1000), 2)
    blub_amount = random.randint(10000000, 1000000000)
    liquidity = f"${random.randint(1_000_000, 10_000_000):,}"
    mcap = f"${random.randint(10_000_000, 100_000_000):,}"
    return {
        "coin_name": coin_name,
        "txn_id": txn_id,
        "txn_type": txn_type,
        "sui_cost": sui_cost,
        "blub_amount": blub_amount,
        "liquidity": liquidity,
        "mcap": mcap
    }

async def send_info_board(context: ContextTypes.DEFAULT_TYPE, chat_id: str) -> None:
    transaction = generate_random_transaction()

    # Styled message content with header and updated arrow icons
    message = (
        "🟢 <b>Sui Trending</b>\n"  # Simulated green header with a green dot
        f"<b>{transaction['coin_name']} {transaction['txn_type']}!</b>\n\n"  # Bolded for emphasis
        "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢\n\n"  # Green dots with line break
        f"➡️ <b>{transaction['sui_cost']} SUI</b> (${transaction['sui_cost'] * 1.83:.2f})\n"  # Green right arrow
        f"⬅️ <b>{transaction['blub_amount']:,} {transaction['coin_name'][1:]}</b>\n\n"  # Yellow left arrow for blub amount
        f"👤 <code>0x{transaction['txn_id']}</code> ({transaction['txn_type']})\n"
        f"💧 <b>Liquidity:</b> {transaction['liquidity']}\n"
        f"🏛️ <b>Market Cap:</b> {transaction['mcap']}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<b>TRENDING</b> 🔥 on <a href='https://twitter.com/Trending_Sui'>@Trending_Sui</a>\n\n"
        "🌐 DexS | 🔍 Sui Wallet Tracker | 🎯 Sui Sniper Bot\n\n"
        "👍 13   🔥 8   ❤️ 7   😂 1\n"  # Simulated reaction counts
    )

    # Single-line button at the end
    keyboard = [
        [InlineKeyboardButton(f"Buy {transaction['coin_name']} on Sui Sniper", url="https://example.com/buy_blub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message to channel
    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )
