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


@app.route('/api/rooms', methods=['POST'])
def filterRooms():
	try:
		content = json.loads(request.data)
		if not checkToken(content['token'], False):
			return json.dumps({"error": "Access denied"}), 401
		filters = content['filters']

		# Extract filter values from the request
		min_seats = filters.get('minSeats')
		min_power_sockets = filters.get('minPowerSockets')
		room_type = filters.get('type')
		available_now = filters.get('availableNow')

		# Build the SQL query and parameters based on the filters
		query = "SELECT * FROM rooms WHERE 1=1"
		params = []

		if min_seats is not None:
			query += " AND capacity >= ?"
			params.append(int(min_seats))
		if min_power_sockets is not None:
			query += " AND power_sockets >= ?"
			params.append(int(min_power_sockets))
		if room_type is not None:
			query += " AND description = ?"
			params.append(room_type)
		
		# Execute the query
		rooms = executor(query, params)

		# Filter rooms based on availability if 'availableNow' is True
		if available_now is not None and available_now:
			rooms = [room for room in rooms if checkRoomAvailability(room[0])]

		# Return the filtered rooms
		if len(rooms) > 0:
			return json.dumps({"rooms": rooms}), 200
		else:
			return json.dumps({"error": "No rooms found with the specified parameters"}), 400

	except Exception as e:
		print(e)
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
