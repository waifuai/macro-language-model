import unittest
from unittest.mock import patch
from transformations import apply_transformations, deftransform
from memory import remember
from waifu_frame import WaifuFrame
from topics import talk_about_interest, introduce_topic
from dere_types import dere_response, maybe_change_dere
from response_generation import generate_response
from response_templates import response_templates


class TestTransformations(unittest.TestCase):

    def setUp(self):
        self.transformations = {}
        self.waifu_memory = WaifuFrame("Test")
        self.current_dere = "tsundere"
        self.used_responses: set[str] = set()
        self.dere_types = ["tsundere", "yandere", "kuudere", "dandere", "himedere"]

    def test_deftransform(self):
        deftransform(self.transformations, "my name is *", ["Nice to meet you, *!"], "name")
        self.assertIn("my name is *", self.transformations)
        self.assertEqual(self.transformations["my name is *"], (["Nice to meet you, *!"], "name", 0))

    def test_deftransform_with_affection_change(self):
        deftransform(self.transformations, "my name is *", ["Nice to meet you, *!"], "name", affection_change = 5)
        self.assertIn("my name is *", self.transformations)
        self.assertEqual(self.transformations["my name is *"], (["Nice to meet you, *!"], "name", 5))


    def test_apply_transformations_match(self):
        deftransform(self.transformations, "my name is *", ["Nice to meet you, *!"], "name")
        input_list = ["my", "name", "is", "alice"]
        with patch('memory.remember') as mock_remember:
          response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
          self.assertEqual(response, "Nice to meet you, alice!")
          mock_remember.assert_called_once_with(self.waifu_memory, "name", "alice", 0)

    def test_apply_transformations_no_match(self):
        deftransform(self.transformations, "my name is *", ["Nice to meet you, *!"], "name")
        input_list = ["hello", "there"]
        response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
        self.assertIsNone(response)

    def test_apply_transformations_current_topic_set(self):
      self.waifu_memory.current_topic = "childhood"
      input_list = ["hello"]
      with patch('dere_types.dere_response', return_value="What was your childhood like?") as mock_dere_response:
        response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
        self.assertEqual(response, "What was your childhood like?")
        mock_dere_response.assert_called()


    def test_apply_transformations_callable_response(self):
        def mock_response(name):
            return f"Hello, {name}!"

        deftransform(self.transformations, "my name is *", mock_response, memory_slot="name")
        input_list = ["my", "name", "is", "bob"]
        response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
        self.assertEqual(response, "Hello, bob!")



    def test_apply_transformations_list_response(self):
        deftransform(self.transformations, "do you like *", ["generate", "interest"])  # Removed memory-related parts
        input_list = ["do", "you", "like", "apples"]
        with patch('response_generation.generate_response', return_value="Oh you like apples") as mock_generate_response:
            response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
            self.assertEqual(response, "Oh you like apples")
            mock_generate_response.assert_called_once_with(response_templates, "interest", {'*': ["apples"]}, self.used_responses, self.waifu_memory, self.current_dere, dere_response, False)


    def test_apply_transformations_waifu_memory(self):
        self.waifu_memory.name = "Alice" # Directly set

        deftransform(self.transformations, "what is my name", ["waifu-memory", "name"])
        input_list = ["what", "is", "my", "name"]
        response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)

        self.assertEqual(response, "Alice")


    def test_apply_transformations_dere_response_tuple(self):
      deftransform(self.transformations, "say baka", ["dere-response", "B-baka!"])
      input_list = ["say", "baka"]
      with patch('dere_types.dere_response', return_value="B-baka!") as mock_dere_response:
        response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
        self.assertEqual(response, "B-baka!")
        mock_dere_response.assert_called_with(self.waifu_memory, self.current_dere, self.used_responses, False, "B-baka!")


    def test_apply_transformations_maybe_change_dere(self):
        deftransform(self.transformations, "change dere", ["maybe-change-dere"])
        input_list = ["change", "dere"]
        with patch('dere_types.maybe_change_dere', return_value = "I feel different") as mock_maybe_change_dere:
            response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
            self.assertEqual(response, "I feel different")
            mock_maybe_change_dere.assert_called_once_with(self.waifu_memory, self.current_dere, self.dere_types, self.used_responses, False)


    def test_apply_transformations_talk_about(self):
        deftransform(self.transformations, "talk about interests", ["talk-about"])
        input_list = ["talk", "about", "interests"]
        with patch('topics.talk_about_interest', return_value = "I like reading manga") as mock_talk_about_interest:
            response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
            self.assertEqual(response, "I like reading manga")
            mock_talk_about_interest.assert_called_once_with(self.waifu_memory, self.current_dere, self.used_responses, False)


    def test_apply_transformations_introduce_topic(self):
        deftransform(self.transformations, "talk about family", ["introduce-topic", "family"])
        input_list = ["talk", "about", "family"]
        with patch('topics.introduce_topic', return_value="Let's talk about family") as mock_introduce_topic:
            response = apply_transformations(self.transformations, input_list, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, response_templates, self.used_responses, self.dere_types, False)
            self.assertEqual(response, "Let's talk about family")
            mock_introduce_topic.assert_called_once_with("family", self.waifu_memory, self.current_dere, self.used_responses, False)