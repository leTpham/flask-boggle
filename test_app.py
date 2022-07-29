from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            # ...
            html = response.get_data(as_text = True)
            # test that you're getting a template

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- 4 test purposes only!! -->', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            ...
            response = client.post("/api/new-game")
            json_response = response.get_json()
            # breakpoint()
            # x=response

            self.assertEqual(response.status_code, 200)
            # check if game id is in games dictionary

            self.assertIsInstance((json_response["gameId"]), str)

            # check if board is a list
            self.assertIsInstance((json_response["board"]), list)

            # check if board is list of lists
            self.assertIsInstance((json_response["board"][0]), list)

            #check if game id is in the dictionary
            self.assertIn(json_response["gameId"], games)

            # write a test for this route

    def test_api_score_word(self):
        """Test different cases for scoring word"""

        with self.client as client:
            ...
        # first, need to run a new game by sending post request to api/new-game
        # this generates a new game_id and board
        # extract the json response from the new game
        # take game_id and use as parameter for new post request to
        # api/score-word
        # get response which will be a result
        # if the result is ok, then run score_word instance method on the game
        
            game_resp = client.post("/api/new-game")
            game_info = game_resp.get_json()
            game_id= game_info["gameId"]
            games[game_id].board =[
                        ["O","O","O","O","O"],
                        ["O","C","A","T","O"],
                        ["O","O","O","O","O"],
                        ["O","O","O","O","O"],
                        ["O","O","O","O","O"]
                                    ]

            score_resp = client.post('/api/score-word',
                                json={'game_id': game_id,
                                      'word': 'HAEUK'})
            json_response = score_resp.get_json()

            self.assertEqual({'result': 'not-word'}, json_response)


            score_resp = client.post('/api/score-word',
                                json={'game_id': game_id,
                                      'word': 'SEW'})
            json_response = score_resp.get_json()

            self.assertEqual({'result': 'not-on-board'}, json_response)


            score_resp = client.post('/api/score-word',
                                json={'game_id': game_id,
                                      'word': 'CAT'})
            json_response = score_resp.get_json()

            self.assertEqual({'result': 'ok'}, json_response)