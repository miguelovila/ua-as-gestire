import sqlite3
from con import *
from cfg import *
from flask import Flask, current_app, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/idp/profile/saml2/redirect/sso', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        username = request.form["gestire_username"]
        password = request.form["gestire_password"]
        if len(executor("SELECT * FROM users WHERE email = ? AND password = ?;", (username, password))) > 0:
            return redirect('https://google.com')
        else:
            return render_template('login.html', error="Invalid credentials.")

    return render_template('login.html')

if __name__ == '__main__':
    initializeDatabase()
    fillSampleData()
    app.run(host='0.0.0.0', port=10222)