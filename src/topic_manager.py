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

        # REMOVED response_templates initialization

    maybe_introduce_topic = maybe_introduce_topic
    respond_based_on_current_topic = respond_based_on_current_topic