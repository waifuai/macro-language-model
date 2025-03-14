from transformations import deftransform

def register_food_transforms(waifu):
    deftransform(waifu.registry.transformations, "what is your favorite food", ["waifu-memory", "favorite_food"])
    deftransform(waifu.registry.transformations, "do you like *", [("generate", "food")], [("food", "*")]) # Use "generate"
    deftransform(waifu.registry.transformations, "i like to eat *", ["Oh, you like to eat *? I've never tried that."])
    deftransform(waifu.registry.transformations, "i'm hungry", ["Maybe you should eat something.", "What are you hungry for?"])