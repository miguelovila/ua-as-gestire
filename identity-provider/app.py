import sqlite3
from con import *
from cfg import *
from flask import Flask, current_app, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/idp/profile/saml2/redirect/sso', methods=['GET'])
def loginPage():
    return render_template('login.html')

if __name__ == '__main__':
    initializeDatabase()
    fillSampleData()
    app.run(host='0.0.0.0', port=10222)