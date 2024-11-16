import time
import requests
import json
import telegram

# Telegram Bot Token and Channel ID (Update with your bot token and channel ID)
BOT_TOKEN = '7616802949:AAEVIoSBug1sJBosOzO3lJ13kVqN_82MKRI'
CHAT_ID = "@suiTrending_boost"  # Replace with your actual chat ID
coin_type="0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"

SUI_API_URL = f"https://api.blockberry.one/sui/v1/coins/{coin_type}"

headers = {
    "accept": "*/*",
    "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"  # Replace with your actual API key
}

# Initialize Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

def get_token_price():
    try:
        # Make a request to the SUI API to fetch token data
        response = requests.get(SUI_API_URL, headers=headers)
        response.raise_for_status()  # Check for request errors
        data = response.json()
        print(data)
        # Parse the token information (adjust based on the API response format)
        token_price = data.get("price")  # Example key; replace with actual data structure
        token_name = data.get("coinName")    # Replace with actual data structure
        print(token_price, token_name)
        # return token_name, token_price
        return data

    except requests.RequestException as e:
        print(f"Error fetching token data: {e}")
        return None, None

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print("Message sent to Telegram channel")
    except Exception as e:
        print(f"Error sending message: {e}")

def main():
    while True:
        # Fetch the latest token price
        # token_name, token_price = get_token_price()
        temp = get_token_price()
        
        # if token_name and token_price:
        #     # Prepare the message
        #     message = f"Token: {token_name}\nPrice: ${token_price}"
            
        #     # Send the message to the Telegram channel
        #     send_telegram_message(message)
        
        # Wait for 5 seconds before fetching the data again
        time.sleep(5)

if __name__ == "__main__":
    main()