from transformations import deftransform

def register_interests_transforms(waifu):
    deftransform(waifu.registry.transformations, "what are your interests", ["talk-about"])
    deftransform(waifu.registry.transformations, "do you like *", ["generate", "interest"], [("interest", "*")])
    deftransform(waifu.registry.transformations, "i like to *", ["Oh, you like to *? That's interesting."])
    deftransform(waifu.registry.transformations, "i enjoy *", ["Oh, you enjoy *? Tell me more."])