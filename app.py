import os
from flask import Flask, request, abort, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth, AUTH0_AUTHORIZE_URL

# AUTH0_AUTHORIZE_URL = "https://noisy-pond-1849.us.auth0.com/authorize?
# audience=casting-agency&response_type=token&client_id=7NCGYZ6utWFtYbuGU2bQ3U2H8fbs3Nrb
# &redirect_uri=https://casting-agency1996.herokuapp.com/callback"

# pagination
items_PER_PAGE = 5


def paginate_items(request, selection):
    # i copied this function from the lesson\
    '''takes in request and a list of db items objects,
        format them, then return a page of items'''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * items_PER_PAGE
    end = start + items_PER_PAGE
    items = [item.format() for item in selection] if selection else []
    current_items = items[start:end]
    return current_items


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.route("/")
    def index():
        return render_template("signin.html",
                               AUTH0_AUTHORIZE_URL=AUTH0_AUTHORIZE_URL)

    @app.route("/callback")
    def callback_redirector():
        return render_template("index.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return render_template("logout.html")

# ---------------------------------------
#                API
# ---------------------------------------
    @app.route('/actors')
    @requires_auth(test_config, permission='get:actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        current_selection = paginate_items(request, actors)
        if len(current_selection) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "actors": current_selection,
            "total number of actors": len(actors)
        }), 200

    @app.route('/movies')
    @requires_auth(test_config, permission='get:movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        current_selection = paginate_items(request, movies)
        if len(current_selection) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "movies": current_selection,
            "total number of movies": len(movies)
        }), 200

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(test_config, permission="delete:actors")
    def delete_actor(id):
        actor = Actor.query.get_or_404(id)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "deleted actor id": id
            }), 200
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(test_config, permission="delete:movies")
    def delete_movie(id):
        movie = Movie.query.get_or_404(id)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted movie id": id
            }), 200
        except Exception as e:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth(test_config, permission="post:actors")
    def add_actors():
        try:
            body = request.get_json()
            actor = Actor(name=body['name'],
                          dob=body['DOB'], gender=body.get('gender'))
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth(test_config, permission="post:movies")
    def add_movies():
        try:
            body = request.get_json()
            movie = Movie(title=body['title'],
                          release_date=body.get('release_date'))
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format(),
            })
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(test_config, permission="patch:actors")
    def update_actors(id):
        actor = Actor.query.get_or_404(id)
        try:
            body = request.get_json()
            # if it's body.get('attribute'') is none it
            # defaults to the original value
            # but if it has attribute -as a proberty of python or-
            #  it chooses the first one if both are true
            actor.name = body.get('name', None) or actor.name
            actor.dob = body.get('DOB', None) or actor.dob
            actor.gender = body.get('gender', None) or actor.gender
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(test_config, permission="patch:movies")
    def update_movies(id):
        movie = Movie.query.get_or_404(id)
        try:
            body = request.get_json()
            # if it's body.get('attribute'') is none it defaults to
            #  the original value
            # but if it has attribute -as a proberty of python or-
            # it chooses the first one if both are true
            movie.title = body.get('title', None) or movie.title
            movie.release_date = body.get(
                'release_date', None) or movie.release_date
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 200

        except Exception as e:
            abort(422)

    # to get or assign movies to actors or vice versa

    @app.route('/movies/<int:id>/actors')
    @requires_auth(test_config, permission="get:movies")
    def get_movie_actors(id):
        'get actors acting in movie'
        movie = Movie.query.get_or_404(id)
        try:
            actors_list = [a.format() for a in movie.actors]

            return jsonify({
                'success': True,
                'movie': id,
                'actors': actors_list
            }), 200

        except Exception as e:
            abort(422)

    @app.route('/movies/<int:id>/actors', methods=['POST'])
    @requires_auth(test_config, permission="patch:movies")
    def assign_actors_to_movie(id):
        '''hire actors to act in this movie, can be used to modify
             or delete the actors list, the "CUD" in "CRUD"'''
        movie = Movie.query.get_or_404(id)
        body = request.get_json()
        try:
            # make a list of actors object form the list of id's sent
            actors_list = [Actor.query.get_or_404(
                actor_id) for actor_id in body['actors']]
            # reset the actors of that movie
            movie.actors = []
            for actor in actors_list:
                movie.actors.append(actor)
            movie.insert()
            return jsonify({
                'success': True,
            }), 200
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:id>/movies')
    @requires_auth(test_config, permission="get:actors")
    def get_actor_movies(id):
        'get movies actor is acting in'
        actor = Actor.query.get_or_404(id)
        try:
            movie_list = [v.format() for v in actor.movies]

            return jsonify({
                'success': True,
                'actor': id,
                'movies': movie_list
            }), 200

        except Exception as e:
            abort(422)

    @app.route('/actors/<int:id>/movies', methods=['POST'])
    @requires_auth(test_config, permission="patch:actors")
    def assign_movies_to_actors(id):
        '''assign new movies to actors, can be used to modify
         or delete the movie list, the "CUD" in "CRUD"'''
        actor = Actor.query.get_or_404(id)
        body = request.get_json()
        try:
            # make a list of movies object form the list of id's sent
            movie_list = [Movie.query.get_or_404(
                movie_id) for movie_id in body['movies']]
            actor.movies = []
            for movie in movie_list:
                actor.movies.append(movie)
            actor.insert()
            return jsonify({
                'success': True,
            }), 200
        except Exception as e:
            abort(422)

    # error handling

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    # source https://knowledge.udacity.com/questions/97965
    @app.errorhandler(AuthError)
    def autherror(error):
        error_details = error.error
        error_status_code = error.status_code
        return jsonify({
            'success': False,
            'error': error_status_code,
            'message':
                f"{error_details['code']}: {error_details['description']}"
        }), error_status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
