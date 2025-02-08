import unittest
from unittest.mock import patch
from waifu_frame import WaifuFrame
from topics import talk_about_interest, introduce_topic
from dere_types import dere_response

class TestTopics(unittest.TestCase):
    def setUp(self):
        self.waifu_memory = WaifuFrame("TestWaifu")
        self.waifu_memory.interests = ["reading manga", "watching anime", "playing video games", "cooking"]
        self.waifu_memory.favorite_food = "pocky"
        self.used_responses:set[str] = set()

    @patch('random.choice', return_value="reading manga")
    def test_talk_about_interest_manga(self, mock_choice):
        with patch('dere_types.dere_response', return_value="a magical girl fighting evil") as mock_dere:
            response = talk_about_interest(self.waifu_memory, "tsundere", [], False)
            self.assertTrue("manga" in response and ("baka" in response if "tsundere" == "tsundere" else True))

    @patch('random.choice', return_value="watching anime")
    def test_talk_about_interest_anime(self, mock_choice):
        with patch('dere_types.dere_response', return_value="slice-of-life") as mock_dere:
            response = talk_about_interest(self.waifu_memory, "yandere", [], False)
            self.assertTrue("anime" in response and ("every night" in response if "yandere" == "yandere" else True))

    @patch('random.choice', return_value="playing video games")
    def test_talk_about_interest_games(self, mock_choice):
        with patch('dere_types.dere_response', return_value="JRPG") as mock_dere:
            response = talk_about_interest(self.waifu_memory, "kuudere", [], False)
            self.assertTrue("game" in response and ("...If you insist." in response if "kuudere" == "kuudere" else True))

    @patch('random.choice', return_value="cooking")
    def test_talk_about_interest_cooking(self, mock_choice):
        with patch('dere_types.dere_response', return_value=f"I-it's not like I made these cookies for you or anything, b-baka! I just had some extra ingredients. They're pocky flavored.") as mock_dere:
            response = talk_about_interest(self.waifu_memory, "tsundere", [], False)
            self.assertIn(self.waifu_memory.favorite_food, response)
            self.assertIn("pocky", response)

    def test_introduce_topic_family(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
            response = introduce_topic("family", self.waifu_memory, "tsundere", self.used_responses, False)
            topic = "family"
            self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))

    def test_introduce_topic_childhood(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
            response = introduce_topic("childhood", self.waifu_memory, "tsundere", self.used_responses, False)
            topic = "childhood"
            self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))


    def test_introduce_topic_feelings(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
            response = introduce_topic("feelings", self.waifu_memory, "tsundere", self.used_responses, False)
            topic = "feelings"
            self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))


    def test_introduce_topic_interests(self):
      with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
        response = introduce_topic("interests", self.waifu_memory, "tsundere", self.used_responses, False)
        topic = "interests"
        self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))


    def test_introduce_topic_unknown(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
            response = introduce_topic("unknown", self.waifu_memory, "tsundere", self.used_responses, False)
        topic = "unknown"
        self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))


    def test_introduce_topic_relationship_status(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
            response = introduce_topic("relationship_status", self.waifu_memory, "tsundere", self.used_responses, False)
        topic = "relationship_status"
        self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))

    def test_introduce_topic_favorite_food(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
            response = introduce_topic("favorite_food", self.waifu_memory, "tsundere", self.used_responses, False)
        topic = "favorite_food"
        self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))

    def test_introduce_topic_personality_quirks(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about this all of a sudden?") as mock_dere:
            response = introduce_topic("personality_quirks", self.waifu_memory, "tsundere", self.used_responses, False)
        topic = "personality_quirks"
        self.assertTrue(topic in response and any(phrase in response for phrase in ["Hmph, why do you want to talk about this all of a sudden?", "I suppose we can talk about that, if you insist.", "Um, what about this...?", "You should be honored that I'm even talking to you about this!"]))