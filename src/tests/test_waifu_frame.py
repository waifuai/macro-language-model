import unittest
from waifu_frame import WaifuFrame

class TestWaifuFrame(unittest.TestCase):
    def setUp(self):
        self.frame = WaifuFrame("TestWaifu")

    def test_initialization(self):
        self.assertEqual(self.frame.name, "TestWaifu")
        self.assertEqual(self.frame.affection, 50)
        self.assertEqual(self.frame.interests, ["reading manga", "watching anime", "playing video games", "cooking"])
        self.assertEqual(self.frame.hobbies, ["cosplay", "singing karaoke", "collecting anime figures"])
        self.assertEqual(self.frame.relationship_status, "just friends")
        self.assertEqual(self.frame.favorite_food, "pocky")
        self.assertEqual(self.frame.personality_quirks, [])
        self.assertIsNone(self.frame.current_topic)

    def test_set_favorite_food_frame(self):
        self.frame.set_favorite_food("sushi")
        self.assertEqual(self.frame.favorite_food, "sushi")