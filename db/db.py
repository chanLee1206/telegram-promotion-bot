import pymysql
import asyncio

import time  
from datetime import datetime, timedelta

from api_test.txns_account import fetch_account_txns

db_config = {
    'host': 'autorack.proxy.rlwy.net',
    'user': 'root',
    'password': 'GbOlKeFDrsnprEQizCkdtfwjxHEhXMav',
    'db': 'railway',
    'port': 14715
}

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
    global connection
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
                # query = "SELECT symbol, name, launchPad, decimals, coinType, supply FROM tb_tokens where allow = 1"
                query = "SELECT * FROM tb_tokens where allow = 1"
                cursor.execute(query)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                
                token_arr = [dict(zip(column_names, row)) for row in results]

                # print("Data loaded successfully:", token_arr)
                return token_arr
            
            conn.commit()
        except pymysql.MySQLError as err:
            print(f"Error during query: {err}")
    else:
        print("Database connection is not available.")

def fetch_Cointype(coin_type):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT * FROM tb_tokens WHERE coinType = %s LIMIT 1"
            cursor.execute(query, (coin_type,))
            # Fetch result
            record = cursor.fetchone()
            return record
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

async def fetch_db_payments(server_account, timestamp = 1704067200) :
# async def fetch_db_payments(timestamp = 1704067200) :
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = f"SELECT * FROM tb_trend_txns WHERE to_account = '{server_account}' and timestamp > {timestamp}"
            print(query)
            cursor.execute(query)
            # Fetch result
            records = cursor.fetchall()
            return records
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

    
async def reg_memeToken(token):
    connection = get_connection()
    success = False
    message = None

    try:
        with connection.cursor() as cursor:
            # Insert into tokens if the symbol does not already exist
            query = """
                INSERT INTO tb_tokens (symbol, name, launchpad, launchURL, coinType, decimals, supply)
                SELECT %s, %s, %s, %s, %s, %s, %s
                FROM DUAL
                WHERE NOT EXISTS (
                    SELECT 1 FROM tb_tokens WHERE symbol = %s
                );"""
            data = (
                token.get('symbol'),
                token.get('name'),
                token.get('launchpad'),
                token['launchURL'],
                token['coinType'],
                token.get('decimals'),
                token.get('supply'),
                token.get('symbol'),  # Added this to match the WHERE clause placeholder
            )
            cursor.execute(query, data)
        
        # Check if the row was inserted (affected rows)
        if cursor.rowcount == 0:
            message = f"Token {token.get('symbol')} already exists."
        else:
            connection.commit()
            success = True
            message = f"Token {token.get('symbol')} has been successfully added."

    except pymysql.MySQLError as e:
        message = f"Failed to add token {token.get('symbol')}. Error: {e}"
        connection.rollback()

    return success, message
    
async def regist_payment(user_data, payment_data) :

    period_ms = {'12hours': 43200000, '24hours': 86400000, '48hours': 172800000, '3days': 259200000,
                  '1week': 604800000, '2weeks': 1209600000, '3weeks': 1814400000, '1month': 2592000000}
    
    trend_txn_record = {'from_account': payment_data['fromAccount'],
                        'to_account' : payment_data['account'],
                        'timestamp' : payment_data['timestamp'],
                        'sui_amount': payment_data['amount'],
                        'digest' : payment_data['digest']
                    }
    trend_history_record = {'digest' : payment_data['digest'],
                            'username' : user_data['user_name'],
                            'token_symbol' : user_data['coinSymbol'],
                            'start_timestamp' : payment_data['timestamp'],
                            'end_timestamp' : payment_data['timestamp'] + period_ms[user_data['period']],
                    }
    print(trend_txn_record, '\n', trend_history_record, '\n')     

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Insert into tb_trend_txns
            txn_query = """
                INSERT INTO tb_trend_txns (from_account, to_account, timestamp, sui_amount, digest)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(txn_query, (
                trend_txn_record['from_account'],
                trend_txn_record['to_account'],
                trend_txn_record['timestamp'],   # BIGINT
                trend_txn_record['sui_amount'],  # INT
                trend_txn_record['digest']
            ))

            # Insert into tb_trend_history
            history_query = """
                INSERT INTO tb_trend_history (digest, username, token_symbol, start_timestamp, end_timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(history_query, (
                trend_history_record['digest'],
                trend_history_record['username'],
                trend_history_record['token_symbol'],
                trend_history_record['start_timestamp'],  # BIGINT
                trend_history_record['end_timestamp']      # BIGINT
            ))

        # Commit the transaction
        connection.commit()
        print("Records inserted successfully.")

    except pymysql.MySQLError as e:
        print("Error occurred:", e)
        connection.rollback()

async def main():
    account = "0xd6840994167c67bf8063921f5da138a17da41b3f64bb328db1687ddd713c5281"
    timestamp = 1704067200
   
    current_time = datetime.now()
    time_ahead = current_time - timedelta(minutes=20)
    timestamp_ahead_ms = int(time_ahead.timestamp()) * 1000

    # detected_txns = await fetch_account_txns(account, 10000000 , timestamp_ahead)
    # detected_txns = await fetch_account_txns(account, 10000000 , 1730427928668)
    # details = await fetch_account_txns(account, 100000000, 1730427928668)
    print(current_time.timestamp(), timestamp_ahead_ms) #1731417311
    checked_txns = await fetch_db_payments(account, timestamp_ahead_ms)

    # print('detected from account--------', detected_txns, '\n')
    print('detected from db ------------', checked_txns, '\n')

if __name__ == "__main__":
    asyncio.run(main())
