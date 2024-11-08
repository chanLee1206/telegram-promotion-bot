import pymysql

# Define a global variable to hold token data
global global_token_arr

# Database connection details
db_config = {
    'host': 'autorack.proxy.rlwy.net',
    'user': 'root',
    'password': 'GbOlKeFDrsnprEQizCkdtfwjxHEhXMav',
    'db': 'railway',
    'port': 14715
}

def load_global_token_arr():
    try:
        # Connect to the database synchronously
        print("Connecting to the database...")
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # Fetch data from tb_tokens table
            query = "SELECT nickSymbol, name, symbol, decimals, coinType, supply FROM tb_tokens"
            cursor.execute(query)
            
            # Load the data into the global array
            global_token_arr = cursor.fetchall()
            
            print("Data loaded successfully:", global_token_arr)

        # Close the connection
        connection.close()

        return global_token_arr
        
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return None

