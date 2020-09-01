import item_list_ripper
import db_connect

db = db_connect.connection()
con = db.cursor()
con.execute("show tables;")
x = con.fetchall()
print(x)

