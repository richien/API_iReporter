from flask import Flask 

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = "esi5xKgrycPdTE5f9d1"

from api.routes.urls import Routes
Routes.fetch_urls(app)