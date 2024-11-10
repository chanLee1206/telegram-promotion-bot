from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext, MessageHandler, filters, CallbackQueryHandler

from bot.validator import validate_coinType, validate_boosting_period, validate_wallet_address

# Store the procedure handlers globally for later removal
procedure_handler = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    
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

    # Define the inline keyboard with the "I'm ready to trend" button
    keyboard = [
        [InlineKeyboardButton("I'm ready to trend", callback_data="ready_to_start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline button
    await bot.send_message(
        chat_id=update.message.chat_id,
        text=message_text,
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to:\n/start - Start the bot\n/help - Show this help message'
    )

async def btn_trendStart_handler(update: Update, context: CallbackContext) -> None:
    global procedure_handler 

    query = update.callback_query
    await query.answer()  
    await query.message.reply_text(text="➡️ Please enter your coinType of your meme Token to boost trending:")

    # Register the handler for token ID input
    procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_coinType)
    context.application.add_handler(procedure_handler)

async def get_coinType(update: Update, context: CallbackContext) -> None:
    global procedure_handler  # Declare global to modify the handler

    coinType = update.message.text
    
    # If user types 'exit', reset to start
    if coinType.lower() == 'exit':
        await reset_to_start(update, context)
        return
    val_response = validate_coinType(coinType)
    if val_response['val']:
        context.user_data["coinType"] = coinType
        await update.message.reply_text(f"Token ID received: {coinType}. Now, select the boosting period:")
        
        # Remove the token handler and proceed to the next input for boosting period
        context.application.remove_handler(procedure_handler)
        
        # Display the boosting period options with buttons
        await send_trending_boost_options(update, context)

        # Register handler for boosting period input
        # procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_boosting_period)
        # context.application.add_handler(procedure_handler)
    else:
        await update.message.reply_text(f"❌ {val_response['text']}. Type 'exit' to cancel and restart.")
        print(f"Invalid Token ID: {coinType}")

async def send_trending_boost_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = (
        "<b>Trending Boost</b>\n"
        "Trending boost guarantees your token on Multichain Trending\n\n"
        "<b>Select the Period:</b>"
    )

    # Define the inline keyboard with multiple buttons in a grid format
    keyboard = [
        [InlineKeyboardButton("3 Hours | 149 SUI", callback_data="top6_3h_149"),
         InlineKeyboardButton("3 Hours | 199 SUI", callback_data="top3_3h_199")],
        [InlineKeyboardButton("6 Hours | 269 SUI", callback_data="top6_6h_269"),
         InlineKeyboardButton("6 Hours | 349 SUI", callback_data="top3_6h_349")],
        [InlineKeyboardButton("12 Hours | 469 SUI", callback_data="top6_12h_469"),
         InlineKeyboardButton("12 Hours | 599 SUI", callback_data="top3_12h_599")],
        [InlineKeyboardButton("24 Hours | 799 SUI", callback_data="top6_24h_799"),
         InlineKeyboardButton("24 Hours | 999 SUI", callback_data="top3_24h_999")],
        [InlineKeyboardButton("🔙 Back", callback_data="go_back")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline buttons
    await update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

    # Register the handler for boosting period button selection
    global procedure_handler
    procedure_handler = CallbackQueryHandler(handle_boosting_period_selection)
    context.application.add_handler(procedure_handler)

# Handler for the boosting period selection
async def handle_boosting_period_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Stop the "loading" indicator on the button
    
    # Parse the selected option from callback data
    data = query.data
    parts = data.split('_')
    tier = parts[0]  # e.g., "top6"
    duration = parts[1]  # e.g., "3h"
    cost = parts[2]  # e.g., "149"

    # Process the selected option and store it in the user data
    context.user_data["boosting_period"] = {
        "tier": tier,
        "duration": duration,
        "cost": cost
    }

    # Notify the user about their selection
    await query.message.reply_text(
        f"You selected: {tier.upper()} for {duration} at {cost} SUI.\n\n"
        "Now, please enter your wallet address:"
    )

    # Remove the current handler for boosting period selection
    context.application.remove_handler(handle_boosting_period_selection)

    # Register a new handler for wallet address input
    procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_wallet_address)
    context.application.add_handler(procedure_handler)


async def get_wallet_address(update: Update, context: CallbackContext) -> None:
    global procedure_handler  # Declare global to modify the handler

    wallet_address = update.message.text

    # If user types 'exit', reset to start
    if wallet_address.lower() == 'exit':
        await reset_to_start(update, context)
        return

    if validate_wallet_address(wallet_address):
        context.user_data["wallet_address"] = wallet_address
        await update.message.reply_text(f"Wallet address received: {wallet_address}. Now, let's confirm your details.")

        # Remove the wallet address handler after success
        context.application.remove_handler(procedure_handler)
        
        # Send summary and ask for confirmation
        await confirm_details(update, context)
    else:
        await update.message.reply_text(f"❌ Invalid wallet address: {wallet_address}. Type 'exit' to cancel and restart.")
        print(f"Invalid wallet address: {wallet_address}")

async def confirm_details(update: Update, context: CallbackContext) -> None:
    # Retrieve all the information collected
    coinType = context.user_data.get("coinType", "Not provided")
    boosting_period = context.user_data.get("boosting_period", "Not provided")
    wallet_address = context.user_data.get("wallet_address", "Not provided")

    # Summarize the information and ask for confirmation
    confirmation_text = (
        "Please confirm the following details:\n\n"
        f"Token ID: {coinType}\n"
        f"Boosting Period: {boosting_period} minutes\n"
        f"Wallet Address: {wallet_address}\n\n"
        "Type 'ok' to confirm or 'exit' to cancel and restart."
    )

    # Ask for confirmation
    await update.message.reply_text(confirmation_text)

    # Register handler for confirmation input
    global procedure_handler
    context.application.remove_handler(procedure_handler)
    
    procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_confirmation)
    context.application.add_handler(procedure_handler)

async def process_confirmation(update: Update, context: CallbackContext) -> None:
    global procedure_handler    
    user_input = update.message.text.lower()

    # If user confirms with 'OK'
    print('here process_confirmation sting- ', user_input, '\n')
    if user_input == 'ok':
        # Proceed with the next action (e.g., start trending process)
        await update.message.reply_text("✅ Your details are confirmed. Processing your request...")
        print("User confirmed all details. Proceeding with the trending process.")
        
        context.application.remove_handler(procedure_handler)
        # Here you can call a function to process the user's request, such as starting the trending
        # For example: await start_trending(context.user_data)
    elif user_input == 'exit':
        # Reset to start if 'exit' is typed
        await reset_to_start(update, context)
    else:
        # Handle invalid confirmation
        await update.message.reply_text("❌ Invalid input. Type 'OK' to confirm or 'exit' to cancel and restart.")
        print(f"Invalid confirmation input: {user_input}")


# Reset to the start state when 'exit' is typed
async def reset_to_start(update: Update, context: CallbackContext) -> None:
    # Remove the current procedure handler
    global procedure_handler
    context.application.remove_handler(procedure_handler)
    
    # Send the start message again to restart the process
    await start(update, context)
