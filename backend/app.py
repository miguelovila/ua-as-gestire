from cfg import *
from database.con import *
from flask import Flask, jsonify 

app = Flask(__name__)

from routes.auth import *
from routes.rooms import *
from routes.equipments import *
    
if __name__ == '__main__':
    initializeDatabase()
    fillSampleUserData()
    fillSampleRoomData()
    fillSampleEquipmentData()
    app.run(host='0.0.0.0', port=5000)
    
    
    
# Compare this snippet from ua-as-gestire-project\backend\database\__init__.py:
# from .con import *
# Compare this snippet from ua-as-gestire-project\backend\database\cfg.py: 
# Compare this snippet from ua-as-gestire-project\backend\database\con.py:
# import os
# import sqlite3
#
#
# def initializeDatabase():
#     if not os.path.exists('database.db'):
#         conn = sqlite3.connect('database.db')
#         c = conn.cursor()
#         c.execute('''CREATE TABLE users
#                      (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, name TEXT NOT NULL, surname TEXT NOT NULL, role TEXT NOT NULL)''')
#         c.execute('''CREATE TABLE rooms
#                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, picture TEXT NOT NULL)''')
#         c.execute('''CREATE TABLE equipments
#                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, picture TEXT NOT NULL)''')
#         c.execute('''CREATE TABLE room_equipment
#                      (id INTEGER PRIMARY KEY AUTOINCREMENT, room_id INTEGER NOT NULL, equipment_id INTEGER NOT NULL, FOREIGN KEY(room_id) REFERENCES rooms(id), FOREIGN KEY(equipment_id) REFERENCES equipments(id))''')
#         c.execute('''CREATE TABLE tokens
#                      (id INTEGER PRIMARY KEY AUTOINCREMENT, token TEXT NOT NULL, expiration INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))''')
#         conn.commit()
#         conn.close()
#
# def fillSampleUserData():
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     c.execute("INSERT INTO users (username, password, email, name, surname, role) VALUES ('admin', 'admin', 'admin@admin', 'admin', 'admin', 'admin');")
#     conn.commit()
#     conn.close()
#



