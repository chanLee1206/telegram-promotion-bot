import asyncio
import websockets
import json

coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508%3A%3Aancy%3A%3AANCY"
url = f"https://api.blockvision.org/v2/sui/coin/detail?coinType={coin_type}"

# headers = {
#     "accept": "application/json",
#     "x-api-key": "2oAWXc23NfVKN0E4TxFfnnVZP6Q"
# }

# response = requests.get(url, headers=headers)

# Replace with the BlockEden WebSocket endpoint
API_KEY = "jM6hFH1NfPqb8SCaRxF2"
TOKEN_ADDRESS = "your_sui_token_address"  # Replace with the SUI token address you want to track
BLOCKEDEN_WEBSOCKET_URL =  f"wss://api.blockeden.xyz/v1/sui/stream"
async def track_transactions():
    print("Connecting to BlockEden WebSocket...")
    async with websockets.connect(BLOCKEDEN_WEBSOCKET_URL) as websocket:
        # Construct a subscription message based on BlockEden’s WebSocket API requirements
        subscribe_message = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "subscribe",
            "params": {
                "address": "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY",
                "event_type": "transfer"  # Adjust if needed based on the exact event type
            }
        })
        await websocket.send(subscribe_message)
        print("Subscribed to transactions for token:", TOKEN_ADDRESS)

        while True:
            data = await websocket.recv()
            parsed_data = json.loads(data)

            # Process and print transaction data
            print("Transaction Data:", parsed_data)

def main():
    asyncio.run(track_transactions())

# Run the event loop
if __name__ == "__main__":
    main()
