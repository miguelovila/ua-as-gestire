import sqlite3
import bcrypt
import json
from con import *
from cfg import *
from flask import Flask, request
import time

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
                token = bcrypt.hashpw((str(user[0]) + str(time.time())).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                executor("INSERT INTO tokens (token, expiration, user_id) VALUES (?, ?, ?);", (token, int(time.time()) + 600, user[0]))
                return json.dumps(
                    {
                      "mec": user[1],
                      "name": user[2],
                      "email": user[3],
                      "profile_picture": user[5],
                      "token": token
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
    
@app.route('/api/auth/check', methods=['POST'])
def checkToken(token = None, external = True):
    try:
        if external:
            content = json.loads(request.data)
            token = content['token']
        db_token = executor("SELECT * FROM tokens WHERE token = ?;", (token,))
        if len(db_token) > 0:
            db_token = db_token[0]
            if int(time.time()) < db_token[2]:
                executor("UPDATE tokens SET expiration = ? WHERE id = ?;", (int(time.time()) + 600, db_token[0]))
                if external:
                    return json.dumps(
                        {
                          "valid": True
                        }
                    ), 200
                return True
            else:
                executor("DELETE FROM tokens WHERE id = ?;", (db_token[0],))
                if external:
                    return json.dumps(
                        {
                          "valid": False
                        }
                    ), 401
                return False
        else:
            if external:
                return json.dumps(
                    {
                      "valid": False
                    }
                ), 401
            return False
    except:
        if external:
            return json.dumps(
                {
                  "error": "Invalid request"
                }
            ), 401
        return False

@app.route('/api/rooms', methods=['GET'])
def listRooms():
    try:
        content = json.loads(request.data)
        if not checkToken(content['token'], False):
            return json.dumps(
                {
                  "error": "Access denied"
                }
            ),401
        
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
    
# ======================== Filtering Results =======================
# Rooms can be filtered by combinations of the following parameters:
# - name
# - description
# - capacity
# - number of power sockets
# - number of computers
# - number of oscilloscopes
# - number of signal generators
# - number of multimeters
# - sound system
# - projector
# - whiteboard
#
# If the parameter is not specified, it is not considered in the filter
# for numeric parameters, the filter means "greater than or equal to"

@app.route('/api/rooms/filter', methods=['POST'])
def filterRooms():
    try:
        content = json.loads(request.data)
        if not checkToken(content['token'], False):
            return json.dumps({"error": "Access denied"}), 401

        name = content['name'] if 'name' in content and content['name'] != '' else None
        description = content['description'] if 'description' in content and content['description'] != '' else None
        capacity = content['capacity'] if 'capacity' in content and content['capacity'] != '' else None
        power_sockets = content['power_sockets'] if 'power_sockets' in content and content['power_sockets'] != '' else None
        computers = content['computers'] if 'computers' in content and content['computers'] != '' else None
        oscilloscopes = content['oscilloscopes'] if 'oscilloscopes' in content and content['oscilloscopes'] != '' else None
        signal_generators = content['signal_generators'] if 'signal_generators' in content and content['signal_generators'] != '' else None
        multimeters = content['multimeters'] if 'multimeters' in content and content['multimeters'] != '' else None
        sound_system = content['sound_system'] if 'sound_system' in content and content['sound_system'] != '' else None
        projector = content['projector'] if 'projector' in content and content['projector'] != '' else None
        whiteboard = content['whiteboard'] if 'whiteboard' in content and content['whiteboard'] != '' else None

        query = "SELECT * FROM rooms WHERE "
        params = []

        if name:
            query += "name LIKE ? AND "
            params.append("%" + name + "%")

        if description:
            query += "description LIKE ? AND "
            params.append("%" + description + "%")

        if capacity:
            query += "capacity >= ? AND "
            params.append(int(capacity))

        if power_sockets:
            query += "power_sockets >= ? AND "
            params.append(int(power_sockets))

        if computers:
            query += "computers >= ? AND "
            params.append(int(computers))

        if oscilloscopes:
            query += "oscilloscopes >= ? AND "
            params.append(int(oscilloscopes))

        if signal_generators:
            query += "signal_generators >= ? AND "
            params.append(int(signal_generators))

        if multimeters:
            query += "multimeters >= ? AND "
            params.append(int(multimeters))

        if sound_system is not None:
            query += "sound_system = ? AND "
            params.append(bool(int(sound_system)))

        if projector is not None:
            query += "projector = ? AND "
            params.append(bool(int(projector)))

        if whiteboard is not None:
            query += "whiteboard = ? AND "
            params.append(bool(int(whiteboard)))

        query = query[:-5] + ";"
        rooms = executor(query, params)

        if len(rooms) > 0:
            return json.dumps({"rooms": rooms}), 200

        return json.dumps({"error": "No rooms found with the specified parameters"}), 400

    except:
        return json.dumps({"error": "Invalid request"}), 400

@app.route('/api/rooms/<int:room_id>', methods=['GET'])
def getRoom(room_id):
    try:
        content = json.loads(request.data)
        if not checkToken(content['token'], False):
            return json.dumps(
                {
                  "error": "Access denied"
                }
            ),401

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

@app.route('/api/equipments', methods=['GET'])
def listEquipments():
    try:
        content = json.loads(request.data)
        if not checkToken(content['token'], False):
            return json.dumps(
                {
                  "error": "Access denied"
                }
            ),401
        
        equipments = executor("SELECT * FROM equipments;")
        if len(equipments) > 0:
            return json.dumps(
                {
                  "equipments": equipments
                }
            ), 200
        return json.dumps(
            {
              "error": "No equipments found"
            }
        ),400
    except:
        return json.dumps(
            {
              "error": "Invalid request"
            }
        ),400
    
@app.route('/api/equipments/<int:equipment_id>', methods=['GET'])
def getEquipment(equipment_id):
    try:
        content = json.loads(request.data)
        if not checkToken(content['token'], False):
            return json.dumps(
                {
                  "error": "Access denied"
                }
            ),401

        equipment = executor("SELECT * FROM equipments WHERE id = ?;", (equipment_id,))
        if len(equipment) > 0:
            return json.dumps(
                {
                  "equipment": equipment[0]
                }
            ), 200
        return json.dumps(
            {
              "error": "Equipment not found"
            }
        ),400
    except:
        return json.dumps(
            {
              "error": "Invalid request"
            }
        ),400
    
@app.route('/api/equipments', methods=['GET'])
def listEquipaents():
    try:
        equipments = executor("SELECT * FROM equipments;")
        return json.dump(
            {
                "equipments": equipments 
            }
        ),200
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