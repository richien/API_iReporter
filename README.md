# iReporterAPI

The api endpoints to be integrated for the iReporter application of the Andela bootcamp challenge. 

## Getting Stated
Install virtual environment using the requirements.txt.

**Get all red flags**
----
  Returns json data with a list of all red flags.

* **URL**

  /api/v1/red-flags

* **Method:**
  
  `GET`
  
* **Success Response:**
  
  On success, the status code returned is 200. The data returned is a list of red-flags.
  * **Code:** 200 SUCCESS <br />
    **Content:** `{ "status" : 200, "data" : [] }`
 
* **Error Response:**
  On failure, the following error responses are returned.
  * **Code:** 400 INVALID REQUEST  <br />
    **Content:** `{ "status" : 400, "error" : "Invalid request" }`
 
* **Sample Call:**

 `curl "https://api-ireporter-heroku.herokuapp.com/api/v1/red-flags"`

**Get a red flag**
----
  Returns json data about a single red flag.

* **URL**

  /api/v1/red-flags/:red_flag_id

* **Method:**

  `GET` 
  
*  **URL Params**

   **Required:**
 
   `red_flag_id=[integer]`

* **Data Params**

  `{"red_flag_id" : 234}`

* **Success Response:**
  On success, the status code returned is 200. The data returned is a dictionary the instance of red-flag with the red_flag_id.
  * **Code:** 200 SUCCESS <br />
    **Content:** `{ "status" : 200, "data" :  {} }`
 
* **Error Response:**

  * **Code:** 400 INVALID REQUEST <br />
    **Content:** `{ "status" : 400, "error" : "nvalid request - invalid red_flag_id supplied or key error in request body" }`

  
* **Sample Call:**

  `curl --header "Content-Type: application/json" --request GET --data '{"red_flag_id":2}' https://api-ireporter-heroku.herokuapp.com/api/v1/red-flags/2`

**Create a red flag**
----
  Creates a red flag and returns json data of the created red flag.

* **URL**

  /api/v1/red-flags

* **Method:**

  `POST`
  
*  **URL Params**
   
* **Data Params**

  `{ "createdBy" : 5000,"type" : "red-flag","location" : "33.92300, 44.9084551","status" : "draft", "images" : ["image_1.png", "image_2.jpg" ], "videos" : ["vid_1.mp4"], "comment" : "I almost got runover by a car that was dodging potholes!", "title": "Roads in poor condition"}`

* **Success Response:**
  On success, the status code returned is 201. Returns the id of the created red flag.
  * **Code:** 201 CREATED <br />
    **Content:** `{"data":{"id":21622,"message":"Created red-flag record"},"status":201}
`
 
* **Error Response:**

  * **Code:** 400 INVALID REQUEST <br />
    **Content:** `{"status" : 400, "error" : "Incident[Red-flag] - not created"}`

* **Sample Call:**

  `curl --header "Content-Type: application/json" --request POST --data '{ "createdBy" : 5000,"type" : "red-flag","location" : "33.92300, 44.9084551","status" : "draft", "images" : ["image_1.png", "image_2.jpg" ], "videos" : ["vid_1.mp4"], "comment" : "I almost got runover by a car that was dodging potholes!", "title": "Roads in poor condition"}' https://api-ireporter-heroku.herokuapp.com/api/v1/red-flags`
 
 **Edit a red flag's location**
----
  Edits the location of a red flag and returns json data of the edited red flag.

* **URL**

  /api/v1/red-flags/:red_flag_id/location

* **Method:**

  `PUT`
  
*  **URL Params**

   **Required:**
 
   `red_flag_id=[integer]`

* **Data Params**

  `{"red_flag_id" : 21622, "location" : "22.223, 33.990"}`

* **Success Response:**
  On success, the status code returned is 200. The data returned is a dictionary the instance of red-flag with the red_flag_id.
  * **Code:** 200 <br />
    **Content:** `{"data":{"content":{"comment":"I almost got runover by a car that was dodging potholes!","createdBy":5000,"createdOn":"12-12-2018","id":21622,"images":["image_1.png","image_2.jpg"],"location":"22.223, 33.990","status":"draft","title":"Roads in poor condition","type":"red-flag","videos":["vid_1.mp4"]},"id":2,"message":"Updated red-flag record's location"},"status":200}`
 
* **Error Response:**

  * **Code:** 400 <br />
    **Content:** `{"status" : 400, "error" : {"id" : 21622,
    "message" : "Failed to update red-flag record's location" }`

  OR

  * **Code:** 404 <br />
    **Content:** `{"status" : 404,"error" : { "id" : red_flag_id, "message" : "No record  with ID: 21622 was found" }`

* **Sample Call:**

  `curl --header "Content-Type: application/json" --request PUT --data '{"red_flag_id":21622, "location" : "32.223, 43.990"}' https://api-ireporter-heroku.herokuapp.com/api/v1/red-flags/2/location`

**Edit a red flag's comment**
----
  Edits the comment on a red flag and returns json data of the edited red flag.

* **URL**

  /api/v1/red-flags/:red_flag_id/comment

* **Method:**

  `PUT`
  
*  **URL Params**

   **Required:**
 
   `red_flag_id=[integer]`

* **Data Params**

  `{"red_flag_id" : 21622, "comment" : "Huge potholes..."}`

* **Success Response:**
  On success, the status code returned is 200. The data returned is a dictionary the instance of red-flag with the red_flag_id.
  * **Code:** 200 <br />
    **Content:** `{"data":{"content":{"comment":"Huge potholes...","createdBy":5000,"createdOn":"12-12-2018","id":2,"images":["image_1.png","image_2.jpg"],"location":"22.223, 33.990","status":"draft","title":"Roads in poor condition","type":"red-flag","videos":["vid_1.mp4"]},"id":21622,"message":"Updated red-flag record's location"},"status":200}`
 
* **Error Response:**

  * **Code:** 400 <br />
    **Content:** `{"status" : 400, "error" : {"id" : 21622,
    "message" : "Failed to update red-flag record's comment" }`

  OR

  * **Code:** 404 <br />
    **Content:** `{"status" : 404,"error" : { "id" : 21622, "message" : "No record  with ID: 21622 was found"}`

* **Sample Call:**

  `curl --header "Content-Type: application/json" --request PUT --data '{"red_flag_id":21622, "comment" : "Huge potholes..."}' https://api-ireporter-heroku.herokuapp.com/api/v1/red-flags/21622/comment`

**Delete a red flag**
----
  Deletes a red-flag record.

* **URL**

  /api/v1/red-flags/:red_flag_id

* **Method:**

  `DELETE` 
  
*  **URL Params**

   **Required:**
 
   `red_flag_id=[integer]`

* **Data Params**

  `{"red_flag_id" : 2}`

* **Success Response:**
  On success, the status code returned is 200. 
  * **Code:** 200 SUCCESS <br />
    **Content:** `{"data":{"id":2,"message":"Red-flag record deleted"},"status":200}
`
 
* **Error Response:**

  * **Code:** 400 INVALID REQUEST <br />
    **Content:** `{ "status" : 400, "error" : "nvalid request - invalid red_flag_id supplied or key error in request body" }`
    
    OR

  * **Code:** 404 <br />
    **Content:** `{"error":{"id":2,"message":"No record  with ID: 2 was found"},"status":404}`
    
* **Sample Call:**
  `curl --header "Content-Type: application/json" --request DELETE --data '{"red_flag_id":2}' https://api-ireporter-heroku.herokuapp.com/api/v1/red-flags/2`

## Built With
* Python 3.7.1
* Flask
* Pytest
