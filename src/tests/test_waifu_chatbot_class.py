import unittest
from unittest.mock import patch
from waifu_chatbot import WaifuChatbot
from transformations import deftransform
import pytest

class TestWaifuChatbot:

    def setup_method(self):
        self.chatbot = WaifuChatbot("TestWaifu")

    def test_initialization(self):
        assert self.chatbot.waifu_memory.name == "TestWaifu"
        assert self.chatbot.current_dere in self.chatbot.dere_types
        assert self.chatbot.greetings is not None
        assert self.chatbot.farewells is not None

    def test_defkeyword(self):
        self.chatbot.defkeyword("test", ["This is a test response."])
        assert "test" in self.chatbot.keywords
        assert len(self.chatbot.keywords["test"]) == 1

    def test_defsynonym(self):
        self.chatbot.defkeyword("hello", ["Hi there!"])
        self.chatbot.defsynonym("hi", "hello")
        # Now, modifying the *original* keyword should affect the synonym
        self.chatbot.keywords["hello"].append(("hello", "Another hello response!"))
        assert ("hello", "Another hello response!") in self.chatbot.keywords["hi"]

    def test_set_favorite_food(self):
        self.chatbot.set_favorite_food("sushi")
        assert self.chatbot.waifu_memory.favorite_food == "sushi"

    def test_respond_keyword(self):
        self.chatbot.defkeyword("hello", ["Hi there!"])
        response = self.chatbot.respond("hello")
        assert response == "Hi there!"
        assert self.chatbot.current_topic not in response if self.chatbot.current_topic else True

    def test_respond_transformation(self):
        self.chatbot.transformations = {}
        deftransform(self.chatbot.transformations, "my name is *", ["Nice to meet you, *!"], "name")
        response = self.chatbot.respond("my name is Alice")
        assert self.chatbot.waifu_memory.name.lower() == "alice".lower() # Correct assertion, case-insensitive
        assert response is None
        assert self.chatbot.current_topic not in response if self.chatbot.current_topic else True

    @patch('topics.introduce_topic', return_value="Test Topic Introduction")
    @patch('dere_types.maybe_change_dere', return_value="Test Dere Response")
    def test_respond_no_match(self, mock_maybe_change_dere, mock_introduce_topic):
        with patch('random.random', return_value=0.1):
            response = self.chatbot.respond("random input")
            # Check if it's *either* a topic introduction *or* a default dere response.
            assert response == "Test Topic Introduction" or response == "Test Dere Response"

    @patch('topics.introduce_topic', return_value="Test Topic Introduction")
    @patch('dere_types.dere_response', return_value="Test Dere Response")
    def test_introduce_topic(self, mock_dere_response, mock_introduce_topic):
        with patch('random.random', return_value=0.1):
            # Set up a current topic
            self.chatbot.current_topic = 'family'

            # Call respond with an input that won't match any keywords or transformations
            response = self.chatbot.respond("random input")

            # Verify that _respond_based_on_current_topic takes precedence
            mock_introduce_topic.assert_not_called()  # Should not introduce a new topic
            mock_dere_response.assert_called_once() # Check dere response was called.
            assert response == "Test Dere Response"

    @patch('topics.introduce_topic', return_value="Test Topic Introduction")
    def test_integrated_conversation_topic_persistence(self, mock_introduce_topic):
        with patch('random.random', return_value=0.1):
            # Introduce initial topic
            self.chatbot.respond("random input")
            self.chatbot.current_topic = "family"
            initial_topic = self.chatbot.current_topic
            # Add keyword to clear topic
            self.chatbot.defkeyword("clear", ["clearing"])

            if initial_topic:
                # Simulate next response with a keyword, topic should be reset
                self.chatbot.respond("clear")
                assert self.chatbot.current_topic is None

    def test_respond_memory(self):
        self.chatbot.transformations = {}
        deftransform(self.chatbot.transformations, "my name is *", ["Nice to meet you, *!"], "name")
        self.chatbot.respond("my name is Bob")
        assert self.chatbot.waifu_memory.name.lower() == "bob".lower() #Correct assertion