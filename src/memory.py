from typing import Any

def remember(waifu_memory: Any, slot: str, value: str, affection_change: int = 0) -> None:
    """Stores a value in the waifu's memory and updates affection.

    Args:
        waifu_memory: The waifu's memory object.
        slot: The memory slot to store the value in.
        value: The value to store.
        affection_change: The amount to change the waifu's affection by.
    """
    value = value.encode('utf-8', 'replace').decode('utf-8')
    setattr(waifu_memory, slot, value)
    if "love" in value.lower() or "care" in value.lower():
        affection_change += 3
    elif "hate" in value.lower() or "dislike" in value.lower():
        affection_change -= 2
    waifu_memory.affection += affection_change
    waifu_memory.affection = max(0, min(100, waifu_memory.affection))
    print(f"{waifu_memory.name}: I-I'll remember that, okay?")
    print()