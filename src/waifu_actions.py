from typing import Any, List
from transformations import deftransform
from memory import remember

def register_actions(waifu: Any) -> None:
    """Registers keywords, synonyms, and transformations for the waifu chatbot.

    Args:
        waifu: The waifu chatbot object.
    """

    # Example of setting favorite food (keep this logic)
    patterns = [
        "my favorite food is *",
        "i love eating *",
        "i enjoy eating *",
        "i like eating *",
        "i really like *",
        "i really love *"
    ]
    for pattern in patterns:
        deftransform(waifu.transformations, pattern, waifu.set_favorite_food, "favorite_food")

def set_favorite_food(self, food: str) -> str:
    """Updates the waifu's favorite food.

    Args:
        food: The waifu's favorite food.

    Returns:
        A string containing the generated response.
    """
    self.waifu_memory.set_favorite_food(food)
    response = f"Okay, I'll remember that your favorite food is {food}!"
    if self.debug: # Debug print
        print(f"{self.waifu_memory.name}: {response}")
        print()
    return response