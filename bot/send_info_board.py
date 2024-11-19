# send_info_board.py
import os

import string
from math import log10

from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.api import fetch_coin_details

import globals

async def send_info_board(bot, chat_id: str, txn_info) -> None:
    print('channel_board_add')
    print(txn_info)
    coin_symbol = txn_info.get('token').split('::')[-1]
    search_coinType = txn_info.get('token')
    selected_token = next((item for item in globals.global_token_arr if item['coinType'] == search_coinType), None)

    api_coin_data = await fetch_coin_details(search_coinType)
    liquidity = api_coin_data.get('liquidity_usd', '_')
    
    # print(search_coinType, ' : ', selected_token)

    img_cnt = int(log10(float(txn_info['quoteAmount']) + 1) * 10) + 1
    image_particles = "🟢" *  img_cnt  
    # coin_symbol = selected_token['symbol']

    
    message = (
        f"<b>${coin_symbol} :  {txn_info['tradingType']}!</b>\n\n"  # Bolded for emphasis
        f"{image_particles}\n\n"  
        f"➡️ <b>{float(txn_info['quoteAmount']):.2f,} SUI</b> (${float(txn_info['totalUsd']):.2f,})\n"  
        f"⬅️ <b>{int(txn_info['baseAmount']):,} </b> ${coin_symbol}\n\n"  
        f"👤 <a href='https://suiscan.xyz/mainnet/account/{txn_info['maker'].get('address')}/activity'>0x{txn_info['maker'].get('address')[:2]}...{txn_info['maker'].get('address')[-3:]}</a>: New <a href='https://suiscan.xyz/mainnet/tx/{txn_info['hash']}'>TXN</a>\n"

        # f"{price_variation_str}"  # Display formatted price variation with line break
        f"💧 <b>Liquidity:</b> ${int(liquidity):,}\n"
        f"🏛️ <b>Market Cap: $</b> {int(float(txn_info.get('priceUsd'))*selected_token['supply']):,}\n\n"
        f"<b>TRENDING </b> #{1} on @Ancy Trending\n\n"
        
        f"🏆<a href='{globals.pinned_trending_url}'>Trending</a> | 👁️<a href='{selected_token['launchURL']}'>{selected_token['launchPad']}</a>"         
    )
    # print(message)
    keyboard = [
        [InlineKeyboardButton(f"Buy {coin_symbol} on {selected_token['launchPad']}", url=f"{selected_token['launchURL']}")]
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

