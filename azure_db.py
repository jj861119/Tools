import pyodbc
import socket
import requests
import logging
from utils import write_log
IP = requests.get('https://api.ipify.org').text
IP_BYTES = socket.inet_aton(IP)

SERVER = 'server_address'
DATABASE = 'db_name'
USERNAME = 'username'
PASSWORD = 'password'
CONN_STR = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

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

class AzureDB():
    def __init__(self):
        self.conn = pyodbc.connect(CONN_STR) 
        self.cursor = self.conn.cursor()
        self.falied_count = 0

    def write(self, user_name, project_name, method, api_result):
        try:
            self.cursor.execute(
                SQL_STATEMENT,
                user_name, 
                project_name, 
                IP_BYTES,
                method,
                api_result
            )

            self.conn.commit()
            self.falied_count = 0
        except pyodbc.Error as e:
            write_log(f'{type(e).__name__}: {e}', logging.ERROR)
            self.falied_count+=1

    def conn_valid(self):
        return self.falied_count < 5

    def __del__(self):
        self.cursor.close()
        self.conn.close()
