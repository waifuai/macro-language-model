import unittest
from unittest.mock import patch
from waifu_frame import WaifuFrame
from response_generation import generate_response
from response_templates import response_templates
from dere_types import dere_response, DereContext


class TestResponseGeneration(unittest.TestCase):

    def test_generate_response(self):
        test_cases = [
            # Test case 1: Template found
            {
                "keyword": "feeling",
                "affection": -10,  # tsundere
                "substitutions": {"*": ["happy"]},
                "expected_response": "B-baka! It's not like I care how you feel, happy, or anything!",
                "should_be_found": True,
            },
            # Test case 2: Template not found
            {
                "keyword": "unknown",
                "affection": -10,
                "substitutions": {"*": ["happy"]},
                "expected_response": "I don't know what to say.",
                "should_be_found": False,
            },
            # Test case 3: Empty substitutions
            {
                "keyword": "feeling",
                "affection": -10,
                "substitutions": {},
                "expected_response": "B-baka! It's not like I care how you feel, *, or anything!",
                "should_be_found": True,
            },
            # Test case 4: Substitutions with special characters
            {
                "keyword": "feeling",
                "affection": -10,
                "substitutions": {"*": ["happy!", "sad?", "angry."]},
                "expected_response": "B-baka! It's not like I care how you feel, happy! sad? angry., or anything!",
                "should_be_found": True,
            },
        ]

        for test_case in test_cases:
            waifu_memory = WaifuFrame("Test")
            waifu_memory.affection = test_case["affection"]
            current_dere = "tsundere"
            used_responses = set()
            context = DereContext(waifu_memory, current_dere, used_responses, False)
            response = generate_response(response_templates, test_case["keyword"], test_case["substitutions"], used_responses, waifu_memory, current_dere, dere_response, False)

            if test_case["should_be_found"]:
                self.assertEqual(response, test_case["expected_response"])
                self.assertTrue(response in used_responses)
                self.assertEqual(len(used_responses), 1)
            else:
                self.assertIn("I don't know what to say.", response)
                self.assertNotIn(response, used_responses)