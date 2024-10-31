# main.py

from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN, CHAT_ID
from commands import start, help_command
from send_info_board import send_info_board  # Import clear_bot_messages


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers for the /start and /help commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.job_queue.run_once(lambda context: send_info_board(context, CHAT_ID), when=0)

    application.run_polling()

if __name__ == '__main__':
    main()
