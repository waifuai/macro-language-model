def register_greeting_keywords(waifu):
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