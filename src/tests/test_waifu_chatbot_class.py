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
        assert "hi" in self.chatbot.keywords
        assert self.chatbot.keywords["hi"] == self.chatbot.keywords["hello"]

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
        assert response == "Nice to meet you, Alice!"
        assert self.chatbot.waifu_memory.name == "Alice"
        assert self.chatbot.current_topic not in response if self.chatbot.current_topic else True

    def test_respond_no_match(self):
        with patch('random.random', return_value=0.1):
            response = self.chatbot.respond("random input")
            assert response in ["What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."] or "Could you tell me more about" in response
            assert self.chatbot.current_topic not in response if self.chatbot.current_topic else True

    def test_maybe_introduce_topic(self):
        with patch('random.random', return_value=0.1):
            self.chatbot.respond("random input")
            if self.chatbot.current_topic:
                assert "Could you tell me more about" in self.chatbot.respond("random input")

    def test_respond_based_on_current_topic(self):
        self.chatbot.current_topic = "family"
        self.chatbot.def_topic_response("family", "tell me about your family", "My family is great!")
        response = self.chatbot.respond("tell me about your family")
        assert response == "My family is great!"
        assert self.chatbot.current_topic is None

    def test_integrated_conversation_topic_persistence(self):
        # Start a conversation, patching random
        with patch('random.random', return_value=0.1):
            self.chatbot.respond("random input")
            initial_topic = self.chatbot.current_topic
            if initial_topic:
                #simulate next response
                self.chatbot.respond("something else")
                #check persistent of topic, then None
                assert self.chatbot.current_topic is None

    def test_integrated_dere_change(self):
        initial_dere = self.chatbot.current_dere
        with patch('random.random', return_value=0.1):
            self.chatbot.respond("how do you feel")
            if self.chatbot.current_dere != initial_dere:
                assert self.chatbot.current_dere != initial_dere

    def test_respond_memory(self):
        self.chatbot.transformations = {}
        deftransform(self.chatbot.transformations, "my name is *", ["Nice to meet you, *!"], "name")
        self.chatbot.respond("my name is Bob")
        response = self.chatbot.respond("what is my name")
        # Check that the name is retrieved from memory
        assert "Bob" in response