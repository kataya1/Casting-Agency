import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
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
            '/actors', json={"name": "testy mctest", "DOB": "1965-3-16", "gender": "female"})
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
                                 json={"name": "testy mctest",   "DOB": "1965-3-16", "gender": "female"})
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
            '/movies', json={"title": "the test",   "release_date": "1990-4-12"})
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
                                 json={"name": "testy mctest",   "DOB": "1965-3-16", "gender": "female"})
        data = json.loads(res.data)
        actorIDforTesting = data['actor']['id']
        res = self.client().delete(f'/actors/{actorIDforTesting}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted actor id'], actorIDforTesting)

    def test_delete_movie(self):
        res = self.client().post(
            '/movies', json={"title": "the test",   "release_date": "1990-4-12"})
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
