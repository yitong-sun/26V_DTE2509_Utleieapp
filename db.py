import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL444",
        database="UtstyrsUtleiedb"
    )
    return connection