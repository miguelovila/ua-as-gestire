import json
from flask import request
from __main__ import app, executor, checkToken

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