import json
from flask import request
from __main__ import app, executor, checkToken

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

@app.route('/api/rooms', methods=['GET'])
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
        

@app.route('/api/rooms/reserve', methods=['POST'])
def reserveRoom():
    try:
        content = json.loads(request.data)
        if not checkToken(content['token'], False):
            return json.dumps(
                {
                  "error": "Access denied"
                }
            ),401
        
        room_id = content['room_id']
        user_id = content['user_id']
        start_time = content['start_time']
        end_time = content['end_time']
        
        executor("INSERT INTO reservations (room_id, user_id, start_time, end_time) VALUES (?, ?, ?, ?);", (room_id, user_id, start_time, end_time))
        
        return json.dumps(
            {
              "success": "Room reserved"
            }
        ),200
    except:
        return json.dumps(
            {
              "error": "Invalid request"
            }
        ),400