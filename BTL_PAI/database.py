# database.py
import sqlite3

def setup_database():
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Faces
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp TEXT,
                       image BLOB)''')
    conn.commit()
    conn.close()

def fetch_from_database():
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faces")
    records = cursor.fetchall()
    conn.close()
    return records
