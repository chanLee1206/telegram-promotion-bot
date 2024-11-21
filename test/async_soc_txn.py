import socketio
import asyncio
import json

sio = socketio.AsyncClient()

async def on_connect():

    print("Connected to WebSocket!")
    await sio.emit("SUBSCRIBE_REALTIME_TRANSACTION", {
        'pairId': 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356',
        # 'pairId': '31ab399cb31e4c682f0e38cecf469742f13c190180fbae3b332468d670d28584'
    })

    await sio.emit("SUBSCRIBE_REALTIME_TRANSACTION", {
        'pairId': '31ab399cb31e4c682f0e38cecf469742f13c190180fbae3b332468d670d28584'
    })

    await sio.emit('SUBSCRIBE_REALTIME_PAIR_STATS_CHANGED', {
        'pairId': 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356'
    })

    await sio.emit('SUBSCRIBE_REALTIME_TRANSACTION', { 
        'maker': '0xd6840994167c67bf8063921.......17da41b3f64bb328db1687ddd713c5281',
    })
        
    print("Subscription message sent.")

@sio.event
async def connect():
    print("Socket connected!")
    await on_connect()

@sio.event
async def connect_error(data):
    print(f"Connection failed with error: {data}")

@sio.event
async def disconnect():
    print("Disconnected from WebSocket!")

@sio.on("TRANSACTION")
async def handle_transaction(data):
    try:
        print(data, '\n')
    except Exception as e:
        print(f"Error processing transaction: {e}")

@sio.on("PAIR_STATS_CHANGED")  # Match the event name used in the API guide
async def handle_pair(data):
    print("Pair stats changed::")
    print(json.dumps(data, indent=4), '\n')

async def main():
    SOCKET_URL = "wss://ws-sui.raidenx.io"
    try:
        await sio.connect(SOCKET_URL)  # Replace with your WebSocket URL
        print("Attempting to connect to WebSocket server...")

        await sio.wait()
    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
