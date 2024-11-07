from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext, MessageHandler, filters

from bot.validator import validate_token_id, validate_boosting_period, validate_wallet_address

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
    global procedure_handler  # Declare global to modify the handler

    query = update.callback_query
    await query.answer()  # Required to stop the "loading" circle

    # Ask for the token ID
    await query.message.reply_text(text="➡️ Please enter your token ID to boost trending:")

    # Register the handler for token ID input
    procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_token_id)
    context.application.add_handler(procedure_handler)

async def get_token_id(update: Update, context: CallbackContext) -> None:
    global procedure_handler  # Declare global to modify the handler

    token_id = update.message.text
    
    # If user types 'exit', reset to start
    if token_id.lower() == 'exit':
        await reset_to_start(update, context)
        return

    if validate_token_id(token_id):
        context.user_data["token_id"] = token_id
        await update.message.reply_text(f"Token ID received: {token_id}. Now, enter the boosting period:")
        
        # Remove the token handler and proceed to the next input for boosting period
        context.application.remove_handler(procedure_handler)
        
        # Register handler for boosting period input
        procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_boosting_period)
        context.application.add_handler(procedure_handler)
    else:
        await update.message.reply_text(f"❌ Invalid Token ID: {token_id}. Type 'exit' to cancel and restart.")
        print(f"Invalid Token ID: {token_id}")

async def get_boosting_period(update: Update, context: CallbackContext) -> None:
    global procedure_handler  # Declare global to modify the handler

    boosting_period = update.message.text

    # If user types 'exit', reset to start
    if boosting_period.lower() == 'exit':
        await reset_to_start(update, context)
        return

    if validate_boosting_period(boosting_period):
        context.user_data["boosting_period"] = boosting_period
        await update.message.reply_text(f"Boosting period received: {boosting_period}. Now, enter your wallet address:")
        
        # Remove the boosting period handler and proceed to the next input for wallet address
        context.application.remove_handler(procedure_handler)
        
        # Register handler for wallet address input
        procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_wallet_address)
        context.application.add_handler(procedure_handler)
    else:
        await update.message.reply_text(f"❌ Invalid boosting period: {boosting_period}. Type 'exit' to cancel and restart.")
        print(f"Invalid boosting period: {boosting_period}")

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
    token_id = context.user_data.get("token_id", "Not provided")
    boosting_period = context.user_data.get("boosting_period", "Not provided")
    wallet_address = context.user_data.get("wallet_address", "Not provided")

    # Summarize the information and ask for confirmation
    confirmation_text = (
        "Please confirm the following details:\n\n"
        f"Token ID: {token_id}\n"
        f"Boosting Period: {boosting_period} minutes\n"
        f"Wallet Address: {wallet_address}\n\n"
        "Type 'ok' to confirm or 'exit' to cancel and restart."
    )

    # Ask for confirmation
    await update.message.reply_text(confirmation_text)

    # Register handler for confirmation input
    global procedure_handler
    procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_confirmation)
    context.application.add_handler(procedure_handler)

async def process_confirmation(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.lower()

    # If user confirms with 'OK'
    if user_input == 'ok':
        # Proceed with the next action (e.g., start trending process)
        await update.message.reply_text("✅ Your details are confirmed. Processing your request...")
        print("User confirmed all details. Proceeding with the trending process.")

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
