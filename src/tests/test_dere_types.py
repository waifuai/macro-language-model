import unittest

from dere_types import get_current_dere, maybe_change_dere, dere_response
from waifu_frame import WaifuFrame
import random
from unittest.mock import patch

class TestDereTypes(unittest.TestCase):

    def test_get_current_dere(self):
        self.assertEqual(get_current_dere(-10), "tsundere")
        self.assertEqual(get_current_dere(-5), "yandere")
        self.assertEqual(get_current_dere(0), "yandere")
        self.assertEqual(get_current_dere(1), "kuudere")
        self.assertEqual(get_current_dere(40), "kuudere")
        self.assertEqual(get_current_dere(41), "dandere")
        self.assertEqual(get_current_dere(75), "dandere")
        self.assertEqual(get_current_dere(76), "deredere")
        self.assertEqual(get_current_dere(100), "deredere")

    @patch('random.randint', return_value=0)
    @patch('random.choice', return_value='tsundere')
    def test_maybe_change_dere_change(self, mock_choice, mock_randint):
        waifu_memory = WaifuFrame("Test")
        current_dere = "yandere"
        dere_types = ["tsundere", "yandere"]
        used_responses = set()
        response = maybe_change_dere(waifu_memory, current_dere, dere_types, used_responses, False)
        self.assertIn(response, ["B-baka! It's not like I care what you say!", "Hmph! Whatever."])

    @patch('random.randint', return_value=1)
    def test_maybe_change_dere_no_change(self, mock_randint):
        waifu_memory = WaifuFrame("Test")
        current_dere = "yandere"
        dere_types = ["tsundere", "yandere"]
        used_responses = set()
        response = maybe_change_dere(waifu_memory, current_dere, dere_types, used_responses, False)
        self.assertIn(response, ["You're mine forever, you know that?", "Don't even think about leaving me.", "I will never let you go.", "You belong to me, and me alone."])


    def test_dere_response_with_provided_responses(self):
        waifu_memory = WaifuFrame("Test")
        current_dere = "tsundere"
        used_responses = set()
        response = dere_response(waifu_memory, current_dere, used_responses, False, "B-baka!", "Hmph!")
        self.assertIn(response, ["B-baka!", "Hmph!"])
        self.assertIn(response, used_responses)


    def test_dere_response_no_provided_responses(self):
        waifu_memory = WaifuFrame("Test")
        current_dere = "tsundere"
        used_responses = set()
        response = dere_response(waifu_memory, current_dere, used_responses, False)
        self.assertIn(response, ["B-baka! It's not like I care what you say!", "Hmph! Whatever."])
        self.assertIn(response, used_responses)

    def test_dere_response_all_used(self):
        waifu_memory = WaifuFrame("Test")
        current_dere = "tsundere"
        used_responses = {"B-baka!", "Hmph!"}
        # Use list() to create a *copy* of the set for dere_response's arguments
        response = dere_response(waifu_memory, current_dere, used_responses, False, *list(used_responses))
        self.assertIn(response, ["B-baka!", "Hmph!"])  # Should still work but clear used responses
        # After dere_response is called, it should add the chosen response, THEN clear.
        self.assertEqual(len(used_responses), 1)


    def test_dere_response_empty_used_responses_and_provided_responses(self):
        # Tests edge case when `responses` is empty AND `used_responses` is also empty
        waifu_memory = WaifuFrame("Test")
        current_dere = "yandere"  # Choose a dere type that expects responses
        used_responses:set[str] = set()

        # Provide empty responses tuple
        responses:tuple[str,...] = ()

        result = dere_response(waifu_memory, current_dere, used_responses, False, *responses)

        # Assert that the default yandere responses have been used.
        self.assertIn(result, ("You're mine forever, you know that?", "Don't even think about leaving me.", "I will never let you go.", "You belong to me, and me alone."))
        self.assertIn(result, used_responses)