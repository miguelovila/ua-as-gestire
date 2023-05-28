import json
import time
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
# - available now
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
		available_now = content['available_now'] if 'available_now' in content and content['available_now'] != '' else None
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
		if available_now is not None:
			if bool(int(available_now)):
				rooms = [
					room for room in rooms if checkRoomAvailability(room[0])]
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
			), 401
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
		), 400
	except:
		return json.dumps(
			{
				"error": "Invalid request"
			}
		), 400


@app.route('/api/rooms/<int:room_id>/reserve', methods=['POST'])
def reserveRoom(room_id):
	try:
		content = json.loads(request.data)
		if not checkToken(content['token'], False):
			return json.dumps(
				{
					"error": "Access denied"
				}
			), 401
		user_id = executor("SELECT user_id FROM tokens WHERE token = ?;", (content['token'],))[0][0]
		start_time = int(content['start_time'])
		end_time = start_time + int(content['duration'])
		reason = content['reason'] if 'reason' in content else None
		if start_time < 0 or end_time < 0 or end_time - start_time < 900:
			return json.dumps(
				{
					"error": "Invalid reservation time"
				}
			), 400
		if not checkRoomAvailability(room_id, start_time, end_time):
			return json.dumps(
				{
					"error": "Room not available"
				}
			), 400
		executor("INSERT INTO reservations (user_id, room_id, start_time, end_time, reason) VALUES (?, ?, ?, ?, ?);",
			(user_id, room_id, start_time, end_time, reason))
		return json.dumps(
			{
				"success": "Room reserved"
			}
		), 200
	except:
		return json.dumps(
			{
				"error": "Invalid request"
			}
		), 400


def checkRoomAvailability(room_id, start_time=int(time.time()), end_time=int(time.time()) + 900):
	try:
		reservations = executor("SELECT * FROM reservations WHERE room_id = ? AND ((start_time <= ? AND end_time >= ?) OR (start_time <= ? AND end_time >= ?));",
			(room_id, start_time, start_time, end_time, end_time))
		if len(reservations) > 0:
			return False
		return True
	except:
		return False
