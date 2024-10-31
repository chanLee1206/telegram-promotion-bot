def vote_command(update, context):
    # Command handler for voting
    handle_vote(update, context)

def leaderboard_command(update, context):
    # Retrieve and display the leaderboard
    trending_tokens = VotingSystem.get_trending_tokens(30)  # Get top 30 tokens
    # Format and send the leaderboard to the user
