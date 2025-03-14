from transformations import deftransform

def register_childhood_transforms(waifu):
    deftransform(waifu.registry.transformations, "talk about childhood", ["introduce-topic", "childhood"])
    deftransform(waifu.registry.transformations, "tell me about your childhood", ["introduce-topic", "childhood"])
    deftransform(waifu.registry.transformations, "what was your childhood like", ["It was a childhood. What was *yours* like?"])
    deftransform(waifu.registry.transformations, "i had a * childhood", ["Oh, you had a * childhood? Mine was pretty normal."])
    deftransform(waifu.registry.transformations, "did you have a good childhood", ["Did *you* have a good childhood?", "It was alright, I guess."])