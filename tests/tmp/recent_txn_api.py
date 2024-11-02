import time
import requests
import json
import telegram

# Telegram Bot Token and Channel ID (Update with your bot token and channel ID)
BOT_TOKEN = '7616802949:AAEVIoSBug1sJBosOzO3lJ13kVqN_82MKRI'
CHAT_ID = "@suiTrending_boost"  # Replace with your actual chat ID
coin_type="0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"


headers = {
    "accept": "*/*",
    "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"  # Replace with your actual API key
}

# Initialize Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

def get_token_txns(coinType):
    txn_arr=[]
    try:
        # get txn lists according to coin type
        txn_array_url = f"https://api.blockberry.one/sui/v1/coins/{coinType}/transactions?page=0&size=1&orderBy=DESC&sortBy=AGE"
        response = requests.post(txn_array_url, headers=headers)
        response.raise_for_status()  # Check for request errors
        data = response.json()
        # print(data)
        
        content_list = data.get("content", [])
        print(content_list)
        
        # Check if the content list has items
        if content_list:
            for transaction in content_list:
                txn_id = transaction.get("txHash")  # Access txHash inside each dictionary
                tx_type = transaction.get("txType")
                # txn_arr.push({'txn_id' => txn_id, 'txn_type' => txn_type})
                txn_arr.append({'txn_id': txn_id, 'txn_type': txn_type})
                # Continue processing each transaction item as needed
                print(f"Transaction ID: {txn_id}, Type: {txn_type}")
        else:
            print("No transactions found.")
        
        # return token_name, token_price
        return txn_arr

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
        temp = get_token_txns(coin_type)
        
        # if token_name and token_price:
        #     # Prepare the message
        #     message = f"Token: {token_name}\nPrice: ${token_price}"
            
        #     # Send the message to the Telegram channel
        #     send_telegram_message(message)
        
        # Wait for 5 seconds before fetching the data again
        time.sleep(5)

if __name__ == "__main__":
    main()