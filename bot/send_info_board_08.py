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
    coin_amount = random.randint(10000000, 1000000000)
    liquidity = f"${random.randint(1_000_000, 10_000_000):,}"
    mcap = f"${random.randint(10_000_000, 100_000_000):,}"
    price_variation = random.randint(-20, 40)  # Price variation between -20 and +40 percent
    return {
        "coin_name": coin_name,
        "txn_id": txn_id,
        "txn_type": txn_type,
        "sui_cost": sui_cost,
        "coin_amount": coin_amount,
        "liquidity": liquidity,
        "mcap": mcap,
        "price_variation": price_variation
    }

async def send_info_board(context: ContextTypes.DEFAULT_TYPE, chat_id: str) -> None:
    transaction = generate_random_transaction()

    # Format price variation with + or - sign as needed
    price_variation_str = f"{'+' if transaction['price_variation'] > 0 else ''}{transaction['price_variation']}% | Txn\n"

    # Styled message content with header and updated arrow icons
    message = (
        "🟢 <b>Sui Trending</b>\n"  # Simulated green header with a green dot
        f"<b>{transaction['coin_name']} {transaction['txn_type']}!</b>\n\n"  # Bolded for emphasis
        "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢\n\n"  # Green dots with line break
        f"➡️ <b>{transaction['sui_cost']} SUI</b> (${transaction['sui_cost'] * 1.83:.2f})\n\n"  # Green right arrow
        f"⬅️ <b>{transaction['coin_amount']:,} {transaction['coin_name'][1:]}</b>\n\n"  # Yellow left arrow for coin amount
        f"👤 <a href='https://example.com/txn/{transaction['txn_id']}'>0x{transaction['txn_id']}</a>: "
        f"{price_variation_str}"  # Display formatted price variation with line break
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
