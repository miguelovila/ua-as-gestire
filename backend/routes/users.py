import json, random, time, sched, threading
from flask import request
from __main__ import app, executor, checkToken


@app.route("/api/users/reservations", methods=["GET"]) 
def getReservationsByToken():
    try:
        if not checkToken(request.headers['token']):
            return json.dumps({"error": "Access denied"}), 401
        user_id = executor("SELECT id FROM users WHERE token = ?;", (request.headers['token'],))[0][0]
        room_reservations = executor("SELECT * FROM reservations WHERE user_id = ? ORDER BY start_time DESC LIMIT 100;", (user_id,))
        equipment_reservations = executor("SELECT * FROM equipment_reservations WHERE user_id = ? ORDER BY start_time DESC LIMIT 100;", (user_id,))
        
        reservations = room_reservations + equipment_reservations

        if len(reservations) > 0:
            return json.dumps({"reservations": reservations}), 200
        else:
            return json.dumps({"error": "No reservations found"}), 404
    except:
        return json.dumps({"error": "Invalid request"}), 400
    
