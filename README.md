# Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create a database and setup the models(tables).  in terminal run.
```bash
createdb <database name>
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
From the  files in the misc folder provided you can make dummy database entry. 
```bash
source misc/actornames.sh
source misc/movienames.sh
```

## Running the server

from withing the `root` directory first ensure you are working using your created virtual environment. first ensure that the environment varables are setup in the `setup.sh` change it as appropriate.
To run the server, execute:

```bash
source setup.sh
```
---
## API reference
### Getting Started
 - Base URL: runs Locally and is not hosted as a base URL. the backend app is hosted at http://0.0.0.0:8080 as a proxy in the frontend configurations 
 - Authentication: Doesn't require authentication or API keys
### Error Handling
errors are returned as a json objects in the following format:
```JSON
{
    "success": False,
    "error": 404,
    "message": "resource not found",
}
```
the API will return four error types when requests fail:
 - 400: Bad Request
 - 404: Resource Not Found
 - 422: Not Processable
 - 500: Internal server Error 
 ### Endpoints
 - GET /actors
 - GET /movies
 - POST /actors
 - POST /movies
 - DELETE /actors/`<actor_id>`
 - DELETE /movies/`<movie_id>`
 - PATCH /actors/`<actor_id>`
 - PATCH /movies/`<movie_id>`

#### GET /actors
 - Fetches the actor page, 5 actors per page. if page in the url is ommited it gets the first page
 - Request Argument: None
 - Returns: a json object that has a list of 5 or less actor objects, and the success status
```JSON
{
  "actors": [
    {
      "DOB": "Sat, 13 Nov 1971 00:00:00 GMT",
      "gender": "female",
      "id": 1,
      "name": "Actor1"
    }, 
    .
    .
    .
    {
      "DOB": "Sat, 10 Jan 1959 00:00:00 GMT",
      "gender": "other",
      "id": 5,
      "name": "Actor5"
    }
  ],
  "success": true
}
```
#### GET /movies
 - Fetches the movie page, 5 movies per page. if page in the url is ommited it gets the first page
 - Request Argument: None
 - Returns: a json object that has a list of 5 or less movie objects, and the success status
```JSON
{
  "movies": [
    {
      "id": 1,
      "release date": "Sun, 05 May 2019 00:00:00 GMT",
      "title": "Jojo Rabit"
    },
    .
    .
    .
    {
      "id": 5,
      "release date": "Tue, 02 May 1995 00:00:00 GMT",
      "title": "movie5"
    }
  ],
  "success": true
}
```
#### POST /actors
- Create a new actor 
- Request Arguments: actor's name, actors date of birth, actor's gender
```JSON
{
    "name": "Huda Sha'arawi",
    "DOB": "1965-3-16",
    "gender": "female"
}
```
- Return: a json object with an actor object
```JSON
{
  "actor": {
    "DOB": "Tue, 16 Mar 1965 00:00:00 GMT",
    "gender": "female",
    "id": 131,
    "name": "Huda Sha'arawi"
  },
  "success": true
}
```
#### POST /movies
- Create a new movie
- Request Arguments: movie's title, movie's release_date
```JSON
{
    "title": "Schindler's List",
    "release_date": "1993-11-30"
}
```
- Return: a json object with an movie object
```JSON
{
  "movie": {
    "id": 141,
    "release date": "Tue, 30 Nov 1993 00:00:00 GMT",
    "title": "Schindler's List"
  },
  "success": true
}
```
#### DELETE /actors/`<actor_id>`
- deletes an actor
- Request argument: None
- Returns:  a json object with success status, and deleted actor id
```JSON
{
"success": true,
"deleted actor id": <actor_id>
}
```
#### DELETE /movies/`<movie_id>`
- deletes a movie
- Request argument: None
- Returns: a json object with success status, and deleted movie id
```JSON
{
"success": true,
"deleted movie id": <movie_id>
}
```
#### PATCH /actors/`<actor_id>`
- update the values of actor's object attributes
- Request argument: one or more new values for the attributes of the actor object to be modified
```JSON
{
    "name": "Rosavelt"
}
```
- Returns: the modified actor object and the success status
```JSON
{
  "actor": {
    "DOB": "Mon, 26 May 1902 00:00:00 GMT",
    "gender": "female",
    "id": 44,
    "name": "Rosavelt"
  },
  "success": true
}
```
#### PATCH /movies/`<movie_id>`
- update the values of movie's object attributes
- Request argument: one or more new values for the attributes of the movie object to be modified
```JSON
{
    "title": "Appolo 13"
}
```
- Returns: the modified movie object and the success status
```JSON
{
  "movie": {
    "id": 2,
    "release date": "Sat, 27 May 1995 00:00:00 GMT",
    "title": "Appolo 13"
  },
  "success": true
}
```