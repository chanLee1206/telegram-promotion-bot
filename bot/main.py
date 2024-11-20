import asyncio
import socketio

import signal
import sys
import json
from threading import Event

import time  
from datetime import datetime, timedelta

from threading import Timer

from bot.validator import validate_coinType, validate_boosting_period, validate_wallet_address

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder
from bot.config import BOT_TOKEN, CHAT_ID


from bot.send_info_board import send_tracking_token, send_ranking

from bot.api import getLast_trans_info_of_coin, fetch_account_txns, fetch_coin_details, load_rank_data

from bot.db import db_initialize, close_connection, load_tokens, fetch_db_payments, regist_payment, reg_memeToken

import atexit

import globals
application = None

sio = socketio.AsyncClient()
stop_event = Event()  # Event to signal when to stop

input_seq = {}

front_msg_id = ""
front_chat_id = ""

# Store timers for each user to allow cancellation upon verification success
verification_timers = {}

paying_account_arr = []

async def other_task():
    while True:
        await asyncio.sleep(10)  # Example delay for other processing

async def run_polling(application):
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    while True:
        await asyncio.sleep(0.1)

async def delete_last_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")


async def start_menu(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    # Initial message
    message_text = (
        "📈 Sui Trending Fast Track\n\n"
        "@Trending_Sui\n\n"
        "How to use:\n"
        "1️⃣ Click 'I'm ready to Trend'\n"
        "2️⃣ Paste your token's contract address\n"
        "3️⃣ Enter boosting period (e.g., 10 minutes)\n"
        "4️⃣ Provide your wallet address\n"
        "5️⃣ Pay SUI to the given wallet within 10 min\n"
        "6️⃣ Wait for tx confirmation and click 'Start Trending'"
    )
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("I'm ready to trend", callback_data="coinType")]])
    context.user_data['user_id'] = None
    context.user_data['user_name'] = None
        
    if isinstance(update_or_query, Update):
        # await update_or_query.message.reply_text(text=message_text, parse_mode="HTML", reply_markup=reply_markup)
        sent_message = await update_or_query.message.reply_text(
            text=message_text, parse_mode="HTML", reply_markup=reply_markup
        )
        context.user_data['bot_message_id'] = sent_message.message_id
        print('bot_message_id', context.user_data['bot_message_id'])
    else:
        print('bot_message_id', context.user_data['bot_message_id'])
        await update_or_query.edit_message_text(text=message_text, parse_mode="HTML", reply_markup=reply_markup)



   
async def msgHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global input_seq
    input_text = update.message.text

    # Validate coin type
    
    bot_message_id = context.user_data.get('bot_message_id')
    if input_seq == "add_meme_token" : 
        add_coinType = input_text.strip()
        coinInfo = await fetch_coin_details(add_coinType)
        print(coinInfo)
        context.user_data['add_token_info'] = coinInfo
        if coinInfo:
            # print(coinInfo)
            await update.message.reply_text(text=f"Input launchPad URL : \n ex) https://movepump.com/token/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY", parse_mode='HTML',disable_web_page_preview=True)
            input_seq = "input_launchURL"
        else : 
            await update.message.reply_text(text=f"Invalid meme Token, try again", parse_mode='HTML')
        return
    if input_seq == "input_launchURL" :
        launchURL = input_text.strip()
        context.user_data['add_token_info']['launchURL'] = launchURL
        message_text = (
            f"<b>{context.user_data['add_token_info'].get('name')}</b>\n\n"
            f"Symbol : {context.user_data['add_token_info'].get('symbol')}"
            f"Name: {context.user_data['add_token_info'].get('name')}\n"
            f"LaunchPad URL: {context.user_data['add_token_info'].get('launchURL')}\n"
            f"Ca:\n <code>{context.user_data['add_token_info'].get('coinType')}</code>\n"                
        )
        reply_keyboard = [
            [InlineKeyboardButton("❌ Close", callback_data="close"),
            InlineKeyboardButton("✅ Confirm", callback_data="confirm_add")]]
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
        await update.message.reply_text(text=message_text, reply_markup=reply_markup, parse_mode='HTML')
        return
    if context.user_data['user_id'] and input_seq == "coinType" :
        coinValidating = validate_coinType(input_text.strip())
        if coinValidating['val']:
            context.user_data['coinType'] = input_text
            selected_token = next((token for token in globals.global_token_arr if token['coinType'] == context.user_data['coinType']), None)
            print('inputted coinInfo----------', selected_token)
            context.user_data['coinSymbol'] = selected_token['symbol']
            context.user_data['coinName'] = selected_token['name']
            context.user_data['launchPad'] = selected_token.get('launchPad', 'Unknown')  
            
            await delete_last_message(update, context)  # Delete the user's reply

            # Edit the original bot message with confirmation details
            if bot_message_id:
                text = (
                    f"Selected Token:\n\n"
                    f"Name : {context.user_data['coinName']}\n"
                    f"Symbol : {context.user_data['coinSymbol']}\n"
                    f"LuanchPad : 💸{context.user_data['launchPad']}💸\n\n"

                    f"CA:{context.user_data['coinType']}"
                )
                reply_keyboard = [
                    [InlineKeyboardButton("❌ Close", callback_data="cancel"),
                    InlineKeyboardButton("✅ Confirm", callback_data="period_select")]]
                reply_markup = InlineKeyboardMarkup(reply_keyboard)

                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=bot_message_id,
                    text=text,
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )
        else:
            text = f"Failed Token:\n\nCA:\n{coinValidating['text']}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="toStartMenu")]])

            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=bot_message_id,
                text=text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            await delete_last_message(update, context)  # Delete the user's reply
            
