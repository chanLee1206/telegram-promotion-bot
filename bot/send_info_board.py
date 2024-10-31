# send_info_board.py

import random
import string
from datetime import datetime, timedelta
from telegram.constants import ParseMode
from telegram.ext import ContextTypes  # Add this import

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

async def send_info_board(context: ContextTypes.DEFAULT_TYPE, chat_id: str) -> None:
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
    
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
