from flask import Flask 

app = Flask(__name__)

from api.routes.urls import Routes
Routes.fetch_urls(app)