import socketio
import requests
import json

# WebSocket endpoint (Socket.IO)
SOCKET_IO_URL = "wss://ws-sui.raidenx.io"

# Create a Socket.IO client
sio = socketio.Client()

# Event: Connect to the WebSocket server
@sio.event
def connect():
    print("Connected to Socket.IO server!")
    # Subscribe to transaction updates for a specific pair (replace with actual pairId)
    pair_id = "0xb785e6eed355c1f8367c06d2b0cb9303ab167f8359a129bb003891ee54c6fce0"  # Example pairId
    subscription_message = {
        "pairId": pair_id
    }
    sio.emit("SUBSCRIBE_REALTIME_TRANSACTION", subscription_message)
    print(f"Subscribed to real-time transactions for pairId: {pair_id}")

# Event: Handle incoming transaction messages
@sio.event
def message(data):
    print("Transaction update received:", data)
    
    # Extract relevant transaction data
    try:
        print(data)
        
    except KeyError as e:
        print(f"Error extracting data: {e}")

# Event: Handle WebSocket disconnection
@sio.event
def disconnect():
    print("Disconnected from Socket.IO server")

# Function to connect and listen for updates
def main():
    try:
        sio.connect(SOCKET_IO_URL)  # Connect to the WebSocket server
        sio.wait()  # Wait for events (this is a blocking call)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
