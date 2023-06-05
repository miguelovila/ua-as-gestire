from flask import request, send_file
import json
from __main__ import app

@app.route("/api/images/<path:path>")
def getImage(path):
    try:
        image_extension = path.split(".")[-1]
        return send_file(f"static/{path}", mimetype=f"image/{image_extension}")
    except:
        return json.dumps({"error": "Invalid request"}), 400