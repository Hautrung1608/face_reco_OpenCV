import sqlite3

def save_to_database(image, timestamp):
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Faces (timestamp, image) VALUES (?, ?)", (timestamp, image))
    conn.commit()
    conn.close()
