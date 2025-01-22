def remember(waifu_memory, slot, value, affection_change=0):
    """Stores a value in the waifu's memory and updates affection."""
    setattr(waifu_memory, slot, value)
    waifu_memory.affection += affection_change
    waifu_memory.affection = max(0, min(100, waifu_memory.affection))
    print(f"{waifu_memory.name}: I-I'll remember that, okay?")
    print()