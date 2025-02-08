import unittest
import re
from waifu_frame import WaifuFrame
from topics import talk_about_interest, introduce_topic
from dere_types import DereContext

class TestTopics(unittest.TestCase):

    def setUp(self):
        self.waifu_memory = WaifuFrame("TestWaifu")
        self.waifu_memory.interests = ["reading manga", "watching anime", "playing video games", "cooking"]
        self.used_responses = set()
        self.context = DereContext(self.waifu_memory, "tsundere", self.used_responses, False)

    def test_talk_about_interest(self):
        response = talk_about_interest(self.waifu_memory, "tsundere", self.used_responses, False)
        self.assertIn(response, [
            "You know, I've been reading this really great manga lately. It's about a magical girl fighting evil. You should check it out! ...Not that I care if you read it or not. B-baka!",
            "I just finished watching this amazing anime. It's a slice-of-life anime with beautiful animation. I cried at the end, not that I would admit that normally. ...Don't get any weird ideas just because I shared this with you.",
            "I'm so addicted to this new game! It's a JRPG where you have to collect rare items. Wanna play with me sometime? ...But don't think this means I'll go easy on you!",
            "I-it's not like I made these cookies for you or anything, b-baka! I just had some extra ingredients. They're pocky flavored. ...And don't expect me to cook for you again!"
        ])

    def test_talk_about_interest_empty_interests(self):
        self.waifu_memory.interests = []
        response = talk_about_interest(self.waifu_memory, "tsundere", self.used_responses, False)
        self.assertIn(response, ["What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."])

    def test_introduce_topic(self):
        response = introduce_topic("family", self.waifu_memory, "tsundere", self.used_responses, False)
        self.assertIn("family", response)
        self.assertTrue(
            any(phrase in response for phrase in [
                "Hmph, why do you want to talk about this all of a sudden?",
                "I suppose we can talk about that, if you insist.",
                "Um, what about this...?",
                "You should be honored that I'm even talking to you about this!"
            ])
        )