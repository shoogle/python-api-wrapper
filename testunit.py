from MuseScoreAPI import MuseScoreAPI
import unittest
import sys

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.api = MuseScoreAPI("credentials.json")

    def test_me(self):
        print sys._getframe().f_code.co_name
        r = self.api.request('me')
        self.assertEqual(r.status_code, 200)
        

        r = self.api.request('me/sets')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('me/scores')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('me/favorites')
        self.assertEqual(r.status_code, 200)

    def test_user_read(self):
        print sys._getframe().f_code.co_name
        r = self.api.request('user/:3')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('user/:3/score')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('user/:3/favorites')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('user/:3/followers')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('user/:3/following')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('user/:3/groups')
        self.assertEqual(r.status_code, 200)

    def test_score_read(self):
        print sys._getframe().f_code.co_name
        r = self.api.request('score')
        self.assertEqual(r.status_code, 200)
    
        r = self.api.request('score', {"text": "Promenade"})
        self.assertEqual(r.status_code, 200)

        r = self.api.request('score/:46274')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('score/:179821/space')
        self.assertEqual(r.status_code, 200)

        r = self.api.request('score/:179821/time')
        self.assertEqual(r.status_code, 200)

    def test_set(self):
        print sys._getframe().f_code.co_name
        r = self.api.request('set/:29516')
        self.assertEqual(r.status_code, 200)

    def test_score_create_delete(self):
        print sys._getframe().f_code.co_name
        files = {'score_data': ('test.mscz', open('test.mscz', 'rb'), 'application/octet-stream'),
            "title": ('',' test'), 
            "description": ('', 'description'), 
            "private" : ('', '1')
        }
        r = self.api.request('score',  method="POST", files=files)
        self.assertEqual(r.status_code, 200)
        score = r.response.json()
        score_id = score["score_id"]

        r = self.api.request('score/:' + score_id, method="DELETE")
        self.assertEqual(r.text, "true")
        self.assertEqual(r.status_code, 200)

    def test_favorite(self):
        r = self.api.request('score/:46274')
        self.assertEqual(r.status_code, 200)
        score = r.response.json()
        score_id_fav = score["id"]
        score_fav = score["user_favorite"]
        self.assertEqual(score_fav, 0)

        r = self.api.request('score/:' + score_id_fav + '/favorite')
        self.assertEqual(r.text, "true")
        self.assertEqual(r.status_code, 200)

        r = self.api.request('score/:' + score_id_fav)
        score = r.response.json()
        score_id_fav = score["id"]
        score_fav = score["user_favorite"]
        self.assertEqual(score_fav, 1)

        r = self.api.request('score/:' + score_id_fav + '/favorite')
        self.assertEqual(r.text, "true")
        self.assertEqual(r.status_code, 200)

        r = self.api.request('score/:' + score_id_fav)
        score = r.response.json()
        score_id_fav = score["id"]
        score_fav = score["user_favorite"]
        self.assertEqual(score_fav, 0)

if __name__ == '__main__':
    unittest.main()