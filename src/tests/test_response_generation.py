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
                "substitutions": {"*": "happy"}, # Removed list
                "expected_responses": response_templates[("feeling", "tsundere")],
                "should_be_found": True,
            },
            # Test case 2: Template not found
            {
                "keyword": "unknown",
                "affection": -10,
                "substitutions": {"*": "happy"},
                "expected_responses": ["I don't know what to say.", "Is that so?", "Hmph.", "O-okay..."], # Added dere responses for default case
                "should_be_found": False,
            },
            # Test case 3: Empty substitutions
            {
                "keyword": "feeling",
                "affection": -10,
                "substitutions": {},
                "expected_responses": response_templates[("feeling", "tsundere")],
                "should_be_found": True,
            },
            # Test case 4: Substitutions with special characters
            {
                "keyword": "feeling",
                "affection": -10,
                "substitutions":{"*": "happy!"}, #Removed extra list, and changed expected responses to a list
                "expected_responses": response_templates[("feeling", "tsundere")],
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
                self.assertIn(response, [t.replace("*", test_case["substitutions"].get("*", "*")) for t in test_case["expected_responses"]]) #Fixed: Check if in expected responses
                self.assertTrue(response in used_responses)
                self.assertEqual(len(used_responses), 1)
            else:
                self.assertIn(response, test_case["expected_responses"])  # Check if response in default responses.
                self.assertIn(response, used_responses) # Should be in used_responses