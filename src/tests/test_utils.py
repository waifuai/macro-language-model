import unittest
from utils import tokenize, matches, substitute_template

class TestUtils(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(tokenize("Hello, world!"), ["hello", "world"])
        self.assertEqual(tokenize("This is a test."), ["this", "is", "a", "test"])
        self.assertEqual(tokenize("  Multiple   spaces  "), ["multiple", "spaces"])
        self.assertEqual(tokenize(""), [])

    def test_matches(self):
        self.assertTrue(matches(["hello", "*"], ["hello", "world"]))
        self.assertTrue(matches(["*", "world"], ["hello", "world"]))
        self.assertTrue(matches(["hello", "world"], ["hello", "world"]))
        self.assertFalse(matches(["hello", "world"], ["hello"]))
        self.assertFalse(matches(["hello"], ["hello", "world"]))
        self.assertTrue(matches(["*"], ["anything"]))
        self.assertFalse(matches(["*"], []))  # * can match empty list
        self.assertTrue(matches([], []))  # Empty pattern matches empty list
        self.assertFalse(matches([], ["not", "empty"]))  # Empty pattern doesn't match non-empty

    def test_substitute_template(self):
        template = "Hello, {name}! You are {age} years old."
        substitutions = {"{name}": "Alice", "{age}": 30}
        self.assertEqual(substitute_template(template, substitutions), "Hello, Alice! You are 30 years old.")

        template = "No substitutions here."
        substitutions = {"{name}": "Alice", "{age}": 30}
        self.assertEqual(substitute_template(template, substitutions), "No substitutions here.")