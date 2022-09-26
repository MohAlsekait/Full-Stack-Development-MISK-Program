import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db
from auth import *




def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
      return response

  def paginated(request, selection):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 10
      end = start + 10

      a = [x.format() for x in selection]
      current_paginated = b[start:end]

      return current_paginated

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
      get_actors = Actor.query.all()
      if len(get_actors) == 0:
          abort(404)
      paginated_actors = paginated(request, get_actors)

      return jsonify({
          'success': True,
          'actors': [actor.format() for actor in paginated_actors]
      }), 200

  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, actor_id):
      try:
          actor = Actor.query.get(actor_id)

          actor.delete()

          return jsonify({
              'success': True,
              'deleted': actor_id,
          })
      except:
          abort(422)

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actors(payload):
      try:
          body = request.get_json()
          if body is None:
              abort(400)

          act_name = body.get('name', None)
          act_age = body.get('age', None)
          act_gender = body.get('gender', 'Other')
          actor = (Actor(name=act_name,age=act_age,gender=act_gender))
          actor.insert()
          return jsonify({
            'success': True,
            'created': actor.id,
         })
      except:
       abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth("patch:actors")
  def update_actor(payload, actor_id):
      try:
          body = request.get_json()
          if body is None:
              abort(400)
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
          act_name = body.get('name', actor.name)
          act_age = body.get('age', actor.age)
          act_gender = body.get('gender', actor.gender)

          actor.name = act_name
          actor.age = act_age
          actor.gender = act_gender

          actor.update()

          return jsonify({
              'success': True,
              'updated': actor.id,
              'actor': actor.format()
          })
      except:
          abort(422)

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(token):
      movies = Movie.query.all()
      movie_paginated = paginated(request, movies)
      if len(movie_paginated) == 0:
          abort(404)
      return jsonify({
          'success': True,
          'movies': movie_paginated
      })

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def create_movie(token):
      body = request.get_json()

      if not body:
          abort(400)

      title = body.get('title', None)
      release_date = body.get('release_date', None)
      movie = Movie(title=title, release_date=release_date)
      movie.insert()
      return jsonify(
          {'success': True}
      )

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(token, id):
      try:
        body = request.get_json()
        if not body:
            abort(400)
        movie = Movie.query.get(id)
        if not movie:
            abort(404)

        title = body.get('title', movie.title)
        release_date = body.get('release_date', movie.release_date)
        movie.title = title
        movie.release_date = release_date
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })
      except:
          abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(token, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
          movie.delete()
          return jsonify({
              'success': True,
              'deleted': movie_id
          }), 200
      except Exception:
          abort(422)

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": get_error_message(error, "unprocessable")
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": get_error_message(error, "bad request")
      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": get_error_message(error, "resource not found")
      }), 404

  @app.errorhandler(AuthError)
  def authentification_failed(AuthError):
      return jsonify({
          "success": False,
          "error": AuthError.status_code,
          "message": AuthError.error['description']
      }), AuthError.status_code

  return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)