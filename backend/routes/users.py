import json, random, time, sched, threading
from flask import request
from __main__ import app, executor, checkToken


@app.route("/api/users/reservations", methods=["GET"]) 
def getReservationsByToken():
	try:
		content = json.loads(request.data)
		if not checkToken(content["token"], False):
			return json.dumps({"error": "Access denied"}), 401
		user_id = executor("SELECT user_id FROM tokens WHERE token = ?;", (content['token'],))[0][0]
		room_reservations = executor("SELECT * FROM reservations WHERE user_id = ? ORDER BY start_time DESC LIMIT 100;", (user_id,))
		equipment_reservations = executor("SELECT * FROM equipment_reservations WHERE user_id = ? ORDER BY start_time DESC LIMIT 100;", (user_id,))
		detailed_room_reservations = []
		detailed_equipment_reservations = []
		for reservation in room_reservations:
			room = executor("SELECT * FROM rooms WHERE id = ?;", (reservation[2],))[0]
			detailed_room_reservations.append({
				"id": reservation[0],
				"start_time": reservation[3],
				"end_time": reservation[4],
				"room": {
					"id": room[0],
					"name": room[1],
					"capacity": room[2],
					"available": room[3]
				}
			})
		for reservation in equipment_reservations:
			equipment = executor("SELECT * FROM equipments WHERE id = ?;", (reservation[2],))[0]
			detailed_equipment_reservations.append({
				"id": reservation[0],
				"start_time": reservation[3],
				"end_time": reservation[4],
				"equipment": {
					"id": equipment[0],
					"name": equipment[1],
					"available": equipment[6]
				}
			})
		detailed_reservations = {
			"rooms": detailed_room_reservations,
			"equipments": detailed_equipment_reservations
		}
		if len(detailed_reservations) > 0:
			return json.dumps({"reservations": detailed_reservations}), 200
		else:
			return json.dumps({"error": "No reservations found"}), 404
	except:
	    return json.dumps({"error": "Invalid request"}), 400
	
