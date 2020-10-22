# ManAudio-API
Flask API to manipulate and process audio that make use of JWT authentication using Redis, RQ and more

## Getting Started

This Project uses **Pipenv** for environment and dependency management.
so it is a ***prerequisit***.<br/> 
To run the API in your local enviroment:

1. clone the project and install the pipenv dependencies.
    1. `git clone < repo link > && cd ManAudio-API` 
    2. `pipenv install` to install dependencies 
    3. `pipenv shell` to activate the virtual environment
2. in a termial run ``flask rq worker`` in the project directory to spin up a worker that takes the jobs from your redis/rq queue to work on them.
3. in other terminal window start the flask API.
    1. `export FLASK_APP=run`
    2. `export FLASK_ENV=development`
    3. `flask run`

Otherwise you may install the dependencies below using something else
          

### Dependencies

What things you need to install the software and how to install them

```
flask
psycopg2-binary
flask-sqlalchemy
flask-migrate
flask-bcrypt
pydub
numpy
pyjwt
flask-rq2
```

## Running the tests

This project uses **Pytest** you can find the tests in the *tests* directory

to run all the tests you can use the `pytest` command in the project directory

### code style 

this project uses **PEP8** code style guide
with the aid of *autopep8* 



## Resources

### User
user model had many attributes like username, email, password hashed using *bcrypt* and methods to generate and decode / verify JWT tokens using *pyjwt*

#### Endpoints 
* `POST /auth/register` to register user and return an authentication JWT token
* `POST /auth/login` to login via email and password and return an authentication JWT 
* `GET /auth/status` to get the user info and status must have a valid JWT in Authorization Brearer Header
* `POST /auth/logout` to logout and blacklist the associated authentication JWT 

### Audio
audio file that's sent to the api and get processed
#### Endpoints 
* `POST /audio/bass-boost` to post the audio file to the API to process it and bass-boost it 
* `GET /audio/bass-boost` to get resulting file of the bass-boosting process if the process is finished otherwise you'll get JSON message ***processing***

### *Authentication*
any endpoint of audio can be protected with the @auth_required decorator that I made in the app/auth/decorators.py file

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