async def boost_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global input_seq
    query = update.callback_query
    await query.answer()
  
    print(f"Boost!-----{query.data}\n")

    callback_data = query.data
    if callback_data.startswith("boost_"):
        # Parse the period and cost from the callback data
        period, cost = callback_data.split("_")[1:3]
        context.user_data['period'] = period
        context.user_data['cost'] = cost
        await summaryView(update, context)

def get_trendReceiveAccount() : 
    return "0xd6840994167c67bf8063921f5da138a17da41b3f64bb328db1687ddd713c5281"


async def summaryView(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    period = context.user_data['period']
    cost = context.user_data['cost']
    server_account = get_trendReceiveAccount()
    context.user_data['server_account'] = server_account
    message_text = (
        "⚡ <b>ANCY Trending Boost</b> ⚡\n\n"
        f"<b>Top Trending  for {period}</b>\n\n"
        f"<b>Token Name: </b>{context.user_data['coinName']}\n"
        f"<b>Token Symbol: </b>{context.user_data['coinSymbol']}\n\n"
        # "<b>Telegram:</b> https://t.me/AncyPeosiPortal\n\n"
        f"🔗 <b>Activate the boost by sending {cost} SUI to:</b>\n"
        f"<code>{server_account}</code>\n\n"
        f"<b>Step 1:</b> Send {cost} SUI\n"
        "<b>Step 2:</b> Click Verify Payment to verify the transaction\n"
        "<b>Step 3:</b> Watch ANCY soar to the Top trending shortly!\n\n"
        "🚀 <i>Get ready for a double dose of trending power!</i> 🚀\n\n"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Verify Payment", callback_data="verify_payment")],
        [InlineKeyboardButton("🔙 Back", callback_data="period_select")],        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    
    if update.message:
        await update.message.edit_text(text=message_text, reply_markup=reply_markup, parse_mode='HTML')
    elif update.callback_query:
        await update.callback_query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode='HTML')

async def route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global input_seq
    global paying_account_arr
    query = update.callback_query
    await query.answer()
  
    print(f"here ROUTE!-----{query.data}\n")
    
    if query.data == "cancel":
        await query.message.delete()
        
    if query.data == "coinType" :
        context.user_data['user_id'] = query.from_user.id
        context.user_data['user_name'] = query.from_user.name
        input_seq = "coinType"
        await query.edit_message_text(
            text=f"❔ Send me the token's coinType(regist ahead): \n\n Supported Chains: SUI"
        )
        
    if query.data == "toStartMenu":
        await start_menu(query, context)
        
    if query.data == "period_select":
        message_text = (
            "<b>Trending Boost</b>\n"
            "Trending boost guarantees your token on Multichain Trending\n\n"
            "<b>Select the Period:</b>"
        )

        # Define the inline keyboard with multiple buttons in a grid format
        keyboard = [
            [InlineKeyboardButton("12 Hours | 45 SUI", callback_data="boost_12hours_45"),
            InlineKeyboardButton("1 week | 350 SUI", callback_data="boost_1week_350")],
            [InlineKeyboardButton("24 Hours | 75 SUI", callback_data="boost_24hours_75"),
            InlineKeyboardButton("2 weeks | 600 SUI", callback_data="boost_2weeks_600")],
            [InlineKeyboardButton("48 Hours | 125 SUI", callback_data="boost_48hours_125"),
            InlineKeyboardButton("3 weeks | 800 SUI", callback_data="boost_3weeks_800")],
            [InlineKeyboardButton("3 days  | 180 SUI", callback_data="boost_3days_180"),
            InlineKeyboardButton("1 month | 1000 SUI", callback_data="boost_1month_1000")],
            [InlineKeyboardButton("🔙 Back", callback_data="toStartMenu")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        input_seq = "coinType"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode='HTML')

    if query.data == "view_summary":
        paying_accounts = {account for account, username, start_timestamp, end_timestamp in paying_account_arr}
        available_account_arr = [account for account in globals.total_account_arr if account not in paying_accounts]

        if(available_account_arr) :
            active_account = available_account_arr[0]  # First available account
            start_timestamp = datetime.now()
            end_timestamp = start_timestamp + timedelta(minutes=10)

            paying_account_arr.append((active_account, context.user_data['user_name'], start_timestamp, end_timestamp))
            await summaryView(update, context)
            
        else : 
            query.message.reply_text(
                text="Payment Account is not ready, try again!",
            )            

    if query.data == "verify_payment" : 
        user_id = query.from_user.id
         
        print('here verify payment!')
        await query.edit_message_text(text="Validating Purchase ...")
        
        valid_payment = await check_vaild_payment(context.user_data['cost'], context.user_data['server_account'])

        if valid_payment:
            await query.edit_message_text(
                text="Congratulations! You succeeded in Trend boosting! 👍 Your trend boost will be applied immediately."
            )
            print('user_data : ', context.user_data, '\n')
            print('payment_data : ', valid_payment[0], '\n')
            await regist_payment(context.user_data, valid_payment[0])

        else:
            await query.edit_message_text(text="⚠️ Payment not detected! If already sent, try again in a minute.")
            await asyncio.sleep(5)    
            await summaryView(update, context)       # Return to summary if payment     
    if query.data == "confirm_add" :
        # print('you confirm add!')
        res, res_message = await reg_memeToken(context.user_data['add_token_info'])
        if (res == True) :
            await query.edit_message_text(text=f"Adding success! Wait for allow. {res_message}")
        else :
            await query.edit_message_text(text=f"Failt to regist! {res_message}")
    if query.data == "close":
        await query.message.delete()
        

async def check_vaild_payment(amount, server_account="0xd6840994167c67bf8063921f5da138a17da41b3f64bb328db1687ddd713c5281"):
    amount = float(amount)
    current_time = datetime.now()
    time_ahead = current_time - timedelta(minutes=15)
    timestamp_ahead = int(time_ahead.timestamp()*1000)

    # amount = 100000000
    # timestamp_ahead = 0
    
    detected_txns = await fetch_account_txns(server_account, amount, timestamp_ahead)
    # digests = await fetch_db_payments(server_account, int(time_ahead.timestamp()*1000))
    digests = await fetch_db_payments(server_account, timestamp_ahead)
    print('detected_txns', detected_txns, '\n')
    print('db_txns', digests, '\n')
    
    digest_set = {item['digest'] for item in digests}
    filtered_detected_txns = [item for item in detected_txns if item['digest'] not in digest_set]
    print('filtered_txns', filtered_detected_txns)
    
    return filtered_detected_txns

# Get the timestamp for 15 minutes ahead

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to:\n/start - Start trend\n /add - add memeToken\n /help - Show this help message'
    )
async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global input_seq
    input_seq = "add_meme_token"
    await update.message.reply_text("❔ Send me the token's exact coinType \nSupported Chains: SUI\n\n ex) 0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY")
    

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_menu(update, context)

async def on_connect():
    print("Connected to WebSocket!")
    for pair_item in globals.global_pair_arr:
        await sio.emit("SUBSCRIBE_REALTIME_TRANSACTION", {'pairId': pair_item.get('pairId')})
        print(f"Emitted subscription for pairId: {pair_item.get('pairId')}")
    # await sio.emit("SUBSCRIBE_REALTIME_TRANSACTION", {
    #     'pairId': 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356',
    # })
 
    # await sio.emit('SUBSCRIBE_REALTIME_PAIR_STATS_CHANGED', {
    #     'pairId': 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356'
    # })
        

@sio.event
async def connect():
    print("Socket connected!")
    await on_connect()
    
@sio.event
async def connect_error(data):
    print(f"Connection failed with error: {data}")

@sio.event
async def disconnect():
    print("Disconnected from WebSocket!")

@sio.on("TRANSACTION")
async def handle_transaction(data):
    global application
    try:
        # print(data, '\n')
        if data.get('tradingType') == "BUY" :
            await send_tracking_token(application.bot, CHAT_ID, data)
        # await send_tracking_token(application.bot, CHAT_ID, data)
        
    except Exception as e:
        print(f"Error processing transaction: {e}")

# @sio.on("PAIR_STATS_CHANGED")  # Match the event name used in the API guide
async def handle_pair(data):
    print("Pair stats changed::")
    print(data, '\n')

async def track_transactions():
    # global sio
    SOCKET_URL = "wss://ws-sui.raidenx.io"
    try:
        await sio.connect(SOCKET_URL)  # Replace with your WebSocket URL
        print("Attempting to connect to WebSocket server...")       
        await sio.wait()
    except Exception as e:
        print(f"An error occurred: {e}") 
    finally:
        await sio.disconnect()

def stop_gracefully(signal_received, frame):
    """Handles Ctrl+C (SIGINT) signal."""
    print("\nStopping gracefully...")
    stop_event.set()  # Signal to stop the main loop
    sio.disconnect()  # Disconnect from WebSocket
    sys.exit(0)       # Exit the script

async def calc_rank_score(rank_data):
    # Weights for each parameter
    weights = {
        'marketCap': 0.2,
        'holder': 0.15,
        'liquidity': 0.15,
        'volume': 0.2,
        'transaction': 0.15,
        'maker': 0.15
    }

    # Parameters to normalize
    parameters = ["marketCap", "holder", "liquidity", "volume", "transaction", "maker"]

    # Initialize max and min values for each parameter
    max_min_values = {param: {"max": float('-inf'), "min": float('inf')} for param in parameters}

    # Determine the max and min values for normalization
    for item in rank_data:
        for param in parameters:
            value = item[param]
            if value > max_min_values[param]["max"]:
                max_min_values[param]["max"] = value
            if value < max_min_values[param]["min"]:
                max_min_values[param]["min"] = value

    # Calculate normalized scores and rank scores
    rank_scores = []
    for item in rank_data:
        normalized_scores = {}
        for param in parameters:
            max_val = max_min_values[param]["max"]
            min_val = max_min_values[param]["min"]
            # Normalize using min-max scaling
            if max_val != min_val:
                normalized_scores[param] = (item[param] - min_val) / (max_val - min_val) * 100
            else:
                normalized_scores[param] = 0  # Handle case where max == min

        # Calculate rank score using weights
        rank_score = sum(normalized_scores[param] * weights[param] for param in parameters)
        rank_scores.append({"symbol": item["symbol"], "coinType": item["coinType"], "marketCap": item["marketCap"], "score": rank_score})

    # Sort by score in descending order
    sorted_rank_scores = sorted(rank_scores, key=lambda x: x['score'], reverse=True)

    # Assign ranks
    for i, item in enumerate(sorted_rank_scores, start=0):
        item['rank'] = i

    return sorted_rank_scores

   
async def run_ranking():
    global application
    
    rank_data = await load_rank_data()
    print('rank_data\n', json.dumps(rank_data, indent=4))
    
    rank_score = await calc_rank_score(rank_data)
    print('rank_score\n', json.dumps(rank_score, indent=4))

    await send_ranking(application.bot, CHAT_ID, rank_score)

async def schedule_ranking_task():
    while True:
        await run_ranking()
        await asyncio.sleep(15 * 60)  # Wait for 15 minutes (15 * 60 seconds)

async def main():
    global application

    db_initialize()

    signal.signal(signal.SIGINT, stop_gracefully)    
    atexit.register(close_connection)
    atexit.register(globals.save_globals)

    globals.load_globals()

    
    application = Application.builder().token(BOT_TOKEN).read_timeout(40).write_timeout(40).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msgHandler))
    
    application.add_handler(CallbackQueryHandler(route, pattern="^(cancel|confirm_add|coinType|period_select|toStartMenu|verify_payment|confirm|ack_to_main|close)$"))
    application.add_handler(CallbackQueryHandler(boost_callback_handler, pattern=r"^boost_"))

    # asyncio.create_task(scrap_transactions(application, interval=30))
    asyncio.create_task(track_transactions())
    asyncio.create_task(schedule_ranking_task())
    
    await run_polling(application)

if __name__ == "__main__":
    asyncio.run(main())

