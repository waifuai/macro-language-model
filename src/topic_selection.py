import random
from typing import Optional

def select_new_topic(self) -> Optional[str]:
    available_topics = [
        "family", "childhood", "feelings", "interest_manga", "interest_anime",
        "interest_games", "interest_cooking", "relationship_status", "favorite_food",
        "personality_quirks"
    ]
    for topic in available_topics:
        if topic not in self.waifu_memory.topic_counts:
            self.waifu_memory.topic_counts[topic] = 0
    if self.last_topic in available_topics:
        available_topics.remove(self.last_topic)
    if not available_topics:
        return None
    topic_counts = [(topic, self.waifu_memory.topic_counts[topic]) for topic in available_topics]
    topic_counts.sort(key=lambda x: x[1])
    min_count = topic_counts[0][1]
    min_count_topics = [topic for topic, count in topic_counts if count == min_count]
    return random.choice(min_count_topics)