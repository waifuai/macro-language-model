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
            response = talk_about_interest(self.waifu_memory, "tsundere", self.used_responses, False)
            self.assertIn("You know, I've been reading this really great manga lately. It's about reading manga", response)
            mock_dere.assert_called()

    @patch('random.choice', return_value="watching anime")
    def test_talk_about_interest_anime(self, mock_choice):
        with patch('dere_types.dere_response', return_value="slice-of-life") as mock_dere:
            response = talk_about_interest(self.waifu_memory, "yandere", self.used_responses, False)
            self.assertIn("I just finished watching this amazing anime. It's a watching anime anime with watching anime.", response)
            mock_dere.assert_called()

    @patch('random.choice', return_value="playing video games")
    def test_talk_about_interest_games(self, mock_choice):
        with patch('dere_types.dere_response', return_value="JRPG") as mock_dere:
            response = talk_about_interest(self.waifu_memory, "kuudere", self.used_responses, False)
            self.assertIn("I'm so addicted to this new game! It's a playing video games where you have to playing video games.", response)
            mock_dere.assert_called()

    @patch('random.choice', return_value="cooking")
    def test_talk_about_interest_cooking(self, mock_choice):
        with patch('dere_types.dere_response') as mock_dere:
            response = talk_about_interest(self.waifu_memory, "tsundere", self.used_responses, False)
            self.assertIn("cooking", response)
            mock_dere.assert_called()

    @patch('random.choice', return_value="unknown")
    def test_talk_about_interest_unknown(self, mock_choice):
         with patch('dere_types.dere_response', return_value="What are you talking about?") as mock_dere:
            response = talk_about_interest(self.waifu_memory, "tsundere", self.used_responses, False)
            self.assertEqual("What are you talking about?", response)
            mock_dere.assert_called()

    def test_introduce_topic_family(self):
        with patch('dere_types.dere_response', return_value="Hmph, why do you want to talk about family all of a sudden?") as mock_dere:
            response = introduce_topic("family", self.waifu_memory, "tsundere", self.used_responses, False)
            self.assertIn("Hmph, why do you want to talk about family all of a sudden?", response)
            self.assertTrue(response.endswith("Could you tell me more about your family?"))

    def test_introduce_topic_childhood(self):
        with patch('dere_types.dere_response', return_value="Childhood memories? Don't bore me with such childish things.") as mock_dere:
          response = introduce_topic("childhood", self.waifu_memory, "tsundere", self.used_responses, False)
          self.assertIn("Childhood memories? Don't bore me with such childish things.", response)
          self.assertTrue(response.endswith("What was your childhood like?"))


    def test_introduce_topic_feelings(self):
        with patch('dere_types.dere_response', return_value="Feelings? Don't be ridiculous, I don't care about your feelings!") as mock_dere:
          response = introduce_topic("feelings", self.waifu_memory, "tsundere", self.used_responses, False)
          self.assertIn("Feelings? Don't be ridiculous, I don't care about your feelings!", response)
          self.assertTrue(response.endswith("How are you feeling right now?"))


    def test_introduce_topic_interests(self):
      with patch('dere_types.dere_response') as mock_dere:
        response = introduce_topic("interests", self.waifu_memory, "tsundere", self.used_responses, False)
        self.assertIn("A princess has many interests! You couldn't possibly comprehend them all. What are you interested in?", response)
        mock_dere.assert_called()


    def test_introduce_topic_unknown(self):
        with patch('dere_types.dere_response', return_value="What's that supposed to mean?") as mock_dere:
            response = introduce_topic("unknown", self.waifu_memory, "tsundere", self.used_responses, False)
            self.assertIn("What's that supposed to mean?", response)
            self.assertTrue(response.endswith("...So, what were we talking about?"))


    def test_introduce_topic_relationship_status(self):
        test_cases = {
            "tsundere": "H-huh? What's that supposed to mean, baka?! It's not like I care about our relationship status or anything! What do you think about our relationship status?",
            "yandere": "Our relationship status? We're together forever, of course! There's no other option~ Do you agree that we are together forever?",
            "kuudere": "Relationship status... That's irrelevant. Do what you want. What do you want our relationship status to be?",
            "dandere": "U-um, our relationship status...? I-I... I l-like you... How do you feel about our relationship status?",
            "himedere": "Hmph, as if a peasant like you could ever change my relationship status. But if you must know, we are destined to be together! Do you think we are destined to be together?"
        }
        for dere_type, expected in test_cases.items():
            response = introduce_topic("relationship_status", self.waifu_memory, dere_type, self.used_responses, False)
            self.assertEqual(response, expected)

    def test_introduce_topic_favorite_food(self):
        self.waifu_memory.favorite_food = "Sushi"
        test_cases = {
                "tsundere": f"Hmph, why do you want to know about my favorite food all of a sudden? It's Sushi, by the way. What's your favorite food? Do you like Sushi?",
                "yandere": f"My favorite food...? I'll only tell you if you prove your worth. It's Sushi, just so you know. What's your favorite food? Do you like Sushi?",
                "kuudere": f"My favorite food is... Sushi. What's your favorite food? Do you like Sushi?",
                "dandere": f"M-my favorite food? I-It's Sushi... What's your favorite food? Do you like Sushi?",
                "himedere": f"A princess enjoys only the finest delicacies! My favorite food, Sushi, is obviously superior to yours. What's your favorite food? Do you like Sushi?"
        }
        for dere_type, expected in test_cases.items():
            response = introduce_topic("favorite_food", self.waifu_memory, dere_type, self.used_responses, False)
            self.assertEqual(response, expected)

    def test_introduce_topic_personality_quirks(self):
        test_cases = {
            "tsundere": "Hmph, personality quirks? It's not like I have any weird habits or anything! B-baka! Do you think I have personality quirks?",
            "yandere": "My only quirk is loving you too much! Is that a problem? You're not thinking of leaving me, are you? What personality quirks do you like in a person?",
            "kuudere": "Quirks... I have no particular quirks. ...Unless you consider my indifference a quirk. What personality quirks do you think I have?",
            "dandere": "P-personality quirks...? U-um... I-I don't think I have any... I-I hope that's okay... Do you have any personality quirks?",
            "himedere": "Personality quirks? A princess is perfect in every way! Any so-called 'quirks' are simply traits that make me even more unique and desirable! What are your personality quirks?"
        }
        for dere_type, expected in test_cases.items():
            response = introduce_topic("personality_quirks", self.waifu_memory, dere_type, self.used_responses, False)
            self.assertEqual(response, expected)