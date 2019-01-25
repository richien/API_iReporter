import os
from flask import Flask, jsonify 


app = Flask(__name__)

app_settings = os.getenv(
	'APP_SETTINGS',
	'config.DevelopmentConfig'
)
app.config.from_object(app_settings)

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
