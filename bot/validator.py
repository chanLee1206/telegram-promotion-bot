def validate_token_id(token_id: str) -> bool:
    """Validate that the token ID has at least 5 characters."""
    if len(token_id) >= 5:
        return True
    else:
        return False