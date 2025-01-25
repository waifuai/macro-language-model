def register_keywords(waifu):
    waifu.defkeyword("hello", ["Hi!", "Hello there!"])
    waifu.defkeyword("how are you", ["I'm doing well, thank you!", "I'm fine."])
    waifu.defkeyword("how's it going", ["I'm doing well, thank you!", "I'm fine."])
    waifu.defkeyword("how's things", ["I'm doing well, thank you!", "I'm fine."])
    waifu.defkeyword("what's up", ["I'm doing well, thank you!", "I'm fine."])
    # Add more general conversational keywords
    waifu.defkeyword("what are you doing", ["Just chatting with you!", "Thinking about you.", "Nothing much, what about you?"])
    waifu.defkeyword("what do you think", ["I think it's interesting.", "Hmm, I'm not sure.", "What do you think?"])
    waifu.defkeyword("bye", waifu.farewells)
    waifu.defkeyword("goodbye", waifu.farewells)
    waifu.defkeyword("see you", waifu.farewells)

    waifu.defsynonym("hi", "hello", "hey", "hiya", "greetings")