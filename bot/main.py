from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes
import random
import string
from datetime import datetime, timedelta

# Your bot token from BotFather
BOT_TOKEN = '7616802949:AAEVIoSBug1sJBosOzO3lJ13kVqN_82MKRI'
CHAT_ID = "@suiTrending_boost"  # Replace with your actual chat ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. Use /help to see what I can do.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('I can respond to:\n/start - Start the bot\n/help - Show this help message')

def generate_random_transaction():
    txn_id = ''.join(random.choices(string.ascii_letters + string.digits, k=43))
    txn_date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%m/%d/%y")
    txn_type = random.choice(["buy", "sell"])
    sui_cost = random.randint(10000000000, 500000000000)
    volume = random.randint(1, 1000)
    return {
        "txn_id": txn_id,
        "txn_date": txn_date,
        "txn_type": txn_type,
        "sui_cost": sui_cost,
        "volume": volume
    }

async def send_info_board(context: ContextTypes.DEFAULT_TYPE) -> None:
    transaction = generate_random_transaction()
    
    message = (
        f"📊 <b>Transaction Info</b> 📊\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Transaction ID:</b> {transaction['txn_id']}\n"
        f"<b>Date:</b> {transaction['txn_date']}\n"
        f"<b>Type:</b> {transaction['txn_type']}\n"
        f"<b>SUI Cost:</b> {transaction['sui_cost']}\n"
        f"<b>Volume:</b> {transaction['volume']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )
    
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers for the /start and /help commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Schedule the send_info_board function to run every 10 seconds
    application.job_queue.run_repeating(send_info_board, interval=10)

    application.run_polling()

if __name__ == '__main__':
    main()
