# send_info_board.py
import os

import string
from math import log10

from datetime import datetime, timedelta
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import globals

async def send_info_board(bot, chat_id: str, txn_info) -> None:
    print('channel_board_add')
    img_cnt = int(log10(abs(txn_info['realUnitCoinAmount']) + 1) * 10) + 1
    image_particles = "🟢" *  img_cnt  

    real_unit_icon = "➡️" if txn_info['realUnitCoinAmount'] >= 0 else "⬅️"
    real_cur_icon = "➡️" if txn_info['realCurCoinAmount'] >= 0 else "⬅️"

    message = (
        f"<b>${txn_info['coinName']} :  {txn_info['function']}!</b>\n\n"  # Bolded for emphasis
        f"{image_particles}\n\n"  
        f"{real_unit_icon} <b>{txn_info['realUnitCoinAmount']:.2f} SUI</b> (${txn_info['realUnitCoinAmount'] * globals.unit_coin_price:.2f})\n"  
        f"{real_cur_icon} <b>{int(txn_info['realCurCoinAmount']):,} </b> ${txn_info['coinSymbol']}\n\n"  
        f"👤 <a href='https://suiscan.xyz/mainnet/account/{txn_info['sender']}/activity'>0x{txn_info['sender'][:2]}...{txn_info['sender'][-3:]}</a>: New <a href='https://suiscan.xyz/mainnet/tx/{txn_info['digest']}'>TXN</a>\n"

        # f"{price_variation_str}"  # Display formatted price variation with line break
        # f"💧 <b>Liquidity:</b> {txn_info['liquidity']}\n"
        f"🏛️ <b>Market Cap: $</b> {int(txn_info['marketCap']):,}\n"
        "\n"
        f"<b>TRENDING </b> #{1} on @Ancy Trending\n\n"
        
        f"🏆<a href='{globals.pinned_trending_url}'>Trending</a> | 👁️<a href='{txn_info['launchURL']}'>{txn_info['launchPad']}</a>"         
    )

    keyboard = [
        [InlineKeyboardButton(f"Buy {txn_info['coinName']} on {txn_info['launchPad']}", url=f"{txn_info['launchURL']}")]
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

    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
        # reply_markup=reply_markup
        disable_web_page_preview=True
    )

