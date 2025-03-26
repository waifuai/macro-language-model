from typing import List, Dict, Any, Optional
from personalities.personality_interface import PersonalityInterface
from .defaults import get_default_response
from topic_manager import TopicManager
from topics import talk_about_interest
from memory import remember
from dere_data.deredere import deredere_default_responses
import random

class DeredereLogic(PersonalityInterface):
    def __init__(self, debug: bool):
        self.debug = debug
        self.topic_manager = None
        self.waifu_chatbot = None
        self.last_response_was_question: bool = False # Track if last response was a question

    def generate_response(self, input_tokens: List[str], context: Dict[str, Any]) -> str:
        if self.waifu_chatbot is None:
            self.waifu_chatbot = context["waifu_chatbot"]
            self.topic_manager = TopicManager(self.waifu_chatbot)

        # Introduce a new topic sometimes
        maybe_topic_response = self.maybe_introduce_topic(" ".join(input_tokens), context["waifu_chatbot"].turn_count)
        if maybe_topic_response:
            return maybe_topic_response

        # Prioritize topic response if a topic is active
        if self.topic_manager.get_current_topic():
            topic_response = self.topic_manager.generate_topic_response(self.topic_manager.get_current_topic(), input_tokens)
            self.topic_manager.decrement_topic_turns()
            if topic_response:
                return topic_response

        # Probabilistic response selection (if no active topic)
        choice = random.random()
        input_str = " ".join(input_tokens) # Join tokens for easier checks
        response = "" # Initialize response
        current_response_is_question = False # Track if the *selected* response is a question

        # Very low chance for random interest/default
        if choice < 0.01: # 1% interest
            response = talk_about_interest(context["waifu_memory"], context["current_dere"], [], self.debug)
        elif choice < 0.03: # 2% basic default
             response = random.choice(deredere_default_responses)
        else: # Main fallback logic (97% chance)
            # Reactions to statements (less prompting)
            statement_reactions = [
                "Wow, really?!", "That sounds super interesting!", "No way!",
                "Ooh, exciting!", "Sounds like fun!", "That's amazing!",
                "Seriously? That's wild!", "Awesome!", "Hehe, okay!",
                "Oh wow!", "Uh-huh!", "Okay!", "Totally!", "Right?!",
            ]
            # Answers/deflections to user questions - MORE ANSWERS
            question_reactions = [
                 "Good question! What do *you* think?", # Deflect
                 "Hmm, let me think... hehe!", # Deflect
                 "That's a fun question! My answer is... maybe! 😉", # Deflect
                 "I'm not sure! Let's brainstorm together!", # Collaborate
                 "You tell me first!", # Challenge
                 "Hehe, secrets!", # Deflect
                 "Why do you ask? 😊", # Deflect
                 "I was just thinking the same thing!", # Agree/Answer
                 "Probably!", # Answer
                 "Definitely!", # Answer
                 "I think so!", # Answer
                 "Just relaxing!", # Answer (generic activity)
                 "Thinking about you!", # Answer (deredere classic)
                 "Not much, just hanging out!", # Answer (generic activity)
                 "The usual!", # Answer (generic)
            ]
            # Prompts (use sparingly)
            prompt_reactions = [ # Mostly questions
                "Tell me more!", "Go on!", "I'm listening!", "And then?", "What else?",
                "Keep going!",
            ]

            user_asked_question = input_str.endswith('?')

            # --- Response Selection ---
            if user_asked_question:
                 # User asked a question -> Waifu MUST answer/deflect.
                 response = random.choice(question_reactions)
                 current_response_is_question = response.endswith('?') # Check if the *answer* is also a question
            elif self.last_response_was_question:
                 # User made a statement after waifu asked -> Waifu should react strongly.
                 response = random.choice(statement_reactions)
                 current_response_is_question = False
            else:
                 # User made a statement, waifu didn't just ask. Primarily react.
                 if random.random() < 0.85: # 85% chance to react
                     response = random.choice(statement_reactions)
                     current_response_is_question = False
                 else: # 15% chance to prompt
                     response = random.choice(prompt_reactions)
                     # Check if the prompt itself is a question
                     current_response_is_question = response.endswith('?') or response in ["Tell me more!", "Go on!", "I'm listening!", "Keep going!"]


        # --- Follow-up Logic ---
        # Add a short follow-up question *very* infrequently, only if waifu made a statement.
        if not current_response_is_question and not self.last_response_was_question and random.random() < 0.10: # Reduced chance to 10%
            follow_ups = [ "Right?", "What do you think?", "How about you?" ]
            response += f" {random.choice(follow_ups)}"
            current_response_is_question = True

        # Update state for next turn *before* final cleanup
        self.last_response_was_question = current_response_is_question

        # Final cleanup
        response = response.replace("..", ".").replace("!!", "!").replace("??", "?").strip()
        if response.count('?') > 1:
            first_q_index = response.find('?')
            response = response[:first_q_index+1]

        # Ensure response isn't empty
        if not response:
             response = random.choice(["Hehe!", "Okay!", "Wow!"]) # Safe default

        return response


    def introduce_topic(self, topic: str, context: Dict[str, Any]) -> Optional[str]:
        # Ensure standard apostrophe is used
        if topic == "family":
            return "Hey, let's chat about family! What are they like?" # Standard apostrophe
        elif topic == "food":
            return "Hey, let's talk about food! What's your favorite thing to eat?" # Standard apostrophe
        elif topic == "games":
            return "Hey, let's talk about games! What do you like to play?" # Standard apostrophe
        return None

    def maybe_introduce_topic(self, input_str: str, turn_count: int) -> Optional[str]:
        if random.random() < 0.2 and turn_count % 3 == 0:  # Every 3 turns, 20% chance
            topics = ["family", "food", "games"]
            return self.topic_manager.maybe_introduce_topic(input_str, turn_count, random.choice(topics))
        return None

    def get_default_response(self, context: Dict[str, Any]) -> str:
        return get_default_response(context)

    def get_data(self) -> Dict[str, Any]:
        return {}

    def talk_about_interest(self, waifu_memory: Any, current_dere: str, used_responses: List[str], debug: bool) -> str:
        return talk_about_interest(waifu_memory, current_dere, used_responses, debug)

    def remember(self, waifu_memory: Any, slot: str, value: str, affection_change: int = 0) -> None:
        return remember(waifu_memory, slot, value, affection_change)
