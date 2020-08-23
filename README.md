# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies
## Motivation
the motivation is to help  the casting company through easing the procedures to achieve it's goals
### hosting (APP URL)
The app is  hosted at https://casting-agency1996.herokuapp.com/
### Authentication (`/authorize`)
the base url will have a link for signing up (note: the roles and permission are added by the admin and there is no defaul role to new registers). here is the link for the login/signup page 
- https://noisy-pond-1849.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=7NCGYZ6utWFtYbuGU2bQ3U2H8fbs3Nrb&redirect_uri=https://casting-agency1996.herokuapp.com/callback
#### mock accounts:
 - Role: no role assigned: email: rachael97@qacmemphis.com pw: 3432stnrM
 - Role: Casting Assistant: email: michial7@gannoyingl.com  pw: rst23ST2232
 - Role: Casting Director: email: rosalbaa4@gannoyingl.com   pw: rosalbaa4@gannoyingl.com
 - Role: Executive Producer: email: tess5@kweekendci.com    pw: 165svbX5

use the bearer token  (access_token) in the callback url. For API calls for cURL commands check [API cURL](https://documenter.getpostman.com/view/11760714/T1LV94Nj?version=latest) or import the the postman-collection `Casting-Agency.postman_collection.json` in postman and update the tokens there
### RBAC tokens 
are in the postman collection  `Casting-Agency.postman_collection.json`

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory and running:

```bash
$ pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in `app.py` and can reference `models.py`.
- [jose](https://pypi.org/project/python-jose/) The JavaScript Object Signing and Encryption (JOSE) technologies, used to handle JWT decrypton and verification in `auth.py`

&nbsp;

## Local Development
### Auth0 
there needs to be an auth0 application and api to handle user data and to assign roles and provide tokens with the following roles and permissions
Roles:
- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and 
Add or delete an actor from the database
Modify actors or movies
- Executive Producer
   - All permissions a Casting Director has and…
Add or delete a movie from the database

for more information check out [heroku auth0 addon](https://devcenter.heroku.com/articles/auth0) and [auth0 Documentation](https://auth0.com/docs/).

or you can use the mock emails in the already configured app

&nbsp;
### Database Setup

With Postgres running, create a database.  in terminal run.
```bash
$ dropdb <database name>
$ createdb <database name>
```
run to setup environment variables e.g.` DATABASE_URL`, you should change the DATABASE_URL with the new database name in setup.sh
```bash
$ source setup.sh
```
and setup the models(tables)
```
$ python3 manage.py db init
$ python3 manage.py db migrate
$ python3 manage.py db upgrade
```
&nbsp;

#### `or` 
run this for a quick setup after setting up the database (you need the above steps to be able to modify models and migrate for local development)
```bash
$ psql <database name>  < capstone.psql 
```

&nbsp;

(optional) From the files in the misc folder provided you can make dummy database entries.(the server needs to be running first) 
```bash
$ source misc/actornames.sh
$ source misc/movienames.sh
```

### Running the server
\
from withing the `root` directory first ensure you are working using your created virtual environment. first ensure that the environment variables are setup in `setup.sh` change it as appropriate.
To run the server execute:

```bash
$ python3 app.py
```
## Testing
- Unit-test: The tests is in `test_app.py`. There is a flag/parameter to the create_app() function `create_app(test_config=None)`  so when unit testing  it sets `test_config` with value 'unittest' i.g. `create_app('unittest')`  and pass it as an argument to i.g. `@requires_auth(test_config, permission='get:actors')`  for a simple if statement in `auth.py` to test for token validity or not. This way we can respect the unit-test concept and do no proprietary cryptographic algorithm like generating a token in code and such, to test run:
```bash
$ python3 test_app.py
```
- RBAC(Role Based Acess Control) test: there is a postman collection for API testing in file: `Casting-Agency.postman_collection.json` you can import it into postman. it's  extensive and covers almost every thing



---
## API reference
API documentation is in it's own markdown file here
[API Documentation](/API_Documentation.md)

---
## Deployment
you can deploy on heroku 
for more info [heroku deployment](https://devcenter.heroku.com/articles/python-support)

---
## Authors
I

---

## Acknowledgemenet
stackoverflow, the knowledge hub 
and the FSND slack community
