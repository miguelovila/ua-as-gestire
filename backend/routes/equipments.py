import json
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


@app.route("/api/equipments/reserve", methods=["POST"])
def reserveEquipment():
	try:
		content = json.loads(request.data)
		if not checkToken(content["token"], False):
			return json.dumps({"error": "Access denied"}), 401

		equipment_id = content["equipment_id"]
		user_id = content["user_id"]
		start_time = content["start_time"]
		end_time = content["end_time"]

		executor(
			"INSERT INTO reservations (equipment_id, user_id, start_time, end_time) VALUES (?, ?, ?, ?);",
			(equipment_id, user_id, start_time, end_time),
		)

		return json.dumps({"success": True}), 200
	except:
		return json.dumps({"error": "Invalid request"}), 400
