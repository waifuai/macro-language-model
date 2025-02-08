import unittest
from unittest.mock import patch
from waifu_frame import WaifuFrame
from response_generation import generate_response
from response_templates import response_templates
from dere_types import dere_response


class TestResponseGeneration(unittest.TestCase):

    def test_generate_response_found(self):
        waifu_memory = WaifuFrame("Test")
        waifu_memory.affection = -10  # tsundere
        current_dere = "tsundere"
        used_responses = set()
        response = generate_response(response_templates, "feeling", {"*": ["happy"]}, used_responses, waifu_memory, current_dere, dere_response, False)
        expected_responses = [
            "B-baka! It's not like I care how you feel, happy, or anything!",
            "H-how you feel is none of my business, happy!",
            "Whatever, just tell me already, happy!",
            "Don't worry about me, worry about yourself, baka!",
            "I-it's not like I want you to comfort me or anything!",
            "Hmph, so you finally noticed how I feel?",
            "It's not like I'm expecting you to understand, but...",
            "Just leave me alone, okay?!"
        ]
        self.assertIn(response, expected_responses)
        self.assertIn(response, used_responses)


    def test_generate_response_not_found(self):
        waifu_memory = WaifuFrame("Test")
        waifu_memory.affection = -10
        current_dere = "tsundere"
        used_responses = set()
        response = generate_response(response_templates, "unknown", {"*": ["happy"]}, used_responses, waifu_memory, current_dere, dere_response, False)
        self.assertIn(response, ["I don't know what to say.", "Is that so?", "Hmph.", "O-okay..."])

    def test_generate_response_clears_used_responses(self):
        waifu_memory = WaifuFrame("Test")
        waifu_memory.affection = -10
        current_dere = "tsundere"
        used_responses = set()  # Start with an EMPTY set
        response = generate_response(response_templates, "feeling", {"*": ["happy"]}, used_responses, waifu_memory, current_dere, dere_response, False)
        expected_responses = [
            "B-baka! It's not like I care how you feel, happy, or anything!",
            "H-how you feel is none of my business, happy!",
            "Whatever, just tell me already, happy!",
            "Don't worry about me, worry about yourself, baka!",
            "I-it's not like I want you to comfort me or anything!",
            "Hmph, so you finally noticed how I feel?",
            "It's not like I'm expecting you to understand, but...",
            "Just leave me alone, okay?!"
        ]
        self.assertIn(response, expected_responses)
        self.assertIn(response, used_responses)
        self.assertEqual(len(used_responses), 1)  # One response should be added