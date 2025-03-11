from typing import List, Optional, Dict, Any, Tuple
from dere_manager import DereContext
from topic_introduction import maybe_introduce_topic
from topic_response import respond_based_on_current_topic
# Corrected imports:
from response_templates.tsundere import tsundere_responses
from response_templates.yandere import yandere_responses
from response_templates.kuudere import kuudere_responses
from response_templates.dandere import dandere_responses
from response_templates.himedere import himedere_responses

class TopicManager:
    def __init__(self, waifu_chatbot: Any):
        self.waifu_chatbot = waifu_chatbot
        self.waifu_memory = waifu_chatbot.waifu_memory
        self.dere_context = waifu_chatbot.dere_context
        self.current_topic: Optional[str] = None
        self.last_topic: Optional[str] = None
        self.last_topic_keyword: Optional[str] = None # Store the extracted topic keyword
        self.turns_since_last_topic: int = 0 # Counter for turns since last topic
        self.previous_input: str = "" # Store the previous input
        self.topic_dere: Optional[str] = None # Store the dere type when the topic was introduced
        self.topic_turns: int = 0 # Counter for turns since a topic-specific response
        self.max_topic_turns: int = 4 # Maximum turns to stay on a topic

        self.response_templates = {
            ("feeling", "tsundere"): tsundere_responses["feeling"],
            ("family", "tsundere"): tsundere_responses["family"],
            ("childhood", "tsundere"): tsundere_responses["childhood"],
            ("insult", "tsundere"): tsundere_responses["insult"],
            ("compliment", "tsundere"): tsundere_responses["compliment"],
            ("interest_manga", "tsundere"): tsundere_responses["interest_manga"],
            ("interest_anime", "tsundere"): tsundere_responses["interest_anime"],
            ("interest_games", "tsundere"): tsundere_responses["interest_games"],
            ("interest_cooking", "tsundere"): tsundere_responses["interest_cooking"],
            ("relationship_status", "tsundere"): tsundere_responses["relationship_status"],
            ("favorite_food", "tsundere"): tsundere_responses["favorite_food"],
            ("personality_quirks", "tsundere"): tsundere_responses["personality_quirks"],
            ("feeling", "yandere"): yandere_responses["feeling"],
            ("family", "yandere"): yandere_responses["family"],
            ("childhood", "yandere"): yandere_responses["childhood"],
            ("insult", "yandere"): yandere_responses["insult"],
            ("compliment", "yandere"): yandere_responses["compliment"],
            ("interest_manga", "yandere"): yandere_responses["interest_manga"],
            ("interest_anime", "yandere"): yandere_responses["interest_anime"],
            ("interest_games", "yandere"): yandere_responses["interest_games"],
            ("interest_cooking", "yandere"): yandere_responses["interest_cooking"],
            ("relationship_status", "yandere"): yandere_responses["relationship_status"],
            ("favorite_food", "yandere"): yandere_responses["favorite_food"],
            ("personality_quirks", "yandere"): yandere_responses["personality_quirks"],
            ("feeling", "kuudere"): kuudere_responses["feeling"],
            ("family", "kuudere"): kuudere_responses["family"],
            ("childhood", "kuudere"): kuudere_responses["childhood"],
            ("insult", "kuudere"): kuudere_responses["insult"],
            ("compliment", "kuudere"): kuudere_responses["compliment"],
            ("interest_manga", "kuudere"): kuudere_responses["interest_manga"],
            ("interest_anime", "kuudere"): kuudere_responses["interest_anime"],
            ("interest_games", "kuudere"): kuudere_responses["interest_games"],
            ("interest_cooking", "kuudere"): kuudere_responses["interest_cooking"],
            ("relationship_status", "kuudere"): kuudere_responses["relationship_status"],
            ("favorite_food", "kuudere"): kuudere_responses["favorite_food"],
            ("personality_quirks", "kuudere"): kuudere_responses["personality_quirks"],
            ("feeling", "dandere"): dandere_responses["feeling"],
            ("family", "dandere"): dandere_responses["family"],
            ("childhood", "dandere"): dandere_responses["childhood"],
            ("insult", "dandere"): dandere_responses["insult"],
            ("compliment", "dandere"): dandere_responses["compliment"],
            ("interest_manga", "dandere"): dandere_responses["interest_manga"],
            ("interest_anime", "dandere"): dandere_responses["interest_anime"],
            ("interest_games", "dandere"): dandere_responses["interest_games"],
            ("interest_cooking", "dandere"): dandere_responses["interest_cooking"],
            ("relationship_status", "dandere"): dandere_responses["relationship_status"],
            ("favorite_food", "dandere"): dandere_responses["favorite_food"],
            ("personality_quirks", "dandere"): dandere_responses["personality_quirks"],
            ("feeling", "himedere"): himedere_responses["feeling"],
            ("family", "himedere"): himedere_responses["family"],
            ("childhood", "himedere"): himedere_responses["childhood"],
            ("insult", "himedere"): himedere_responses["insult"],
            ("compliment", "himedere"): himedere_responses["compliment"],
            ("interest_manga", "himedere"): himedere_responses["interest_manga"],
            ("interest_anime", "himedere"): himedere_responses["interest_anime"],
            ("interest_games", "himedere"): himedere_responses["interest_games"],
            ("interest_cooking", "himedere"): himedere_responses["interest_cooking"],
            ("relationship_status", "himedere"): himedere_responses["relationship_status"],
            ("favorite_food", "himedere"): himedere_responses["favorite_food"],
            ("personality_quirks", "himedere"): himedere_responses["personality_quirks"],
        }

    maybe_introduce_topic = maybe_introduce_topic
    respond_based_on_current_topic = respond_based_on_current_topic