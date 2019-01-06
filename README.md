# iReporterAPI

The api endpoints to be integrated for the iReporter application of the Andela bootcamp challenge.

## Getting Stated
Install virtual environment using the requirements.txt.

** Get Red Flags
  Returns json data with a list of all red flags.

* **URL**

  /api/v1/red-flags

* **Method:**
  
  `GET`
  
* **Success Response:**
  
  On success, the status code returned is 200. The data returned is a list of red-flags.

  * **Code:** 200 <br />
    **Content:** `{ "status" : 200, "data" : [] }`
 
* **Error Response:**
  On failure, the following error responses are returned.
  * **Code:** 400  <br />
    **Content:** `{ "status" : 400, "error" : "Invalid request" }`
 
* **Sample Call:**

 `curl "https://api-ireporter-heroku.herokuapp.com/api/v1/red-flags"`

## Built With
* Python 3.7.1
* Flask
* Pytest
* Pylint