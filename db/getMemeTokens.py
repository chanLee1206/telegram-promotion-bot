import pymysql

# Define a global variable to hold token data
global_token_arr = []

# Database connection details
db_config = {
    'host': 'autorack.proxy.rlwy.net',
    'user': 'root',
    'password': 'GbOlKeFDrsnprEQizCkdtfwjxHEhXMav',
    'database': 'railway',
    'port': 14715
}

def load_global_token_arr():
    global global_token_arr
    try:
        # Connect to the database using PyMySQL
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Fetch data from tb_tokens table
        query = "SELECT nickSymbol, name, symbol, decimals, coinType, supply FROM tb_tokens"
        cursor.execute(query)
        
        # Load the data into the global array
        global_token_arr = cursor.fetchall()  # Retrieves all rows as a list of tuples
        print("Data loaded successfully:", global_token_arr)

    except pymysql.MySQLError as err:
        print(f"Error: {err}")
    finally:
        # Close cursor and connection if open
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.open:
            connection.close()

# Call the function to load data
def main():
    load_global_token_arr()
    # Print the loaded data
    print(global_token_arr)

if __name__ == "__main__":
    main()
