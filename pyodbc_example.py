import pyodbc
import json
import socket
import requests
ip = requests.get('https://api.ipify.org').text
# ip_hex_str = '0x' + socket.inet_aton(ip).hex()
ip_bytes = socket.inet_aton(ip)
print(ip)
print(ip_bytes.hex())

api_result = {
    "time": "2024-10-28T11:10:37.782856+08:00", 
    "blur_score": 0.5676911039324237
}

SERVER = 'server_address'
DATABASE = 'db_name'
USERNAME = 'username'
PASSWORD = 'password'

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

conn = pyodbc.connect(connectionString) 
cursor = conn.cursor()

SQL_STATEMENT = """
INSERT dbo.API_LOG (
timestamp, 
user_name, 
project_name, 
ip, 
method,
api_result
)
VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
"""
print(ip_bytes)
print(json.dumps(api_result))
# cursor.execute(
#     SQL_STATEMENT,
#     'asus', 
#     'test_db.py', 
#     ip_bytes,
#     'test_method',
#     json.dumps(api_result)
# )

# conn.commit()

cursor.close()
conn.close()
