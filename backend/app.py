from cfg import *
from database.con import *
from flask import Flask, jsonify 

app = Flask(__name__)

from routes.auth import *
from routes.rooms import *
from routes.equipments import *

@app.route('/')
def index():
    return jsonify({'message': 'Hello World!'})

if __name__ == '__main__':
    initializeDatabase()
    fillSampleUserData()
    fillSampleRoomData()
    fillSampleEquipmentData()
    app.run(host='0.0.0.0', port=5000)
