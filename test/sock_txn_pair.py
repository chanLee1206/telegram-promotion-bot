import socketio
import json
import signal
import sys
from threading import Event

SOCKET_URL = "wss://ws-sui.raidenx.io"
pair_id = "fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356"

sio = socketio.Client()
stop_event = Event()  # Event to signal when to stop

@sio.event
def connect():
    print("Connected to the WebSocket server!")
    subscription_message = {
        # "pairId": pair_id
    }
    print(f"Subscribing to pair ID: {pair_id}")
    # sio.emit('SUBSCRIBE_REALTIME_TRANSACTION', {
    #     'pairId': 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356'
    # })
    # sio.emit('SUBSCRIBE_REALTIME_TRANSACTION', {
    #     'pairId': 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356',
    # })
    sio.emit('SUBSCRIBE_REALTIME_TRANSACTION', {
        
    })
   
    sio.emit('SUBSCRIBE_REALTIME_PAIR_STATS_CHANGED', {
        'pairId': 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356',
    })

# Event to handle disconnection from the WebSocket
@sio.event
def disconnect():
    print("Disconnected from the WebSocket server!")

# Event to handle real-time transaction data
@sio.on("TRANSACTION")  # Match the event name used in the API guide
def handle_transaction(data):
    print("Real-time transaction data received:")
    print(json.dumps(data, indent=4))

@sio.on("PAIR_STATS_CHANGED")  # Match the event name used in the API guide
def handle_pair(data):
    print("Pair stats changed::")
    print(json.dumps(data, indent=4))

# Event for error handling
@sio.event
def connect_error(data):
    print("Connection failed:", data)

# Event for handling unknown messages
@sio.event
def message(data):
    print("Unknown message received:")
    print(json.dumps(data, indent=4))

def stop_gracefully(signal_received, frame):
    """Handles Ctrl+C (SIGINT) signal."""
    print("\nStopping gracefully...")
    stop_event.set()  # Signal to stop the main loop
    sio.disconnect()  # Disconnect from WebSocket
    sys.exit(0)       # Exit the script

def main():
    # Register signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, stop_gracefully)
    try:
        # Connect to the WebSocket server
        print("Connecting to the WebSocket server...")
        sio.connect(SOCKET_URL)

        # Run a loop to allow signal handling and keep the connection alive
        while not stop_event.is_set():
            pass

    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")
    finally:
        sio.disconnect()

if __name__ == "__main__":
    main()
