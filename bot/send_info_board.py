# send_info_board.py

import random
import string
from datetime import datetime, timedelta
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
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
    coin_ranking = random.randint(1, 100)  # Random ranking for the coin
    return {
        "coin_name": coin_name,
        "txn_id": txn_id,
        "txn_type": txn_type,
        "sui_cost": sui_cost,
        "coin_amount": coin_amount,
        "liquidity": liquidity,
        "mcap": mcap,
        "price_variation": price_variation,
        "coin_ranking": coin_ranking
    }

async def send_info_board(bot, chat_id: str, txn_info) -> None:
    # transaction = generate_random_transaction()
    # {'digest': '4DsF3wo9BPjYqe6dE7XiGCtpCSDrxHFKuVwa1dqd3yFF', 'time': '2024-11-04 16:40:38', 'coinName': 'Ancy Peosi', 'coinType': '0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY', 'price': '0.0000037975401766068425741056', 'decimals': 6, 'function': 'sell', 'marketCap': '37975.4018', 'realUnitCoinAmount': 71.719221024, 'realCurCoinAmount': -65642166.187885}
    print(txn_info)

    # Format price variation with + or - sign as needed
    # price_variation_str = f"{'+' if transaction['price_variation'] > 0 else ''}{transaction['price_variation']}% | Txn\n"

    # Styled message content with header and updated arrow icons
    message = (
        f"<b>Sui Trending</b>\n"  # Simulated green header with a green dot
        f"<b>${txn_info['coinName']} {txn_info['function']}!</b>\n\n"  # Bolded for emphasis
        "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢\n\n"  # Green dots with line break
        f"➡️ <b>{txn_info['realUnitCoinAmount']:.2f} SUI</b> (${txn_info['realUnitCoinAmount'] * 1.98:.2f})\n"  # Green right arrow
        f"⬅️ <b>{int(txn_info['realCurCoinAmount']):,} {txn_info['coinName']}</b>\n\n"  # Yellow left arrow for coin amount
        f"👤 <a href='https://example.com/txn/{txn_info['digest']}'>0x{txn_info['digest']}</a>: "
        # f"{price_variation_str}"  # Display formatted price variation with line break
        # f"💧 <b>Liquidity:</b> {txn_info['liquidity']}\n"
        f"🏛️ <b>Market Cap:</b> {txn_info['marketCap']}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>TRENDING</b> #{1} on <a href='https://twitter.com/Trending_Sui'>@Trending_Sui</a>\n\n"
        "🌐 <a href='https://example.com/dexs'>DexS</a> | 🔍 <a href='https://example.com/wallet'>Sui Wallet Tracker</a> | 🎯 <a href='https://example.com/sniper'>Sui Sniper Bot</a>\n\n"
        "👍 13   🔥 8   ❤️ 7   😂 1\n"  # Simulated reaction counts
    )

    # Single-line button at the end
    keyboard = [
        [InlineKeyboardButton(f"Buy {txn_info['coinName']} on Sui Sniper", url="https://example.com/buy_blub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message to channel
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )
