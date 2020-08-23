## API reference
### Getting Started
 - Base URL: runs Locally at http://0.0.0.0:8080 and is hosted at https://casting-agency1996.herokuapp.com
 - Authentication: jwt authenticaton Auth0 access_token (Bearer Token), the base url `/` will direct you to a page were you can login or sign up 
 - for cURL requests for this API check [API documentation](https://documenter.getpostman.com/view/11760714/T1LV94Nj?version=latest)
### Error Handling
errors are returned as a json objects in the following format:
```JSON
{
    "success": false,
    "error": 404,
    "message": "resource not found",
}
```
Common error types the API will return  error types when requests fail:
 - 400: Bad Request
 - 404: Resource Not Found
 - 422: Not Processable
 - 500: Internal server Error 
 - 401 authentication problem (something is wrong with the bearer token)
 - 403 Forbidden (don't have permission to do this action)
 ### Endpoints
 - GET /actors
 - GET /movies
 - POST /actors
 - POST /movies
 - DELETE /actors/`<actor_id>`
 - DELETE /movies/`<movie_id>`
 - PATCH /actors/`<actor_id>`
 - PATCH /movies/`<movie_id>`
 - GET /actors/`<actor_id>`/movies
 - GET /movies/`<movie_id>`/actors
 - POST /actors/`<actor_id>`/movies
 - POST /movies/`<movie_id>`/actors

#### GET /actors
 - Fetches the actor page, 5 actors per page. if page in the url is ommited it gets the first page
 - Permission: get:actors
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
 - Permission: get:movies
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
 - Permission: post:actors
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
- Permission: post:movies
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
- Permission: delete:actors
- Request argument: None
- Returns:  a json object with success status, and deleted actor id
```JSON
{
"success": true,
"deleted actor id": "<actor_id>"
}
```
#### DELETE /movies/`<movie_id>`
- deletes a movie
- Permission: delete:movies
- Request argument: None
- Returns: a json object with success status, and deleted movie id
```JSON
{
"success": true,
"deleted movie id": "<movie_id>"
}
```
#### PATCH /actors/`<actor_id>`
- update the values of actor's object attributes
- Permission: patch:actors
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
- Permission: patch:movies
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

#### GET /actors/`<actor_id>`/movies
- get the list of movies the actor is acting in
- Permission: get:actors
- Request arguments: None
- Returns: a JSON object with the success status, actor id and movie list
```json
{
  "actor": 7,
  "movies": [
    {
      "id": 1,
      "release date": "Thu, 12 Apr 1990 00:00:00 GMT",
      "title": "the test"
    },
    {
      "id": 3,
      "release date": "Thu, 12 Apr 1990 00:00:00 GMT",
      "title": "spirited away"
    }
  ],
  "success": true
}
```
#### GET /movies/`<movie_id>`/actors
- get the list of actors acting in the movies
- Permission: get:movies
- Request arguments: none
- Returns: a JSON object with the success status, movie id and actors list
```json
{
  "actors": [
    {
      "DOB": "Tue, 16 Mar 1965 00:00:00 GMT",
      "gender": "female",
      "id": 1,
      "name": "Rosavelt"
    },
    {
      "DOB": "Tue, 16 Mar 1965 00:00:00 GMT",
      "gender": "female",
      "id": 7,
      "name": "testy mctest"
    }
  ],
  "movie": 3,
  "success": true
}
```
#### POST /actors/`<actor_id>`/movies
- updates the movies the actor is acting in (overwritten)
- Permission: patch:actors
- Request argument: a list of `id`s of the movies 
```json
{
    "movies": [1, 3]
}
```
- Returns: a JSON object with the success flag
```json
{
  "success": true
}
```
#### POST /movies/`<movie_id>`/actors
- update the actors list assigned to that movie (overwritten)
- Permission: patch:movies
- Request Arguments: a list of `id`s of the actors 
```json
{
    "actors": [3, 433, 533, 5445]
}
```
- Returns: a JSON object with the success flag
```json
{
  "success": true
}
```