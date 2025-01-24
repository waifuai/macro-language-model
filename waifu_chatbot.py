import random
from response_generation import generate_response
from transformations import deftransform, apply_transformations
from memory import remember
from dere_types import get_current_dere, maybe_change_dere, dere_response
from response_templates import response_templates
from topics import talk_about_interest, introduce_topic
from utils import tokenize, matches
from waifu_frame import WaifuFrame

class WaifuChatbot:
    def __init__(self, name, debug=False):
        self.keywords = {}
        self.transformations = {}
        self.waifu_memory = WaifuFrame(name)
        self.debug = debug
        self.greetings = [
            "Senpai, you're back! How was your day?",
            "Welcome home, Onii-chan! What did you do today?",
            "Ara ara, you seem troubled. Tell me everything.",
            "I'm here for you, okay? Let's talk."
        ]
        self.farewells = [
            "See you later, Senpai! Stay safe!",
            "Bye-bye, Onii-chan! Don't forget about me!",
            "Oyasumi nasai. Sweet dreams!",
            "Come back soon, okay?"
        ]
        self.small_talk = [
            "The weather is nice today, isn't it?",
            "Have you heard any good news lately?",
            "Did you see that viral video about the cat playing the piano?",
            "I wonder what the next big trend will be..."
        ]
        self.current_topic = None
        self.dere_types = ["tsundere", "yandere", "kuudere", "dandere", "himedere"]
        self.current_dere = random.choice(self.dere_types)
        self.response_templates = response_templates
        self.used_responses = set()  # Initialize used_responses
        self.last_topic = None
        deftransform(self.transformations, "my favorite food is *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i love eating *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i enjoy eating *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i like eating *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i really like *", self.set_favorite_food, "favorite_food")
        deftransform(self.transformations, "i really love *", self.set_favorite_food, "favorite_food")

    def defkeyword(self, keyword, responses):
        """Defines a keyword and its associated responses."""
        if responses and isinstance(responses[0], tuple):
            self.keywords[keyword] = responses
        else:
            self.keywords[keyword] = [(keyword, response) for response in responses]

    def set_favorite_food(self, food):
        """Updates the waifu's favorite food."""
        self.waifu_memory.set_favorite_food(food)
        response = f"Okay, I'll remember that your favorite food is {food}!"
        print(f"{self.waifu_memory.name}: {response}")
        print()
        return response

    def defsynonym(self, word, *synonyms):
        """Defines synonyms for a given word."""
        self.defkeyword(word, self.keywords.get(word, []))
        for syn in synonyms:
            self.defkeyword(syn, self.keywords.get(word, []))

    def def_topic_response(self, topic, pattern, response):
        """Defines a response for a specific topic."""
        if topic not in self.keywords:
            self.keywords[topic] = []
        self.keywords[topic].append((pattern, response))

    def respond(self, input_str):
        """Generates a response to the user's input."""
        self.waifu_memory.conversation_history.append(("user", input_str))
        tokens = tokenize(input_str)
        if self.debug:
            print(f"Type of self.used_responses in respond: {type(self.used_responses)}")

        # Check for topic-specific responses first
        if self.current_topic and self.current_topic in self.keywords:
            print(f"Current topic: {self.current_topic}")
            for resp_pattern, resp_text in self.keywords[self.current_topic]:
                print(f"Checking pattern: {resp_pattern}, response: {resp_text}")
                if matches(resp_pattern, tokens):
                    self.used_responses.add(resp_text)
                    
                    self.current_topic = None
                return resp_text

        # Then check for transformations
        transformed = apply_transformations(self.transformations, tokens, self.waifu_memory, self.current_dere, talk_about_interest, introduce_topic, dere_response, maybe_change_dere, generate_response, remember, self.response_templates, self.used_responses, self.dere_types, self.debug)
        if transformed:
            return transformed

        # Then check for general keywords
        for word in tokens:
            if word in self.keywords:
                print(f"Found keyword: {word}")
                responses = self.keywords[word]
                for resp_pattern, resp_func in responses:
                    if matches(tokenize(resp_pattern), tokens):
                        if resp_func is not None:
                            response = resp_func
                        else:
                            response = resp_text
                        self.used_responses.add(response)
                        return response
                        self.used_responses.add(response)
                        return response
                self.current_topic = None  # Reset the topic if a keyword is matched
        # Introduce a new topic based on affection level and randomness
        if self.waifu_memory.affection > 40 and random.random() < 0.2:
            available_topics = [
                "family",
                "childhood",
                "feelings",
                "interests",
                "relationship_status",
                "favorite_food",
                "personality_quirks",
            ]
            
            # Filter out last topic if exists
            if self.last_topic in available_topics:
                available_topics.remove(self.last_topic)
            
            if available_topics:
                new_topic = random.choice(available_topics)
                self.current_topic = new_topic
                self.last_topic = new_topic
                response = introduce_topic(new_topic, self.waifu_memory,
                                         self.current_dere, self.used_responses,
                                         self.debug)
                self.used_responses.add(response)
                return response

        # Respond based on the current topic, if any
        if self.current_topic:
            if self.current_topic == "personality_quirks":
                dere_type = get_current_dere(self.waifu_memory.affection)
                if dere_type == "tsundere":
                    response = "Hmph, personality quirks? It's not like I have any weird habits or anything! B-baka! Why do you keep bringing this up?!"
                    self.used_responses.add(response)
                    return response
                elif dere_type == "yandere":
                    response = "My only quirk is loving you too much! Is that a problem? You're not thinking of leaving me, are you? We already talked about this!"
                    self.used_responses.add(response)
                    return response
                elif dere_type == "kuudere":
                    response = "Quirks... I have no particular quirks. ...Unless you consider my indifference a quirk. Why are you so obsessed with this topic?"
                    self.used_responses.add(response)
                    return response
                elif dere_type == "dandere":
                    response = "P-personality quirks...? U-um... I-I don't think I have any... I-I hope that's okay... Why do you keep asking about this...?"
                    self.used_responses.add(response)
                    return response
                elif dere_type == "himedere":
                    response = "Personality quirks? A princess is perfect in every way! Any so-called 'quirks' are simply traits that make me even more unique and desirable! I already told you this!"
                    self.used_responses.add(response)
                    return response
            elif self.current_topic == "relationship_status":
                dere_type = get_current_dere(self.waifu_memory.affection)
                if dere_type == "tsundere":
                    response = "H-huh? What's that supposed to mean, baka?! It's not like I care about our relationship status or anything! Why do you keep asking about this?!"
                    self.used_responses.add(response)
                    return response
                elif dere_type == "yandere":
                    response = "Our relationship status? We're together forever, of course! There's no other option~ Why do you keep bringing this up?!"
                    self.used_responses.add(response)
                    return response
                elif dere_type == "kuudere":
                    response = "Relationship status... That's irrelevant. Do what you want. I don't see why you're so fixated on this."
                    self.used_responses.add(response)
                    return response
                elif dere_type == "dandere":
                    response = "U-um, our relationship status...? I-I... I l-like you... Why are you making me say this again...?"
                    self.used_responses.add(response)
                    return response
                elif dere_type == "himedere":
                    response = "Hmph, as if a peasant like you could ever change my relationship status. But if you must know, we are destined to be together! I've already made this clear!"
                    self.used_responses.add(response)
                    return response
            else:
                # Check if current_topic is favorite_food and replace with actual value
                topic_value = self.waifu_memory.favorite_food if self.current_topic == "favorite_food" else self.current_topic
                response = dere_response(self.waifu_memory, self.current_dere, self.used_responses, self.debug,
                    f"We were talking about {topic_value}, remember?",
                    f"Let's get back to {topic_value}.",
                    f"A-are you trying to avoid talking about {topic_value}...?",
                    f"As I was saying about {topic_value}..."
                )
                self.used_responses.add(response)
                return response

        response = maybe_change_dere(self.waifu_memory, self.current_dere, self.dere_types, self.used_responses, self.debug,
            "What are you talking about?", "I don't get it.", "Hmph.", "O-okay..."
        )
        self.used_responses.add(response)
        return response