import os
from flask import Flask, request, abort, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
# from auth import AuthError, requires_auth, AUTH0_AUTHORIZE_URL

# pagination
items_PER_PAGE = 5
AUTH0_AUTHORIZE_URL = "https://noisy-pond-1849.us.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=7NCGYZ6utWFtYbuGU2bQ3U2H8fbs3Nrb&redirect_uri=https://casting-agency1996.herokuapp.com/callback"


def paginate_items(request, selection):
    # i copied this function from the lesson
    'takes in request and a list of db items objects, format them, then return a page of items'
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
        return render_template("signin.html", AUTH0_AUTHORIZE_URL=AUTH0_AUTHORIZE_URL)

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
    # @requires_auth(permission='get:actors')
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
    # @requires_auth(permission='get:movies')
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
    # @requires_auth(permission="delete:actors")
    def delete_actor(id):
        actor = Actor.query.get_or_404(id)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "deleted actor id": id
            }), 200
        except Exceptions as e:
            print(f"error: {e}")
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    # @requires_auth(permission="delete:movies")
    def delete_movie(id):
        movie = Movie.query.get_or_404(id)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted movie id": id
            }), 200
        except Exceptions as e:
            print(f"error: {e}")
            abort(422)

    @app.route('/actors', methods=['POST'])
    # @requires_auth(permission="post:actors")
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
            print(f"error: {e}")
            abort(422)

    @app.route('/movies', methods=['POST'])
    # @requires_auth(permission="post:movies")
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
            print(f"error: {e}")
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    # @requires_auth(permission="patch:actors")
    def update_actors(id):
        actor = Actor.query.get_or_404(id)
        try:
            body = request.get_json()
            # if it's body.get('attribute'') is none it defaults to the original
            #  value
            # but if it has attribute -as a proberty of python or- it chooses the
            #  first one if both are true
            actor.name = body.get('name', None) or actor.name
            actor.dob = body.get('DOB', None) or actor.dob
            actor.gender = body.get('gender', None) or actor.gender
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except Exception as e:
            print(f'error: {e}')
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    # @requires_auth(permission="patch:movies")
    def update_movies(id):
        movie = Movie.query.get_or_404(id)
        try:
            body = request.get_json()
            # if it's body.get('attribute'') is none it defaults to the original
            #  value
            # but if it has attribute -as a proberty of python or- it chooses the
            #  first one if both are true
            movie.title = body.get('title', None) or movie.title
            movie.release_date = body.get(
                'release_date', None) or movie.release_date
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 200

        except Exception as e:
            print(f'error: {e}')
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
    # @app.errorhandler(AuthError)
    # def autherror(error):
    #     error_details = error.error
    #     error_status_code = error.status_code
    #     return jsonify({
    #         'success': False,
    #         'error': error_status_code,
    #         'message': f"{error_details['code']}: {error_details['description']}"
    #     }), error_status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
