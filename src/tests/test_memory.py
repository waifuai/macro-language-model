import unittest
from memory import remember
from waifu_frame import WaifuFrame

class TestMemory(unittest.TestCase):

    def test_remember(self):
        waifu_memory = WaifuFrame("Test")
        remember(waifu_memory, "name", "Alice")
        self.assertEqual(waifu_memory.name, "Alice")
        self.assertEqual(waifu_memory.affection, 50)  # No affection change

    def test_remember_affection_increase(self):
        waifu_memory = WaifuFrame("Test")
        remember(waifu_memory, "feeling", "love", affection_change=2)
        self.assertEqual(waifu_memory.feeling, "love")
        self.assertEqual(waifu_memory.affection, 55)  # 50 + 3 ("love") + 2

    def test_remember_affection_decrease(self):
        waifu_memory = WaifuFrame("Test")
        remember(waifu_memory, "feeling", "hate", affection_change=-2)
        self.assertEqual(waifu_memory.feeling, "hate")
        self.assertEqual(waifu_memory.affection, 46)  # 50 - 2 ("hate") - 2

    def test_remember_affection_bounds(self):
        waifu_memory = WaifuFrame("Test")
        remember(waifu_memory, "feeling", "love", affection_change=100)
        self.assertEqual(waifu_memory.affection, 100)  # Max 100
        remember(waifu_memory, "feeling", "hate", affection_change=-100)
        self.assertEqual(waifu_memory.affection, 0)  # Min 0