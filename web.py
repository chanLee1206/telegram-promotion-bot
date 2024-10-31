import websocket
import json

# Callback function when a new message is received
def on_message(ws, message):
    print("Received message:", message)

# Callback function when an error occurs
def on_error(ws, error):
    print("Error:", error)

# Callback function when the WebSocket connection is closed
def on_close(ws, close_status_code, close_msg):
    print("Connection closed with code:", close_status_code, "and message:", close_msg)

# Callback function when the WebSocket connection is opened
def on_open(ws):
    # Example of subscribing to a token price feed or other channel
    subscription_message = json.dumps({
        "type": "subscribe",
        "channel": "price_updates",  # Change to appropriate channel
        "token": "your_token_address"
    })
    ws.send(subscription_message)

# Initialize the WebSocket connection
ws_url = "wss://api.birdeye.so/sui/v1/ws"
ws = websocket.WebSocketApp(
    ws_url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# Run the WebSocket client
ws.run_forever()
