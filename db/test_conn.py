import pymysql

db_config = {
    'host': 'autorack.proxy.rlwy.net',
    'user': 'root',
    'password': 'GbOlKeFDrsnprEQizCkdtfwjxHEhXMav',
    'database': 'railway',
    'port': 14715
}

try:
    connection = pymysql.connect(**db_config)
    print("Connection successful!")
except pymysql.MySQLError as err:
    print(f"Error: {err}")
finally:
    if 'connection' in locals() and connection.open:
        connection.close()
