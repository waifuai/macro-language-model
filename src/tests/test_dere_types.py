import unittest

from dere_types import get_current_dere, maybe_change_dere, dere_response, DereContext
from waifu_frame import WaifuFrame
import random
from unittest.mock import patch

class TestDereTypes(unittest.TestCase):

    def test_get_current_dere(self):
        test_cases = [
            (-10, "tsundere"),
            (-5, "yandere"),
            (0, "yandere"),
            (1, "kuudere"),
            (40, "kuudere"),
            (41, "dandere"),
            (75, "dandere"),
            (76, "deredere"),
            (100, "deredere"),
        ]
        for affection, expected_dere in test_cases:
            self.assertEqual(get_current_dere(affection), expected_dere)

    def test_maybe_change_dere_probability(self):
        waifu_memory = WaifuFrame("Test")
        current_dere = "yandere"
        dere_types = ["tsundere", "yandere"]
        used_responses = set()
        context = DereContext(waifu_memory, current_dere, used_responses, False)
        
        num_trials = 100
        change_count = 0
        for _ in range(num_trials):
            with patch('random.randint', return_value=0 if random.random() < 0.1 else 1):
                response = maybe_change_dere(context, dere_types)
                if context.current_dere != current_dere:
                    change_count += 1
        # Probability of change should be around 10%
        self.assertTrue(7 <= change_count <= 13)

    def test_dere_response(self):
        test_cases = [
            ("tsundere", ["B-baka!", "Hmph!"], set(), ["B-baka!", "Hmph!"]),
            ("yandere", [], set(), ["You're mine forever, you know that?", "Don't even think about leaving me.", "I will never let you go.", "You belong to me, and me alone."]),
            ("kuudere", [], {"Hmph."}, ["Hmph.", "...", "Is that so.", "I see.", "Understood."]),
            ("dandere", ["U-um..."], set(), ["U-um..."]),
            ("himedere", [], set(), ["Bow down to me, you peasant!", "You are lucky to be in my presence.", "Hmph, how amusing.", "Do as I command!", "You should be honored."]),
        ]

        for current_dere, provided_responses, used_responses, expected_responses in test_cases:
            waifu_memory = WaifuFrame("Test")
            context = DereContext(waifu_memory, current_dere, used_responses, False)
            if provided_responses:
                response = dere_response(context, *provided_responses)
                self.assertIn(response, provided_responses)
            else:
                response = dere_response(context)
                self.assertIn(response, expected_responses)
            self.assertIn(response, context.used_responses)
            if len(used_responses) == 0:
                self.assertEqual(len(context.used_responses), 1)