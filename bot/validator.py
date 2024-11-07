def validate_token_id(token_id: str) -> bool:
    """Validate that the token ID has at least 5 characters."""
    if len(token_id) >= 5:
        return True
    else:
        return False

def validate_boosting_period(boosting_period) -> bool :
    if boosting_period.isdigit():
        period = int(boosting_period)
        return 1 <= period <= 10  # Valid boosting period if it is between 1 and 10 (inclusive)
    return False  # If not a number, return False

def validate_wallet_address(wallet_address) -> bool :
    return True

