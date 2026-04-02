import mysql.connector

def get_connection():
    conn=mysql.connector.connect(
        host="127.0.0.1",
        port=8889,
        user="root",
        password="root",
        database="financegestor"
    )
    return conn
def fetch(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def execute(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()
