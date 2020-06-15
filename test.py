import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9nXzhJVnl0MXAwQ3NGRWJndF9udiJ9.eyJpc3MiOiJodHRwczovL2Rldi04Y251NjB3aC51cy5hdXRoMC5jb20vIiwic3ViIjoiSzNibDVHVmc1Q1pUdUY2eWg4WFdHcElUY3lLeG42VGRAY2xpZW50cyIsImF1ZCI6ImZzbmQtY2Fwc3RvbmUiLCJpYXQiOjE1OTIxODAwMjksImV4cCI6MTU5MjI2NjQyOSwiYXpwIjoiSzNibDVHVmc1Q1pUdUY2eWg4WFdHcElUY3lLeG42VGQiLCJzY29wZSI6ImdldDphY3RvcnMgZ2V0OmFjdG9ycy1pbmZvIGdldDptb3ZpZXMgZ2V0Om1vdmllcy1pbmZvIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphY3RvcnMtaW5mbyIsImdldDptb3ZpZXMiLCJnZXQ6bW92aWVzLWluZm8iXX0.of-z_k03lmrbAbJO4lWUDKcCC4W5frgak0SIEys5l5RYrYHyZPDlbLF9rQrdB_Lxs20IYIbPTBZLzruhtc0cMcU_u7o-dv0traG-3uI3LVFHpak6r7DrpljIG3L-LggYlA5GClvAiJLxsSD50qffG0ziKviCY-2vckL8uoj2nXh9AW4aBZakgKacBzGuCetsotT62qq16UZ7Bl6kAHaY1fGVn2aZ9ifU7kTWY6iIt4-wNEZ4pqr803LAJ-5T0gJP7bWHWWEcwsa-iKx25QftfqxOmv88zMY89FnxOrcA_vpVaR07ext2hjjX9WyreJA6vAdP_MsmnQTpBY5YJ3oVCw'
        self.manager_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9nXzhJVnl0MXAwQ3NGRWJndF9udiJ9.eyJpc3MiOiJodHRwczovL2Rldi04Y251NjB3aC51cy5hdXRoMC5jb20vIiwic3ViIjoiSzNibDVHVmc1Q1pUdUY2eWg4WFdHcElUY3lLeG42VGRAY2xpZW50cyIsImF1ZCI6ImZzbmQtY2Fwc3RvbmUiLCJpYXQiOjE1OTIxODIwNDQsImV4cCI6MTU5MjI2ODQ0NCwiYXpwIjoiSzNibDVHVmc1Q1pUdUY2eWg4WFdHcElUY3lLeG42VGQiLCJzY29wZSI6ImdldDphY3RvcnMgZ2V0OmFjdG9ycy1pbmZvIGdldDptb3ZpZXMgZ2V0Om1vdmllcy1pbmZvIHBhdGNoOmFjdG9yIHBhdGNoOm1vdmllIHBvc3Q6YWN0b3IgcG9zdDptb3ZpZSIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6YWN0b3JzLWluZm8iLCJnZXQ6bW92aWVzIiwiZ2V0Om1vdmllcy1pbmZvIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.RXTFUHaemH0ml2MXFFg625KcW1CphgSptkIkUfkPOUAkmCkzgKdCj4RV40NdPhwDgbX1Yn3EwuvQEnYhPPgeQGyNJqp4dTyviHxUWkvM9B1K4bX6-EfHBdUZ6ntjJLTj87am1EhWKQetbuq_TfZFQ_hiK_UipIB14cidXByEfoGKXF84LA0RhxAs0LJXjJMW4CKvw5UtDOD81hjnN9Jej3L-6J_M5dJDa985oetwAuYLnNVZPVZW9obIuucvucs_p_EEcI2iPGKO734ggnwzm-D0kooAF9K_0NGmjfV18HMsKW3C0VttIKKzn0KEj1XXyjoXeZguHJD87KNGD-7HpQ'
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9nXzhJVnl0MXAwQ3NGRWJndF9udiJ9.eyJpc3MiOiJodHRwczovL2Rldi04Y251NjB3aC51cy5hdXRoMC5jb20vIiwic3ViIjoiSzNibDVHVmc1Q1pUdUY2eWg4WFdHcElUY3lLeG42VGRAY2xpZW50cyIsImF1ZCI6ImZzbmQtY2Fwc3RvbmUiLCJpYXQiOjE1OTIyMDQ0ODUsImV4cCI6MTU5MjI5MDg4NSwiYXpwIjoiSzNibDVHVmc1Q1pUdUY2eWg4WFdHcElUY3lLeG42VGQiLCJzY29wZSI6ImdldDphY3RvcnMgZ2V0OmFjdG9ycy1pbmZvIGdldDptb3ZpZXMgZ2V0Om1vdmllcy1pbmZvIHBhdGNoOmFjdG9yIHBhdGNoOm1vdmllIHBvc3Q6YWN0b3IgcG9zdDptb3ZpZSBkZWxldGU6YWN0b3IgZGVsZXRlOm1vdmllIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDphY3RvcnMtaW5mbyIsImdldDptb3ZpZXMiLCJnZXQ6bW92aWVzLWluZm8iLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiXX0.iEVOIX1ej7AGdR9op9dFBfET8By30lkrhCw2MmwnHsDnZ71Tc3DgDoXIrickjQ8m8Xr94l8KOfbUCYkTknC1xAi7P24LGeBYQmD6dL4QcMiv3MAeUbYG8vZAmDcM9yEgpwMX-JRtqpUGzYpnixV45zeq-SZAKQMSwOzkO92V2ODoSYoSm4aEY11Susz7kATFyypXUWgaH_15olFtzsTIle8YgJejSbMPxjyUtWrTFo3cIkiKsFDnaMerFkMVNIq8IOdUv2_LaKdE2s1DCixrrFCMhg1ASRPClLnvSbw6y-KPwRI8BsrJyuXVdY6qePl0Y8uTOKTRVX9Aye_jp81odw'
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_NEW_ACTOR = {
            "name": "Ana de Armas",
            "full_name": "Ana Celia de Armas Caso",
            "date_of_birth": "April 30, 1988"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Ana de Armas"
        }

        self.VALID_UPDATE_ACTOR = {
            "full_name": "Anne Hathaway"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "Suicide Squad",
            "duration": 137,
            "release_year": 2016,
            "imdb_rating": 6,
            "cast": ["Margot Robbie"]
        }

        self.INVALID_NEW_MOVIE = {
            "title": "Knives Out",
            "imdb_rating": 7.9,
            "cast": ["Ana de Armas"]
        }

        self.VALID_UPDATE_MOVIE = {
            "imdb_rating": 6.5
        }

        self.INVALID_UPDATE_MOVIE = {}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_health(self):
        """Test for GET / (health endpoint)"""
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'Running!!')

    def test_api_call_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization Header is required.")

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

    def test_get_actors_by_id(self):
        """Passing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor', data)
        self.assertIn('full_name', data['actor'])
        self.assertTrue(len(data["actor"]["movies"]))

    def test_404_get_actors_by_id(self):
        """Failing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_actor_with_user_token(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_actor(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created_actor_id', data)

    def test_422_create_actor(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_actor_info(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor_info', data)
        self.assertEqual(data["actor_info"]["full_name"],
                         self.VALID_UPDATE_ACTOR["full_name"])

    def test_422_update_actor_info(self):
        """Failing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_actor_with_manager_token(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/5', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/5', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted_actor_id', data)

    def test_404_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('movies', data)
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id(self):
        """Passing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie', data)
        self.assertIn('imdb_rating', data['movie'])
        self.assertIn('duration', data['movie'])
        self.assertIn('cast', data['movie'])
        self.assertTrue(len(data["movie"]["cast"]))

    def test_404_get_movie_by_id(self):
        """Failing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_movie_with_user_token(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_movie(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created_movie_id', data)

    def test_422_create_movie(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_movie_info(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie_info', data)
        self.assertEqual(data["movie_info"]["imdb_rating"],
                         self.VALID_UPDATE_MOVIE["imdb_rating"])

    def test_422_update_movie_info(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_movie_with_manager_token(self):
        """Failing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted_movie_id', data)

    def test_404_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
