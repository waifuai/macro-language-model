from transformations import deftransform

def register_family_transforms(waifu):
    deftransform(waifu.registry.transformations, "talk about family", ["introduce-topic", "family"])
    deftransform(waifu.registry.transformations, "tell me about your family", ["introduce-topic", "family"])
    deftransform(waifu.registry.transformations, "do you have siblings", ["Do *you* have siblings?", "I'm not sure, do you?"])
    deftransform(waifu.registry.transformations, "what are your parents like", ["They're... parents. What are *your* parents like?"])
    deftransform(waifu.registry.transformations, "my family is *", ["Oh, your family is *? Mine is complicated."])