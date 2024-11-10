import pymysql
from globals import global_token_arr

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
            # if(record) :
            #     print("fetched record data - " , record, record["allow"])
            # else :
            #     print("fetched record data - " , "None")
                
            return record
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []
