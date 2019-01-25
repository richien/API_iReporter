# iReporterAPI
[![Build Status](https://travis-ci.com/richien/API_iReporter.svg?branch=develop)](https://travis-ci.com/richien/API_iReporter)
[![Coverage Status](https://coveralls.io/repos/github/richien/API_iReporter/badge.svg?branch=develop)](https://coveralls.io/github/richien/API_iReporter?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/a6ce65585611a0f514e6/maintainability)](https://codeclimate.com/github/richien/API_iReporter/maintainability)

The api endpoints for the iReporter application of the Andela bootcamp challenge 15. 
It can be accessed on [Heroku](https://irepo-api.herokuapp.com/api/v1/interventions).

## Getting Stated

* Clone this repository using 

    ```https://github.com/richien/API_iReporter.git```

* Then change directory to the new folder

    ```cd <DirectoryName>```

* Create a virtual environment

    ```pip install pipenv```

* Activate the virtual environment

    ```pipenv shell```

* Install all the dependencies

    ```pip install -r requirements.txt```

* Database Installation
    Once the local Postgres Server is running, create two 
    new database from psql
    
    ```postgres=# CREATE DATABASE dev_ireporter_api```
    ```postgres=# CREATE DATABASE test_ireporter_api```

    Before applying database migrations, update the config 
    file config.py

    ```database_name = 'dev_ireporter_api'```

    Create the Incidents and Users table in the terminal

     ```python -m api.model.database.schema```

    Set up the environment variables in the termnal

    ```export APP_SETTINGS="config.DevelopmentConfig"```
    ```export SECRETKEY=your-secret-key```
    ```export COVERALLS_REPO_TOKEN=coveralls-repo-token```
    ```export DATABASE_URI=<you postres uri>```
    ```export APP_SETTINGS="config.DevelopmentConfig"```
    ```export FLASK_ENV=development```
    ```export FLASK_NAME=app```



* Running the app

   From within the virtual environment, set the application name and environment and then start the developement server.
   
   ```flask run```

**Running tests**

From within the virtual environment, you can run the test code and view the test coverage for each of the unit tests.

* Run test with coverage  with the following command

    ```python -m pytest --cov```

**Supported Routes**

Read the API-DOCS.md file for information about supported routes

## Built With
* Python 3.7.1
* Flask 1.0.2
* pytest-cov-2.6.0
* pylint
* PostreSQL-11.1

### AUTHOR 
* [Geoffrey Willis Barugahare](https://github.com/richien)
