Capstone project:

1)Getting Started

a)installing dependencies:
-Python 3.7 or more.
-Virtual Enviornment.
-PIP Dependencies: pip install -r requirements.txt

b)To run the server:
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py
flask run --reload


The application has three different types of roles:
1)Manager:
can perform all the permissions.
2)employee:
can perform get:actors, post:actors, get:movies, post:movies
3)customer:
can perform get:actors, get:movies 



c)Endpoints:



GET /actors
General

gets all the actors
requires get:actors permission
Sample Request

https://capstone-xxx.herokuapp.com/actors
-----------------------------------------
POST /actors
General:
creates a new actor
requires post:actor permission

Sample Request:
https://capstone-xxx.herokuapp.com/actors
-----------------------------------------
PATCH /actors/{id}
General:
updates an actor info 
requires patch:actor permission

Sample Request:
https://capstone-xxx.herokuapp.com/actors/1
-------------------------------------------
DELETE /actors/{actor_id}
General

delete an actor
requires delete:actor permission
will also delete the mapping to the movie but will not delete the movie from the database
Sample Request:
https://capstone-xxx.herokuapp.com/actors/1
--------------------------------------------
GET /movies
General:
gets all the movies
requires get:movies permission
Sample Request:
https://capstone-xxx.herokuapp.com/movies
---------------------------------------------
POST /movies
General:
creates a new movie
requires post:movie permission
Sample Request:
https://capstone-xxx.herokuapp.com/actors
----------------------------------------------
PATCH /movie/{id}
General:
update movie info 
require patch:movie permission
Sample Request:
https://capstone-xxx.herokuapp.com/movies/1
-----------------------------------------------
DELETE /movies/{id}
General
deletes the movie
require delete:movie permission
Sample Request:
https://capstone-xxx.herokuapp.com/movies/1









