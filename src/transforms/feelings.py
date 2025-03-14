from transformations import deftransform

def register_feelings_transforms(waifu):
    deftransform(waifu.registry.transformations, "i am feeling *", ["Oh, you're feeling *.  Why are you feeling that way?", "I'm here for you if you want to talk."])
    deftransform(waifu.registry.transformations, "are you feeling *", ["maybe-change-dere", "Why do you ask?", "I'm feeling... complicated."])
    deftransform(waifu.registry.transformations, "i'm feeling *", ["Oh, you're feeling *.  Why are you feeling that way?", "I'm here for you if you want to talk."])