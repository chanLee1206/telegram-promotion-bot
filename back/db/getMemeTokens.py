import pymysql


# Define a global variable to hold token data
from globals import global_token_arr

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
            query = "SELECT symbol, name, decimals, coinType, supply FROM tb_tokens"
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            # Map each row to a dictionary using the column names
            global_token_arr.clear()
            global_token_arr.extend([dict(zip(column_names, row)) for row in results])
          
            print("Data loaded successfully:", global_token_arr)

        # Close the connection
        connection.close()

        return global_token_arr
        
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return None
