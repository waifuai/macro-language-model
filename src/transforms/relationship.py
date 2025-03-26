from transformations import deftransform

def register_relationship_transforms(waifu):
    deftransform(waifu.registry.transformations, "what is your relationship status", ["introduce-topic", "relationship_status"])
    deftransform(waifu.registry.transformations, "are you in a relationship", ["Why do you ask? Are *you* in a relationship?", "That's a personal question!"]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "do you have a boyfriend", ["Do *you* have a boyfriend?", "That's none of your business!"]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "do you have a girlfriend", ["Do *you* have a girlfriend?", "That's none of your business!"]) # Removed maybe-change-dere
    deftransform(waifu.registry.transformations, "i have a *", ["Oh, you have a *? That's nice."])