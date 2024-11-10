import asyncio
import time


from bot.validator import validate_coinType, validate_boosting_period, validate_wallet_address

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder
from bot.config import BOT_TOKEN, CHAT_ID


from bot.send_info_board import send_info_board
from api_test.get_last_txn_info import getLast_trans_info_of_coin

from db.db import initialize_connection, close_connection, load_global_token_arr
from db.collet_last_txns import init_last_txns
import atexit

from globals import global_token_arr

# Initialize the application globally

last_txn_arr = []
cur_coin_idx = 0 

user_config = {}
user_data = {}

curCoinType = ""

front_msg_id = ""
front_chat_id = ""

async def other_task():
    while True:
        await asyncio.sleep(10)  # Example delay for other processing

def regist_lastTxn(txn_info):
    global last_txn_arr
    
    last_txn_arr[txn_info['coinSymbol']] = txn_info['digest']
   
    print('regist-', last_txn_arr)

async def track_coin_post(application, track_coin):
    global last_txn_arr

    print(f"Fetching Last_txn for {track_coin} at {time.strftime('%X')}")
    # print(last_txn_arr)

    txn_info = await getLast_trans_info_of_coin(track_coin['coinType'], last_txn_arr[track_coin['symbol']])
    
    print(txn_info)
    if 'digest' not in txn_info:
        print('old digest, or not formal transaction')
        return False
    # if LastTxnDigest == txn_info['digest']:
    # print('lastDigest-', txn_info['coinSymbol'], last_txn_arr[txn_info['coinSymbol']])

    if last_txn_arr[txn_info['coinSymbol']] == txn_info['digest']:
        print("Continue, not new!")
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    message = await update.message.reply_text(
        message_text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("I'm ready to trend", callback_data="startTrending")]])
    )
    # Save message details in context for later reference
    context.user_data['message_id'] = message.message_id
    context.user_data['chat_id'] = update.message.chat_id

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if we've stored a message ID
    if 'message_id' in context.user_data:
        # Get the user's reply text
        user_reply = update.message.text
        chat_id = context.user_data['chat_id']
        message_id = context.user_data['message_id']
        
        # Update the message with the user's reply
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Updated message: {user_reply}"
        )
    
async def handle_startTrending(update: Update, context: CallbackContext) -> None:
    global front_msg_id, front_chat_id
    
    front_chat_id = context.user_data['chat_id']
    front_msg_id = context.user_data['message_id']
    
    user_config['isStart'] = True
        
    await context.bot.edit_message_text(
        chat_id=front_chat_id,
        message_id=front_msg_id,
        text=f"❔ Send me the token's Contract Address or Pair Address or the Launchpad/Presale Url: \n\n Supported Chains: BASE, BSC, ETH, MANTA, POL, SOL, SUI, TRX"
    )



async def handle_coinConfirmation(update: Update, context: CallbackContext) -> None:
    global front_msg_id, front_chat_id

    text=f"Selected Token: \n\n CA : \n {context.user_data['coinType']}"
    
    reply_keyboard = [
        [
            InlineKeyboardButton("❌ Close", callback_data="close"),
            InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await context.bot.edit_message_text(chat_id=front_chat_id, message_id=front_msg_id, text=text, parse_mode="HTML", reply_markup=reply_markup)
    
async def msgHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    input_text = update.message.text
    print('inputed Text', input_text)
    if 'user_id' not in user_config:
        user_config['user_id'] = update.message.from_user.id
        context.user_data['user_id'] = update.message.from_user.id
        
        user_config['curInput'] = "coinType"
        coinValidating = validate_coinType(input_text.strip())
                
        if coinValidating['val'] : 
            user_config['curInput'] = "cointype_confirmation"
            context.user_data['coinType'] = input_text
            
            await delete_last_message(update, context)
            await handle_coinConfirmation(update, context)
            
            # context.user_data['coinType'] = input_text.strip()
            
    elif user_config['curInput'] == "cointype":
        a =5
        
async def route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query = update.callback_query
  user_id = query.from_user.id
  await query.answer()
  print("here ROUTE!--------------------")
  if query.data == "support":
    text = (
      f"Support Account: @Boso098\n"
      f"Our FAQ Channel: @Dgitalworld\n"
    )
    await query.message.reply_text(text=text)
  if query.data == "balance_check":
    text = (
      f"🎉Prepaids Stock Bot— Checker\n\n"
      f"Reply to this message with the card details in the format:\n"
      f"<code>cc:mm:yy:cvv</code> | e.g., <code>1234567890123456:01:24:123</code>\n\n"
      f"<i>Checks are charged at</i> <code>US$0.03</code> <i>per successful check.</i>"
    )
    await query.message.reply_text(text=text, parse_mode="HTML")
  if query.data == "close":
    await query.message.delete()
      
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
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply))
    # application.add_handler(CommandHandler("help", help_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msgHandler))
    application.add_handler(CallbackQueryHandler(handle_startTrending, pattern="startTrending"))
    application.add_handler(CallbackQueryHandler(
        route, 
        pattern="^(close|support|balance_check|help|profile|listings|back_to_main|toggle_stock_notification|withdraw_lltc|deposit_lltc|deposit|withdraw|addone|back_to_profile|view_card_history|transfer_balance|get_vendor_access|get_relist_access)$")
    )

    # Start the polling for transactions
    asyncio.create_task(poll_transactions(application, interval=30))
    await run_polling(application)

if __name__ == "__main__":
    asyncio.run(main())  # Properly call the main function

