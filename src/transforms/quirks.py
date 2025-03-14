from transformations import deftransform

def register_quirks_transforms(waifu):
    deftransform(waifu.registry.transformations, "what are your quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.registry.transformations, "do you have any quirks", ["talk-about", "personality_quirks"])
    deftransform(waifu.registry.transformations, "i have a quirk", ["Oh? What is it?", "Tell me more about your quirk."])
    deftransform(waifu.registry.transformations, "you are *", ["Am I? And how does that make you feel?"]) # More open-ended