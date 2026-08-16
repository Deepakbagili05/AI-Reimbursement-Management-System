import pymysql
from config import *

try:
    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

    print("Database Connected Successfully")

except Exception as e:
    print("Database Connection Failed")
    print(e)