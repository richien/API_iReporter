import os
from flask import Flask, jsonify 
from flask-cors import CORS
from dotenv import load_dotenv


app = Flask(__name__)

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app_settings = os.getenv('APP_SETTINGS')

app.config.from_object(app_settings)
CORS(app)

from api.routes.urls import Routes

Routes.fetch_urls(app)

@app.errorhandler(404)
def page_not_found(e):
    valid_urls = { 'urls' : [
        ['/api/v1/red-flags', 'GET'],
        ['/api/v1/red-flags/<int:red_flag_id>', 'GET', {'body' : {'red_flag_id': 'int'}}],
        ['/api/v1/red-flags', 'POST', {'body': {
			    	  "createdBy" : "int",
			          "type" : "string",
			          "location" : "int, int",
			          "status" : "string",
			          "images" : "list",
			          "videos" : "list",
			          "comment" : "string",
			          "title": "string"
			          }}],
        ['/api/v1/red-flags/<int:red_flag_id>/location', 'PATCH', {'body' : {'red_flag_id': 'int'}}],
        ['/api/v1/red-flags/<int:red_flag_id>/comment', 'PATCH', {'body' : {'red_flag_id': 'int'}}],
        ['/api/v1/red-flags/<int:red_flag_id>', 'DELETE', {'body' : {'red_flag_id': 'int'}}],
        ['/api/v1/auth/signup', 'POST', {'body': {
        			"firstname" : "string",
            		"lastname" : "string",
            		"othernames" : "string",
            		"email" : "example@email.com",
            		"phonenumber" : "string",
            		"username" : "string",
            		"password" : "string - Atleast 8 characters long"
        			}}],
        ['/api/v1/auth/login', 'POST', {'body': {
        			'username': 'String',
        			'password': 'Enter user password.',
        			'Options' : "Can use email instead of username, to log in"
        		}}],
        ['/api/v1/users', 'GET'],
        ['/api/v1/users/<int:user_id>', 'GET', {'body': {'user_id': 'int'}}]
        ]
    }

    return jsonify({"status" : 404, "error" : str(e), "USAGE" : valid_urls}), 404
