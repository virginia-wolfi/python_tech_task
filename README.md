# RESTful API application for managing a task list (ToDo list) 

Service functionality:
+ user registration
+ user login
+ user logout
+ display a profile (only by owner)
+ delete a profile (only by owner, with all tasks created by user)
+ create a task
+ delete a task (only by owner)
+ update a task (only by owner)
+ display a task 
+ display tasks with pagination and filters

API endpoints:
+ /registration POST 
+ /login POST
+ /logout POST
+ /profile GET
+ /profile DELETE
+ /tasks/create POST
+ /tasks/\<int:task_id\> DELETE 
+ /tasks/\<int:task_id\> PATCH 
+ /tasks/\<int:task_id\> GET
+ /tasks GET, query string params: page: int, per_page: int, title: string, username: string, status: string, description: string


# Backend
The backend is based on Flask framework. 
# Database
PostgreSQL was used as the database to store data. Flask-SQLAlchemy was used as ORM.

# Authentication
User authentication and authorization implemented using JWT.
After the user sends login data to the /login endpoint, a response is received in format 
~~~
{"access_token": "<JWT>"}
~~~
When the client wants to access a protected route, the user agent should send the JWT in the Authorization HTTP header using the Bearer schema. 
The content of Authorization header should look like
~~~
Authorization: Bearer <JWT>
~~~
# Application installation
```
git clone https://github.com/virginia-wolfi/python_tech_task.git
cd python_tech_task
python3 -m venv env
./env/bin/activate
pip install -r requirements-dev.txt
```
# Configuration
Create .env file in the root folder and fill it according to the .env.example file. 
This is required to run the application, test it, and build a Docker image.
Create databases for development and testing and fill DEVELOPMENT_DATABASE_URL and TESTING_DATABASE_URL in .env file in format
~~~
postgresql://username:password@host:port/database
~~~
# Service start

First create tables with command
```
$ flask db create
```
to delete tables run
```
$ flask db delete
```
to start server run from the terminal in root directory
```
$ flask run
```

visit http://127.0.0.1:5000/ in a browser. You should see the site generated with Swagger. You can send requests with ready payload JSON schemas

# Docker

to build Docker image and start container run
```
$ docker compose up -d
$ docker exec to_do_app flask db create
```
now visit http://127.0.0.1:5000/ in a browser. You can also manage database in pgadmin at http://127.0.0.1:5555/.
Note that all the environment variables the docker container uses are in the docker-compose.yaml.
You'll need these to log in pgadmin site:
~~~
PGADMIN_DEFAULT_EMAIL=myemail@gmail.com
PGADMIN_DEFAULT_PASSWORD=mypassword
~~~
and these to add server:

~~~
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=to_do_list
~~~
server name is db

# Running Tests
~~~
$ python3 -m pytest
~~~