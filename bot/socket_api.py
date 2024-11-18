import asyncio
import websockets
import json  # Import json for serialization

# WebSocket URL
WEBSOCKET_URL = "wss://ws-sui-order.raidenx.io/TRANSACTION"

async def track_transactions():
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("Connected to WebSocket")
            
            # Example subscription message as a dictionary
            subscription_message = {
                "pairId": "fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356"
            }
            
            # Serialize the subscription message to JSON and send it
            await websocket.send(json.dumps(subscription_message))
            
            # Receive messages from the WebSocket
            async for message in websocket:
                print("Message received:", message)
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"WebSocket connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(track_transactions())
