import pymysql
import asyncio
from globals import global_token_arr

import time  
from datetime import datetime, timedelta

from api_test.txns_account import fetch_account_txns

# Database connection details
db_config = {
    'host': 'autorack.proxy.rlwy.net',
    'user': 'root',
    'password': 'GbOlKeFDrsnprEQizCkdtfwjxHEhXMav',
    'db': 'railway',
    'port': 14715
}

# Global variable to hold the database connection
connection = None

def initialize_connection():
    """Initialize the global database connection."""
    global connection
    if connection is None:
        try:
            print("Connecting to the database...")
            connection = pymysql.connect(**db_config)
            print("Database connected successfully.")
        except pymysql.MySQLError as err:
            print(f"Error connecting to database: {err}")
            connection = None

def get_connection():
    """Retrieve the current database connection."""
    if connection is None:
        initialize_connection()
    return connection

def close_connection():
    """Close the global database connection."""
    global connection
    if connection:
        print("Closing the database connection...")
        connection.close()
        connection = None
        print("Database connection closed.")

def load_global_token_arr():
    """Load data from tb_tokens into global_token_arr."""
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                query = "SELECT symbol, name, decimals, coinType, supply FROM tb_tokens"
                cursor.execute(query)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                
                global_token_arr.clear()
                global_token_arr.extend([dict(zip(column_names, row)) for row in results])
              
                print("Data loaded successfully:", global_token_arr)
            conn.commit()
        except pymysql.MySQLError as err:
            print(f"Error during query: {err}")
    else:
        print("Database connection is not available.")

def fetch_Cointype(coin_type):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        # with conn.cursor() as cursor:
            # Query to check if the coinType exists in the tb_tokens table
            query = "SELECT * FROM tb_tokens WHERE coinType = %s LIMIT 1"
            cursor.execute(query, (coin_type,))
            # Fetch result
            record = cursor.fetchone()
            return record
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

async def fetch_account_payments(timestamp = 1704067200) :
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        # with conn.cursor() as cursor:
            # Query to check if the coinType exists in the tb_tokens table
            query = f"SELECT * FROM tb_trend_receive WHERE timestamps > {timestamp}"
            print(query)
            cursor.execute(query)
            # Fetch result
            records = cursor.fetchall()
            return records
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

async def main():
    account = "0xd6840994167c67bf8063921f5da138a17da41b3f64bb328db1687ddd713c5281"
    # queryType = "unReg" # all / reg / unReg
    # timestamp = 1704067200
    # print(fetch_account_payments(account, 1704067200, queryType))
    # Simulate payment validation delay
    # await asyncio.sleep(5)
    current_time = datetime.now()
    time_ahead = current_time - timedelta(minutes=20)
    timestamp_ahead = int(time_ahead.timestamp())
    
    detected_txns = await fetch_account_txns(account, timestamp_ahead)
    checked_txns = await fetch_account_payments(account, timestamp_ahead, 'reg')
    print('detected from account--------', detected_txns, '\n')
    print('detected from db ------------', checked_txns, '\n')

if __name__ == "__main__":
    asyncio.run(main())
