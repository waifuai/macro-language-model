from typing import Any, List

def register_keywords(waifu: Any) -> None:
    """Registers keywords and synonyms for the waifu chatbot.

    Args:
        waifu: The waifu chatbot object.
    """
    waifu.registry.defkeyword("hello", ["Hi!", "Hello there!"])
    waifu.registry.defkeyword("how are you", ["I'm doing well, thank you!", "I'm fine."])
    waifu.registry.defkeyword("how's it going", ["I'm doing well, thank you!", "I'm fine."])
    waifu.registry.defkeyword("how's things", ["I'm doing well, thank you!", "I'm fine."])
    waifu.registry.defkeyword("what's up", ["I'm doing well, thank you!", "I'm fine."])
    # Add more general conversational keywords
    waifu.registry.defkeyword("what are you doing", ["Just chatting with you!", "Thinking about you.", "Nothing much, what about you?"])
    waifu.registry.defkeyword("what do you think", ["I think it's interesting.", "Hmm, I'm not sure.", "What do you think?"])
    waifu.registry.defkeyword("bye", waifu.farewells)
    waifu.registry.defkeyword("goodbye", waifu.farewells)
    waifu.registry.defkeyword("see you", waifu.farewells)

    waifu.registry.defsynonym("hi", "hello", "hey", "hiya", "greetings")

    # More general keywords
    waifu.registry.defkeyword("yes", ["Yes, that's right!", "Yeah!", "Yup!"])
    waifu.registry.defkeyword("no", ["No, that's not right.", "Nope!"])
    waifu.registry.defkeyword("maybe", ["Maybe...", "Perhaps...", "I'm not sure."])
    waifu.registry.defkeyword("okay", ["Okay!", "Alright."])
    waifu.registry.defkeyword("thanks", ["You're welcome!", "No problem!"])
    waifu.registry.defkeyword("thank you", ["You're welcome!", "No problem!"])

    # Topic-related keywords
    waifu.registry.defkeyword("family", ["family", "parents", "siblings", "relatives", "mom", "dad", "brother", "sister"])
    waifu.registry.defkeyword("childhood", ["childhood", "past", "young", "kid", "baby", "teenager", "child"])
    waifu.registry.defkeyword("feelings", ["feelings", "emotions", "happy", "sad", "angry", "excited", "scared", "worried", "anxious"])
    waifu.registry.defkeyword("interests", ["interests", "hobbies", "like", "enjoy", "passion", "favorite", "love", "hate"])
    waifu.registry.defkeyword("relationship", ["relationship", "friends", "dating", "love", "friendship", "partner", "boyfriend", "girlfriend"])
    waifu.registry.defkeyword("food", ["food", "eat", "hungry", "favorite food", "cooking", "pocky", "dish", "meal", "delicious", "tasty"])
    waifu.registry.defkeyword("quirks", ["quirks", "personality", "unique", "special", "weird", "strange", "unusual"])

    # Keywords for asking questions
    waifu.registry.defkeyword("who", ["Who are you talking about?", "I don't know who that is."])
    waifu.registry.defkeyword("what", ["What are you talking about?", "I don't understand."])
    waifu.registry.defkeyword("where", ["Where is that?", "I don't know where that is."])
    waifu.registry.defkeyword("when", ["When was that?", "I don't remember."])
    waifu.registry.defkeyword("why", ["Why do you ask?", "I don't know why."])
    waifu.registry.defkeyword("how", ["How is that possible?", "I don't know how."])

    # Synonyms for question words
    waifu.registry.defsynonym("what's", "what", "is")
    waifu.registry.defsynonym("where's", "where", "is")
    waifu.registry.defsynonym("who's", "who", "is")
    waifu.registry.defsynonym("when's", "when", "is")
    waifu.registry.defsynonym("why's", "why", "is")
    waifu.registry.defsynonym("how's", "how", "is")

    # Synonyms for family members
    waifu.registry.defsynonym("mom", "mother", "mommy", "mama")
    waifu.registry.defsynonym("dad", "father", "daddy", "papa")
    waifu.registry.defsynonym("brother", "sibling")
    waifu.registry.defsynonym("sister", "sibling")

    # Synonyms for feelings
    waifu.registry.defsynonym("happy", "joyful", "cheerful", "glad", "delighted")
    waifu.registry.defsynonym("sad", "unhappy", "depressed", "miserable", "down")
    waifu.registry.defsynonym("angry", "mad", "furious", "irritated", "enraged")
    waifu.registry.defsynonym("excited", "thrilled", "enthusiastic", "eager")
    waifu.registry.defsynonym("scared", "afraid", "frightened", "terrified")
    waifu.registry.defsynonym("worried", "anxious", "concerned", "nervous")

    # Synonyms for like/dislike
    waifu.registry.defsynonym("like", "enjoy", "love", "adore", "appreciate")
    waifu.registry.defsynonym("hate", "dislike", "despise", "loathe", "abhor")

     # Keywords for clarification and context
    waifu.registry.defkeyword("explain", ["Can you explain that?", "What do you mean?"])
    waifu.registry.defkeyword("context", ["I need more context.", "Can you give me some context?"])
    waifu.registry.defkeyword("what do you mean", ["What do you mean by that?", "Can you clarify?"])
    waifu.registry.defkeyword("clarify", ["Can you clarify that?", "I don't understand."])
    waifu.registry.defkeyword("doing", ["What are we doing?", "I'm not sure what we're doing."]) # Added 'doing'
    waifu.registry.defsynonym("doing", "do") # Added synonym

    # Keywords for agreement/disagreement (more specific responses)
    waifu.registry.defkeyword("yes", [("yes", "Yes, that's right!"), ("yeah", "Yeah!"), ("yep", "Yup!")]) # Keep original
    waifu.registry.defkeyword("no", [("no", "No, that's not right."), ("nope", "Nope!")]) # Keep original
    waifu.registry.defkeyword("okay", [("okay", "Okay, I understand."), ("alright", "Alright, I get it.")]) # More specific
    waifu.registry.defkeyword("sure", [("sure", "Sure, I guess."), ("yeah", "Yeah, I suppose.")]) # More specific
    waifu.registry.defkeyword("understand", [("understand", "I understand."), ("i see", "I see.")]) # More specific
    waifu.registry.defkeyword("got it", [("got it", "Got it."), ("ok", "Okay.")]) # More specific