# Weather_API_Flask
An app, to give weather forecast for different cities

## Functions
Uses Open Weather API to get weather report for a given city and store data in database.
For a particular city gets weather report each day at 5:00 PM, that represents the weather of a city for that day.
Contains a scheduler logic, which makes sure to record weather report each day at 17:00 Hrs.


### APIs:
#### City API:
GET: get the list of all cities in the system
DELETE: delete a city
POST: add a new city into the system. 

#### Weather API:
GET: get weather of all cities of last 5 days.
add filter functionality to the api, where you should be able to filter by name of city, or date 
example: http://127.0.0.1:5000/weather/filter?city=Bangalore&date=2017-12-13

(Because the workstation is manipulative, we can delete or update weather report also)
DELETE: delete a particular weather report(by id)
UPDATE: update a particular weather report(by id)

No front end, APIs running in Postman.
All APIs are RESTful
