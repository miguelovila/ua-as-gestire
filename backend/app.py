from cfg import *
from database.con import *
from flask import Flask

app = Flask(__name__)

from routes.auth import *
from routes.rooms import *
from routes.equipments import *
    
if __name__ == '__main__':
    initializeDatabase()
    fillSampleUserData()
    fillSampleRoomData()
    fillSampleEquipmentData()
    app.run(host='0.0.0.0', port=5000)