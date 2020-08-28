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
tables = db_cursor.fetchall()
chairs = tables[0]
print(chairs)