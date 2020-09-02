import mysql.connector as connector

def connection():

    config = {
        "user": "newuser",
        "password": "password",
        "host": "127.0.0.1",
        "database": "midcentury"
    }
    try:
        c = connector.connect(**config)
        return c
    except:
        print ("connection error, please double check your settings")
        exit(1)


def makeConnection(): #no error method
    cn = connection()
    cur = cn.cursor()
    return cur
    #cur.execute("show tables;")
    #x = cur.fetchall()
    