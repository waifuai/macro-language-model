from typing import List, Dict, Any, Optional, Set, Tuple, Callable
from personalities.personality_interface import PersonalityInterface
from personalities.deredere.data import deredere_responses, deredere_default_responses
import random
from utils import tokenize, matches
from transformations import apply_transformations
from keyword_handler import handle_keywords


class DeredereLogic(PersonalityInterface):

    def __init__(self, debug: bool = False):
        self.debug = debug

    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        """Generates a response to the user's input."""
        keyword_response = self.handle_keywords(input_tokens, context["waifu_chatbot"].registry.keywords, self.debug)
        if keyword_response:
            return keyword_response

        topic_response = self.handle_topic_response(input_tokens, context["waifu_chatbot"].registry.keywords, {}, self.debug)
        if topic_response:
            return topic_response

        transformed_response = self.handle_transformations(context["waifu_chatbot"].registry.transformations, input_tokens, context["waifu_memory"], self.talk_about_interest, self.introduce_topic, self.debug, context)
        if transformed_response:
            return transformed_response
        return self.get_default_response(context)

    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
        """Introduces a new topic."""
        # Deredere-specific topic introductions
        introductions = {
            "family": "Hey, let's talk about family! What are they like?",
            "childhood": "Ooh, childhood memories! Tell me about yours!",
            "feelings": "How are you feeling right now? Let's share!",
            "interest_manga": "I love manga! What are you reading?",  # Specific
            "interest_anime": "Anime is awesome! What are you watching?",  # Specific
            "interest_games": "Let's play some games! What are your favorites?",  # Specific
            "interest_cooking": "I love to cook! What's your favorite dish to make?",  # Specific
            "relationship_status": "So, what's your relationship status? Spill the tea!",
            "favorite_food": "I love talking about food! What's your favorite?",
            "personality_quirks": "Everyone has quirks! What are some of yours?",
        }
        return introductions.get(topic, f"Let's talk about {topic}! I'm so excited!")

    def get_default_response(self, context: Dict[str, Any]) -> str:
        """Gets a default response."""
        if self.debug:
            print("DeredereLogic: Getting default response")

        used_responses = context["conversation_context"].used_responses
        unused_responses = [resp for resp in deredere_default_responses if resp not in used_responses]

        if unused_responses:
            response = random.choice(unused_responses)
            used_responses.add(response)
            return response
        else:
            used_responses.clear()
            return random.choice(deredere_default_responses)

    def get_data(self) -> Dict[str, Any]:
        """Gets personality-specific data."""
        return {"responses": deredere_responses, "default_responses": deredere_default_responses}

    def handle_transformations(self, transformations: Dict[str, Tuple[Any, Optional[str], int]], input_list: List[str], waifu_memory: Any, talk_about_interest: Callable[..., str], introduce_topic: Callable[..., str], debug: bool, context: Dict[str, Any]) -> Optional[str]:
        """Applies transformations to the input and returns a transformed response."""
        return apply_transformations(transformations, input_list, waifu_memory, "deredere", talk_about_interest, introduce_topic, lambda context, *responses: self.get_default_response(context), {}, set(), [], self.debug, context["waifu_chatbot"])


    def handle_keywords(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], debug: bool) -> Optional[str]:
        """Handles general keywords."""
        return handle_keywords(tokens, keywords, set(), self.debug)

    def handle_topic_response(self, tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], response_templates: Dict[tuple[str, str], List[str]], debug: bool) -> Optional[str]:
        """Handles topic responses"""
        # Simplified logic, just returns None, as the logic is now in `generate_response`
        return None
    
    def maybe_introduce_topic(self, context: Dict[str, Any], input_str: str, turn_count: int) -> Optional[str]:
        """Introduces a new topic based on affection level, randomness, and topic counts."""
        topic_manager = context["waifu_chatbot"].topic_manager
        if self.debug:
            print(f"DeredereLogic.maybe_introduce_topic: Entering with input: {input_str}, turn: {turn_count}")
        if (topic_manager.waifu_memory.affection > 20 and  # Reduced affection threshold
                random.random() < 0.5 and  # Increased probability
                (topic_manager.last_topic_keyword is None or topic_manager.last_topic_keyword not in input_str) and
                topic_manager.turns_since_last_topic >= 4):  # Reduced turns_since_last_topic

            available_topics = [
                "family",
                "childhood",
                "feelings",
                "interest_manga",
                "interest_anime",
                "interest_games",
                "interest_cooking",
                "relationship_status",
                "favorite_food",
                "personality_quirks",
            ]

            # Initialize topic counts if not already present
            for topic in available_topics:
                if topic not in topic_manager.waifu_memory.topic_counts:
                    topic_manager.waifu_memory.topic_counts[topic] = 0

            # Filter out last topic if exists
            if topic_manager.last_topic in available_topics:
                available_topics.remove(topic_manager.last_topic)

            if available_topics:
                # Create a list of (topic, count) tuples and sort by count
                topic_counts = [(topic, topic_manager.waifu_memory.topic_counts[topic]) for topic in available_topics]
                topic_counts.sort(key=lambda x: x[1])  # Sort by count (ascending)

                # Get the topics with the lowest count
                min_count = topic_counts[0][1]
                min_count_topics = [topic for topic, count in topic_counts if count == min_count]

                # Choose a random topic from the topics with the lowest count
                new_topic = random.choice(min_count_topics)

                response = self.introduce_topic(new_topic, {"waifu_memory": topic_manager.waifu_memory, "debug": self.debug})

                topic_manager.current_topic = new_topic

                # Increment the topic count
                topic_manager.waifu_memory.topic_counts[new_topic] += 1
                if self.debug:
                    print(f"TopicManager.maybe_introduce_topic: Introduced topic: {new_topic}")
                # Extract and store the topic keyword

                topic_manager.last_topic_keyword = new_topic  # Store topic directly
                if self.debug:
                    print(f"TopicManager.maybe_introduce_topic: Stored topic keyword: {topic_manager.last_topic_keyword}")
                topic_manager.turns_since_last_topic = 0  # Reset the counter
                topic_manager.topic_turns = 2  # Reduced topic_turns
                print(f"TopicManager.maybe_introduce_topic: topic_turns set to: {topic_manager.topic_turns}")  # DEBUG
                topic_manager.waifu_chatbot.response_generator.topic_context = True  # Set topic_context
                return response
        topic_manager.turns_since_last_topic += 1  # Increment the counter
        topic_manager.last_topic = None  # Reset last_topic if no new topic is introduced
        topic_manager.last_topic_keyword = None  # Reset the keyword as well
        return None

    def respond_based_on_current_topic(self, context: Dict[str, Any], tokens: List[str], keywords: Dict[str, List[Tuple[str, Any]]], context_dict: Dict[str, Any], response_templates: Dict[tuple[str, str], List[str]]) -> Optional[str]:
        """Responds based on the current topic, if any."""
        topic_manager = context["waifu_chatbot"].topic_manager
        if self.debug:
            print(f"DeredereLogic.respond_based_on_current_topic: Entering with tokens: {tokens}")
        if topic_manager.current_topic:
            if self.debug:
                print(f"DeredereLogic.respond_based_on_current_topic: Current topic: {topic_manager.current_topic}, topic_turns: {topic_manager.topic_turns}")

            # Check if user input relates to the current topic
            input_relates_to_topic = False
            for token in tokens:
                # Check if the token is the topic itself or a synonym
                if token == topic_manager.current_topic or (topic_manager.current_topic in topic_manager.waifu_chatbot.registry.keywords and token in topic_manager.waifu_chatbot.registry.keywords and topic_manager.waifu_chatbot.registry.keywords.get(token) == topic_manager.waifu_chatbot.registry.keywords.get(topic_manager.current_topic)):
                    input_relates_to_topic = True
                    break
            print(f"DeredereLogic.respond_based_on_current_topic: input_relates_to_topic = {input_relates_to_topic}")  # DEBUG

            if topic_manager.topic_turns > 0:  # Only respond if topic_turns > 0
                if topic_manager.current_topic in keywords:
                    for resp_pattern, resp_text in keywords[topic_manager.current_topic]:
                        if matches(tokenize(resp_pattern), tokens):
                            context_dict["conversation_context"].used_responses.add(resp_text)
                            if self.debug:
                                print(f"DeredereLogic.respond_based_on_current_topic: Found response: {resp_text}")
                            return resp_text

                # If we have a current_topic, but no specific keyword was found:
                # Deredere-specific responses based on topic
                if topic_manager.current_topic in deredere_responses:
                    responses = deredere_responses[topic_manager.current_topic]
                    unused_responses = [resp for resp in responses if resp not in context_dict["conversation_context"].used_responses]
                    if unused_responses:
                        response = random.choice(unused_responses)
                        context_dict["conversation_context"].used_responses.add(response)
                        return response

                if self.debug:
                    print(f"DeredereLogic.respond_based_on_current_topic: Before decrement, topic_turns = {topic_manager.topic_turns}")
                topic_manager.topic_turns -= 1
                print(f"DeredereLogic.respond_based_on_current_topic: topic_turns after decrement: {topic_manager.topic_turns}")  # DEBUG
                if self.debug:
                    print(f"DeredereLogic.respond_based_on_current_topic: After decrement, topic_turns = {topic_manager.topic_turns}")

                if topic_manager.topic_turns == 0:
                    topic_manager.current_topic = None  # Reset the topic when turns run out
                topic_manager.turns_since_last_topic = 0  # Reset the counter
                topic_manager.waifu_chatbot.response_generator.topic_context = False  # Reset topic_context

                return None # No specific response found
            else:
                if self.debug:
                    print(f"DeredereLogic.respond_based_on_current_topic: No more topic turns remaining")
                topic_manager.current_topic = None  # Reset if no current topic
                topic_manager.turns_since_last_topic = 0  # Reset turns_since_last_topic

        if topic_manager.topic_turns <= 0 or not input_relates_to_topic:
            if self.debug:
                print("DeredereLogic.respond_based_on_current_topic: Exiting topic due to no engagement or turns limit")
            topic_manager.current_topic = None
            topic_manager.turns_since_last_topic = 0

        return None

    def talk_about_interest(self, waifu_memory: Any, current_dere: str, used_responses: List[str], debug: bool) -> str:
        """Generates a deredere-specific response about a random interest."""
        interests = {
            "reading manga": "You know, I've been reading this really great manga lately. It's about a magical girl fighting evil. You should check it out! We could even read it together!",
            "watching anime": "I just finished watching this amazing anime. It's a slice-of-life anime with beautiful animation. I cried at the end! Let's watch something together sometime!",
            "playing video games": "I'm so addicted to this new game! It's a JRPG where you have to collect rare items. Wanna play with me sometime? It'll be so much fun!",
            "cooking": "I made these cookies for us! They're pocky flavored. I hope you like them! Let's enjoy them together!",
        }
        if not waifu_memory.interests:
            return "What are you talking about? I love lots of things!"  # Deredere-style default response

        interest = random.choice(waifu_memory.interests)
        return interests.get(interest, "Hmm, what should we talk about? I'm up for anything!")