import os, sqlite3
from cfg import *

def initializeDatabase():
    try:
        if not os.path.exists(STORAGE_PATH): os.makedirs(STORAGE_PATH)
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                mec INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                profile_picture TEXT NOT NULL
            );      
        """)
        con.commit()
        con.close()
    except sqlite3.Error as error:
        raise Exception("Error connecting to the database: ", error)

def executor(query, tupledata=None):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    if tupledata == None :
        cursor.execute(query)
    else:
        cursor.execute(query, tupledata)
    data =  cursor.fetchall()
    connection.commit()
    connection.close()
    return data

def fillSampleData():
    if len(executor("SELECT * FROM users;")) > 0 : return

    print("Filling sample data...")
    executor("""
        INSERT INTO users (mec, name, email, password, profile_picture)
        VALUES (107000, 'Dummy User Zero', 'du0@ua.pt', 'du0', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand');
    """)

    executor("""
        INSERT INTO users (mec, name, email, password, profile_picture)
        VALUES (107001, 'Dummy User One', 'du1@ua.pt', 'du1', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand');
    """)

    executor("""
        INSERT INTO users (mec, name, email, password, profile_picture)
        VALUES (107002, 'Dummy User Two', 'du2@ua.pt', 'du2', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand');
    """)