# send_info_board.py
import os

import string
from math import log10

from datetime import datetime, timedelta
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def send_info_board(bot, chat_id: str, txn_info) -> None:
    print('channel_board_add')
    img_cnt = int(log10(abs(txn_info['realUnitCoinAmount']) + 10) * 10)
    image_particles = "🟢" *  img_cnt  # You can replace this emoji with another if needed

    real_unit_icon = "➡️" if txn_info['realUnitCoinAmount'] >= 0 else "⬅️"
    real_cur_icon = "➡️" if txn_info['realCurCoinAmount'] >= 0 else "⬅️"

    # Styled message content with header and updated arrow icons
    message = (
        # f"<b>Sui Trending</b>\n"  # Simulated green header with a green dot
        f"<b>${txn_info['coinName']} :  {txn_info['function']}!</b>\n\n"  # Bolded for emphasis
        f"{image_particles}\n\n"  # Add the image particles row
        f"{real_unit_icon} <b>{txn_info['realUnitCoinAmount']:.2f} SUI</b> (${txn_info['realUnitCoinAmount'] * 1.98:.2f})\n"  # Green right arrow
        f"{real_cur_icon} <b>{int(txn_info['realCurCoinAmount']):,} ${txn_info['coinSymbol']}</b>\n\n"  # Yellow left arrow for coin amount
        f"👤 <a href='https://suiscan.xyz/mainnet/tx/{txn_info['digest']}'>0x{txn_info['digest'][:2]}...{txn_info['digest'][-3:]}</a>: New TXN\n"
        # f"{price_variation_str}"  # Display formatted price variation with line break
        # f"💧 <b>Liquidity:</b> {txn_info['liquidity']}\n"
        f"🏛️ <b>Market Cap: $</b> {int(txn_info['marketCap']):,}\n"
        "\n"
        f"<b>TRENDING</b> #{1} on <a href='https://twitter.com/Trending_Sui'>@Trending_Sui</a>\n\n"
        # "🌐 <a href='https://example.com/dexs'>DexS</a> | 🔍 <a href='https://example.com/wallet'>Sui Wallet Tracker</a> | 🎯 <a href='https://example.com/sniper'>Sui Sniper Bot</a>\n\n"
        # "👍 13   🔥 8   ❤️ 7   😂 1\n"  # Simulated reaction counts
    )

    # Single-line button at the end
    keyboard = [
        [InlineKeyboardButton(f"Buy {txn_info['coinName']} on Sui Sniper", url="https://example.com/buy_blub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

        # Path to your image file
    # image_path = os.path.join(os.path.dirname(__file__), "../assets/ancy_expand.png")

    # # Send image with caption as message content
    # await bot.send_photo(
    #     chat_id=chat_id,
    #     photo=open(image_path, 'rb'),
    #     caption=message,
    #     parse_mode=ParseMode.HTML,
    #     reply_markup=reply_markup
    # )

    # Send message to channel
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

