import os
import mysql.connector

connection = None

try:
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "19617")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB", "defaultdb"),
        ssl_disabled=False,
        connection_timeout=15
    )

    if connection.is_connected():
        print("Database Connected Successfully")

except mysql.connector.Error as err:
    print("Database Connection Failed")
    print(err)
    connection = None