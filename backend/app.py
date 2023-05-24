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
        if len(executor("SELECT * FROM users WHERE email = ?;", (email,))) > 0:
            user = executor("SELECT * FROM users WHERE email = ?;", (email,))[0]
            print(user)
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
                "error": "Invalid username or password"
            }
        ), 401
@app.route('/api/rooms', methods=['GET'])
def listRooms():
    try:
        rooms = executor("SELECT * FROM rooms;")
        return json.dumps(
            {
                "rooms": rooms
            }
        ), 200
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