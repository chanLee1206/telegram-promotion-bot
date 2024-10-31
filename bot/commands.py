# commands.py

from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. Use /help to see what I can do.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('I can respond to:\n/start - Start the bot\n/help - Show this help message')

# def vote_command(update, context):
#     # Command handler for voting
#     handle_vote(update, context)

# def leaderboard_command(update, context):
#     # Retrieve and display the leaderboard
#     trending_tokens = VotingSystem.get_trending_tokens(30)  # Get top 30 tokens
#     # Format and send the leaderboard to the user
