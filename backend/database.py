import os
import socket
import pymysql
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB", "defaultdb")

print("MYSQL_HOST:", MYSQL_HOST)
print("MYSQL_PORT:", MYSQL_PORT)

try:
    ip = socket.gethostbyname(MYSQL_HOST)
    print("Aiven DNS resolved to:", ip)
except Exception as e:
    print("Aiven DNS resolution failed:", e)

connection = None

try:
    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        ssl={"ssl": {}},
        connect_timeout=30,
        cursorclass=pymysql.cursors.DictCursor
    )

    print("Database Connected Successfully")

except Exception as e:
    print("Database Connection Failed")
    print(e)