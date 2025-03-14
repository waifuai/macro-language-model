from typing import Optional
import random
from topic_selection import select_new_topic
from topic_responses import generate_topic_response

def maybe_introduce_topic(self, input_str: str, turn_count: int) -> Optional[str]:
    if self.waifu_chatbot.debug:
        print(f"TopicManager.maybe_introduce_topic: Input: {input_str}, Turn: {turn_count}")
    if (self.waifu_memory.affection > 20 and
            random.random() < 0.5 and
            (self.last_topic_keyword is None or self.last_topic_keyword not in input_str) and
            self.turns_since_last_topic >= 4):
        new_topic = select_new_topic(self)
        if new_topic:
            response = generate_topic_response(self, new_topic)
            self.current_topic = new_topic
            self.waifu_memory.topic_counts[new_topic] += 1
            self.last_topic_keyword = new_topic
            self.turns_since_last_topic = 0
            self.topic_turns = 2
            self.waifu_chatbot.response_generator.topic_context = True
            if self.waifu_chatbot.debug:
                print(f"Introduced topic: {new_topic}")
            return response
    self.turns_since_last_topic += 1
    self.last_topic = None
    self.last_topic_keyword = None
    return None