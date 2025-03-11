from typing import List, Set, Tuple, NamedTuple, Dict, Any

def get_current_dere(affection: int) -> str:
    """
    Determines the current dere type based on the affection level.

    Args:
        affection: The affection level of the waifu.

    Returns:
        The current dere type (e.g., "tsundere", "yandere").
    """
    if affection < -5:
        return "tsundere"
    elif -5 <= affection <= 20:
        return "dandere"
    elif 20 < affection <= 60:
        return "kuudere"
    else:
        return "yandere"