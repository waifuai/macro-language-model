from typing import Any
from transforms import *


def register_transforms(waifu: Any) -> None:
    """Registers transformations for the waifu chatbot.

    Args:
        waifu: The waifu chatbot object.
    """
    register_general_transforms(waifu)
    register_family_transforms(waifu)
    register_childhood_transforms(waifu)
    register_feelings_transforms(waifu)
    register_interests_transforms(waifu)
    register_relationship_transforms(waifu)
    register_food_transforms(waifu)
    register_quirks_transforms(waifu)