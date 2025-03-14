from typing import Any, List

def register_keywords(waifu: Any) -> None:
    waifu.registry.defkeyword("hello", ["Hi!", "Hello there!", "Hey!", "Hi there!"])
    waifu.registry.defkeyword("how are you", ["I'm doing well, thank you!", "I'm fine.", "I'm great! How about you?", "Doing good!"])
    waifu.registry.defkeyword("how's it going", ["I'm doing well, thank you!", "I'm fine.", "Things are going great!", "Pretty good!"])
    waifu.registry.defkeyword("how's things", ["I'm doing well, thank you!", "I'm fine.", "Things are good!", "Can't complain!"])
    waifu.registry.defkeyword("what's up", ["I'm doing well, thank you!", "I'm fine.", "Just hanging out!", "Not much, what's up with you?"])
    waifu.registry.defkeyword("what are you doing", ["Just chatting with you!", "Thinking about you.", "Nothing much, what about you?", "Just relaxing!", "Browsing the internet."])
    waifu.registry.defkeyword("what do you think", ["I think it's interesting.", "Hmm, I'm not sure.", "What do you think?", "That's a good question!", "I'm still thinking about it."])
    waifu.registry.defkeyword("bye", waifu.farewells)
    waifu.registry.defkeyword("goodbye", waifu.farewells)
    waifu.registry.defkeyword("see you", waifu.farewells)

    waifu.registry.defsynonym("hi", "hello", "hey", "hiya", "greetings")

    # More general keywords
    waifu.registry.defkeyword("yes", [("yes", "Yes, that's right!"), ("yeah", "Yeah!"), ("yep", "Yup!"), ("yes", "Absolutely!"), ("yeah", "Totally!"), ("yep", "For sure!")])
    waifu.registry.defkeyword("no", [("no", "No, that's not right."), ("nope", "Nope!"), ("no", "Hmm, I don't think so."), ("nope", "Nah."), ("no", "Not really.")])
    waifu.registry.defkeyword("maybe", ["Maybe...", "Perhaps...", "I'm not sure.", "Possibly...", "Could be!"])
    waifu.registry.defkeyword("okay", [("okay", "Okay, I understand."), ("alright", "Alright, I get it."), ("okay", "Okay, what's next?"), ("alright", "Alright, let's do it!"), ("okay", "Okay, sounds good!")])
    waifu.registry.defkeyword("thanks", ["You're welcome!", "No problem!", "Anytime!", "Glad to help!"])
    waifu.registry.defkeyword("thank you", ["You're welcome!", "No problem!", "My pleasure!", "Don't mention it!"])

    # Topic-related keywords (for detection)
    waifu.registry.defkeyword("family", ["family"])
    waifu.registry.defkeyword("childhood", ["childhood"])
    waifu.registry.defkeyword("feelings", ["feelings"])
    waifu.registry.defkeyword("interest_manga", ["interest_manga"]) # Specific interest
    waifu.registry.defkeyword("interest_anime", ["interest_anime"]) # Specific interest
    waifu.registry.defkeyword("interest_games", ["interest_games"]) # Specific interest
    waifu.registry.defkeyword("interest_cooking", ["interest_cooking"]) # Specific interest
    waifu.registry.defkeyword("relationship", ["relationship"])
    waifu.registry.defkeyword("food", ["food"])
    waifu.registry.defkeyword("quirks", ["quirks"])


    # Keywords for asking questions
    waifu.registry.defkeyword("who", ["Who are you talking about?", "I don't know who that is.", "Who's that?"])
    waifu.registry.defkeyword("what", ["What are you talking about?", "I don't understand.", "What is it?", "What do you mean?"])
    waifu.registry.defkeyword("where", ["Where is that?", "I don't know where that is.", "Where are we going?"])
    waifu.registry.defkeyword("when", ["When was that?", "I don't remember.", "When will that be?"])
    waifu.registry.defkeyword("why", ["Why do you ask?", "I don't know why.", "That's a good question!", "Why not?"])
    waifu.registry.defkeyword("how", ["How is that possible?", "I don't know how.", "How does that work?", "How are you?"])

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
    waifu.registry.defkeyword("doing", ["What are we doing?", "I'm not sure what we're doing."])
    waifu.registry.defsynonym("doing", "do")

    # Keywords for agreement/disagreement (more specific responses)
    waifu.registry.defkeyword("yes", [("yes", "Yes, that's right!"), ("yeah", "Yeah!"), ("yep", "Yup!"), ("yes", "Absolutely!"), ("yeah", "Totally!"), ("yep", "For sure!")])
    waifu.registry.defkeyword("no", [("no", "No, that's not right."), ("nope", "Nope!"), ("no", "Hmm, I don't think so."), ("nope", "Nah."), ("no", "Not really.")])
    waifu.registry.defkeyword("okay", [("okay", "Okay, I understand."), ("alright", "Alright, I get it."), ("okay", "Okay, what's next?"), ("alright", "Alright, let's do it!"), ("okay", "Okay, sounds good!")])
    waifu.registry.defkeyword("sure", [("sure", "Sure, I guess."), ("yeah", "Yeah, I suppose."), ("sure", "Sure, why not?"), ("sure", "Sure, what do you mean?"), ("yeah", "Yeah, tell me more.")])
    waifu.registry.defkeyword("understand", [("understand", "I understand."), ("i see", "I see."), ("understand", "I get it now."), ("i see", "I see what you mean."), ("got it", "Gotcha!")])
    waifu.registry.defkeyword("got it", [("got it", "Got it."), ("ok", "Okay."), ("got it", "Gotcha!"), ("ok", "Okay, I'm with you."), ("got it", "I understand now.")])

    # New keywords for prompting conversation
    waifu.registry.defkeyword("tell me", [("tell me", "What do you want to know?"), ("tell me", "I'm all ears!"), ("tell me", "Okay, I'm listening.")])
    waifu.registry.defkeyword("and you", [("and you", "What about you?"), ("and you", "How about you?"), ("and you", "And you?")])
    waifu.registry.defsynonym("and you", "you")