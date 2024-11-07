from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext, MessageHandler, filters

from bot.validator import validate_token_id, validate_boosting_period, validate_wallet_address

# Store the procedure handlers globally for later removal
procedure_handler = None

# Step 1: Start command to initiate the procedure
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

# Step 2: Handle "/help" command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to:\n/start - Start the bot\n/help - Show this help message'
    )

# Step 3: Handle the "I'm ready to trend" button click
async def btn_trendStart_handler(update: Update, context: CallbackContext) -> None:
    global procedure_handler  # Declare global to modify the handler

    query = update.callback_query
    await query.answer()  # Required to stop the "loading" circle

    # Ask for the token ID
    await query.message.reply_text(text="➡️ Please enter your token ID to boost trending:")

    # Register the handler for token ID input
    procedure_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_token_id)
    context.application.add_handler(procedure_handler)

# Step 4: Capture the token ID and validate it
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

# Step 5: Capture the boosting period and validate it
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

# Step 6: Capture the wallet address and validate it
async def get_wallet_address(update: Update, context: CallbackContext) -> None:
    global procedure_handler  # Declare global to modify the handler

    wallet_address = update.message.text

    # If user types 'exit', reset to start
    if wallet_address.lower() == 'exit':
        await reset_to_start(update, context)
        return

    if validate_wallet_address(wallet_address):
        context.user_data["wallet_address"] = wallet_address
        await update.message.reply_text(f"Wallet address received: {wallet_address}. Processing your request...")

        # Remove the wallet address handler after success
        context.application.remove_handler(procedure_handler)
        
        # Now all parameters are gathered, you can proceed with the actual trending process
        print(f"User provided wallet address: {wallet_address}")
        # Add any logic to proceed with the actual boosting here (e.g., processing payment, etc.)
    else:
        await update.message.reply_text(f"❌ Invalid wallet address: {wallet_address}. Type 'exit' to cancel and restart.")
        print(f"Invalid wallet address: {wallet_address}")

# Reset to the start state when 'exit' is typed
async def reset_to_start(update: Update, context: CallbackContext) -> None:
    # Remove the current procedure handler
    global procedure_handler
    context.application.remove_handler(procedure_handler)
    
    # Send the start message again to restart the process
    await start(update, context)
