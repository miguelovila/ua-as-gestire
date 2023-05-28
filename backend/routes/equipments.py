import json, random, time, sched, threading
from flask import request
from __main__ import app, executor, checkToken

# ======================== Filtering Results =======================
# Equipments can be filtered by combinations of the following parameters:
# - name
# - description
# - Locker
# - Initial date
# - Final date
# If the parameter is not specified, it is not considered in the filter
# for numeric parameters, the filter means "greater than or equal to"


@app.route("/api/equipments", methods=["GET"])
def listEquipments():
	try:
		content = json.loads(request.data)
		if not checkToken(content["token"], False):
			return json.dumps({"error": "Access denied"}), 401

		equipments = executor("SELECT * FROM equipments;")
		if len(equipments) > 0:
			return json.dumps({"equipments": equipments}), 200
		return json.dumps({"error": "No equipments found"}), 400
	except:
		return json.dumps({"error": "Invalid request"}), 400


@app.route("/api/equipments/<int:equipment_id>", methods=["GET"])
def getEquipment(equipment_id):
	try:
		content = json.loads(request.data)
		if not checkToken(content["token"], False):
			return json.dumps({"error": "Access denied"}), 401

		equipment = executor("SELECT * FROM equipments WHERE id = ?;", (equipment_id,))
		if len(equipment) > 0:
				return json.dumps({"equipment": equipment[0]}), 200
		return json.dumps({"error": "Equipment not found"}), 400
	except:
		return json.dumps({"error": "Invalid request"}), 400


codes = {}
scheduler = sched.scheduler(time.time, time.sleep)

def release_equipment(code, reservation_id):
  if code in codes:
    equipment_id = codes[code]["equipment_id"]
    executor("UPDATE equipments SET available = 1 WHERE id = ?;", (equipment_id,))
    executor("UPDATE equipment_reservations SET observation = 'User didn''t pick up the equipment' WHERE id = ?;", (reservation_id,))
    del codes[code]

def run_scheduler():
  scheduler.run()

@app.route("/api/equipments/<int:equipment_id>/reserve", methods=["POST"])
def reserveEquipment(equipment_id):
	try:
		content = json.loads(request.data)
		if not checkToken(content["token"], False):
			return json.dumps({"error": "Access denied"}), 401
		user_id = executor("SELECT user_id FROM tokens WHERE token = ?;", (content['token'],))[0][0]
		equipment = executor("SELECT * FROM equipments WHERE id = ?;", (equipment_id,))
		if len(equipment) > 0:
			if equipment[0][6] == 1:
				start_time = int(content['start_time'])
				end_time = start_time + int(content['duration'])
				usage_place = content['usage_place'] if 'usage_place' in content else None
				
				if start_time < 0 or end_time < 0 or end_time - start_time < 900:
					return json.dumps({"error": "Invalid time"}), 400
				
				executor("INSERT INTO equipment_reservations (equipment_id, user_id, start_time, end_time, usage_place) VALUES (?, ?, ?, ?, ?);", (equipment_id, user_id, start_time, end_time, usage_place))
				executor("UPDATE equipments SET available = 0 WHERE id = ?;", (equipment_id,))
				code = random.randint(100000, 999999)
				reservation_id = executor("SELECT id FROM equipment_reservations WHERE equipment_id = ? AND user_id = ? AND start_time = ? AND end_time = ?;", (equipment_id, user_id, start_time, end_time))[0][0]
				codes[code] = {"expires": time.time() + 120, "equipment_id": equipment_id, "user_id": user_id, "type": "get"}
				scheduler.enter(120, 1, release_equipment, argument=(code, reservation_id))
				thread = threading.Thread(target=run_scheduler)
				thread.start()
				return json.dumps({"message": "Equipment reserved", "code": code}), 200
			else:
				return json.dumps({"error": "Equipment not available"}), 400
		return json.dumps({"error": "Equipment not found"}), 400
	except:
		return json.dumps({"error": "Invalid request"}), 400

def returnEquipmentCode(code):
	try:
		if code in codes:
			del codes[code]
	except:
		pass

@app.route("/api/equipments/<int:equipment_id>/return", methods=["POST"])
def returnEquipment(equipment_id):
	try:
		content = json.loads(request.data)
		if not checkToken(content["token"], False):
			return json.dumps({"error": "Access denied"}), 401
		user_id = executor("SELECT user_id FROM tokens WHERE token = ?;", (content['token'],))[0][0]

		reservation = executor("SELECT * FROM equipment_reservations WHERE equipment_id = ? ORDER BY id DESC LIMIT 1;", (equipment_id,))
		if len(reservation) > 0:
			if user_id != reservation[0][1]:
				return json.dumps({"error": "Access denied"}), 401

		equipment = executor("SELECT * FROM equipments WHERE id = ?;", (equipment_id,))
		if len(equipment) > 0:
			if equipment[0][6] == 0:
				code = random.randint(100000, 999999)
				codes[code] = {"expires": time.time() + 120, "equipment_id": equipment_id, "user_id": user_id, "type": "put"}
				scheduler.enter(120, 1, returnEquipmentCode, argument=(code))
				thread = threading.Thread(target=run_scheduler)
				thread.start()
				return json.dumps({"message": "Equipment return code", "code": code}), 200
			else:
				return json.dumps({"error": "Equipment not available for return"}), 400
		return json.dumps({"error": "Equipment not found"}), 400
	except:
		return json.dumps({"error": "Invalid request"}), 400
