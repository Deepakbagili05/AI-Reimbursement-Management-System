import os
import mysql.connector

connection = None

try:
    host = os.getenv("MYSQL_HOST")
    port = int(os.getenv("MYSQL_PORT", "19617"))
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    database = os.getenv("MYSQL_DB", "defaultdb")

    print("MYSQL_HOST:", host)
    print("MYSQL_PORT:", port)

    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl_disabled=False
    )

    print("Database Connected Successfully")

except mysql.connector.Error as e:
    print("Database Connection Failed")
    print(e)
    connection = None