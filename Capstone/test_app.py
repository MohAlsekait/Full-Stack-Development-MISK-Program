import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Actor, Movie, setup_db,database_path
from app import create_app



manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJQdEEzTGNPQllvaHZzUk5nMTZkNiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTE5MzkudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1ODM2NDUxODM3NDcxODUyMDIyIiwiYXVkIjoiY2FwIiwiaWF0IjoxNjMxMTE1NjMyLCJleHAiOjE2MzExMjI4MzIsImF6cCI6ImpKWUdJRjB4c0ZIbWJ5UHNDSjBpS3lacmRURnRkRktFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZSJdfQ.bJErLKW-4vMyiXCrAWNb_D7qOBSACuOYibdYRiODYC2ry4ZZig2RHE45SfcqeGg6bs-t7J_XzjTU5eKlXN9B89hsxQR1f6YnNgw1or3UTPGSIYzl30qVNcupWiH6-UojbbfrgDkDsBarhhKEVaZKq_7r_JsbY5_wTHcqW3pR58Sg5NR48l39pkAc0J5liwhXHTGQNz_jMNA3HdZ6oeVke19CdmQiv70JcNjXi_NRjHRlU2bXVUYfF2as82FHNqtAulVlz6qzYKbbW_OJ50bx15h89IQr8hPJjwdLPrFUwyqNCAM-Eh3NtcvpGHRDfxvxkpR8QzCVXKL1hMBp41Tvmg'
employee = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJQdEEzTGNPQllvaHZzUk5nMTZkNiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTE5MzkudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1ODM2NDUxODM3NDcxODUyMDIyIiwiYXVkIjoiY2FwIiwiaWF0IjoxNjMxMTE2MDMzLCJleHAiOjE2MzExMjMyMzMsImF6cCI6ImpKWUdJRjB4c0ZIbWJ5UHNDSjBpS3lacmRURnRkRktFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZSJdfQ.wlvCAeks1ocVG0pXYQwXskxuDvOl9j9pqH-fL6OIr-22iYlEgmUJ5yA9vL1QXdDNI6R5lpW0X928Zcy0PuquQZzQKqO0EdyUxmTkxpati2-KTygR2XjrH7SRao9BQJIcg-hphqiIp1XXWFbHCGUkNmTCNgAISm-AWV56ut8KVnA2Q4RCE6REqt_EeP84QQyvHABBZRxrVQLx6Q9ZvAj3DcOG45yjEtTY94OfP6hyxUWC2WilpLJa8FnrZfpLl83X0JjRdpPg21EbqY97YgElU19GR9XLhNeku_IvfxH_uZ1pGtK7EJQ2uAkiTwVFUFEcqmluJ1ZuVoJZhsl9tiy4CA'
customer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJQdEEzTGNPQllvaHZzUk5nMTZkNiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTE5MzkudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1ODM2NDUxODM3NDcxODUyMDIyIiwiYXVkIjoiY2FwIiwiaWF0IjoxNjMxMTE2MTc2LCJleHAiOjE2MzExMjMzNzYsImF6cCI6ImpKWUdJRjB4c0ZIbWJ5UHNDSjBpS3lacmRURnRkRktFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.r88vJyl48FE6VyjLXJ3tPYXzM6LqyQaGOJzD0GpNQdFejMJFHJku6CfQCSzHzl-9RTeit9zVB1QoHisJhg8hVo-zgHqaPCNSjI4zXYC8ci7ezSUC6Oq6AdCImA-fxLx84LCF9uWA8LE20p5IopujEC9iifbHhmT4LSXqf-TZvXbCqbm9PI_3IQiYMCUx_yOBZh2ttrWprizvBiUQyT75BkrwiDwGe1e63yY1zQAXzn80PxWygZa_kPu8FIbFJIIR5quKJv1jfRfheaTLjjHGT9DEA5UNqrzQB6hAfgnVa-xyxjzKCwdUomWLlZPhqmBQCSkGDl7gCywFP3llYNhi4w'


class AgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_actors(self):
        """Passing Test for GET /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('actors', data)
        self.assertTrue(len(data["actors"]))



    def test_404_get_actors(self):
            res = self.client().get('/actors?page=100000', headers={'Authorization': "Bearer {}".format(manager)})
            data = json.loads(res.data)


            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')

    def test_create_actor(self):
        res = self.client().post('/actors',
            json={'name': 'a','age': '22','gender': 'M'},
            headers={'Authorization': "Bearer {}".format(customer)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_actor(self):
        res = self.client().post('/actors', json={}, headers={'Authorization': "Bearer {}".format(customer)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_actor(self):
        actor = Actor(name="b", age="23", gender="F")
        actor.update()

        res = self.client().patch(f'/actors/{actor.id}',
            json={'name': 'b'},
            headers={'Authorization': "Bearer {}".format(manager)}),
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_404_update_actor(self):
        res = self.client().patch(f'/actors/10000000',
            json={'name': 'b'},
            headers={'Authorization': "Bearer {}".format(customer)})
        data = json.loads(res.data)



        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        actor = Actor(name="c", age=24, gender='F')
        actor.delete()

        res = self.client().delete(f'/actors/{actor.id}', headers={'Authorization': "Bearer {}".format(manager)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_delete_actor(self):
        res = self.client().delete(f'/actors/1000', headers={'Authorization': "Bearer {}".format(customer)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_movie(self):
        res = self.client().post('/movies',
            json={'title': 'test','release_date': '11-11-2011'},
            headers={'Authorization': "Bearer {}".format(manager)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 2)

    def test_422_create_new_movie(self):
        res = self.client().post('/movies', json={}, headers={'Authorization': "Bearer {}".format(customer)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': "Bearer {}".format(manager)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies']> 0)

    def test_404_get_movies(self):
        res = self.client().get('/movies?page=1000', headers={
            'Authorization': "Bearer {}".format(manager)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        movie = Movie(title='test', release_date='12-12-1222')
        res = self.client().delete(f'/movies/{movie.id}', headers={'Authorization': "Bearer {}".format(manager)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_delete_movie(self):
        res = self.client().delete(f'/movies/1000', headers={'Authorization': "Bearer {}".format(customer)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_movie(self):
        movie = Movie(title='test', release_date='10-10-2010')
        res = self.client().patch(f'/movies/{movie.id}',
            json={'title': 'IT'},
            headers={'Authorization': "Bearer {}".format(manager)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    def test_404_update_movie(self):
        res = self.client().patch(f'/movies/1000',
            json={'title': 'it'},
            headers={'Authorization': "Bearer {}".format(customer)})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

