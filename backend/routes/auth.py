import bcrypt, json, time
from flask import request
from __main__ import app, executor

@app.route('/api/auth', methods=['POST'])
def authenticate():
    try:
        content = json.loads(request.data)
        email = content['email']
        password = content['password']
        user = executor("SELECT * FROM users WHERE email = ?;", (email,))
        if len(user) > 0:
            user = user[0]
            if bcrypt.checkpw(password.encode('utf-8'), user[4]):
                token = bcrypt.hashpw((str(user[0]) + str(time.time())).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                executor("INSERT INTO tokens (token, expiration, user_id) VALUES (?, ?, ?);", (token, int(time.time()) + 600, user[0]))
                return json.dumps(
                    {
                      "mec": user[1],
                      "name": user[2],
                      "email": user[3],
                      "profile_picture": user[5],
                      "token": token
                    }
                ), 200
            else:
                return json.dumps(
                    {
                      "error": "Invalid username or password"
                    }
                ), 401
        else:
            return json.dumps(
                {
                  "error": "Invalid username or password"
                }
            ), 401
    except:
        return json.dumps(
            {
              "error": "Invalid request"
            }
        ), 401
    
@app.route('/api/auth/check', methods=['POST'])
def checkToken(token = None, external = True):
    try:
        if external:
            content = json.loads(request.data)
            token = content['token']
        db_token = executor("SELECT * FROM tokens WHERE token = ?;", (token,))
        if len(db_token) > 0:
            db_token = db_token[0]
            if int(time.time()) < db_token[2]:
                executor("UPDATE tokens SET expiration = ? WHERE id = ?;", (int(time.time()) + 600, db_token[0]))
                if external:
                    return json.dumps(
                        {
                          "valid": True
                        }
                    ), 200
                return True
            else:
                executor("DELETE FROM tokens WHERE id = ?;", (db_token[0],))
                if external:
                    return json.dumps(
                        {
                          "valid": False
                        }
                    ), 401
                return False
        else:
            if external:
                return json.dumps(
                    {
                      "valid": False
                    }
                ), 401
            return False
    except:
        if external:
            return json.dumps(
                {
                  "error": "Invalid request"
                }
            ), 401
        return False