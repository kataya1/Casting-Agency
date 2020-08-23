import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('unittest')
        self.client = self.app.test_client
        setup_db(self.app)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass
        # self.db.session.remove()
        # self.db.drop_all()
        # self.app_context.pop()
        # self.session.bind.dispose()

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'])

    def test_add_actor(self):
        res = self.client().post(
            '/actors', json={
                "name": "testy mctest",
                "DOB": "1965-3-16", "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_add_movie(self):
        res = self.client().post(
            '/movies', json={"title": "the test", "release_date": "1990-4-12"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    def test_patch_actor(self):
        # check if thit works
        res = self.client().post('/actors',
                                 json={
                                    "name": "testy mctest",
                                    "DOB": "1965-3-16",
                                    "gender": "female"})
        data = json.loads(res.data)
        actorIDforTesting = data['actor']['id']
        # actor = Actor.query.get(self.actorIDforTesting)
        old_name = data['actor']['name']
        res = self.client().patch(
            f'actors/{actorIDforTesting}', json={"name": "timmy turner"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])
        self.assertNotEqual(data['actor']['name'], old_name)

    def test_patch_movie(self):
        # check if this works
        res = self.client().post(
            '/movies', json={
                "title": "the test",   "release_date": "1990-4-12"})
        data = json.loads(res.data)
        movieIDforTesting = data['movie']['id']
        old_title = data['movie']['title']

        res = self.client().patch(
            f'movies/{movieIDforTesting}', json={"title": "spirited away"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])
        self.assertNotEqual(data['movie']['title'], old_title)

    def test_delete_actor(self):
        res = self.client().post('/actors',
                                 json={
                                    "name": "testy mctest",
                                    "DOB": "1965-3-16", "gender": "female"})
        data = json.loads(res.data)
        actorIDforTesting = data['actor']['id']
        res = self.client().delete(f'/actors/{actorIDforTesting}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted actor id'], actorIDforTesting)

    def test_delete_movie(self):
        res = self.client().post(
            '/movies', json={
                "title": "the test",   "release_date": "1990-4-12"})
        data = json.loads(res.data)
        movieIDforTesting = data['movie']['id']

        res = self.client().delete(f'/movies/{movieIDforTesting}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted movie id'], movieIDforTesting)

    def test_get_actors_beyond_pagination_limit(self):
        res = self.client().get('/actors?page=999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movie_beyond_pagination_limit(self):
        res = self.client().get('/movies?page=999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_actor_fail(self):
        res = self.client().post(
            '/actors', json={"DOB": "1965-3-16", "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

    def test_add_movie_fail(self):
        res = self.client().post('/movies', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

    def test_patch_actor_fail(self):
        res = self.client().patch('/actors/9999999', json={})
        self.assertEqual(res.status_code, 404)

    def test_patch_movie_fail(self):
        res = self.client().patch('movies/9999999', json={})
        self.assertEqual(res.status_code, 404)

    def test_delete_nonexistant_actor(self):
        res = self.client().delete('/actors/9999999')
        self.assertEqual(res.status_code, 404)

    def test_delete_nonexistant_movie(self):
        res = self.client().delete('movies/9999999')
        self.assertEqual(res.status_code, 404)

#   comment for error:
#   sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) FATAL:
#   too many connections for role "qcwhzhmdbijavy"
# tried to solve it but no avail it's tested in postman
    def test_get_movie_actors(self):
        # get actors acting in movie 1
        res = self.client().get('/movies/1/actors')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie'], 1)

    def test_get_movie_actors_fail(self):
        res = self.client().get('/movies/999/actors')
        self.assertEqual(res.status_code, 404)

    def test_assign_actors_to_movie(self):
        # hire actor to act in movie 1
        res = self.client().post('/movies/1/actors', json={'actors': [1, 3]})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_assign_actors_to_movie_fail(self):
        res = self.client().post('/movies/1/actors', json={'actors': [1, 999]})
        self.assertEqual(res.status_code, 422)

    def test_actor_movies(self):
        # get movies that actor 1 is acting in
        res = self.client().get('/actors/1/movies')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor'], 1)

    def test_actor_movies_fail(self):
        res = self.client().get('/actors/999/movies')
        self.assertEqual(res.status_code, 404)

    def test_assign_movies_to_actor(self):
        res = self.client().post('/actors/1/movies', json={'movies': [1, 3]})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_assign_movies_to_actor_fail(self):
        res = self.client().post('/actors/1/movies', json={'movies': [999]})
        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
