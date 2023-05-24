import sqlite3
import bcrypt
import json
from con import *
from cfg import *
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/auth', methods=['POST'])
def authenticate():
    try:
        content = json.loads(request.data)
        email = content['email']
        password = content['password']
        user = executor("SELECT * FROM users WHERE email = ?;", (email,))
        if len(user) > 0:
            user = user[0]
            if bcrypt.checkpw(password.encode('utf-8'), user[4]):
                return json.dumps(
                    {
                        "mec": user[1],
                        "name": user[2],
                        "email": user[3],
                        "profile_picture": user[5]
                    }
                ), 200
            else:
                return json.dumps(
                    {
                        "error": "Invalid username or password"
                    }
                ), 401
        else:
            return json.dumps(
                {
                    "error": "Invalid username or password"
                }
            ), 401
    except:
        return json.dumps(
            {
                "error": "Invalid request"
            }
        ), 401

@app.route('/api/rooms', methods=['GET'])
def listRooms():
    try:
        rooms = executor("SELECT * FROM rooms;")
        if len(rooms) > 0:
            return json.dumps(
                {
                    "rooms": rooms
                }
            ), 200
        return json.dumps(
            {
                "error": "No rooms found"
            }
        ),400
    except:
        return json.dumps(
            {
                "error": "Invalid request"
            }
        ),400
    
@app.route('/api/rooms/<int:room_id>', methods=['GET'])
def getRoom(room_id):
    try:
        room = executor("SELECT * FROM rooms WHERE id = ?;", (room_id,))
        if len(room) > 0:
            return json.dumps(
                {
                    "room": room[0]
                }
            ), 200
        return json.dumps(
            {
                "error": "Room not found"
            }
        ),400
    except:
        return json.dumps(
            {
                "error": "Invalid request"
            }
        ),400
    
if __name__ == '__main__':
    initializeDatabase()
    fillSampleUserData()
    fillSampleRoomData()
    fillSampleEquipmentData()
    app.run(host='0.0.0.0', port=5000)