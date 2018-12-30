from flask import Flask, jsonify 

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = "esi5xKgrycPdTE5f9d1"

from api.routes.urls import Routes

Routes.fetch_urls(app)

@app.errorhandler(404)
def page_not_founddd(e):
    return jsonify({"status" : 404, "error" : "Unknown URL entered"})
