import bcrypt
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

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY,
                token TEXT NOT NULL,
                expiration INTEGER NOT NULL,
                user_id INTEGER NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                image TEXT NOT NULL
                caracteristics TEXT NOT NULL,
                reservations TEXT NOT NULL,
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS equipments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                reservations TEXT NOT NULL,
                locker TEXT NOT NULL,
                image TEXT NOT NULL
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

def fillSampleUserData():
    if len(executor("SELECT * FROM users;")) > 0 : return

    executor("""
        INSERT INTO users (mec, name, email, password, profile_picture)
        VALUES (107000, 'Dummy User Zero', 'du0@ua.pt', ?, 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand');
    """, (bcrypt.hashpw("du0".encode('utf-8'), bcrypt.gensalt()),))

    executor("""
        INSERT INTO users (mec, name, email, password, profile_picture)
        VALUES (107001, 'Dummy User One', 'du1@ua.pt', ?, 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand');
    """, (bcrypt.hashpw("du1".encode('utf-8'), bcrypt.gensalt()),))

    executor("""
        INSERT INTO users (mec, name, email, password, profile_picture)
        VALUES (107002, 'Dummy User Two', 'du2@ua.pt', ?, 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand');
    """, (bcrypt.hashpw("du2".encode('utf-8'), bcrypt.gensalt()),))
    
def fillSampleRoomData():
    if len(executor("SELECT * FROM rooms;")) > 0 : return

    #
    # FIRST FLOOR
    #

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.01', 'Teaching Laboratory', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 10, "Computers": 10, "Oscilloscopes": 10, "Signal Generators": 10, "Multimeters": 10, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.02', 'Videoconference Room', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 60, "Power Sockets": 30, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": true, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.03', 'Office', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.04', 'Teaching Laboratory', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 10, "Computers": 10, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.05', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 9, "Power Sockets": 3, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.06', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 10, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.07', 'Office', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": false}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.19', 'Classroom', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 40, "Power Sockets": 30, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.23', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 15, "Computers": 10, "Oscilloscopes": 5, "Signal Generators": 5, "Multimeters": 5, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.24', 'Office', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": false}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.25', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": false}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.26', 'Classroom', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 10, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.27', 'Office', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": false}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.28', 'Classroom', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.29', 'Office', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": false}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.30', 'Classroom', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand', '{"Capacity": 30, "Power Sockets": 25, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": true, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.1.32', 'Classroom', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": true, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('ANF IV', 'Auditorium', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 200, "Power Sockets": 70, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": true, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('ANF V', 'Auditorium', 'https://i.imgur.com/F9Nf9Fx_d.webp?fidelity=grand', '{"Capacity": 200, "Power Sockets": 70, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": true, "Projector": true, "Whiteboard": true}', '[]');
    """)

    #
    # SECOND FLOOR
    #

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.01', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.02', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.03', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 20, "Oscilloscopes": 20, "Signal Generators": 20, "Multimeters": 20, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.04', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.05', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.06', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.07', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 20, "Oscilloscopes": 20, "Signal Generators": 20, "Multimeters": 20, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.08', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 20, "Oscilloscopes": 20, "Signal Generators": 20, "Multimeters": 20, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.09', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.10', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.11', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 20, "Oscilloscopes": 20, "Signal Generators": 20, "Multimeters": 20, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.14', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 20, "Oscilloscopes": 20, "Signal Generators": 20, "Multimeters": 20, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.15', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 20, "Oscilloscopes": 20, "Signal Generators": 20, "Multimeters": 20, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.16', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 10, "Oscilloscopes": 10, "Signal Generators": 10, "Multimeters": 10, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.17', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 10, "Oscilloscopes": 10, "Signal Generators": 10, "Multimeters": 10, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.18', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.19', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.20', 'Teaching Laboratory', 'https://i.imgur.com/r7lTF4V_d.webp?fidelity=grand', '{"Capacity": 20, "Power Sockets": 20, "Computers": 10, "Oscilloscopes": 10, "Signal Generators": 10, "Multimeters": 10, "Sound System": false, "Projector": true, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.21', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": false, "Projector": false, "Whiteboard": true}', '[]');
    """)

    executor("""
        INSERT INTO rooms (name, description, image, caracteristics, reservations)
        VALUES ('4.2.22', 'Office', 'https://i.imgur.com/O9Wmyek_d.webp?fidelity=grand', '{"Capacity": 6, "Power Sockets": 4, "Computers": 0, "Oscilloscopes": 0, "Signal Generators": 0, "Multimeters": 0, "Sound System": true, "Projector": false, "Whiteboard": false}', '[]');
    """)


def fillSampleEquipmentData():
    if len(executor("SELECT * FROM equipments;")) > 0 : return

    executor("""
        INSERT INTO equipments (name, description, reservations, locker, image)
        VALUES ('Oscilloscope', 'Oscilloscope', '[]', '1A', 'https://i.imgur.com/5ZQ8X6u_d.webp?fidelity=grand');
    """)

    executor("""
        INSERT INTO equipments (name, description, reservations, locker, image)
        VALUES ('Arduino UNO', 'Development Board & Kit', '[]', '1B', 'https://i.imgur.com/5ZQ8X6u_d.webp?fidelity=grand');
    """)

    executor("""
        INSERT INTO equipments (name, description, reservations, locker, image)
        VALUES ('Raspberry Pi 4B', 'Development Board & Kit', '[]', '1C', 'https://i.imgur.com/5ZQ8X6u_d.webp?fidelity=grand');
    """)

    executor("""
        INSERT INTO equipments (name, description, reservations, locker, image)
        VALUES ('Raspberry Pi 3B+', 'Development Board & Kit', '[]', '1D', 'https://i.imgur.com/5ZQ8X6u_d.webp?fidelity=grand');
    """)

    executor("""
        INSERT INTO equipments (name, description, reservations, locker, image)
        VALUES ('DETPIC', 'Development Board', '[]', '2A', 'https://i.imgur.com/5ZQ8X6u_d.webp?fidelity=grand');
    """)

    executor("""
        INSERT INTO equipments (name, description, reservations, locker, image)
        VALUES ('FPGA Cyclone IV', 'Development Board', '[]', '2B', 'https://i.imgur.com/5ZQ8X6u_d.webp?fidelity=grand');
    """)
