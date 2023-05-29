from __main__ import app, executor
from flask import request
from cfg import *
import json
import time
from routes.equipments import codes

@app.route("/api/locker/<int:code>", methods=["POST"])
def getLocker(code):
	try:
		content = json.loads(request.data)
		if content["token"] != LOCKER_SECRET:
			return json.dumps({"error": "Access denied"}), 401

		if not (code in codes):
			return json.dumps({"error": "Invalid code"}), 400

		code_data = codes[code]
		locker = executor("SELECT * FROM equipments WHERE id = ?;", (code_data["equipment_id"],))[0][4]
		del codes[code]

		if code_data["type"] == "get":
			executor("UPDATE equipments SET available = 0 WHERE id = ?;", (code_data["equipment_id"],))
		if code_data["type"] == "put":
			executor("UPDATE equipments SET available = 1 WHERE id = ?;", (code_data["equipment_id"],))

		return {
			"type": code_data["type"],
			"locker": locker
		}, 200
	except:
		return json.dumps({"error": "Invalid request"}), 400