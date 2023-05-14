import sqlite3
from con import *
from cfg import *
from flask import Flask, current_app

app = Flask(__name__)

@app.route('/idp/profile/saml2/redirect/sso', methods=['GET', 'POST'])
def welcome():
    return current_app.send_static_file('index.html')

if __name__ == '__main__':
    initializeDatabase()
    fillSampleData()
    app.run(host='0.0.0.0', port=10222)