import sqlite3
from con import *
from cfg import *
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def helloWorld():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)