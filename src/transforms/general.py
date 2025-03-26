from transformations import deftransform

def register_general_transforms(waifu):
    deftransform(waifu.registry.transformations, "my name is *", ["Nice to meet you, *!", "Hello *!"], memory_slot="name")
    deftransform(waifu.registry.transformations, "i am feeling *", ["Oh, you're feeling *."], memory_slot="feeling")
    deftransform(waifu.registry.transformations, "i like *", ["Oh, you like *? Tell me more!"], memory_slot="likes") # Removed affection_change
    deftransform(waifu.registry.transformations, "what is my name", ["waifu-memory", "name"])
    deftransform(waifu.registry.transformations, "what is my feeling", ["waifu-memory", "feeling"])
    deftransform(waifu.registry.transformations, "tell me about my likes", ["waifu-memory", "likes"])
    deftransform(waifu.registry.transformations, "tell me a joke", ["Why don't scientists trust atoms? Because they make up everything!"])
    deftransform(waifu.registry.transformations, "how do you feel", ["I'm doing great, thanks for asking!", "I'm feeling alright.", "Not too bad."]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "tell me a joke", ["Why don't scientists trust atoms? Because they make up everything!"]) # Removed affection_change
    deftransform(waifu.registry.transformations, "my name is *", ["Nice to meet you, *!", "Hello *!"], memory_slot="name") # Removed affection_change
    deftransform(waifu.registry.transformations, "yes", ["I agree!", "Yeah!", "Sounds good!"]) # Removed affection_change
    deftransform(waifu.registry.transformations, "yeah", ["I agree!", "Yeah!", "Sounds good!"]) # Removed affection_change
    deftransform(waifu.registry.transformations, "yep", ["I agree!", "Yeah!", "Sounds good!"]) # Removed affection_change
    deftransform(waifu.registry.transformations, "no", ["Oh, really?", "I see...", "Hmm."]) # Removed affection_change
    deftransform(waifu.registry.transformations, "nope", ["Oh, really?", "I see...", "Hmm."]) # Removed affection_change
    deftransform(waifu.registry.transformations, "i agree", ["That's great!", "I'm glad we agree."])
    deftransform(waifu.registry.transformations, "i disagree", ["Oh, that's interesting.", "Why do you think that?"])
    deftransform(waifu.registry.transformations, "you are right", ["Of course I am!", "I know, right?"])
    deftransform(waifu.registry.transformations, "you are wrong", ["Am not!", "I disagree."])
    deftransform(waifu.registry.transformations, "who is *", ["I don't know who * is.", "Who are you talking about?"])
    deftransform(waifu.registry.transformations, "what is *", ["I'm not sure what * is.", "What are you referring to?"])
    deftransform(waifu.registry.transformations, "where is *", ["I don't know where * is.", "Where is that?"])
    deftransform(waifu.registry.transformations, "when is *", ["I don't remember when * is.", "When was that?"])
    deftransform(waifu.registry.transformations, "why is *", ["I don't know why * is.", "Why do you ask?"])
    deftransform(waifu.registry.transformations, "how is *", ["I don't know how * is.", "How is that possible?"])
    deftransform(waifu.registry.transformations, "i am *", ["Why are you *?", "How long have you been *?"]) # Removed affection_change
    deftransform(waifu.registry.transformations, "i feel *", ["Why do you feel *?", "I'm here for you."]) # Removed affection_change
    deftransform(waifu.registry.transformations, "what do you mean", ["What do *you* think I mean?", "I'm not sure what you're asking."]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "what do you think", ["I'm not sure yet. What are your thoughts?", "I haven't made up my mind. What do you think?"]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "are you sure", ["Are *you* sure?", "I'm as sure as I can be."]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "is that so", ["Is it?", "That's what I heard."]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "really", ["Really!", "Is that surprising?"]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "tell me more", ["Tell you more about what, specifically?", "What are you curious about?"])
    deftransform(waifu.registry.transformations, "i don't know", ["You don't know? Maybe we can figure it out together.", "It's okay not to know everything."])
    deftransform(waifu.registry.transformations, "i'm not sure", ["What are you unsure about?", "Maybe I can help you figure it out."])
    deftransform(waifu.registry.transformations, "can you help me", ["I can try. What do you need help with?", "What kind of help are you looking for?"]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "can you tell me", ["Tell you what?", "What do you want me to tell you?"]) # Removed maybe-change-dere