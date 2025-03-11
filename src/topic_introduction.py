import random
from typing import List, Optional, Dict, Any, Tuple
from dere_manager import DereContext, dere_response
from utils import tokenize, matches
from topics import introduce_topic
from conversation_context import ConversationContext
from response_generation import generate_response
import re

def maybe_introduce_topic(self, input_str: str, turn_count: int) -> Optional[str]:
    """Introduces a new topic based on affection level, randomness, and topic counts."""
    if self.waifu_chatbot.debug:
        print(f"TopicManager.maybe_introduce_topic: Entering with input: {input_str}, turn: {turn_count}")
    if (self.waifu_memory.affection > 20 and  # Reduced affection threshold
            random.random() < 0.5 and  # Increased probability
            (self.last_topic_keyword is None or self.last_topic_keyword not in input_str) and
            self.turns_since_last_topic >= 4):  # Reduced turns_since_last_topic

        available_topics = [
            "family",
            "childhood",
            "feelings",
            "interest_manga", # Changed to specific interest
            "interest_anime", # Changed to specific interest
            "interest_games", # Changed to specific interest
            "interest_cooking", # Changed to specific interest
            "relationship_status",
            "favorite_food",
            "personality_quirks",
        ]

        # Initialize topic counts if not already present
        for topic in available_topics:
            if topic not in self.waifu_memory.topic_counts:
                self.waifu_memory.topic_counts[topic] = 0

        # Filter out last topic if exists
        if self.last_topic in available_topics:
            available_topics.remove(self.last_topic)

        if available_topics:
            # Create a list of (topic, count) tuples and sort by count
            topic_counts = [(topic, self.waifu_memory.topic_counts[topic]) for topic in available_topics]
            topic_counts.sort(key=lambda x: x[1])  # Sort by count (ascending)

            # Get the topics with the lowest count
            min_count = topic_counts[0][1]
            min_count_topics = [topic for topic, count in topic_counts if count == min_count]

            # Choose a random topic from the topics with the lowest count
            new_topic = random.choice(min_count_topics)

            # More natural and dere-specific topic introductions
            dere_introductions = {
                "tsundere": {
                    "family": "It's not like I care, b-baka, but what's your family like?",
                    "childhood": "Hmph, I bet your childhood was boring. Tell me about it anyway.",
                    "feelings": "Don't get the wrong idea! I'm not asking because I care, but... what are you feeling?",
                    "interest_manga": "I-It's not like I want to know, but what manga are you reading?", # Specific
                    "interest_anime": "Baka! Don't think I care, but what anime are you watching?", # Specific
                    "interest_games": "Hmph. I bet you're not very good, but what games do you play?", # Specific
                    "interest_cooking": "It's not like I'll cook for you, but what do you like to cook?", # Specific
                    "relationship_status": "It's none of your business, but... what's your relationship status?",
                    "favorite_food": "B-baka! Tell me your favorite food... not that I'll make it for you!",
                    "personality_quirks": "Hmph. Do you have any weird quirks? Not like I care.",
                },
                "yandere": {
                    "family": "Tell me everything about your family. I need to know who might interfere with us.",
                    "childhood": "I want to know everything about your past. Every single detail.",
                    "feelings": "Tell me your deepest feelings. I'm the only one who understands you.",
                    "interest_manga": "We should share all our interests. Tell me about your favorite manga.", # Specific
                    "interest_anime": "You'll watch anime with me, and only me. What are you watching?", # Specific
                    "interest_games": "We'll play games together, forever. What are your favorites?", # Specific
                    "interest_cooking": "I'll cook anything for you. What do you enjoy?", # Specific
                    "relationship_status": "We're meant to be together, so tell me about your relationship history.",
                    "favorite_food": "Your favorite food is my favorite food. Tell me what it is!",
                    "personality_quirks": "I love everything about you, even your quirks. Tell me.",
                },
                "kuudere": {
                    "family": "Family is a social construct. Tell me about yours.",
                    "childhood": "Childhood experiences shape individuals. Describe yours.",
                    "feelings": "Feelings are fleeting. What are you experiencing?",
                    "interest_manga": "Manga is a form of literature. What are you reading?", # Specific
                    "interest_anime": "Anime is a visual medium. What are you watching?", # Specific
                    "interest_games": "Games are interactive entertainment. What do you play?", # Specific
                    "interest_cooking": "Cooking is a practical skill. What do you make?", # Specific
                    "relationship_status": "Relationship status is a label. What is yours?",
                    "favorite_food": "Sustenance is necessary. What is your preferred food?",
                    "personality_quirks": "Quirks are deviations from the norm. Describe yours.",
                },
                "dandere": {
                    "family": "U-um... could you tell me about your family...?",
                    "childhood": "I-I was wondering... what was your childhood like...?",
                    "feelings": "A-are you feeling okay...?  Maybe we could talk about feelings...",
                    "interest_manga": "U-um... do you like manga...?", # Specific
                    "interest_anime": "I-I'm a little shy, but... do you watch anime...?", # Specific
                    "interest_games": "D-do you... um... play any games...?", # Specific
                    "interest_cooking": "S-sorry... do you like to cook...?", # Specific
                    "relationship_status": "I-I'm a little shy, but... um... what's your relationship status...?",
                    "favorite_food": "M-maybe we could share our favorite foods...?  If you want...",
                    "personality_quirks": "S-sorry if I'm awkward... Do you have any quirks...?",
                },
                "himedere": {
                    "family": "Your family should be honored to be in my presence. Tell me about them.",
                    "childhood": "I assume your childhood was unremarkable. Prove me wrong.",
                    "feelings": "As a princess, my feelings are paramount. But tell me yours, peasant.",
                    "interest_manga": "You should be reading manga worthy of my attention. What is it?", # Specific
                    "interest_anime": "Only the finest anime for me. What are you watching?", # Specific
                    "interest_games": "I only play the most exquisite games. What do you play?", # Specific
                    "interest_cooking": "Only the finest cuisine will do. What do you cook?", # Specific
                    "relationship_status": "You should be grateful to even be considered. What's your relationship status?",
                    "favorite_food": "Only the finest foods for me. What do *you* eat, commoner?",
                    "personality_quirks": "My quirks are perfection. What are yours, I wonder?",
                },
                "deredere": {
                    "family": "Hey, let's talk about family! What are they like?",
                    "childhood": "Ooh, childhood memories! Tell me about yours!",
                    "feelings": "How are you feeling right now? Let's share!",
                    "interest_manga": "I love manga! What are you reading?", # Specific
                    "interest_anime": "Anime is awesome! What are you watching?", # Specific
                    "interest_games": "Let's play some games! What are your favorites?", # Specific
                    "interest_cooking": "I love to cook! What's your favorite dish to make?", # Specific
                    "relationship_status": "So, what's your relationship status? Spill the tea!",
                    "favorite_food": "I love talking about food! What's your favorite?",
                    "personality_quirks": "Everyone has quirks! What are some of yours?",
                }
            }
            response = dere_introductions.get(self.dere_context.current_dere, {}).get(new_topic, f"Let's talk about {new_topic}.")
            if self.waifu_chatbot.debug:
                print(f"TopicManager.maybe_introduce_topic: Using intro: {response}")

            self.current_topic = new_topic
            self.topic_dere = self.dere_context.current_dere  # Store the current dere type

            # Increment the topic count
            self.waifu_memory.topic_counts[new_topic] += 1
            if self.waifu_chatbot.debug:
                print(f"TopicManager.maybe_introduce_topic: Introduced topic: {new_topic}")
            # Extract and store the topic keyword

            self.last_topic_keyword = new_topic  # Store topic directly
            if self.waifu_chatbot.debug:
                print(f"TopicManager.maybe_introduce_topic: Stored topic keyword: {self.last_topic_keyword}")
            self.turns_since_last_topic = 0  # Reset the counter
            self.topic_turns = 2  # Reduced topic_turns
            print(f"TopicManager.maybe_introduce_topic: topic_turns set to: {self.topic_turns}") # DEBUG
            self.waifu_chatbot.response_generator.topic_context = True  # Set topic_context
            return response
    self.turns_since_last_topic += 1  # Increment the counter
    self.last_topic = None  # Reset last_topic if no new topic is introduced
    self.last_topic_keyword = None  # Reset the keyword as well
    # self.topic_dere = None  # Removed: Only reset when a NEW topic is introduced
    return None