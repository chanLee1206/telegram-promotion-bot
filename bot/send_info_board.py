# send_tracking_token.py
import os

import string
from math import log10
import datetime


from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.api import fetch_coin_details, fetch_pair_details, fetch_coin_dexes

import globals

async def send_tracking_token(bot, chat_id: str, txn_info) -> None:
    # print(txn_info)
    coin_symbol = txn_info.get('token').split('::')[-1]
    search_coinType = txn_info.get('token')
    selected_token = next((item for item in globals.global_token_arr if item['coinType'] == search_coinType), None)

    # api_coin_data = await fetch_coin_details(search_coinType)
    api_coin_dexes = await fetch_coin_dexes(search_coinType)
    
    api_pair_data = await fetch_pair_details(txn_info['pairId'])

    liquidity_usd = sum(float(dex["liquidityUsd"]) for dex in api_coin_dexes)
    # print(api_coin_dexes, '\n')
    # print(liquidity_usd, '\n')
    
    # liquidity = api_coin_dexes.get('liquidity_usd', '_')
    
    price_vari_6h = float(api_pair_data.get('stats','New').get('percent','New').get('6h','New'))

    if float(price_vari_6h)<0 :
        price_vari_6h = ""
    else :
        price_vari_6h = f"+{price_vari_6h:.2f}%"
    print('channel_board_add')
    
    # print(search_coinType, ' : ', selected_token)

    img_cnt = int(log10(float(txn_info['quoteAmount']) + 1) * 10) + 1
    image_particles = "🟢" *  img_cnt  
    # coin_symbol = selected_token['symbol']

    
    message = (
        f"<b>${coin_symbol} :  {txn_info['tradingType']}!</b>\n\n"  # Bolded for emphasis
        f"{image_particles}\n\n"  
        f"➡️ <b>{float(txn_info['quoteAmount']):.2f} SUI</b> (${float(txn_info['totalUsd']):.2f})\n"  
        f"⬅️ <b>{int(float(txn_info['baseAmount'])):,} </b> ${coin_symbol}\n\n"  
        f"👤 <a href='https://suiscan.xyz/mainnet/account/{txn_info['maker'].get('address')}/activity'>0x{txn_info['maker'].get('address')[:2]}...{txn_info['maker'].get('address')[-3:]}</a>: {price_vari_6h} <a href='https://suiscan.xyz/mainnet/tx/{txn_info['hash']}'>TXN</a>\n"

        f"💧 <b>Liquidity:</b> ${int(liquidity_usd):,}\n"
        f"🏛️ <b>Market Cap: $</b> {int(float(txn_info.get('priceUsd'))*selected_token['supply']):,}\n\n"
        f"<b>TRENDING </b> #{1} on @Ancy Trending\n\n"
        
        f"🏆<a href='{globals.pinned_trending_url}'>Trending</a> | 👁️<a href='{selected_token['launchURL']}'>{selected_token['launchPad']}</a>"         
    )
    # print(message)
    keyboard = [
        [InlineKeyboardButton(f"Buy {coin_symbol} on {selected_token['launchPad']}", url=f"{selected_token['launchURL']}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # image_path = os.path.join(os.path.dirname(__file__), "../assets/ancy_expand.png")
    # await bot.send_photo(chat_id=chat_id,photo=open(image_path, 'rb'), caption=message, parse_mode=ParseMode.HTML,reply_markup=reply_markup)

    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

def format_number(num):
    if num >= 1_000_000_000:  # Billions
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:  # Millions
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:  # Thousands
        return f"{num / 1_000:.2f}K"
    else:  # Less than 1,000
        return f"{num:.2f}"
    
async def send_ranking(bot, chat_id: str, rank_score) -> None:    
    rankingIcons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    formatted_tokens = []

    # Corrected for loop
    for index, token in enumerate(rank_score):
        rankIcon = rankingIcons[index] if index < len(rankingIcons) else "🔘"  # Default fallback icon if out of range
        coin_symbol = token["symbol"]
        launchPad = token.get("launchPad", "No URL")  # Default to "No URL" if launchPad is None
        marketCap = token.get("marketCap", 0)  # Default to "No URL" if launchPad is None
        formatted_tokens.append(f"{rankIcon} {coin_symbol} | {format_number(marketCap)} MCap")

    # Join all formatted token strings into a single paragraph
    rank_paragraph = "\n\n".join(formatted_tokens)

    # Get the current UTC time
    utc_time = datetime.datetime.now(datetime.timezone.utc)
    formatted_utc_time = utc_time.strftime("%H:%M:%S UTC")

    # Create the message text
    message_text = (
        f"🍒 <b>Ancy's Trending:</b> SUI, Move Pump, PUMPFUN, MOONSHOT ...\n\n\n"     
        f"{rank_paragraph}\n\n\n"
        f"📅 Update time: <code>{formatted_utc_time}</code>"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅Book Trending", url="https://t.me/suiTokenPromote_bot?start=1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message and pin it in the channel
    message = await bot.send_message(
        chat_id=chat_id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    globals.pinned_msgID = message.message_id
    globals.pinned_trending_url = f"https://t.me/suitrending_boost/{message.message_id}"
    
    # Pin the message
    await bot.pin_chat_message(chat_id=chat_id, message_id=message.message_id)
