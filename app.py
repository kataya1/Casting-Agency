import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
# from auth import AuthError

# pagination
items_PER_PAGE = 5

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

    # wrong ones

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        current_selection = paginate_items(request, actors)
        if len(current_selection) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "actors": current_selection
        }), 200

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        current_selection = paginate_items(request, movies)
        if len(current_selection) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "movies": current_selection
        }), 200

    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        actor = Actor.query.get_or_404(id)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "actor": id
            }), 200
        except Exceptions as e:
            print(f"error: {e}")
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie(id):
        movie = Movie.query.get_or_404(id)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "movie": id
            }), 200
        except Exceptions as e:
            print(f"error: {e}")
            abort(422)

    @app.route('/actors', methods=['POST'])
    def add_actors():
        try:
            body = request.get_json()
            actor = Actor(name=body.get('name'), dob=body.get(
                'DOB'), gender=body.get('gender'))
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception as e:
            print(f"error: {e}")
            abort(422)

    @app.route('/movies', methods=['POST'])
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
    def update_movies(id):
        movie = Movie.query.get_or_404(id)
        try:
            body = request.get_json()
            # if it's body.get('attribute'') is none it defaults to the original
            #  value
            # but if it has attribute -as a proberty of python or- it chooses the
            #  first one if both are true
            movie.title = body.get('title', None) or movie.title
            movie.release_date = body.get('release_date', None) or movie.release_date
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


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
