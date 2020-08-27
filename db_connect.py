import mysql.connector
db_connection = mysql.connector.connect(
    host = "localhost",
    user = "newuser",
    password = "password",
    database = "midcentury",
)
#print(db_connection)
db_cursor = db_connection.cursor()
db_cursor.execute("SHOW TABLES")
for table in db_cursor:
    print(table)