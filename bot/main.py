import asyncio
import time  
from datetime import datetime, timedelta


from bot.validator import validate_coinType, validate_boosting_period, validate_wallet_address

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder
from bot.config import BOT_TOKEN, CHAT_ID


from bot.send_info_board import send_info_board
from api_test.get_last_txn_info import getLast_trans_info_of_coin
from api_test.txns_account import fetch_account_txns

from db.db import initialize_connection, close_connection, load_global_token_arr, fetch_account_payments
from db.collet_last_txns import init_last_txns
import atexit

from globals import global_token_arr

# Initialize the application globally

last_txn_arr = []
cur_coin_idx = 0 

input_seq = {}
# user_data = {}

curCoinType = ""

front_msg_id = ""
front_chat_id = ""

async def other_task():
    while True:
        await asyncio.sleep(10)  # Example delay for other processing

def regist_lastTxn(txn_info):
    global last_txn_arr
    
    last_txn_arr[txn_info['coinSymbol']] = txn_info['digest']
   
    # print('regist-', last_txn_arr)

async def track_coin_post(application, track_coin):
    global last_txn_arr

    # print(f"Fetching Last_txn for {track_coin} at {time.strftime('%X')}")
    # print(last_txn_arr)

    txn_info = await getLast_trans_info_of_coin(track_coin['coinType'], last_txn_arr[track_coin['symbol']])
    
    # print(txn_info)
    if 'digest' not in txn_info:
        # print('old digest, or not formal transaction')
        return False
    # print('lastDigest-', txn_info['coinSymbol'], last_txn_arr[txn_info['coinSymbol']])

    if last_txn_arr[txn_info['coinSymbol']] == txn_info['digest']:
        # print("Continue, not new!")
        return False
    else:
        LastTxnDigest = txn_info['digest']
        # print(txn_info)
        await send_info_board(application.bot, CHAT_ID, txn_info)
        regist_lastTxn(txn_info)

        return True
    


async def poll_transactions(application, interval=7):
    # global global_token_arr
    global cur_coin_idx

    # print(global_token_arr)
    while True:
        curCoin = global_token_arr[cur_coin_idx]

        postFlag = await track_coin_post(application, curCoin)

        await asyncio.sleep(interval) 
        
        cur_coin_idx = (cur_coin_idx + 1) % len(global_token_arr)
        # cur_coin_idx = 0


async def run_polling(application):
    """Runs the polling for the Telegram bot in the event loop."""
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Keep running until manually stopped
    while True:
        await asyncio.sleep(0.1)

async def delete_last_message(update: Update, context: CallbackContext):
    print('here delete last message', update.message.text)
    # Get the chat ID and message ID of the user's last message
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    
    # Delete the message
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_menu(update, context)

   
async def msgHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global input_seq
    input_text = update.message.text
    print('inputted Text:', input_text)

    # Validate coin type
    coinValidating = validate_coinType(input_text.strip())
    print('msgHandler-------', coinValidating, context.user_data['user_id'], input_seq, context.user_data.get('bot_message_id'))
    bot_message_id = context.user_data.get('bot_message_id')
    if(context.user_data['user_id'] and input_seq == "coinType") :
        if coinValidating['val']:
            context.user_data['coinType'] = input_text
            await delete_last_message(update, context)  # Delete the user's reply

            # Edit the original bot message with confirmation details
            if bot_message_id:
                text = f"Selected Token:\n\nCA:\n{context.user_data['coinType']}"
                reply_keyboard = [
                    [InlineKeyboardButton("❌ Close", callback_data="toStartMenu"),
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
            # Handle invalid coin type here if needed
            
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
        f"<b>Top Trending  for {period}</b>\n"
        "<b>Token:</b> Ancy Peosi\n\n"
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
    query = update.callback_query
    await query.answer()
  
    print(f"here ROUTE!-----{query.data}\n")
    
    if query.data == "cancel":
        await query.message.delete()
        
    if query.data == "coinType" :
        context.user_data['user_id'] = query.from_user.id
        input_seq = "coinType"
        await query.edit_message_text(
            text=f"❔ Send me the token's Contract Address or Pair Address or the Launchpad/Presale Url: \n\n Supported Chains: BASE, BSC, ETH, MANTA, POL, SOL, SUI, TRX"
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
        await summaryView(update, context)

    if query.data == "verify_payment" : 
        print('here verify payment!')
        await query.edit_message_text(text="Validating Purchase ...")
        
        # validate_payment = await check_vaild_payment(context.user_data['server_account'], context.user_data['cost'])
        is_valid_payment = await check_vaild_payment(context.user_data['server_account'], context.user_data['cost'])

        if is_valid_payment:
            await query.edit_message_text(
                text="Congratulations! You succeeded in Trend boosting! 👍 Your trend boost will be applied immediately."
            )
        else:
            await query.edit_message_text(text="⚠️ Payment not detected! If already sent, try again in a minute.")
            await asyncio.sleep(5)    
            await summaryView(update, context)       # Return to summary if payment     

    if query.data == "close":
        await query.message.delete()

async def check_vaild_payment(server_account="0xd6840994167c67bf8063921f5da138a17da41b3f64bb328db1687ddd713c5281", amount):
    # Simulate payment validation delay
    current_time = datetime.now()
    time_ahead = current_time - timedelta(minutes=15)
    timestamp_ahead = int(time_ahead.timestamp())
    
    detected_txns = await fetch_account_txns(server_account, timestamp_ahead, amount)
    checked_txns = await fetch_account_payments(server_account, timestamp_ahead, 'reg')
    print(detected_txns, '\n')
    print(checked_txns, '\n')
    return True

# Get the timestamp for 15 minutes ahead

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to:\n/start - Start the bot\n/help - Show this help message'
    )

   
async def main():
    global cur_coin_idx , last_txn_arr
    cur_coin_idx = 0

    initialize_connection()
    atexit.register(close_connection)

    load_global_token_arr()
    last_txn_arr = init_last_txns(global_token_arr)
    print("Initialized last_txn_arr:", last_txn_arr)  # Debugging line

    if not global_token_arr:
        print("Error: global_token_arr is empty after loading.")
        return

    application = Application.builder().token(BOT_TOKEN).read_timeout(20).write_timeout(20).build()

    application.add_handler(CommandHandler("start", start))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msgHandler))
    
    # application.add_handler(CallbackQueryHandler(handle_startTrending, pattern="startTrending"))
    application.add_handler(CallbackQueryHandler(route, pattern="^(cancel|coinType|period_select|toStartMenu|verify_payment|confirm|ack_to_main|close)$"))
    application.add_handler(CallbackQueryHandler(boost_callback_handler, pattern=r"^boost_"))

    asyncio.create_task(poll_transactions(application, interval=30))
    await run_polling(application)

if __name__ == "__main__":
    asyncio.run(main())

