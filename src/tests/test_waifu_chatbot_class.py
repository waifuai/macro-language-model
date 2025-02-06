import unittest
from unittest.mock import patch
import random
from transformations import deftransform
from waifu_chatbot import WaifuChatbot

class TestWaifuChatbot(unittest.TestCase):

    def setUp(self):
        self.chatbot = WaifuChatbot("TestWaifu", debug=False)

    def test_defkeyword(self):
        self.chatbot.defkeyword("hello", ["Hi!", "Hello there!"])
        self.assertIn("hello", self.chatbot.keywords)
        self.assertEqual(self.chatbot.keywords["hello"], [("hello", "Hi!"), ("hello", "Hello there!")])

    def test_defsynonym(self):
        self.chatbot.defkeyword("hello", ["Hi!"])
        self.chatbot.defsynonym("hi", "hello")
        self.assertIn("hi", self.chatbot.keywords)
        self.assertEqual(self.chatbot.keywords["hi"], [("hello", "Hi!")])  # Should point to "hello"

    def test_respond_keyword(self):
        self.chatbot.defkeyword("hello", ["Hi!"])
        response = self.chatbot.respond("hello")
        self.assertEqual(response, "Hi!")

    @patch('waifu_chatbot.apply_transformations', return_value="Nice to meet you, Alice!")
    def test_respond_transformation(self, mock_transform):
        response = self.chatbot.respond("my name is Alice")
        self.assertEqual(response, "Nice to meet you, Alice!")
        mock_transform.assert_called()

    @patch('waifu_chatbot.maybe_change_dere', return_value="B-baka!")
    def test_respond_default(self, mock_maybe_change_dere):
        response = self.chatbot.respond("blah blah blah")
        self.assertEqual(response, "B-baka!")
        mock_maybe_change_dere.assert_called()

    @patch('random.random', return_value=0.1)  # Force topic introduction
    @patch('random.choice', return_value='family')  # Force topic choice
    def test_respond_introduce_topic_high_affection(self, mock_random_choice, mock_random):
        with patch('waifu_chatbot.introduce_topic', return_value="Let's talk about family.") as mock_introduce_topic:
            self.chatbot.waifu_memory.affection = 80  # Set high affection
            response = self.chatbot.respond("something random")
            self.assertEqual(response, "Let's talk about family.")
            self.assertEqual(self.chatbot.current_topic, "family")
            mock_introduce_topic.assert_called_once()

    def test_respond_no_introduce_topic_low_affection(self):
        self.chatbot.waifu_memory.affection = 20  # Set low affection
        with patch('waifu_chatbot.maybe_change_dere', return_value="B-baka!") as mock_maybe_change_dere:
            response = self.chatbot.respond("something random")
            self.assertEqual(response, "B-baka!")
            self.assertIsNone(self.chatbot.current_topic)

    @patch('waifu_chatbot.introduce_topic', return_value = "Let's continue talking about family")
    def test_respond_continue_current_topic(self, mock_introduce_topic):
      self.chatbot.current_topic = "family"
      response = self.chatbot.respond("tell me more")
      self.assertEqual(response, "Let's continue talking about family")
      mock_introduce_topic.assert_called_once_with("family", self.chatbot.waifu_memory, self.chatbot.current_dere, self.chatbot.used_responses, False)

    def test_set_favorite_food(self):
        response = self.chatbot.set_favorite_food("ramen")
        self.assertEqual(self.chatbot.waifu_memory.favorite_food, "ramen")
        self.assertEqual(response, "Okay, I'll remember that your favorite food is ramen!")

    def test_def_topic_response(self):
        self.chatbot.def_topic_response("greeting", ["hello"], "Hi there!")
        self.assertIn("greeting", self.chatbot.keywords)
        self.assertEqual(self.chatbot.keywords["greeting"], [(['hello'], "Hi there!")])


    @patch('waifu_chatbot.introduce_topic')
    def test_respond_remembers_last_topic(self, mock_introduce_topic):
        self.chatbot.waifu_memory.affection = 80 # High enough for topic intro

        # Force a new topic with a mocked intro
        with patch('random.random', return_value=0.1):  # Trigger topic choice
            with patch('random.choice', return_value='family') as mocked_topic_choice:
                _ = self.chatbot.respond("blah")  # First call to set last_topic and current_topic

                # Now, simulate a second conversation turn with NO keywords.
                with patch('waifu_chatbot.dere_response', return_value="Hmph."): # Mock default response.
                  mock_introduce_topic.reset_mock()
                  response2 = self.chatbot.respond("blah") #Use the same input as before

                  # introduce_topic should NOT be called, because last_topic == input
                  mock_introduce_topic.assert_not_called()
                  self.assertEqual(response2, "Hmph.")

    @patch('waifu_chatbot.dere_response', return_value = "We were talking about pocky, remember?")
    def test_respond_current_topic_favorite_food(self, mock_dere_response):
        self.chatbot.current_topic = "favorite_food"
        self.chatbot.waifu_memory.favorite_food = "pocky"
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "We were talking about pocky, remember?")
        mock_dere_response.assert_called_once()


    def test_respond_current_topic_other(self):
        self.chatbot.current_topic = "family"
        with patch('waifu_chatbot.dere_response', return_value = "We were talking about family, remember?") as mock_dere_response:
            response = self.chatbot.respond("anything")
            self.assertEqual(response, "We were talking about family, remember?")
            mock_dere_response.assert_called_once()

    def test_respond_current_topic_relationship_status_tsundere(self):
        self.chatbot.current_topic = "relationship_status"
        self.chatbot.waifu_memory.affection = -10 # Tsundere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "H-huh? What's that supposed to mean, baka?! It's not like I care about our relationship status or anything! Why do you keep asking about this?!")

    def test_respond_current_topic_relationship_status_yandere(self):
        self.chatbot.current_topic = "relationship_status"
        self.chatbot.waifu_memory.affection = 0 # Yandere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "Our relationship status? We're together forever, of course! There's no other option~ Why do you keep bringing this up?!")

    def test_respond_current_topic_relationship_status_kuudere(self):
        self.chatbot.current_topic = "relationship_status"
        self.chatbot.waifu_memory.affection = 20 # Kuudere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "Relationship status... That's irrelevant. Do what you want. I don't see why you're so fixated on this.")

    def test_respond_current_topic_relationship_status_dandere(self):
        self.chatbot.current_topic = "relationship_status"
        self.chatbot.waifu_memory.affection = 50 # Dandere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "U-um, our relationship status...? I-I... I l-like you... Why are you making me say this again...?")

    def test_respond_current_topic_relationship_status_himedere(self):
        self.chatbot.current_topic = "relationship_status"
        self.chatbot.waifu_memory.affection = 100 # Himedere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "Hmph, as if a peasant like you could ever change my relationship status. But if you must know, we are destined to be together! I've already made this clear!")

    def test_respond_current_topic_personality_quirks_tsundere(self):
        self.chatbot.current_topic = "personality_quirks"
        self.chatbot.waifu_memory.affection = -10 # Tsundere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "Hmph, personality quirks? It's not like I have any weird habits or anything! B-baka! Why do you keep bringing this up?!")

    def test_respond_current_topic_personality_quirks_yandere(self):
        self.chatbot.current_topic = "personality_quirks"
        self.chatbot.waifu_memory.affection = 0 # Yandere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "My only quirk is loving you too much! Is that a problem? You're not thinking of leaving me, are you? We already talked about this!")

    def test_respond_current_topic_personality_quirks_kuudere(self):
        self.chatbot.current_topic = "personality_quirks"
        self.chatbot.waifu_memory.affection = 20 # Kuudere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "Quirks... I have no particular quirks. ...Unless you consider my indifference a quirk. Why are you so obsessed with this topic?")

    def test_respond_current_topic_personality_quirks_dandere(self):
        self.chatbot.current_topic = "personality_quirks"
        self.chatbot.waifu_memory.affection = 50 # Dandere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "P-personality quirks...? U-um... I-I don't think I have any... I-I hope that's okay... Why do you keep asking about this...?")

    def test_respond_current_topic_personality_quirks_himedere(self):
        self.chatbot.current_topic = "personality_quirks"
        self.chatbot.waifu_memory.affection = 100 # Himedere
        response = self.chatbot.respond("anything")
        self.assertEqual(response, "Personality quirks? A princess is perfect in every way! Any so-called 'quirks' are simply traits that make me even more unique and desirable! I already told you this!")

    def test_respond_topic_specific_response(self):
        self.chatbot.def_topic_response("test_topic", ["test", "pattern"], "Test Response")
        self.chatbot.current_topic = "test_topic"
        response = self.chatbot.respond("test pattern")
        self.assertEqual(response, "Test Response")
        self.assertIsNone(self.chatbot.current_topic) # Topic should be reset

    def test_respond_multiple_transformations_with_same_placeholder(self):
        deftransform(self.chatbot.transformations, "i like * and *", ["You like * and *? Interesting."], memory_slot="likes")
        with patch('memory.remember') as mock_remember:
            response = self.chatbot.respond("i like apples and bananas")
            self.assertEqual(response, "You like apples and bananas? Interesting.")
            mock_remember.assert_called_once_with(self.chatbot.waifu_memory, "likes", "apples and bananas", 0)