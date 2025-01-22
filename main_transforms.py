from transformations import deftransform

def register_transforms(waifu):
    deftransform(waifu.transformations, "my name is *", ["Nice to meet you, *!", "Hello *!"], memory_slot="name")
    deftransform(waifu.transformations, "i am feeling *", ["Oh, you're feeling *."], memory_slot="feeling")
    deftransform(waifu.transformations, "i like *", ["Oh, you like *."], memory_slot="likes", affection_change=2)
    deftransform(waifu.transformations, "do you like *", ["generate", "interest"], [("interest", "*")])
    deftransform(waifu.transformations, "what is my name", ["waifu-memory", "name"])
    deftransform(waifu.transformations, "what is my feeling", ["waifu-memory", "feeling"])
    deftransform(waifu.transformations, "tell me about my likes", ["waifu-memory", "likes"])
    deftransform(waifu.transformations, "tell me a joke", ["Why don't scientists trust atoms? Because they make up everything!"])
    deftransform(waifu.transformations, "talk about family", ["introduce-topic", "family"])
    deftransform(waifu.transformations, "talk about childhood", ["introduce-topic", "childhood"])
    deftransform(waifu.transformations, "how do you feel", ["maybe-change-dere", "I'm doing great, thanks for asking!", "I'm feeling alright.", "Not too bad."])
    deftransform(waifu.transformations, "tell me about your interests", ["talk-about"])
    deftransform(waifu.transformations, "what is your relationship status", ["introduce-topic", "relationship_status"])
    deftransform(waifu.transformations, "what is your favorite food", ["waifu-memory", "favorite_food"])
    deftransform(waifu.transformations, "tell me about your personality", ["waifu-memory", "personality_quirks"])
    deftransform(waifu.transformations, "what are your quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.transformations, "do you have any quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.transformations, "i have a quirk", ["Oh? What is it?", "Tell me more about your quirk."])
    # Add more general transformations
    deftransform(waifu.transformations, "i am *", ["Why are you *?", "How long have you been *?"])
    deftransform(waifu.transformations, "i feel *", ["Why do you feel *?", "I'm here for you."])