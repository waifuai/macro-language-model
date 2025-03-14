def register_question_keywords(waifu):
    waifu.registry.defkeyword("who", ["Who are you talking about?", "I don't know who that is.", "Who's that?"])
    waifu.registry.defkeyword("what", ["What are you talking about?", "I don't understand.", "What is it?", "What do you mean?"])
    waifu.registry.defkeyword("where", ["Where is that?", "I don't know where that is.", "Where are we going?"])
    waifu.registry.defkeyword("when", ["When was that?", "I don't remember.", "When will that be?"])
    waifu.registry.defkeyword("why", ["Why do you ask?", "I don't know why.", "That's a good question!", "Why not?"])
    waifu.registry.defkeyword("how", ["How is that possible?", "I don't know how.", "How does that work?", "How are you?"])

    waifu.registry.defsynonym("what's", "what", "is")
    waifu.registry.defsynonym("where's", "where", "is")
    waifu.registry.defsynonym("who's", "who", "is")
    waifu.registry.defsynonym("when's", "when", "is")
    waifu.registry.defsynonym("why's", "why", "is")
    waifu.registry.defsynonym("how's", "how", "is")