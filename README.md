# Weather API: Flask
[![Build Status](https://travis-ci.org/partoftheorigin/clima.svg?branch=master)](https://travis-ci.org/partoftheorigin/clima) [![Coverage Status](https://coveralls.io/repos/github/partoftheorigin/clima/badge.svg?branch=master)](https://coveralls.io/github/partoftheorigin/clima?branch=master)

An app, to give weather forecast for different cities

## Functions
* Uses Open Weather API to get weather report for a given city and store data in database.
* For a particular city gets weather report each day at 5:00 PM, that represents the weather of a city for that day.
* Contains a scheduler logic, which makes sure to record weather report each day at 17:00 Hrs.


## APIs:
#### City API:
1. GET: get the list of all cities in the system
2. DELETE: delete a city
3. POST: add a new city into the system. 

#### Weather API:
1. GET: get weather of all cities of last 5 days.
add filter functionality to the api, where you should be able to filter by name of city, or date 
example: http://0.0.0.0:5000/weather/filter?city=Bangalore&date=2017-12-13
2. DELETE: delete a particular weather report(by id)
3. UPDATE: update a particular weather report(by id)

*No front end, APIs running in Postman.*

*All APIs are RESTful*

*Used an ORM : SQLALCHEMY instead of direct database queries.*
